from __future__ import annotations

from collections.abc import Sequence
from statistics import median

from psygrid_windowau.data.models import Candle


def require_candles(candles: Sequence[Candle], minimum: int) -> tuple[Candle, ...]:
    if minimum <= 0:
        raise ValueError("minimum must be positive")
    if len(candles) < minimum:
        return ()
    return tuple(candles)


def prior_high(candles: Sequence[Candle], lookback: int, current_index: int | None = None) -> float | None:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    i = len(candles) - 1 if current_index is None else current_index
    if i < lookback or i >= len(candles):
        return None
    return max(c.high for c in candles[i - lookback:i])


def prior_low(candles: Sequence[Candle], lookback: int, current_index: int | None = None) -> float | None:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    i = len(candles) - 1 if current_index is None else current_index
    if i < lookback or i >= len(candles):
        return None
    return min(c.low for c in candles[i - lookback:i])


def median_range(candles: Sequence[Candle], lookback: int, current_index: int | None = None) -> float | None:
    i = len(candles) - 1 if current_index is None else current_index
    if lookback <= 0 or i < lookback or i >= len(candles):
        return None
    return median(c.high - c.low for c in candles[i - lookback:i])


def median_body(candles: Sequence[Candle], lookback: int, current_index: int | None = None) -> float | None:
    i = len(candles) - 1 if current_index is None else current_index
    if lookback <= 0 or i < lookback or i >= len(candles):
        return None
    return median(abs(c.close - c.open) for c in candles[i - lookback:i])


def direction(candle: Candle) -> str | None:
    if candle.close > candle.open:
        return "LONG"
    if candle.close < candle.open:
        return "SHORT"
    return None
