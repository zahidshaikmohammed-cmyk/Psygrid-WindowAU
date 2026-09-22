from __future__ import annotations
from collections.abc import Sequence
from math import sqrt
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, invalid, unavailable

def true_ranges(candles: Sequence[Candle]) -> tuple[float,...]:
    if not candles: return ()
    out=[]
    for i,c in enumerate(candles):
        if i==0: out.append(c.high-c.low)
        else:
            prev=candles[i-1].close
            out.append(max(c.high-c.low, abs(c.high-prev), abs(c.low-prev)))
    return tuple(out)

def atr(candles: Sequence[Candle], n: int) -> FeatureValue:
    if n<=0: raise ValueError("n must be positive")
    if len(candles)<n: return unavailable(provenance=f"M1_TR_WILDER_{n}", as_of=candles[-1].timestamp if candles else None, reason=f"requires {n} true ranges")
    tr=true_ranges(candles)
    value=sum(tr[:n])/n
    for x in tr[n:]: value=((n-1)*value+x)/n
    return available(value, provenance=f"M1_TR_WILDER_{n}", as_of=candles[-1].timestamp)

def rolling_atr(candles: Sequence[Candle], n: int) -> FeatureValue:
    if n<=0: raise ValueError("n must be positive")
    if len(candles)<n: return unavailable(provenance=f"M1_TR_ROLLING_{n}", as_of=candles[-1].timestamp if candles else None, reason=f"requires {n} true ranges")
    return available(sum(true_ranges(candles)[-n:])/n, provenance=f"M1_TR_ROLLING_{n}", as_of=candles[-1].timestamp)

def realized_volatility(candles: Sequence[Candle], n: int) -> FeatureValue:
    if n<=0: raise ValueError("n must be positive")
    if len(candles)<n+1: return unavailable(provenance=f"M1_LOG_RETURN_RV_{n}", as_of=candles[-1].timestamp if candles else None, reason=f"requires {n+1} closes")
    from .common import log_returns
    rs=log_returns([c.close for c in candles])[-n:]
    if not rs: return unavailable(provenance=f"M1_LOG_RETURN_RV_{n}", as_of=candles[-1].timestamp, reason="no returns")
    return available(sqrt(n)*sum((x-sum(rs)/len(rs))**2 for x in rs)/len(rs) ** 0.5, provenance=f"M1_LOG_RETURN_RV_{n}", as_of=candles[-1].timestamp)

def percentile(value: float, history: Sequence[float]) -> FeatureValue:
    if not history: return unavailable(provenance="ROLLING_HISTORY", as_of=None, reason="empty distribution")
    xs=sorted(float(x) for x in history)
    rank=sum(x<=value for x in xs)
    return available(100.0*rank/len(xs), provenance="ROLLING_HISTORY", as_of=None)
