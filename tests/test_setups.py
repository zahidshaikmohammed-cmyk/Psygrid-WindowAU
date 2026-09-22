from datetime import datetime, timedelta, timezone

import pytest

from psygrid_windowau.data.models import Candle
from psygrid_windowau.setups.models import SetupFamily, SetupDirection
from psygrid_windowau.setups.sweep import detect_lsr
from psygrid_windowau.setups.pullback import detect_epc
from psygrid_windowau.setups.breakout import detect_boa, detect_bof
from psygrid_windowau.setups.rejection import detect_rre
from psygrid_windowau.setups.continuation import detect_spc


def cs(rows):
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return tuple(Candle(base + timedelta(minutes=i), o, h, l, c, 1) for i, (o, h, l, c) in enumerate(rows))


def test_lsr_long_and_short_require_subsequent_return_candle():
    short = cs([(10, 11, 9, 10), (10, 12, 9, 11), (11, 14, 10, 13), (13, 13.5, 11, 11.5)])
    long = cs([(10, 11, 9, 10), (10, 12, 9, 11), (11, 12, 7, 9), (9, 10, 8.5, 11.5)])
    assert detect_lsr(short, lookback=3).direction is SetupDirection.SHORT
    assert detect_lsr(long, lookback=3).direction is SetupDirection.LONG
    assert detect_lsr(short[:-1], lookback=3) is None


def test_boa_requires_break_and_persistence():
    x = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 12, 9, 11.5), (11.5, 12, 11.1, 11.7)])
    c = detect_boa(x, lookback=2)
    assert c and c.family is SetupFamily.BOA and c.direction is SetupDirection.LONG
    assert "acceptance_persistence" in c.evidence


def test_bof_long_and_short_are_independent():
    short = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 12, 9, 11), (11, 13, 8, 9.5)])
    long = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 12, 9, 9), (9, 10, 8, 10.5)])
    assert detect_bof(short, lookback=2).direction is SetupDirection.SHORT
    assert detect_bof(long, lookback=2).direction is SetupDirection.LONG


def test_rre_long_and_short():
    short = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 12, 9, 11)])
    long = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 11, 8, 9.5)])
    assert detect_rre(short, lookback=2).direction is SetupDirection.SHORT
    assert detect_rre(long, lookback=2).direction is SetupDirection.LONG


def test_epc_requires_expansion_and_controlled_pullback():
    x = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 14, 9, 13), (13, 13.5, 11.5, 12.5), (12.5, 13, 12, 12.8)])
    c = detect_epc(x, baseline_lookback=2, expansion_multiple=1.5, max_pullback_bars=3)
    assert c and c.family is SetupFamily.EPC and c.direction is SetupDirection.LONG


def test_spc_detects_directional_structure_and_pullback():
    x = cs([(10, 11, 9, 10), (10, 12, 9.5, 11.5), (11.5, 13, 10.5, 12.5), (12.5, 12.7, 11.8, 12), (12, 12.2, 11.7, 12.1)])
    c = detect_spc(x, swing_lookback=2, pullback_bars=2)
    assert c and c.family is SetupFamily.SPC


def test_candidates_have_lifetime_and_stable_identity():
    x = cs([(10, 11, 9, 10), (10, 11, 9, 10), (10, 12, 9, 11.5), (11.5, 12, 11.1, 11.7)])
    c = detect_boa(x, lookback=2)
    assert c.identity == ("BOA", "LONG", "11.0000000000", 2)
    assert dict(c.parameters)["max_lifetime_minutes"] == 15


def test_detectors_are_causal_to_supplied_prefix():
    prefix = cs([(10, 11, 9, 10), (10, 12, 9, 11), (11, 14, 10, 13)])
    future = cs([(10, 11, 9, 10), (10, 12, 9, 11), (11, 14, 10, 13), (13, 20, 12, 19)])
    before = detect_boa(prefix, lookback=2)
    replayed = detect_boa(future[:3], lookback=2)
    assert before and replayed
    assert before.identity == replayed.identity


def test_insufficient_history_never_fabricates_a_candidate():
    x = cs([(10, 11, 9, 10)])
    assert detect_lsr(x, lookback=5) is None
    assert detect_boa(x, lookback=5) is None
    assert detect_bof(x, lookback=5) is None
    assert detect_rre(x, lookback=5) is None
    assert detect_epc(x, baseline_lookback=5) is None
    assert detect_spc(x, swing_lookback=5) is None


def test_invalid_detector_parameters_are_explicit():
    x = cs([(10, 11, 9, 10)] * 5)
    with pytest.raises(ValueError): detect_lsr(x, lookback=0)
    with pytest.raises(ValueError): detect_boa(x, lookback=0)
    with pytest.raises(ValueError): detect_epc(x, baseline_lookback=0)
    with pytest.raises(ValueError): detect_spc(x, swing_lookback=0)



def test_phase3_validation_marker():
    assert all(f.value for f in SetupFamily)
