# PSYGRID WindowAU — Permanent Project Constitution

Version 1.2 — Final Architecture Lock
Instrument: XAUUSD

## 1. Mission
Create a precise, empirical XAUUSD intraday intelligence and signal engine that discovers valid opportunities without manufacturing trades or suppressing genuine opportunities through accidental conjunctive filtering.

## 2. Canonical Architecture
DATA → QUALITY → MTF BUILDER → FEATURES → INDEPENDENT SETUP FAMILIES → MINIMUM SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM → OUTCOME → CALIBRATION

Broker order execution is a later external layer. WindowAU's signal validity never depends on Telegram delivery or broker execution.

## 3. Signal-Liveness Contract
The mandatory decision path is:

SETUP FAMILY → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM

Ranking is prioritization, not a universal signal cutoff.

Historical probability, perfect higher-timeframe agreement, preferred session, preferred volatility state, full indicator agreement and research score are not universal prerequisites.

## 4. Independent Setup Families
The initial six families are:
A. Liquidity sweep reversal
B. Expansion-pullback continuation
C. Breakout acceptance
D. Breakout failure
E. Range rejection
F. Structural pullback continuation

Every family must have a versioned contract containing:
- family definition;
- required inputs;
- minimum evidence;
- optional evidence;
- timeframe dependencies;
- M1 trigger;
- invalidation;
- entry hierarchy;
- stop hierarchy;
- target hierarchy;
- maximum lifetime;
- duplicate identity;
- re-arm rule.

A timeframe or feature is mandatory only when that family contract explicitly declares it intrinsic.

## 5. Minimum Actionable Path
A candidate may become ACTIONABLE when:
1. family-specific minimum setup exists;
2. valid M1 trigger exists;
3. required data is valid and fresh;
4. executable entry exists;
5. safe stop/invalidation exists;
6. at least one valid target exists;
7. maximum holding horizon is defined;
8. candidate is not a genuine duplicate;
9. explicit risk/safety rules permit action.

Probability and ranking evidence are outside this mandatory chain.

## 6. Hard-Gate Doctrine
Hard gates are reserved for objective safety/data conditions:
- invalid/stale required data;
- impossible prices/OHLC;
- timestamp corruption;
- intrinsically required family input unavailable;
- duplicate opportunity;
- invalid trade geometry;
- explicit risk-limit violation;
- explicit configured safety blackout;
- execution-safety failure.

Prohibited blanket gates:
- all indicators agree;
- arbitrary model-agreement percentage;
- universal score cutoff;
- universal ATR cutoff;
- universal probability cutoff;
- insufficient sample = no signal;
- preferred session = no signal;
- high volatility = no signal;
- low volatility = no signal;
- neutral/conflicting M30/M15 = no signal;
- preferred stop/target method unavailable = no signal when fallback exists.

## 7. Feature Availability Contract
Every feature exposes a state:
AVAILABLE, UNAVAILABLE, INVALID.

UNAVAILABLE optional evidence is not a directional zero and does not automatically suppress a candidate.

Only a feature declared intrinsically required by the family can block that family.

Global data invalidity can block the entire cycle.

## 8. MTF Doctrine
M30/M15 are contextual layers, M5 is commonly a formation layer, and M1 is the timing layer.

These are architectural defaults, not universal mandatory gates.

Each family contract declares its actual timeframe dependencies.

Higher-timeframe conflict normally changes evidence/ranking rather than vetoing the setup.

## 9. Probability Doctrine
A probability must identify event, sample, horizon, conditioning variables, outcome, uncertainty and calibration.

If sample is insufficient:
- preserve the candidate;
- label INSUFFICIENT_SAMPLE;
- do not fabricate a probability;
- do not suppress solely for insufficient history.

Probability is research evidence unless a later setup-specific validated rule explicitly makes it safety-critical.

## 10. Trade-Plan Fallback Doctrine
Each family must define deterministic fallback hierarchies for entry, stop, target and horizon.

Preferred → secondary → volatility-adjusted structural → documented safe fallback.

If all safe methods fail, suppress with INVALID_TRADE_PLAN and record the exact failure.

R:R is measured from independently justified entry/stop/target. R:R must never be used to manufacture an arbitrary target.

## 11. Session, Volatility and Event Data
Session and volatility influence priority, evidence and research stratification but do not universally disable signals.

If event data is unavailable or unverified:
EVENT_STATUS = UNKNOWN.

UNKNOWN is not equivalent to NO_EVENT and is not equivalent to BLACKOUT.

