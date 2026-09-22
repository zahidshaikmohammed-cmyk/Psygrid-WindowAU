# PSYGRID WindowAU — Canonical Data Source Record

Version 1.0 — Phase 0 Source Lock

## 1. Canonical provider endpoint

Provider: RealMarketAPI
Service payload: `pysgrid-forex`
Timeframe: M1
Endpoint:

`http://140.245.226.102:8080/public/live.json`

This endpoint is the canonical initial data source for WindowAU.

## 2. Instrument scope

WindowAU consumes **XAUUSD only** from the multi-symbol response.

Canonical extraction path:

`symbols → XAUUSD → candles_1m`

Other symbols in the response are outside WindowAU scope and must not be scanned, evaluated, or emitted as WindowAU candidates/signals.

## 3. Confirmed response envelope

The observed payload contains:

- `schema_version`
- `service`
- `provider`
- `timeframe`
- `generated_at`
- `status`
- `universe_size`
- `symbols`

The XAUUSD object contains:

- `symbol`
- `market_state`
- `status`
- `last_candle_timestamp`
- `updated_at`
- `websocket_connected`
- `reconnect_count`
- `gap_recoveries`
- `rejected_count`
- `candles_1m`
- `m1_valid`

Each M1 candle contains:

- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `bid`
- `ask`

## 4. Example observed payload

```json
{
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
      "websocket_connected": true,
      "reconnect_count": 144,
      "gap_recoveries": 5,
      "rejected_count": 129,
      "candles_1m": [
        {
          "timestamp": "2026-09-21T16:18:00Z",
          "open": 4353.205,
          "high": 4355.245,
          "low": 4352.772,
          "close": 4354.423,
          "volume": 169,
          "bid": null,
          "ask": null
        }
      ],
      "m1_valid": true
    }
  }
}
```

The example is a schema fixture, not a claim that these prices or counters remain current.

## 5. Source interpretation rules

- The provider payload is treated as authoritative only for the fields it actually supplies.
- `bid` and `ask` may be null and are optional under the current WindowAU data contract.
- `volume` is feed-volume until its exact provider semantics are verified.
- `timestamp` semantics are **UNVERIFIED** until the provider timestamp-verification procedure establishes that it represents candle opening time or another explicit semantic.
- No undocumented alternate endpoint/schema is silently substituted.
- Provider failure never creates synthetic candles or prices.

## 6. Source-health metadata

The engine must preserve provider metadata for diagnostics:

`status`, `market_state`, `m1_valid`, `last_candle_timestamp`, `updated_at`, `websocket_connected`, `reconnect_count`, `gap_recoveries`, `rejected_count`.

These fields are quality/diagnostic evidence; they do not independently create trading signals.

## 7. Source change control

Changing provider, endpoint, payload schema, symbol extraction path, or timestamp semantics requires:

1. explicit documentation change;
2. source-version update;
3. parser/test fixture update;
4. data-contract audit;
5. causal replay audit;
6. Phase-0/implementation regression tests.

Silent source substitution is prohibited.

## 8. Verification status

Current source status:

`SCHEMA_CONFIRMED_FROM_OBSERVED_PAYLOAD`

Current timestamp status:

`UNVERIFIED`

Current production signal status:

`NOT_YET_ENABLED`

The source record does not claim live trading readiness. It locks the observed schema for implementation and verification.
