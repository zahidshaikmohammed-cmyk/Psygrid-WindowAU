from __future__ import annotations

PAYLOAD = {
    "schema_version": "1.0",
    "service": "pysgrid-forex",
    "provider": "realmarketapi",
    "timeframe": "M1",
    "generated_at": "2026-09-22T19:26:48.792448Z",
    "status": "ok",
    "universe_size": 10,
    "symbols": {
        "XAUUSD": {
            "symbol": "XAUUSD",
            "market_state": "open",
            "status": "ok",
            "last_candle_timestamp": "2026-09-22T19:25:00Z",
            "updated_at": "2026-09-22T19:26:05.868405Z",
            "websocket_connected": True,
            "reconnect_count": 144,
            "gap_recoveries": 5,
            "rejected_count": 129,
            "candles_1m": [
                {
                    "timestamp": "2026-09-22T19:24:00Z",
                    "open": 4353.205,
                    "high": 4355.245,
                    "low": 4352.772,
                    "close": 4354.423,
                    "volume": 169,
                    "bid": None,
                    "ask": None,
                },
                {
                    "timestamp": "2026-09-22T19:25:00Z",
                    "open": 4354.423,
                    "high": 4356.000,
                    "low": 4353.900,
                    "close": 4355.100,
                    "volume": 171,
                    "bid": None,
                    "ask": None,
                },
            ],
            "m1_valid": True,
        }
    },
}
