from __future__ import annotations
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, invalid, unavailable

def geometry(candle: Candle) -> dict[str, FeatureValue]:
    as_of=candle.timestamp
    r=candle.high-candle.low
    if r<0: return {"range":invalid(provenance="M1_OHLC",as_of=as_of,reason="negative range")}
    if r==0:
        z=unavailable(provenance="M1_OHLC",as_of=as_of,reason="zero range")
        return {"range":available(0.0,provenance="M1_OHLC",as_of=as_of),"body":available(abs(candle.close-candle.open),provenance="M1_OHLC",as_of=as_of),"body_ratio":z,"upper_wick":z,"lower_wick":z}
    body=abs(candle.close-candle.open)
    uw=candle.high-max(candle.open,candle.close)
    lw=min(candle.open,candle.close)-candle.low
    return {"range":available(r,provenance="M1_OHLC",as_of=as_of),"body":available(body,provenance="M1_OHLC",as_of=as_of),"body_ratio":available(body/r,provenance="M1_OHLC",as_of=as_of),"upper_wick":available(uw/r,provenance="M1_OHLC",as_of=as_of),"lower_wick":available(lw/r,provenance="M1_OHLC",as_of=as_of)}
