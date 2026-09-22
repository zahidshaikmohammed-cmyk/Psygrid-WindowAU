from datetime import datetime, timedelta, timezone
from math import isclose, log, sqrt
from psygrid_windowau.data.models import Candle, FeatureState
from psygrid_windowau.features.returns import simple_return, log_return
from psygrid_windowau.features.volatility import true_ranges, atr, realized_volatility
from psygrid_windowau.features.trend import ema, ema_slope
from psygrid_windowau.features.vwap import session_vwap
from psygrid_windowau.features.candle_geometry import geometry
from psygrid_windowau.features.structure import prior_high, prior_low, compression_ratio, pullback_depth
from psygrid_windowau.features.momentum import displacement

def candles(closes, ranges=None):
    base=datetime(2026,1,1,tzinfo=timezone.utc)
    ranges=ranges or [2.0]*len(closes)
    return tuple(Candle(base+timedelta(minutes=i), c-0.5, c+r/2, c-r/2, c, 1.0) for i,(c,r) in enumerate(zip(closes,ranges)))

def test_returns():
    xs=candles([100,101])
    assert isclose(simple_return(xs).value,.01)
    assert isclose(log_return(xs).value,log(1.01))

def test_atr_wilder_initialization_and_update():
    xs=candles([100,101,102,104], [2,4,2,6])
    tr=true_ranges(xs)
    expected=sum(tr[:2])/2
    expected=(expected+tr[2])/2
    expected=(expected+tr[3])/2
    assert isclose(atr(xs,2).value,expected)

def test_realized_volatility_formula():
    xs=candles([100,101,100,102,101])
    rs=[log(xs[i].close/xs[i-1].close) for i in range(1,len(xs))]
    rs=rs[-3:]; m=sum(rs)/3
    expected=sqrt(3)*sqrt(sum((x-m)**2 for x in rs)/3)
    assert isclose(realized_volatility(xs,3).value,expected)

def test_ema_simple_mean_seed():
    xs=candles([1,2,3,4,5])
    assert isclose(ema(xs,3).value, (3*(1/2)+4*(1/2)+5*(1/2)) if False else 4.0)

def test_ema_slope():
    xs=candles([1,2,3,4,5,6])
    assert isclose(ema_slope(xs,3,1).value,1.0)

def test_vwap_and_zero_volume():
    xs=candles([100,101])
    assert session_vwap(xs).state is FeatureState.AVAILABLE
    zero=tuple(Candle(c.timestamp,c.open,c.high,c.low,c.close,0) for c in xs)
    assert session_vwap(zero).state is FeatureState.UNAVAILABLE

def test_geometry_and_structure_exclude_current_candle():
    xs=candles([10,12,11,14], [2,4,6,8])
    g=geometry(xs[-1])
    assert isclose(g["range"].value,8)
    assert isclose(g["body_ratio"].value,0.0)
    assert isclose(prior_high(xs,2).value,12)
    assert isclose(prior_low(xs,2).value,9)
    assert isclose(compression_ratio(xs,2).value,8/5)
    assert isclose(pullback_depth(True,10,20,15).value,.5)

def test_displacement_uses_prior_baseline_only():
    xs=candles([10,10,10,10], [2,4,6,20])
    d=displacement(xs,3)
    assert isclose(d["range_ratio"].value,20/4)

def test_warmup_is_unavailable():
    xs=candles([1,2])
    assert ema(xs,3).state is FeatureState.UNAVAILABLE
    assert atr(xs,3).state is FeatureState.UNAVAILABLE
