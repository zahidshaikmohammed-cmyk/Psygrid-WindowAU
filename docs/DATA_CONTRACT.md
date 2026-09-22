# PSYGRID WindowAU — Data Contract

## 1. Primary source

Initial production source:

RealMarketAPI M1 XAUUSD feed.

Expected candle fields:

- timestamp
- open
- high
- low
- close
- volume

Bid/ask may be present.

## 2. Candle semantics

The timestamp is treated as the candle opening time unless the provider contract proves otherwise.

This must be verified before live deployment.

## 3. Closed candle

A candle is closed only after its interval ends under the verified provider semantics.

Never use final OHLC before close.

## 4. Aggregation

For a completed k-minute bar:

Open = first M1 open  
High = maximum M1 high  
Low = minimum M1 low  
Close = last M1 close  
Volume = sum of M1 volume

Only completed component candles may form a completed higher timeframe candle.

## 5. Quality checks

- timestamp monotonicity;
- duplicate detection;
- OHLC consistency;
- non-negative volume;
- gap detection;
- freshness;
- symbol identity;
- source identity.

## 6. Gaps

Represent gaps explicitly.

Do not silently fabricate prices.

A setup depending on missing data becomes uncertain rather than being treated as normal.

## 7. Forming state

Every series exposes:

- closed;
- forming;
- as_of.

This is mandatory for replay correctness.

## 8. Provider failure

Provider failure must never create synthetic prices.

## 9. Source substitution

Do not silently switch providers. Any source change requires explicit documentation/configuration.