Only a verified, explicit, time-bounded, instrument-relevant event rule may create EXPLICIT_EVENT_BLACKOUT.

## 12. Opportunity States
OBSERVE → CANDIDATE → DEVELOPING → TRIGGERED → ACTIVE → CLOSED

Or DEVELOPING → EXPIRED.

All transitions are causal and recorded.

## 13. Re-Arm and Expiry
Each family defines a maximum lifetime.

A candidate can re-arm only after explicit invalidation/expiry or a new structurally distinct setup anchor.

Duplicate identity must not block a genuinely new setup.

## 14. Suppression Ledger
Every non-actionable candidate receives one explicit reason:
DATA_INVALID
DUPLICATE
NO_MINIMUM_SETUP
NO_TRIGGER
INVALID_TRADE_PLAN
RISK_LIMIT
EXPLICIT_EVENT_BLACKOUT
EXPIRED
OTHER_DOCUMENTED_REASON

NO_HIGH_EDGE is prohibited as a final suppression reason.

## 15. Actionability vs Ranking vs Execution Capacity
These are separate layers:
- ACTIONABILITY: is the opportunity valid and safely plan-able?
- RANKING: how should valid opportunities be prioritized?
- EXECUTION CAPACITY: can an account safely take/manage another position?

Execution capacity cannot retroactively make a structurally invalid signal. Ranking cannot decide actionability.

## 16. Daily Quota
No trade quota exists. The engine never trades to satisfy a target count and never suppresses a valid opportunity because a count is high.

## 17. Warm-Up
Insufficient history for an optional feature produces UNAVAILABLE.

Warm-up may block only a family whose declared minimum inputs are intrinsically unavailable.

EMA200, ATR percentiles and other long-history features must not globally starve the engine.

## 18. Liveness Requirements
Mandatory tests:
1. valid setup + neutral M30/M15;
2. valid setup + insufficient history;
3. valid setup outside preferred session;
4. one conflicting indicator;
5. low research rank;
6. stop fallback;
7. target fallback;
8. explicit suppression reason;
9. independent family evaluation;
10. one family failure does not stop another;
11. high volatility;
12. low volatility;
13. session classification;
14. duplicate vs genuine re-arm;
15. event status UNKNOWN;
16. optional feature unavailable;
17. Telegram failure;
18. execution-capacity limit separated from signal validity.

## 19. Change Control
Any new hard gate or new mandatory input must document exact condition, reason, affected families, false-negative risk and tests demonstrating no unintended starvation.

## 20. Final Rule
Optimize for falsifiability, causal correctness, measurable opportunity discovery, realistic execution research and truthful signal paths — never for impressive-looking intelligence.


## 21. Final Phase-0 Locks
The six versioned family contracts are frozen in docs/SETUP_FAMILY_CONTRACTS.md.

Actionability is a market-structure/safety property, not an account-capacity property:
- ACTIONABLE means the detected opportunity has a valid minimum path and a safe deterministic plan.
- EXECUTION_CAPACITY records whether a particular account can actually add/manage exposure.
- Account margin, existing exposure, daily risk budget, broker availability and similar capacity constraints must not rewrite a valid market signal as NO_SETUP.
- Strategy-level safety rules may block actionability when explicitly defined and independently testable.

Provider timestamp semantics have a mandatory verification state:
UNVERIFIED → verification procedure → VERIFIED_OPEN_TIME (or another explicitly documented verified semantic).
No live signal calculation may silently assume timestamp meaning while it is UNVERIFIED.

Raw capture is append-only at observation level. Each observation records:
observation_timestamp, provider_timestamp, candle_state, candle values as observed, source, symbol, feed status and freshness.
Replay may expose only values observed by the historical decision timestamp. A later snapshot must never overwrite earlier information in replay.

Deterministic mathematical conventions are locked:
- M1/M5/M15/M30 boundaries are aligned to absolute UTC minute buckets.
- EMA initialization uses the simple mean of the first n completed closes; recursive EMA begins on the next observation.
- ATR initialization uses the simple mean of the first n completed true ranges; recursive Wilder-style updates begin thereafter.
- VWAP with zero cumulative feed volume is UNAVAILABLE, never fabricated.


## Canonical source record
The authoritative Phase-0 source definition is locked in `docs/CANONICAL_DATA_SOURCE.md`. The implementation must use the documented RealMarketAPI endpoint, XAUUSD extraction path and schema from that record; source changes require the documented change-control process.
