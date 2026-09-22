from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low, direction, candidate_parameters
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_spc(candles: Sequence[Candle], *, swing_lookback: int, pullback_bars: int = 3) -> SetupCandidate | None:
    if swing_lookback <= 0 or pullback_bars <= 0:
        raise ValueError("swing_lookback and pullback_bars must be positive")
    i = len(candles)-1
    if len(candles) < swing_lookback + pullback_bars + 1:
        return None
    anchor_index = i - pullback_bars
    anchor = candles[anchor_index]
    d = direction(anchor)
    if d is None:
        return None
    hi = prior_high(candles, swing_lookback, anchor_index)
    lo = prior_low(candles, swing_lookback, anchor_index)
    if hi is None or lo is None:
        return None
    pull = candles[anchor_index + 1:i + 1]
    if d == "LONG":
        valid = anchor.high >= hi and all(c.low > lo for c in pull)
        reference = lo
    else:
        valid = anchor.low <= lo and all(c.high < hi for c in pull)
        reference = hi
    if not valid:
        return None
    return SetupCandidate(SetupFamily.SPC, SetupDirection(d), anchor.timestamp, candles[-1].timestamp, anchor_index, reference, reference, ("directional_structure", "controlled_pullback", "no_structural_invalidation"), candidate_parameters(swing_lookback=swing_lookback, pullback_bars=pullback_bars, max_lifetime_minutes=20))
