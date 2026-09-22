from datetime import datetime, timezone, timedelta

from psygrid_windowau.data.aggregator import aggregate_complete, bucket_start
from psygrid_windowau.data.models import Candle


def make_candles(start: datetime, count: int) -> tuple[Candle, ...]:
    return tuple(
        Candle(start + timedelta(minutes=i), 100+i, 101+i, 99+i, 100.5+i, 1)
        for i in range(count)
    )


def test_absolute_m5_bucket():
    ts = datetime(2026, 9, 22, 19, 17, tzinfo=timezone.utc)
    assert bucket_start(ts, 5) == datetime(2026, 9, 22, 19, 15, tzinfo=timezone.utc)


def test_complete_m5_requires_exact_five_components():
    start = datetime(2026, 9, 22, 19, 15, tzinfo=timezone.utc)
    bars = aggregate_complete(make_candles(start, 5), 5)
    assert len(bars) == 1
    assert bars[0].open == 100
    assert bars[0].high == 105
    assert bars[0].low == 99
    assert bars[0].close == 104.5
    assert bars[0].volume == 5


def test_incomplete_m5_is_not_emitted():
    start = datetime(2026, 9, 22, 19, 15, tzinfo=timezone.utc)
    assert aggregate_complete(make_candles(start, 4), 5) == ()


def test_gap_inside_bucket_is_not_fabricated():
    start = datetime(2026, 9, 22, 19, 15, tzinfo=timezone.utc)
    candles = list(make_candles(start, 5))
    candles.pop(2)
    assert aggregate_complete(tuple(candles), 5) == ()


def test_m15_and_m30_use_absolute_buckets():
    start = datetime(2026, 9, 22, 19, 0, tzinfo=timezone.utc)
    candles = make_candles(start, 30)
    assert len(aggregate_complete(candles, 15)) == 2
    assert len(aggregate_complete(candles, 30)) == 1
