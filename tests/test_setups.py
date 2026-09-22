from datetime import datetime, timedelta, timezone

from psygrid_windowau.data.models import Candle
from psygrid_windowau.setups.models import SetupFamily, SetupDirection
from psygrid_windowau.setups.sweep import detect_lsr
from psygrid_windowau.setups.pullback import detect_epc
from psygrid_windowau.setups.breakout import detect_boa, detect_bof
from psygrid_windowau.setups.rejection import detect_rre
from psygrid_windowau.setups.continuation import detect_spc


def cs(rows):
    base=datetime(2026,1,1,tzinfo=timezone.utc)
    return tuple(Candle(base+timedelta(minutes=i),o,h,l,c,1) for i,(o,h,l,c) in enumerate(rows))


def test_lsr_and_bof_are_independent():
    x=cs([(10,11,9,10),(10,12,9,11),(11,14,10,11),(11,13,8,9.5)])
    l=detect_lsr(x,lookback=3); b=detect_bof(x,lookback=3)
    assert l and l.family is SetupFamily.LSR and l.direction is SetupDirection.SHORT
    assert b and b.family is SetupFamily.BOF


def test_boa_requires_completed_close_beyond_level():
    x=cs([(10,11,9,10),(10,11,9,10),(10,12,9,11.5)])
    c=detect_boa(x,lookback=2)
    assert c and c.family is SetupFamily.BOA and c.direction is SetupDirection.LONG


def test_rre_detects_range_extreme_rejection():
    x=cs([(10,11,9,10),(10,11,9,10),(10,12,9,11)])
    c=detect_rre(x,lookback=2)
    assert c and c.direction is SetupDirection.SHORT


def test_epc_requires_expansion_and_controlled_pullback():
    x=cs([(10,11,9,10),(10,11,9,10),(10,14,9,13),(13,13.5,11.5,12.5),(12.5,13,12,12.8)])
    c=detect_epc(x,baseline_lookback=2,expansion_multiple=1.5,max_pullback_bars=3)
    assert c and c.family is SetupFamily.EPC and c.direction is SetupDirection.LONG


def test_spc_detects_directional_structure_and_pullback():
    x=cs([(10,11,9,10),(10,12,9.5,11.5),(11.5,13,10.5,12.5),(12.5,12.7,11.8,12),(12,12.2,11.7,12.1)])
    c=detect_spc(x,swing_lookback=2,pullback_bars=2)
    assert c and c.family is SetupFamily.SPC


def test_detectors_do_not_use_future_candles():
    x=cs([(10,11,9,10),(10,12,9,11),(11,14,10,13)])
    before=detect_boa(x,lookback=2)
    future=cs([(10,11,9,10),(10,12,9,11),(11,14,10,13),(13,20,12,19)])
    assert before is not None
    assert before.anchor_timestamp == detect_boa(future[:3],lookback=2).anchor_timestamp


def test_insufficient_history_returns_no_candidate_not_fake_data():
    x=cs([(10,11,9,10)])
    assert detect_lsr(x,lookback=5) is None
    assert detect_boa(x,lookback=5) is None
    assert detect_bof(x,lookback=5) is None
    assert detect_rre(x,lookback=5) is None
