from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path

from .models import CandleObservation


class ObservationCapture:
    """Append-only JSONL capture for causal replay."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, observation: CandleObservation) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(observation)
        payload["observation_timestamp"] = observation.observation_timestamp.isoformat().replace("+00:00", "Z")
        payload["provider_timestamp"] = observation.provider_timestamp.isoformat().replace("+00:00", "Z")
        payload["candle_state"] = observation.candle_state.value
        payload["candle"] = {
            "timestamp": observation.candle.timestamp.isoformat().replace("+00:00", "Z"),
            "open": observation.candle.open,
            "high": observation.candle.high,
            "low": observation.candle.low,
            "close": observation.candle.close,
            "volume": observation.candle.volume,
            "bid": observation.candle.bid,
            "ask": observation.candle.ask,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n")

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]


def observation_now() -> datetime:
    return datetime.now(timezone.utc)
