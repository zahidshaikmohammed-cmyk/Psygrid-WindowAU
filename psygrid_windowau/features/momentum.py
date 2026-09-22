from __future__ import annotations
from collections.abc import Sequence
from statistics import median
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, unavailable

def displacement(candles: Sequence[Candle], n: int) -> dict[str, FeatureValue]:
    if len(candles)<n+1: 
        u=unavailable(provenance=f"M1_DISPLACEMENT_{n}",as_of=candles[-1].timestamp if candles else None,reason=f"requires {n+1} candles")
        return {"range_ratio":u,"body_ratio":u}
    current=candles[-1]
    base_ranges=[c.high-c.low for c in candles[-n-1:-1]]
    base_bodies=[abs(c.close-c.open) for c in candles[-n-1:-1]]
    mr=median(base_ranges); mb=median(base_bodies)
    ur=unavailable(provenance=f"M1_DISPLACEMENT_{n}",as_of=current.timestamp,reason="zero baseline")
    return {"range_ratio":available((current.high-current.low)/mr,provenance=f"M1_DISPLACEMENT_{n}",as_of=current.timestamp) if mr>0 else ur,
            "body_ratio":available(abs(current.close-current.open)/mb,provenance=f"M1_DISPLACEMENT_{n}",as_of=current.timestamp) if mb>0 else ur}
