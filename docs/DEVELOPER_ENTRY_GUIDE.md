# PSYGRID WindowAU — Developer Entry Guide

Version 1.0 — Phase-0 Final Build Handoff

## 1. Read This First

PSYGRID WindowAU is a technical-only XAUUSD intraday research and signal engine.

A new engineer entering this repository should understand:
- Instrument: XAUUSD only.
- Current canonical market source: documented RealMarketAPI M1 feed.
- Current engine scope: technical market data only.
- Macro/news: reserved future optional extension, not a current dependency.
- Multiple independent setup families; no giant confirmation AND-gate.
- Causal correctness and data integrity are higher priority than signal frequency.
- Telegram is a notification output, not part of signal validity.
- Broker order execution is outside the current engine and is a later external layer.
- Production temporal signal calculation is prohibited while provider timestamp semantics remain UNVERIFIED.
- No performance, probability, or live-readiness claim may be invented.

## 2. What We Are Building

The system answers: Does current XAUUSD price action contain a technically valid, safely plan-able short-horizon opportunity?

It does not attempt to predict every price movement or manufacture a trade every few minutes.

Canonical pipeline:

DATA → QUALITY → MTF BUILDER → TECHNICAL FEATURES → INDEPENDENT SETUP FAMILIES → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM → OUTCOME → CALIBRATION

Six initial setup families:
- LSR — Liquidity Sweep Reversal
- EPC — Expansion-Pullback Continuation
- BOA — Breakout Acceptance
- BOF — Breakout Failure
- RRE — Range Rejection
- SPC — Structural Pullback Continuation

Each family has its own normative versioned contract in docs/SETUP_FAMILY_CONTRACTS.md.

## 3. Current Scope vs Future Scope

### In scope now
- XAUUSD
- M1 market data
- causal M5/M15/M30 construction
- technical feature calculations
- six technical setup families
- family-specific M1 triggers
- deterministic trade-plan construction
- actionability
- ranking
- SQLite state/persistence
- observation capture
- causal replay
- outcome measurement
- calibration
- Telegram notification
- forward observation and paper-trading research

### Not in the current technical dependency chain
- economic calendar
- news provider
- Fed/news interpretation
- DXY provider
- Treasury-yield provider
- geopolitical feed
- broker order execution

Future macro/news scope is reserved in docs/FUTURE_MACRO_NEWS_EXTENSION.md.
Broker execution is deliberately a later external layer.

## 4. Canonical Data Source

Provider: RealMarketAPI

Endpoint: http://140.245.226.102:8080/public/live.json

WindowAU consumes only:

response["symbols"]["XAUUSD"]["candles_1m"]

The endpoint is multi-symbol, but WindowAU must never scan the other symbols.

Exact schema and source-health fields are defined in docs/CANONICAL_DATA_SOURCE.md.
Data semantics are defined in docs/DATA_CONTRACT.md.
Do not invent an alternate endpoint, alternate schema, synthetic price, or silent provider fallback.

## 5. Critical Timestamp Rule

Provider timestamp semantics currently begin as UNVERIFIED.

The implementation must represent this state explicitly.

While UNVERIFIED:
- raw capture is allowed;
- diagnostics are allowed;
- schema/quality testing is allowed;
- replay testing is allowed;
- production temporal signal decisions are not allowed.

Verification must establish timestamp meaning from observed provider behavior and documented evidence.

## 6. Causal Data Rule

A decision may use only information actually observable at that decision timestamp.

Raw observations preserve both observation timestamp and provider/candle timestamp.
A later snapshot of a forming candle must never rewrite the historical state available to an earlier decision.

Higher-timeframe bars use absolute UTC bucket boundaries for M5, M15 and M30.
Only complete component M1 intervals form a completed higher-timeframe candle.
No rolling higher-timeframe aggregation.

## 7. Anti-Starvation Rule

Never turn the engine into: M30 + M15 + M5 + M1 + EMA + VWAP + ATR + probability + session + volatility + score = signal.

The minimum decision path is:

SETUP FAMILY → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM

