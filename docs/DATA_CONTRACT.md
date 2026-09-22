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
