# PSYGRID WindowAU — Risk and Trade Plan

## 1. Purpose
Convert a detected setup into a measurable plan without manufacturing setups.

## 2. Required Plan
Every actionable plan contains:
entry, stop, target, stop distance, target distance, R:R, maximum horizon, invalidation and risk status.

Position size is separate and only exists when broker contract specifications are verified.

## 3. Entry Hierarchy
Each family must define:
1. preferred structural entry;
2. secondary structural entry;
3. documented safe fallback entry.

Entry cannot be manufactured merely to satisfy a desired R:R.

## 4. Stop Hierarchy
Default architecture:
1. setup-specific structural invalidation;
2. secondary structural invalidation;
3. volatility-adjusted structural buffer;
4. documented conservative fallback.

A universal fixed-dollar stop is prohibited.

## 5. Target Hierarchy
Default architecture:
1. nearest valid structural target;
2. opposing/next structural level;
3. measured move or range projection;
4. volatility projection;
5. empirical MFE-derived target when sample permits.

Target is independently justified. R:R is measured afterward.

## 6. Invalid Plan
If every safe entry/stop/target method fails:
INVALID_TRADE_PLAN

Record the exact failed methods and data conditions.

## 7. Risk vs Signal
A research/actionable signal and a live execution permission are separate objects.

Risk limits may prevent execution without rewriting the underlying structural signal as NO_SETUP.

For live trading, a hard risk limit remains a safety gate on execution.

## 8. Position Sizing
R_$ = Equity × RiskFraction

PositionSize = R_$ / (StopDistance × ContractValue)

Broker contract value must be verified before live sizing.

## 9. Execution Research
Model:
- spread;
- slippage;
- latency;
- rejection;
- partial fill where relevant.

## 10. Holding Horizon
Initial maximum research horizon: 30 minutes.

Buckets:
1–3, 3–5, 5–10, 10–15, 15–20, 20–30 minutes.

## 11. Emergency Behavior
If required feed data becomes unreliable or a safe plan cannot be calculated, no new live execution occurs.

Existing-position management remains deterministic.

## 12. No R:R Gate
R:R is descriptive unless a setup-specific validated safety rule explicitly requires a minimum geometry. Do not reject a structurally valid signal merely because an arbitrary universal R:R target is not reached.
