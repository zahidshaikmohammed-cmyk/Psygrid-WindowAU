from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TimestampStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED_OPEN_TIME = "VERIFIED_OPEN_TIME"
    VERIFIED_OTHER = "VERIFIED_OTHER"


class CandleState(str, Enum):
    FORMING = "FORMING"
    CLOSED = "CLOSED"


class FeatureState(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    INVALID = "INVALID"


class DataQualityState(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    STALE = "STALE"
    GAP = "GAP"
    DUPLICATE = "DUPLICATE"


def parse_utc(value: str) -> datetime:
    """Parse an ISO-8601 timestamp and normalize it to aware UTC."""
    if not isinstance(value, str) or not value:
        raise ValueError("timestamp must be a non-empty ISO-8601 string")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include an explicit timezone")
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    bid: float | None = None
    ask: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "timestamp", parse_utc(self.timestamp.isoformat()))
        for name in ("open", "high", "low", "close", "volume"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError(f"{name} must be numeric")
        for name in ("bid", "ask"):
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, (int, float)) or isinstance(value, bool)
            ):
                raise TypeError(f"{name} must be numeric or None")


@dataclass(frozen=True)
class FeedHealth:
    schema_version: str
    service: str
    provider: str
    timeframe: str
    generated_at: datetime
    status: str
    universe_size: int
    symbol: str
    market_state: str
    symbol_status: str
    last_candle_timestamp: datetime
    updated_at: datetime
    websocket_connected: bool
    reconnect_count: int
    gap_recoveries: int
    rejected_count: int
    m1_valid: bool


@dataclass(frozen=True)
class FeedSnapshot:
    health: FeedHealth
    candles: tuple[Candle, ...]


@dataclass(frozen=True)
class CandleObservation:
    observation_timestamp: datetime
    provider_timestamp: datetime
    candle_state: CandleState
    candle: Candle
    symbol: str
    source: str
    feed_status: str
    freshness_seconds: float
    connection_state: bool

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "observation_timestamp", parse_utc(self.observation_timestamp.isoformat())
        )
        object.__setattr__(
            self, "provider_timestamp", parse_utc(self.provider_timestamp.isoformat())
        )
        if self.symbol != "XAUUSD":
            raise ValueError("WindowAU observations must be XAUUSD only")
        if not self.source:
            raise ValueError("source is required")
        if self.freshness_seconds < 0:
            raise ValueError("freshness_seconds cannot be negative")


@dataclass(frozen=True)
class TimeframeBar:
    start: datetime
    end: datetime
    timeframe_minutes: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    component_timestamps: tuple[datetime, ...]
    complete: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "start", parse_utc(self.start.isoformat()))
        object.__setattr__(self, "end", parse_utc(self.end.isoformat()))
        if self.timeframe_minutes not in (5, 15, 30):
            raise ValueError("WindowAU supports M5, M15 and M30 aggregation")
        if self.end <= self.start:
            raise ValueError("bar end must be after bar start")
        if self.complete and len(self.component_timestamps) != self.timeframe_minutes:
            raise ValueError("completed bar must contain exactly all component M1 intervals")


@dataclass(frozen=True)
class QualityIssue:
    code: str
    message: str
    timestamp: datetime | None = None


@dataclass(frozen=True)
class QualityReport:
    state: DataQualityState
    issues: tuple[QualityIssue, ...]


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value == value and abs(float(value)) != float("inf")
