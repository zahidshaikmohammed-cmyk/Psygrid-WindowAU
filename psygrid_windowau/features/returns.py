from __future__ import annotations
from collections.abc import Sequence
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, invalid, unavailable, finite_returns, log_returns

def simple_return(candles: Sequence[Candle]) -> FeatureValue:
    if len(candles) < 2: return unavailable(provenance="M1_CLOSE", as_of=candles[-1].timestamp if candles else None, reason="requires two completed closes")
    a,b=candles[-2],candles[-1]
    if a.close <= 0 or b.close <= 0: return invalid(provenance="M1_CLOSE", as_of=b.timestamp, reason="close must be positive")
    return available(b.close/a.close-1.0, provenance="M1_CLOSE", as_of=b.timestamp)

def log_return(candles: Sequence[Candle]) -> FeatureValue:
    if len(candles) < 2: return unavailable(provenance="M1_CLOSE", as_of=candles[-1].timestamp if candles else None, reason="requires two completed closes")
    a,b=candles[-2],candles[-1]
    if a.close <= 0 or b.close <= 0: return invalid(provenance="M1_CLOSE", as_of=b.timestamp, reason="close must be positive")
    from math import log
    return available(log(b.close/a.close), provenance="M1_CLOSE", as_of=b.timestamp)

def rolling_simple_returns(candles: Sequence[Candle], n: int) -> tuple[float,...]:
    if n <= 0: raise ValueError("n must be positive")
    return tuple(finite_returns([c.close for c in candles])[-n:])

def rolling_log_returns(candles: Sequence[Candle], n: int) -> tuple[float,...]:
    if n <= 0: raise ValueError("n must be positive")
    return tuple(log_returns([c.close for c in candles])[-n:])
