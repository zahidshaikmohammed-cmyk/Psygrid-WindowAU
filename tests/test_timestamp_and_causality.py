from datetime import datetime, timezone

import pytest

from psygrid_windowau.data.models import CandleState, TimestampStatus
from psygrid_windowau.data.quality import freshness_seconds


def test_timestamp_starts_unverified():
    assert TimestampStatus.UNVERIFIED.value == "UNVERIFIED"


def test_unverified_timestamp_is_not_treated_as_open_time():
    status = TimestampStatus.UNVERIFIED
    assert status is not TimestampStatus.VERIFIED_OPEN_TIME


def test_future_provider_timestamp_is_rejected_for_freshness():
    provider = datetime(2026, 9, 22, 19, 1, tzinfo=timezone.utc)
    observed = datetime(2026, 9, 22, 19, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        freshness_seconds(observation_time=observed, provider_time=provider)
