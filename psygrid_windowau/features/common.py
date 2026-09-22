from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite, log, sqrt
from statistics import mean, median, pstdev
from typing import Sequence

from psygrid_windowau.data.models import Candle, FeatureState


@dataclass(frozen=True)
class FeatureValue:
    value: float | None
    state: FeatureState
    provenance: str
    as_of: datetime | None
    reason: str | None = None


def available(value: float, *, provenance: str, as_of: datetime | None) -> FeatureValue:
    if not isfinite(float(value)):
        return FeatureValue(None, FeatureState.INVALID, provenance, as_of, "non-finite result")
    return FeatureValue(float(value), FeatureState.AVAILABLE, provenance, as_of)


def unavailable(*, provenance: str, as_of: datetime | None, reason: str) -> FeatureValue:
    return FeatureValue(None, FeatureState.UNAVAILABLE, provenance, as_of, reason)


def invalid(*, provenance: str, as_of: datetime | None, reason: str) -> FeatureValue:
    return FeatureValue(None, FeatureState.INVALID, provenance, as_of, reason)


def closed(candles: Sequence[Candle]) -> list[Candle]:
    return list(candles)


def require_n(candles: Sequence[Candle], n: int) -> tuple[list[Candle], str | None]:
    if n <= 0:
        raise ValueError("n must be positive")
    xs = closed(candles)
    if len(xs) < n:
        return xs, f"requires {n} completed observations; got {len(xs)}"
    return xs, None


def positive_price(value: float) -> bool:
    return isfinite(value) and value > 0


def finite_returns(closes: Sequence[float]) -> list[float]:
    return [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes))]


def log_returns(closes: Sequence[float]) -> list[float]:
    return [log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]


def baseline(values: Sequence[float], n: int, *, statistic: str = "median") -> float | None:
    if len(values) < n:
        return None
    xs = list(values[-n:])
    return median(xs) if statistic == "median" else mean(xs)
