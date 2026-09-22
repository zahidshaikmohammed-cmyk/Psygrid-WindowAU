from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import Candle, FeedHealth, FeedSnapshot, parse_utc

CANONICAL_URL = "http://140.245.226.102:8080/public/live.json"
CANONICAL_PROVIDER = "realmarketapi"
CANONICAL_SERVICE = "pysgrid-forex"
CANONICAL_TIMEFRAME = "M1"
CANONICAL_SYMBOL = "XAUUSD"
REQUIRED_ENVELOPE_FIELDS = (
    "schema_version",
    "service",
    "provider",
    "timeframe",
    "generated_at",
    "status",
    "universe_size",
    "symbols",
)
REQUIRED_SYMBOL_FIELDS = (
    "symbol",
    "market_state",
    "status",
    "last_candle_timestamp",
    "updated_at",
    "websocket_connected",
    "reconnect_count",
    "gap_recoveries",
    "rejected_count",
    "candles_1m",
    "m1_valid",
)
REQUIRED_CANDLE_FIELDS = (
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
)
SOURCE_NAME = "RealMarketAPI"


class DataContractError(ValueError):
    """Raised when the canonical provider contract is violated."""


class ProviderFetchError(RuntimeError):
    """Raised when the canonical endpoint cannot be fetched."""


@dataclass(frozen=True)
class RealMarketApiClient:
    url: str = CANONICAL_URL
    timeout_seconds: float = 10.0

    def fetch_json(self) -> dict:
        if self.url != CANONICAL_URL:
            raise DataContractError(
                "WindowAU source substitution is prohibited: canonical URL required"
            )
        request = Request(
            self.url,
            headers={
                "Accept": "application/json",
                "User-Agent": "PSYGRID-WindowAU/0.1",
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read()
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise ProviderFetchError(f"canonical provider fetch failed: {exc}") from exc
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DataContractError("provider response is not valid UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise DataContractError("provider response root must be an object")
        return payload

    def parse_snapshot(self, payload: dict) -> FeedSnapshot:
        _require_exact_keys(payload, REQUIRED_ENVELOPE_FIELDS, "response")
        if not isinstance(payload["provider"], str):
            raise DataContractError("provider must be a string")
        if not isinstance(payload["service"], str):
            raise DataContractError("service must be a string")
        if not isinstance(payload["timeframe"], str):
            raise DataContractError("timeframe must be a string")
        if payload["provider"] != CANONICAL_PROVIDER:
            raise DataContractError("unexpected provider")
        if payload["service"] != CANONICAL_SERVICE:
            raise DataContractError("unexpected service")
        if payload["timeframe"] != CANONICAL_TIMEFRAME:
            raise DataContractError("unexpected timeframe")
        if not isinstance(payload["schema_version"], str):
            raise DataContractError("schema_version must be a string")
        if payload["schema_version"] != "1.0":
            raise DataContractError("unsupported schema_version")
        if not isinstance(payload["service"], str) or not isinstance(payload["provider"], str) or not isinstance(payload["timeframe"], str):
            raise DataContractError("service, provider and timeframe must be strings")
        if not isinstance(payload["universe_size"], int) or isinstance(payload["universe_size"], bool):
            raise DataContractError("universe_size must be an integer")
        symbols = payload["symbols"]
        if not isinstance(symbols, dict):
            raise DataContractError("symbols must be an object")
        if CANONICAL_SYMBOL not in symbols:
            raise DataContractError("XAUUSD is missing from canonical symbols object")

        symbol_data = symbols[CANONICAL_SYMBOL]
        _require_exact_keys(symbol_data, REQUIRED_SYMBOL_FIELDS, "symbols.XAUUSD")
        if not isinstance(symbol_data["symbol"], str) or symbol_data["symbol"] != CANONICAL_SYMBOL:
            raise DataContractError("XAUUSD symbol identity mismatch")
        if not isinstance(symbol_data["websocket_connected"], bool) or not isinstance(symbol_data["m1_valid"], bool):
            raise DataContractError("websocket_connected and m1_valid must be booleans")
        for field in ("reconnect_count", "gap_recoveries", "rejected_count"):
            if not isinstance(symbol_data[field], int) or isinstance(symbol_data[field], bool):
                raise DataContractError(f"{field} must be an integer")
        if not isinstance(symbol_data["candles_1m"], list):
            raise DataContractError("candles_1m must be an array")

        candles: list[Candle] = []
        for index, raw_candle in enumerate(symbol_data["candles_1m"]):
            if not isinstance(raw_candle, dict):
                raise DataContractError(f"candles_1m[{index}] must be an object")
            allowed = set(REQUIRED_CANDLE_FIELDS) | {"bid", "ask"}
            if not set(raw_candle).issubset(allowed) or not set(REQUIRED_CANDLE_FIELDS).issubset(raw_candle):
                missing = sorted(set(REQUIRED_CANDLE_FIELDS) - set(raw_candle))
                extra = sorted(set(raw_candle) - allowed)
                raise DataContractError(
                    f"candles_1m[{index}] schema mismatch; missing={missing}, extra={extra}"
                )
            try:
                candles.append(
                    Candle(
                        timestamp=parse_utc(raw_candle["timestamp"]),
                        open=_numeric_field(raw_candle["open"], "open"),
                        high=_numeric_field(raw_candle["high"], "high"),
                        low=_numeric_field(raw_candle["low"], "low"),
                        close=_numeric_field(raw_candle["close"], "close"),
                        volume=_numeric_field(raw_candle["volume"], "volume"),
                        bid=_optional_numeric_field(raw_candle.get("bid"), "bid"),
                        ask=_optional_numeric_field(raw_candle.get("ask"), "ask"),
                    )
                )
            except DataContractError:
                raise
            except (TypeError, ValueError) as exc:
                raise DataContractError(
                    f"candles_1m[{index}] contains invalid values"
                ) from exc

        health = FeedHealth(
            schema_version=str(payload["schema_version"]),
            service=str(payload["service"]),
            provider=str(payload["provider"]),
            timeframe=str(payload["timeframe"]),
            generated_at=parse_utc(payload["generated_at"]),
            status=str(payload["status"]),
            universe_size=payload["universe_size"],
            symbol=str(symbol_data["symbol"]),
            market_state=str(symbol_data["market_state"]),
            symbol_status=str(symbol_data["status"]),
            last_candle_timestamp=parse_utc(symbol_data["last_candle_timestamp"]),
            updated_at=parse_utc(symbol_data["updated_at"]),
            websocket_connected=bool(symbol_data["websocket_connected"]),
            reconnect_count=int(symbol_data["reconnect_count"]),
            gap_recoveries=int(symbol_data["gap_recoveries"]),
            rejected_count=int(symbol_data["rejected_count"]),
            m1_valid=bool(symbol_data["m1_valid"]),
        )
        return FeedSnapshot(health=health, candles=tuple(candles))

    def fetch_snapshot(self) -> FeedSnapshot:
        return self.parse_snapshot(self.fetch_json())


def _require_exact_keys(value: object, required: tuple[str, ...], label: str) -> None:
    if not isinstance(value, dict):
        raise DataContractError(f"{label} must be an object")
    actual = set(value)
    expected = set(required)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise DataContractError(
            f"{label} schema mismatch; missing={missing}, extra={extra}"
        )


def _numeric_field(value: object, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise DataContractError(f"{field} must be numeric")
    return float(value)


def _optional_numeric_field(value: object, field: str) -> float | None:
    if value is None:
        return None
    return _numeric_field(value, field)
