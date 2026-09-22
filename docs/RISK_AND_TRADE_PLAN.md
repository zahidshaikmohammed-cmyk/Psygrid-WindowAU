# PSYGRID WindowAU — Risk and Trade Plan

## 1. Purpose

Convert a detected setup into a measurable plan without manufacturing setups.

## 2. Required fields

- entry;
- stop;
- target;
- stop distance;
- target distance;
- R:R;
- risk fraction;
- position size only when broker contract data is verified;
- maximum holding horizon;
- invalidation.

## 3. Stop logic

Candidate anchors:

- beyond swept high/low;
- beyond pullback invalidation;
- beyond breakout failure level;
- volatility-adjusted structural buffer.

A universal fixed-dollar stop is prohibited.

## 4. Target logic

Targets may use:

- structural level;
- range midpoint;
- opposite range extreme;
- measured move;
- volatility projection;
- empirical MFE distribution.

Do not choose a target solely to make R:R attractive.

## 5. Risk

Support:

- fixed fractional risk;
- fixed monetary risk;
- maximum daily loss;
- maximum concurrent exposure.

Live risk limits are hard safety controls.

## 6. Position size

R_$ = Equity × RiskFraction

PositionSize = R_$ / (StopDistance × ContractValue)

Contract value must be verified for the actual broker/account.

## 7. Execution

Research must model:

- spread;
- slippage;
- latency;
- rejection/partial fill where relevant.

## 8. Holding horizon

Initial maximum: 30 minutes.

Measure shorter buckets to discover where the edge actually occurs.

## 9. Emergency behavior

If the feed becomes unreliable or a safe trade plan cannot be calculated, no new position is opened.

Existing-position management must remain deterministic.
