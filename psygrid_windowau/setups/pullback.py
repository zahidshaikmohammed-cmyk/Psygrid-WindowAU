from __future__ import annotations

from collections.abc import Sequence

from psygrid_windowau.data.models import Candle
from .common import direction, median_range, candidate_parameters
from .models import SetupCandidate, SetupDirection, SetupFamily


def detect_epc(candles: Sequence[Candle], *, baseline_lookback: int, expansion_multiple: float = 1.5, max_pullback_bars: int = 5) -> SetupCandidate | None:
    """Detect an expansion followed by a controlled pullback; continuation trigger is Phase 4."""
    if baseline_lookback <= 0 or max_pullback_bars <= 0 or expansion_multiple <= 0:
        raise ValueError("baseline_lookback, max_pullback_bars and expansion_multiple must be positive")
    i = len(candles) - 1
    if len(candles) < baseline_lookback + 3:
        return None
    first = max(baseline_lookback, i - max_pullback_bars)
    for j in range(i - 1, first - 1, -1):
        baseline = median_range(candles, baseline_lookback, j)
        impulse = candles[j]
        d = direction(impulse)
        if baseline is None or baseline <= 0 or d is None or (impulse.high - impulse.low) < baseline * expansion_multiple:
            continue
        pullback = candles[j + 1:i + 1]
        if not pullback:
            continue
        if d == "LONG":
            preserved = min(c.low for c in pullback) > impulse.low
            controlled = min(c.low for c in pullback) < impulse.close
        else:
            preserved = max(c.high for c in pullback) < impulse.high
            controlled = max(c.high for c in pullback) > impulse.close
        if preserved and controlled:
            return SetupCandidate(SetupFamily.EPC, SetupDirection(d), impulse.timestamp, candles[-1].timestamp, j, impulse.close, impulse.low if d == "LONG" else impulse.high, ("qualifying_expansion", "impulse_direction", "controlled_pullback"), candidate_parameters(baseline_lookback=baseline_lookback, expansion_multiple=expansion_multiple, max_pullback_bars=max_pullback_bars, max_lifetime_minutes=20))
    return None
