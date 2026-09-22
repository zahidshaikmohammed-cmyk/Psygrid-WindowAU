from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import direction, median_range
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_epc(candles: Sequence[Candle], *, baseline_lookback: int, expansion_multiple: float = 1.5, max_pullback_bars: int = 5) -> SetupCandidate | None:
    """Detect an expansion followed by a controlled pullback; continuation is Phase 4."""
    if len(candles) < baseline_lookback + 2:
        return None
    if expansion_multiple <= 0 or max_pullback_bars <= 0:
        raise ValueError("expansion_multiple and max_pullback_bars must be positive")
    i = len(candles) - 1
    baseline = median_range(candles, baseline_lookback, i - 1)
    if baseline is None or baseline <= 0:
        return None
    impulse = candles[i - 1]
    d = direction(impulse)
    if d is None or (impulse.high - impulse.low) < baseline * expansion_multiple:
        return None
    start = max(0, i - max_pullback_bars)
    pullback = candles[start:i]
    if not pullback:
        return None
    if d == "LONG":
        preserved = min(c.low for c in pullback) > impulse.low
        touched = min(c.low for c in pullback) < impulse.close
    else:
        preserved = max(c.high for c in pullback) < impulse.high
        touched = max(c.high for c in pullback) > impulse.close
    if not (preserved and touched):
        return None
    return SetupCandidate(SetupFamily.EPC, SetupDirection(d), impulse.timestamp, candles[-1].timestamp, i-1, impulse.close, impulse.low if d == "LONG" else impulse.high, ("qualifying_expansion", "impulse_direction", "controlled_pullback"), (("baseline_lookback", float(baseline_lookback)), ("expansion_multiple", float(expansion_multiple)), ("max_pullback_bars", float(max_pullback_bars))))
