from __future__ import annotations
from collections.abc import Sequence
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, unavailable

def prior_high(candles: Sequence[Candle], n: int) -> FeatureValue:
    if n<=0: raise ValueError("n must be positive")
    if len(candles)<n+1: return unavailable(provenance=f"M1_HIGH_PRIOR_{n}",as_of=candles[-1].timestamp if candles else None,reason=f"requires {n} prior candles")
    return available(max(c.high for c in candles[-n-1:-1]),provenance=f"M1_HIGH_PRIOR_{n}",as_of=candles[-1].timestamp)

def prior_low(candles: Sequence[Candle], n: int) -> FeatureValue:
    if n<=0: raise ValueError("n must be positive")
    if len(candles)<n+1: return unavailable(provenance=f"M1_LOW_PRIOR_{n}",as_of=candles[-1].timestamp if candles else None,reason=f"requires {n} prior candles")
    return available(min(c.low for c in candles[-n-1:-1]),provenance=f"M1_LOW_PRIOR_{n}",as_of=candles[-1].timestamp)

def compression_ratio(candles: Sequence[Candle], n: int) -> FeatureValue:
    if len(candles)<n+1: return unavailable(provenance=f"M1_RANGE_COMPRESSION_{n}",as_of=candles[-1].timestamp if candles else None,reason=f"requires {n+1} ranges")
    current=candles[-1].high-candles[-1].low
    base=median([c.high-c.low for c in candles[-n-1:-1]])
    if base<=0: return unavailable(provenance=f"M1_RANGE_COMPRESSION_{n}",as_of=candles[-1].timestamp,reason="baseline median range is non-positive")
    return available(current/base,provenance=f"M1_RANGE_COMPRESSION_{n}",as_of=candles[-1].timestamp)

def pullback_depth(bullish: bool, low: float, high: float, price: float, *, as_of=None) -> FeatureValue:
    if high<=low: return unavailable(provenance="STRUCTURAL_IMPULSE",as_of=as_of,reason="impulse range is non-positive")
    value=(high-price)/(high-low) if bullish else (price-low)/(high-low)
    return available(value,provenance="STRUCTURAL_IMPULSE",as_of=as_of)
