from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low, candidate_parameters
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_boa(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    """Detect a breakout/acceptance minimum setup; Phase 4 owns the M1 trigger."""
    if len(candles) < lookback + 2:
        return None
    i = len(candles) - 1
    current = candles[i]
    previous = candles[i - 1]
    hi = prior_high(candles, lookback, i - 1)
    lo = prior_low(candles, lookback, i - 1)
    if hi is not None and previous.close > hi and current.low >= hi:
        return SetupCandidate(SetupFamily.BOA, SetupDirection.LONG, previous.timestamp, current.timestamp, i - 1, hi, hi, ("structural_level", "completed_close_beyond_level", "acceptance_persistence"), candidate_parameters(lookback=lookback, max_lifetime_minutes=15))
    if lo is not None and previous.close < lo and current.high <= lo:
        return SetupCandidate(SetupFamily.BOA, SetupDirection.SHORT, previous.timestamp, current.timestamp, i - 1, lo, lo, ("structural_level", "completed_close_beyond_level", "acceptance_persistence"), candidate_parameters(lookback=lookback, max_lifetime_minutes=15))
    return None


def detect_bof(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    """Detect a breakout-failure minimum setup; Phase 4 owns the M1 trigger confirmation."""
    if len(candles) < lookback + 2:
        return None
    i = len(candles) - 1
    previous = candles[i - 1]
    current = candles[i]
    hi = prior_high(candles, lookback, i - 1)
    lo = prior_low(candles, lookback, i - 1)
    if hi is not None and previous.high > hi and current.close < hi:
        return SetupCandidate(SetupFamily.BOF, SetupDirection.SHORT, previous.timestamp, current.timestamp, i - 1, hi, previous.high, ("structural_level", "break", "reentry"), candidate_parameters(lookback=lookback, max_lifetime_minutes=15))
    if lo is not None and previous.low < lo and current.close > lo:
        return SetupCandidate(SetupFamily.BOF, SetupDirection.LONG, previous.timestamp, current.timestamp, i - 1, lo, previous.low, ("structural_level", "break", "reentry"), candidate_parameters(lookback=lookback, max_lifetime_minutes=15))
    return None
