# PSYGRID WindowAU — Signal Engine Specification

Version 1.2 — Final Architecture Lock

## 1. Runtime Cycle
On each newly closed M1 candle:
1. validate required feed;
2. update M1 series;
3. build completed M5/M15/M30 causally;
4. update feature states;
5. classify session/volatility/event status;
6. evaluate all setup families independently;
7. update candidate states;
8. evaluate family-specific M1 trigger;
9. build safe trade plan using fallback hierarchy;
10. classify ACTIONABLE or explicit suppression;
11. rank actionable opportunities;
12. persist decision;
13. attempt Telegram delivery;
14. persist delivery result.

## 2. Signal Object
Every actionable signal must have:
signal_id
symbol
family
direction
setup_anchor
setup_start_time
trigger_time
entry
stop
target_1
optional_target_2
rr
session
volatility_state
event_status
horizon
data_as_of
feature_availability_summary
historical_evidence_status
research_score
actionability_status
risk_status
created_at

Signal existence is independent of Telegram success.

## 3. Candidate Object
Every candidate must have:
candidate_id
family
direction
setup_anchor
setup_start_time
state
required_inputs_status
feature_states
setup_evidence
trigger_evidence
context_evidence
trade_plan_status
suppression_reason
created_at
updated_at
expiry_time
rearm_key

## 4. Decision Pipeline
SETUP FAMILY → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM

No research score, probability, session preference or unrelated indicator may be inserted as a hidden mandatory stage.

## 5. Family Contracts
Each family implementation must declare:
- minimum setup definition;
- required inputs;
- optional inputs;
- timeframe dependencies;
- trigger definition;
- invalidation;
- entry hierarchy;
- stop hierarchy;
- target hierarchy;
- maximum lifetime;
- duplicate key;
- re-arm rule.

## 6. Timeframe Dependencies
M30/M15/M5 are not globally mandatory.

A family declares the minimum timeframe data it intrinsically requires.

Missing optional MTF context is represented as UNAVAILABLE and may alter evidence/ranking only.

## 7. Feature States
AVAILABLE = valid value at decision time.
UNAVAILABLE = not present or insufficient history, but not corrupt.
INVALID = present but fails integrity rules.

Optional UNAVAILABLE does not become zero and does not block a signal.

Required INVALID/UNAVAILABLE blocks only the affected family unless the failure is global feed invalidity.

## 8. Historical Probability
If sample is insufficient, preserve candidate and mark INSUFFICIENT_SAMPLE.

Do not fabricate a percentage.

Probability evidence is separate from actionability.

## 9. Trade Plan
For each family:
preferred entry → secondary entry → safe fallback entry
preferred stop → secondary stop → volatility-adjusted structural stop → safe fallback
preferred target → secondary target → measured/volatility target → empirical target where available

If all safe methods fail: INVALID_TRADE_PLAN.

R:R is calculated after independent plan construction.

## 10. Actionability
ACTIONABLE requires only the minimum safety path:
minimum setup + trigger + required data + executable entry + safe stop + target + horizon + duplicate check + risk/safety permission.

No ranking cutoff exists.

## 11. Ranking
Rank only ACTIONABLE opportunities.

Ranking variables may include evidence, conflicts, historical expectancy, uncertainty, execution quality, maturity, session and volatility.

Ranking must not remove an opportunity from existence.

## 12. Execution Capacity
Execution capacity is separate from signal generation.

A valid signal may exist even when a live account cannot safely add exposure. Such a condition is recorded as execution/risk status, not rewritten as NO_SETUP.

## 13. Session/Volatility
Session and volatility affect evidence, priority and research stratification.

They do not universally suppress signals.

## 14. Event Status
Event status is one of:
VERIFIED_EVENT
VERIFIED_NO_EVENT
UNKNOWN

Only VERIFIED_EVENT plus an explicit configured time window may create EXPLICIT_EVENT_BLACKOUT.

UNKNOWN never means VERIFIED_NO_EVENT.

## 15. Duplicate/Re-Arm
Duplicate identity includes symbol, family, direction, structural anchor and setup-start identity.

A candidate may re-arm after explicit invalidation/expiry when a new qualifying setup event occurs.

Duplicate detection must not collapse distinct events around the same broad price level.

## 16. Expiry
Each family defines maximum candidate lifetime.

Expiry is a recorded state transition, not silent deletion.

## 17. Suppression
Every non-actionable candidate receives:
DATA_INVALID
DUPLICATE
NO_MINIMUM_SETUP
NO_TRIGGER
INVALID_TRADE_PLAN
RISK_LIMIT
EXPLICIT_EVENT_BLACKOUT
EXPIRED
or OTHER_DOCUMENTED_REASON.

NO_HIGH_EDGE is prohibited.

## 18. Warm-Up
The engine may preload history for stable indicators.

If optional history is absent, feature state is UNAVAILABLE.

Global signal starvation during EMA200/ATR-percentile warm-up is prohibited.

## 19. Telemetry
At every completed M1 cycle record:
- candidates by family;
- state counts;
- trigger counts;
- actionable counts;
- suppression counts/reasons;
- last valid candidate;
- last actionable candidate;
- last Telegram attempt/result;
- data quality;
- feature availability;
- event status;
- engine heartbeat.

## 20. Liveness Test Matrix
Mandatory tests:
- neutral M30/M15;
- insufficient probability sample;
- preferred-session false;
- conflicting optional indicator;
- low research score;
- preferred stop unavailable;
- preferred target unavailable;
- optional feature unavailable;
- family-specific required input unavailable;
- one family exception;
- high volatility;
- low volatility;
- session transition;
- event UNKNOWN;
- duplicate vs new setup/re-arm;
- Telegram failure;
- execution-capacity restriction.

## 21. Persistence Order
Persist the signal/candidate decision before Telegram.

Telegram delivery is an output side effect, not part of signal validity.

## 22. Core Principle
Minimum safety path first. Ranking second. Notification third.
