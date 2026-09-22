from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import prior_high, prior_low, direction
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_spc(candles: Sequence[Candle], *, swing_lookback: int, pullback_bars: int = 3) -> SetupCandidate | None:
    if len(candles) < swing_lookback + pullback_bars + 1:
        return None
    if pullback_bars <= 0:
        raise ValueError("pullback_bars must be positive")
    i = len(candles)-1
    anchor = candles[i-pullback_bars]
    d = direction(anchor)
    if d is None:
        return None
    hi = prior_high(candles, swing_lookback, i-pullback_bars)
    lo = prior_low(candles, swing_lookback, i-pullback_bars)
    if hi is None or lo is None:
        return None
    pull = candles[i-pullback_bars+1:i+1]
    if d == "LONG":
        directional_structure = anchor.high >= hi and all(c.low > lo for c in pull)
        reference = lo
    else:
        directional_structure = anchor.low <= lo and all(c.high < hi for c in pull)
        reference = hi
    if not directional_structure:
        return None
    return SetupCandidate(SetupFamily.SPC, SetupDirection(d), anchor.timestamp, candles[-1].timestamp, i-pullback_bars, reference, reference, ("directional_structure", "controlled_pullback", "no_structural_invalidation"), (("swing_lookback", float(swing_lookback)), ("pullback_bars", float(pullback_bars))))