Optional evidence can improve evidence or ranking. It cannot silently become a mandatory gate.

Prohibited universal gates include:
- all indicators agree;
- all timeframes agree;
- probability above arbitrary threshold;
- score above arbitrary threshold;
- preferred session required;
- high volatility required;
- low volatility prohibited;
- insufficient historical sample = no signal;
- optional feature unavailable = no signal;
- preferred stop/target unavailable when a safe fallback exists.

## 8. Six Family Contracts

LSR: structural sweep followed by failure/re-entry.
EPC: directional expansion followed by controlled pullback and continuation.
BOA: breakout followed by demonstrated acceptance.
BOF: breakout followed by failure and re-entry.
RRE: test of a validated range extreme followed by rejection.
SPC: established directional structure followed by controlled pullback and continuation.

Each contract defines required inputs, minimum evidence, optional evidence, timeframe dependency, trigger, invalidation, entry hierarchy, stop hierarchy, target hierarchy, lifetime, duplicate identity and re-arm rule.

Do not add mandatory inputs without versioning the contract and adding required tests.

## 9. Feature Availability

Every derived feature has one of AVAILABLE, UNAVAILABLE, INVALID.
Optional UNAVAILABLE is not a directional zero and does not globally block the engine.
Only an intrinsically required family input can block that family.

## 10. Trade-Plan Rule

Never manufacture an entry, stop or target merely to obtain a desired R:R.
Each family uses deterministic fallback hierarchies: preferred → secondary → safe fallback.
If all safe methods fail, record INVALID_TRADE_PLAN with the exact reason.
R:R is measured after independent plan construction.

## 11. Actionability, Ranking and Execution Capacity

ACTIONABILITY asks whether the detected market opportunity is valid and safely plan-able.
RANKING asks how valid opportunities should be prioritized.
EXECUTION CAPACITY asks whether a particular account can safely take/manage another position.

Account capacity must not rewrite a genuine market signal as NO_SETUP.
Ranking must not decide whether the signal exists.

## 12. Suppression

Every non-actionable candidate must have an explicit documented reason.

Allowed categories:
- DATA_INVALID
- DUPLICATE
- NO_MINIMUM_SETUP
- NO_TRIGGER
- INVALID_TRADE_PLAN
- RISK_LIMIT
- EXPLICIT_EVENT_BLACKOUT
- EXPIRED
- OTHER_DOCUMENTED_REASON

NO_HIGH_EDGE is prohibited as a final suppression reason.

If zero signals occur, telemetry must distinguish market quiet, detector miss, trigger miss, trade-plan failure, risk block, data block, duplicate block or another documented reason.

## 13. State Model

Canonical lifecycle:
OBSERVE → CANDIDATE → DEVELOPING → TRIGGERED → ACTIVE → CLOSED

or DEVELOPING → EXPIRED.

All transitions are causal and recorded.
Re-arm occurs only after explicit invalidation/expiry or a new structurally distinct setup event.

## 14. Session and Volatility

Session and volatility are descriptive/contextual variables.
They can influence evidence, ranking, research stratification and evaluation frequency.
They do not universally suppress technical setups.

Internal time is UTC. Display time is Asia/Kolkata. Session classification must be DST-safe for London/New York.

## 15. Probability

Probability is research evidence, not an automatic signal prerequisite.
A valid probability must carry event definition, sample size, conditioning, horizon, outcome, uncertainty and calibration status.
Insufficient sample means INSUFFICIENT_SAMPLE, not NO_SIGNAL.
No probability may be invented.

## 16. Telegram

Telegram is downstream notification.
The correct order is: persist decision → attempt Telegram → persist delivery result.
Telegram failure must not erase or invalidate a genuine signal.

Repository secrets expected by the notification layer:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Secret values must never be committed to Git. Automated tests should not require sending a real Telegram message.

## 17. Research and Validation

Before real-money use:
1. verify the data source;
2. verify timestamp semantics;
3. validate causal aggregation;
4. implement and test features;
5. implement all family contracts;
6. implement triggers;
7. implement trade planning;
8. capture observations;
9. perform causal replay;
10. measure outcomes;
11. calibrate probabilities where sample permits;
12. run forward observation;
13. paper-test execution costs;
14. validate out-of-sample behavior;
15. obtain explicit deployment approval.

