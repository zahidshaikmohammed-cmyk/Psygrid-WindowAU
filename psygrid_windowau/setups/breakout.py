from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_boa(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    if len(candles) < lookback + 1:
        return None
    c = candles[-1]; hi = prior_high(candles, lookback); lo = prior_low(candles, lookback)
    if hi is not None and c.close > hi:
        return SetupCandidate(SetupFamily.BOA, SetupDirection.LONG, c.timestamp, c.timestamp, len(candles)-1, hi, hi, ("structural_level", "completed_close_beyond_level"), (("lookback", float(lookback)),))
    if lo is not None and c.close < lo:
        return SetupCandidate(SetupFamily.BOA, SetupDirection.SHORT, c.timestamp, c.timestamp, len(candles)-1, lo, lo, ("structural_level", "completed_close_beyond_level"), (("lookback", float(lookback)),))
    return None


def detect_bof(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    if len(candles) < lookback + 1:
        return None
    c = candles[-1]; hi = prior_high(candles, lookback); lo = prior_low(candles, lookback)
    if hi is not None and c.high > hi and c.close < hi:
        return SetupCandidate(SetupFamily.BOF, SetupDirection.SHORT, c.timestamp, c.timestamp, len(candles)-1, hi, c.high, ("structural_level", "break", "reentry"), (("lookback", float(lookback)),))
    if lo is not None and c.low < lo and c.close > lo:
        return SetupCandidate(SetupFamily.BOF, SetupDirection.LONG, c.timestamp, c.timestamp, len(candles)-1, lo, c.low, ("structural_level", "break", "reentry"), (("lookback", float(lookback)),))
    return None
