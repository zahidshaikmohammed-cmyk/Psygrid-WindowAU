from copy import deepcopy

import pytest

from psygrid_windowau.data.client import (
    CANONICAL_URL,
    DataContractError,
    RealMarketApiClient,
)
from tests.fixtures_payload import PAYLOAD


def test_exact_canonical_xauusd_extraction():
    snapshot = RealMarketApiClient().parse_snapshot(PAYLOAD)
    assert snapshot.health.symbol == "XAUUSD"
    assert len(snapshot.candles) == 2
    assert snapshot.candles[0].close == 4354.423
    assert snapshot.health.provider == "realmarketapi"


def test_other_symbols_are_ignored():
    payload = deepcopy(PAYLOAD)
    payload["symbols"]["EURUSD"] = deepcopy(payload["symbols"]["XAUUSD"])
    payload["symbols"]["EURUSD"]["symbol"] = "EURUSD"
    snapshot = RealMarketApiClient().parse_snapshot(payload)
    assert snapshot.health.symbol == "XAUUSD"
    assert all(snapshot.health.symbol == "XAUUSD" for _ in snapshot.candles)


def test_missing_xauusd_fails():
    payload = deepcopy(PAYLOAD)
    del payload["symbols"]["XAUUSD"]
    with pytest.raises(DataContractError, match="XAUUSD"):
        RealMarketApiClient().parse_snapshot(payload)


def test_wrong_schema_fails_explicitly():
    payload = deepcopy(PAYLOAD)
    payload["symbols"]["XAUUSD"]["candles"] = payload["symbols"]["XAUUSD"].pop("candles_1m")
    with pytest.raises(DataContractError, match="schema mismatch"):
        RealMarketApiClient().parse_snapshot(payload)


def test_non_canonical_url_is_rejected():
    with pytest.raises(DataContractError):
        RealMarketApiClient(url="https://example.com").fetch_json()


def test_bid_ask_are_optional():
    payload = deepcopy(PAYLOAD)
    for candle in payload["symbols"]["XAUUSD"]["candles_1m"]:
        del candle["bid"]
        del candle["ask"]
    snapshot = RealMarketApiClient().parse_snapshot(payload)
    assert len(snapshot.candles) == 2
    assert snapshot.candles[0].bid is None
    assert snapshot.candles[0].ask is None