Never invent performance results.

## 18. Implementation Order

Phase 1 — Data: data/client.py, data/models.py, data/quality.py, data/aggregator.py, data/capture.py
Phase 2 — Technical features: returns, volatility, trend, VWAP, structure, candle geometry, momentum
Phase 3 — Six setup families
Phase 4 — M1 triggers
Phase 5 — Trade plans
Phase 6 — Actionability
Phase 7 — Ranking
Phase 8 — SQLite state/persistence/telemetry
Phase 9 — Liveness and architecture tests
Phase 10 — Telegram
Phase 11 — Causal replay
Phase 12 — Outcomes
Phase 13 — Calibration
Phase 14 — Forward observation
Phase 15 — Paper execution
Phase 16 — External live execution

Do not skip directly to strategy or broker execution.

## 19. Phase-1 Acceptance Requirements

Tests must prove at minimum:
- exact canonical JSON parsing;
- exact XAUUSD extraction;
- other symbols ignored;
- malformed schema fails explicitly;
- OHLC integrity;
- non-negative volume;
- duplicate detection;
- timestamp ordering;
- gap detection;
- freshness;
- forming/closed state;
- explicit UNVERIFIED timestamp state;
- absolute UTC M5/M15/M30 boundaries;
- only complete M1 components create completed higher-timeframe bars;
- observation-level capture;
- causal replay protection against forming-candle look-ahead;
- optional bid/ask handling;
- zero-volume VWAP availability semantics;
- no synthetic fallback.

## 20. Document Authority

When documents overlap, use this authority order:
1. PROJECT_CONSTITUTION.md — permanent architecture and hard rules
2. SETUP_FAMILY_CONTRACTS.md — normative family behavior
3. DATA_CONTRACT.md — data semantics and integrity
4. CANONICAL_DATA_SOURCE.md — source/provider/schema
5. MATHEMATICAL_SPECIFICATION.md — formulas
6. SIGNAL_ENGINE_SPEC.md — runtime decision flow and schemas
7. RISK_AND_TRADE_PLAN.md — planning/risk rules
8. SESSION_AND_VOLATILITY.md — contextual conditioning
9. RESEARCH_AND_VALIDATION.md — research/replay/validation
10. ANTI_STARVATION_AUDIT.md — liveness control
11. IMPLEMENTATION_ROADMAP.md — build sequence
12. FUTURE_MACRO_NEWS_EXTENSION.md — future macro/news scope
13. README.md and PROJECT_DESCRIPTION.md — entry-level summaries

If implementation behavior conflicts with a normative document, stop and resolve the contradiction. Do not silently invent a new rule in code.

## 21. Definition of a Correct Implementation

A correct implementation:
- uses the canonical data source;
- preserves causal truth;
- evaluates independent setup families independently;
- does not silently starve valid opportunities;
- constructs safe deterministic plans;
- records why candidates were suppressed;
- persists state before notification;
- supports reproducible replay;
- measures outcomes honestly;
- keeps technical signal validity separate from account execution capacity;
- does not invent data, probabilities or performance;
- remains extensible without hidden dependencies.

## 22. Current Repository State

- architecture documentation: LOCKED;
- canonical source record: LOCKED;
- six family contracts: LOCKED;
- mathematical conventions: LOCKED;
- anti-starvation rules: LOCKED;
- future macro/news extension point: RESERVED;
- Telegram repository secrets: CONFIGURED;
- Phase 1 data-layer implementation: COMPLETE;
- Phase 2 mathematical feature engine: COMPLETE AND LOCKED;
- Phase 3 six setup-family detectors: COMPLETE AND AUDITED;
- production signal generation: NOT ENABLED;
- broker execution: NOT IMPLEMENTED.

Phase 2 is locked under the roadmap change-control record. Phase 3 has been implemented and audited. The next engineering task is Phase 4 family-specific M1 trigger implementation.