from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low, candidate_parameters
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_lsr(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    """Detect the frozen LSR minimum setup from completed M1 observations only."""
    if len(candles) < lookback + 1:
        return None
    c = candles[-1]
    hi = prior_high(candles, lookback)
    lo = prior_low(candles, lookback)
    if hi is not None and c.high > hi and c.close < hi:
        return SetupCandidate(SetupFamily.LSR, SetupDirection.SHORT, c.timestamp, c.timestamp, len(candles)-1, hi, c.high, ("prior_high_exists", "M1_breached_high", "M1_returned_below_level"), candidate_parameters(lookback=lookback, max_lifetime_minutes=15))
    if lo is not None and c.low < lo and c.close > lo:
        return SetupCandidate(SetupFamily.LSR, SetupDirection.LONG, c.timestamp, c.timestamp, len(candles)-1, lo, c.low, ("prior_low_exists", "M1_breached_low", "M1_returned_above_level"), candidate_parameters(lookback=lookback, max_lifetime_minutes=15))
    return None
