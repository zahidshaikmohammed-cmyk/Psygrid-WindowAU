from __future__ import annotations
from collections.abc import Sequence
from psygrid_windowau.data.models import Candle
from .common import FeatureValue, available, unavailable

def session_vwap(candles: Sequence[Candle]) -> FeatureValue:
    if not candles: return unavailable(provenance="SESSION_FEED_VOLUME", as_of=None, reason="empty session")
    volume=sum(c.volume for c in candles)
    if volume==0: return unavailable(provenance="SESSION_FEED_VOLUME", as_of=candles[-1].timestamp, reason="cumulative feed volume is zero")
    if volume<0: return unavailable(provenance="SESSION_FEED_VOLUME", as_of=candles[-1].timestamp, reason="negative cumulative volume")
    pv=sum(((c.high+c.low+c.close)/3.0)*c.volume for c in candles)
    return available(pv/volume, provenance="SESSION_FEED_VOLUME", as_of=candles[-1].timestamp)
