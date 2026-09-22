from __future__ import annotations
from collections.abc import Sequence
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, unavailable

def ema(candles: Sequence[Candle], n: int) -> FeatureValue:
    if n<=0: raise ValueError("n must be positive")
    if len(candles)<n: return unavailable(provenance=f"M1_CLOSE_EMA_{n}", as_of=candles[-1].timestamp if candles else None, reason=f"requires {n} completed closes")
    closes=[c.close for c in candles]
    value=sum(closes[:n])/n
    alpha=2.0/(n+1)
    for close in closes[n:]: value=alpha*close+(1-alpha)*value
    return available(value, provenance=f"M1_CLOSE_EMA_{n}", as_of=candles[-1].timestamp)

def ema_series(candles: Sequence[Candle], n: int) -> tuple[float,...]:
    if len(candles)<n: return ()
    closes=[c.close for c in candles]
    value=sum(closes[:n])/n
    out=[value]
    alpha=2.0/(n+1)
    for close in closes[n:]:
        value=alpha*close+(1-alpha)*value
        out.append(value)
    return tuple(out)

def ema_slope(candles: Sequence[Candle], n: int, k: int) -> FeatureValue:
    if k<=0: raise ValueError("k must be positive")
    series=ema_series(candles,n)
    if len(series)<=k: return unavailable(provenance=f"M1_EMA_{n}_SLOPE_{k}", as_of=candles[-1].timestamp if candles else None, reason=f"requires EMA history for k={k}")
    return available((series[-1]-series[-1-k])/k, provenance=f"M1_EMA_{n}_SLOPE_{k}", as_of=candles[-1].timestamp)

def trend_persistence(candles: Sequence[Candle], n: int) -> FeatureValue:
    if len(candles)<n+1: return unavailable(provenance=f"M1_RETURNS_PERSISTENCE_{n}", as_of=candles[-1].timestamp if candles else None, reason=f"requires {n} returns")
    rs=[1 if candles[i].close>candles[i-1].close else -1 if candles[i].close<candles[i-1].close else 0 for i in range(len(candles)-n,len(candles))]
    return available(sum(rs)/n, provenance=f"M1_RETURNS_PERSISTENCE_{n}", as_of=candles[-1].timestamp)
