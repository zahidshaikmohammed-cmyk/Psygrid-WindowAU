from datetime import datetime, timezone, timedelta

from psygrid_windowau.data.models import Candle, DataQualityState
from psygrid_windowau.data.quality import (
    freshness_seconds,
    is_fresh,
    validate_candle,
    validate_series,
)


def candle(ts: str, close: float = 4350.0) -> Candle:
    return Candle(datetime.fromisoformat(ts.replace("Z", "+00:00")), 4349, 4352, 4348, close, 10)


def test_valid_candle():
    assert validate_candle(candle("2026-09-22T19:00:00Z")).state == DataQualityState.VALID


def test_invalid_ohlc():
    bad = Candle(datetime(2026, 9, 22, tzinfo=timezone.utc), 4355, 4352, 4348, 4350, 10)
    report = validate_candle(bad)
    assert report.state == DataQualityState.INVALID
    assert any(i.code == "INVALID_OPEN" for i in report.issues)


def test_duplicate_detection():
    c1 = candle("2026-09-22T19:00:00Z")
    report = validate_series((c1, c1))
    assert report.state == DataQualityState.DUPLICATE


def test_gap_detection():
    c1 = candle("2026-09-22T19:00:00Z")
    c2 = candle("2026-09-22T19:02:00Z")
    report = validate_series((c1, c2))
    assert report.state == DataQualityState.GAP


def test_freshness():
    provider = datetime(2026, 9, 22, 19, 0, tzinfo=timezone.utc)
    observed = provider + timedelta(seconds=7)
    assert freshness_seconds(observation_time=observed, provider_time=provider) == 7
    assert is_fresh(7, 10)
    assert not is_fresh(11, 10)
