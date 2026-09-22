# PSYGRID WindowAU — Data Contract

## 1. Primary Source
Initial source: RealMarketAPI M1 XAUUSD feed.

Expected candle fields:
timestamp, open, high, low, close, volume.

Bid/ask are optional.

## 2. Candle Semantics
Timestamp is treated as candle opening time until provider semantics are verified.

A candle is CLOSED only after its interval ends under verified semantics.

Never use final OHLC before close.

## 3. Aggregation
Completed k-minute bar:
Open = first M1 open
High = maximum M1 high
Low = minimum M1 low
Close = last M1 close
Volume = sum M1 volume

Only completed component candles form a completed higher-timeframe candle.

## 4. Quality
Check:
- monotonic timestamps;
- duplicates;
- OHLC consistency;
- non-negative volume;
- gaps;
- freshness;
- symbol identity;
- source identity.

Required data failure blocks only the affected family unless the entire feed is invalid.

## 5. Feature Availability
Every derived feature has:
AVAILABLE / UNAVAILABLE / INVALID.

UNAVAILABLE means no reliable value is available at decision time.

INVALID means the available value violates integrity checks.

Optional UNAVAILABLE does not become a directional zero and does not globally block the engine.

## 6. Warm-Up
Features requiring history may be UNAVAILABLE during warm-up.

The engine may preload verified historical M1 data.

Long warm-up features such as EMA200 must not globally suppress signal generation.

## 7. Forming State
Every series exposes:
- closed;
- forming;
- as_of.

A forming candle may be observed for display/monitoring but final OHLC is not available to the decision engine until close.

## 8. Gaps
Represent gaps explicitly.

Do not fabricate prices.

A family requiring missing data is blocked for that family and receives DATA_INVALID or an appropriate documented reason.

## 9. Optional Bid/Ask and Volume
Bid/ask absence does not globally block structural signal generation.

Volume is treated as feed-volume unless its semantics are verified.

VWAP must carry its source label, e.g. FEED_VOLUME.

If a family intrinsically requires spread/execution data, absence may block that family or live execution only.

## 10. Provider Failure
Provider failure never creates synthetic prices.

## 11. Source Substitution
Never silently switch providers.

Any source change requires explicit configuration and documentation.


## 12. Provider Timestamp Verification
Timestamp semantics have an explicit state:
- UNVERIFIED: provider meaning has not been independently established.
- VERIFIED_OPEN_TIME: timestamp identifies the opening instant of the M1 interval.
- VERIFIED_OTHER: another documented semantic has been verified.

Initial implementation must start UNVERIFIED. Verification must compare provider timestamps against observed candle transitions and elapsed intervals across multiple sessions, document the evidence, and store the verified semantic in configuration/test fixtures.

While UNVERIFIED, raw capture and data-quality diagnostics are allowed, but production signal decisions requiring temporal interpretation are not.

## 13. Absolute Timeframe Alignment
All internal timestamps are UTC. M5/M15/M30 bars use absolute epoch-minute bucket boundaries:
- M5: floor(epoch_minutes / 5) × 5
- M15: floor(epoch_minutes / 15) × 15
- M30: floor(epoch_minutes / 30) × 30

Only the complete set of component M1 intervals belonging to a bucket may close that higher-timeframe bar. No rolling aggregation is permitted.

## 14. Observation-Level Capture
Raw capture is append-only. Each observation records:
- observation_timestamp;
- provider_timestamp;
- candle_state = FORMING or CLOSED;
- observed OHLCV;
- symbol/source;
- feed status;
- freshness;
- connection state.

A later observation of the same forming candle is a new observation, not an overwrite of historical knowledge. Replay uses only observations whose observation_timestamp is <= decision time.

## 15. Zero-Volume VWAP
If cumulative feed volume for the session is zero, VWAP state is UNAVAILABLE. The engine must not substitute a price, zero, or prior VWAP as though it were a calculated value.
