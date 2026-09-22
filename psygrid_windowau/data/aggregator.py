from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import Candle, TimeframeBar


def bucket_start(timestamp: datetime, timeframe_minutes: int) -> datetime:
    if timeframe_minutes not in (5, 15, 30):
        raise ValueError("WindowAU supports only M5, M15 and M30")
    ts = timestamp.astimezone(timezone.utc)
    epoch_minutes = int(ts.timestamp() // 60)
    start_epoch_minutes = (epoch_minutes // timeframe_minutes) * timeframe_minutes
    return datetime.fromtimestamp(start_epoch_minutes * 60, tz=timezone.utc)


def bucket_end(start: datetime, timeframe_minutes: int) -> datetime:
    return start + timedelta(minutes=timeframe_minutes)


def aggregate_complete(candles: tuple[Candle, ...], timeframe_minutes: int) -> tuple[TimeframeBar, ...]:
    if timeframe_minutes not in (5, 15, 30):
        raise ValueError("WindowAU supports only M5, M15 and M30")
    ordered = sorted(candles, key=lambda c: c.timestamp)
    buckets: dict[datetime, list[Candle]] = {}
    for candle in ordered:
        start = bucket_start(candle.timestamp, timeframe_minutes)
        buckets.setdefault(start, []).append(candle)

    result: list[TimeframeBar] = []
    for start, members in sorted(buckets.items()):
        expected = tuple(start + timedelta(minutes=i) for i in range(timeframe_minutes))
        timestamps = tuple(c.timestamp for c in members)
        if timestamps != expected:
            continue
        end = bucket_end(start, timeframe_minutes)
        result.append(
            TimeframeBar(
                start=start,
                end=end,
                timeframe_minutes=timeframe_minutes,
                open=members[0].open,
                high=max(c.high for c in members),
                low=min(c.low for c in members),
                close=members[-1].close,
                volume=sum(c.volume for c in members),
                component_timestamps=timestamps,
                complete=True,
            )
        )
    return tuple(result)
