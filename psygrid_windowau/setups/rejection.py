from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low, candidate_parameters
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_rre(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    if len(candles) < lookback + 1:
        return None
    c = candles[-1]; hi = prior_high(candles, lookback); lo = prior_low(candles, lookback)
    if hi is not None and c.high >= hi and c.close < hi:
        return SetupCandidate(SetupFamily.RRE, SetupDirection.SHORT, c.timestamp, c.timestamp, len(candles)-1, hi, c.high, ("range_boundary", "extreme_test", "rejection"), candidate_parameters(lookback=lookback, max_lifetime_minutes=20))
    if lo is not None and c.low <= lo and c.close > lo:
        return SetupCandidate(SetupFamily.RRE, SetupDirection.LONG, c.timestamp, c.timestamp, len(candles)-1, lo, c.low, ("range_boundary", "extreme_test", "rejection"), candidate_parameters(lookback=lookback, max_lifetime_minutes=20))
    return None
