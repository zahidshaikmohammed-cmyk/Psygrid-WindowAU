from datetime import datetime, timezone
from pathlib import Path

from psygrid_windowau.data.capture import ObservationCapture
from psygrid_windowau.data.models import Candle, CandleObservation, CandleState


def test_observation_capture_is_append_only(tmp_path: Path):
    path = tmp_path / "capture.jsonl"
    capture = ObservationCapture(path)
    candle = Candle(datetime(2026, 9, 22, 19, 0, tzinfo=timezone.utc), 4350, 4352, 4349, 4351, 10)
    obs = CandleObservation(
        observation_timestamp=datetime(2026, 9, 22, 19, 1, tzinfo=timezone.utc),
        provider_timestamp=candle.timestamp,
        candle_state=CandleState.CLOSED,
        candle=candle,
        symbol="XAUUSD",
        source="RealMarketAPI",
        feed_status="ok",
        freshness_seconds=1,
        connection_state=True,
    )
    capture.append(obs)
    capture.append(obs)
    rows = capture.read_all()
    assert len(rows) == 2
    assert rows[0]["observation_timestamp"] == rows[1]["observation_timestamp"]
    assert rows[0]["candle"]["close"] == 4351
