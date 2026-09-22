from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low, candidate_parameters
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_lsr(candles: Sequence[Candle], *, lookback: int) -> SetupCandidate | None:
    """Detect LSR only after a breach candle is followed by a completed return candle."""
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if len(candles) < lookback + 2:
        return None
    i = len(candles) - 1
    return_candle = candles[i]
    sweep_index = i - 1
    swept_high = prior_high(candles, lookback, sweep_index)
    swept_low = prior_low(candles, lookback, sweep_index)
    sweep = candles[sweep_index]
    if swept_high is not None and sweep.high > swept_high and return_candle.close < swept_high:
        return SetupCandidate(
            SetupFamily.LSR, SetupDirection.SHORT,
            sweep.timestamp, return_candle.timestamp, sweep_index,
            swept_high, sweep.high,
            ("prior_high_exists", "M1_breached_high", "subsequent_M1_returned_below_level"),
            candidate_parameters(lookback=lookback, max_lifetime_minutes=15),
        )
    if swept_low is not None and sweep.low < swept_low and return_candle.close > swept_low:
        return SetupCandidate(
            SetupFamily.LSR, SetupDirection.LONG,
            sweep.timestamp, return_candle.timestamp, sweep_index,
            swept_low, sweep.low,
            ("prior_low_exists", "M1_breached_low", "subsequent_M1_returned_above_level"),
            candidate_parameters(lookback=lookback, max_lifetime_minutes=15),
        )
    return None
