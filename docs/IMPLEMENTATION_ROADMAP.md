# PSYGRID WindowAU — Python Implementation Roadmap

## Phase 0 — Final architecture lock
Freeze:
- constitution;
- family contracts;
- mathematical formulas;
- data contract;
- feature availability;
- event-status semantics;
- trade-plan fallback hierarchy;
- actionability/ranking/execution-capacity separation;
- signal/candidate schemas;
- state transitions;
- suppression ledger;
- liveness matrix.

No strategy code starts before Phase 0 is frozen.

## Phase 1 — Data layer
Modules:
- data/client.py
- data/models.py
- data/quality.py
- data/aggregator.py
- data/capture.py

Build and test:
- XAUUSD feed parsing;
- timestamp semantics;
- closed/forming state;
- causal M5/M15/M30;
- gaps/duplicates;
- freshness;
- raw capture;
- feature availability primitives.

## Phase 2 — Mathematical feature engine
Modules:
- features/returns.py
- features/volatility.py
- features/trend.py
- features/vwap.py
- features/structure.py
- features/candle_geometry.py
- features/momentum.py

Every feature returns value + availability state + provenance/as_of.

## Phase-2 implementation status

Phase 2 mathematical feature engine is complete for the currently locked mathematical specification.

Implemented modules:
- features/returns.py
- features/volatility.py
- features/trend.py
- features/vwap.py
- features/structure.py
- features/candle_geometry.py
- features/momentum.py

Implemented and tested:
- simple and log returns;
- true range and deterministic Wilder ATR initialization/update;
- rolling ATR;
- realized volatility from log returns;
- ATR percentile capability;
- EMA 9/20/50/200-compatible calculation with simple-mean initialization;
- EMA slope;
- trend persistence, directional run length and higher-high/higher-low counts;
- session feed-volume VWAP with explicit zero-volume UNAVAILABLE state;
- candle range/body/wick geometry and normalized wick values;
- causal prior structural high/low levels;
- pullback depth;
- displacement ratios using prior robust median baselines;
- compression ratio.

Validation:
- GitHub Actions CI run 35778416893: success;
- latest validated commit: ed3f4187a2cbce92c9f07c09cc4d8725d6cb36b1.

Phase-2 boundary remains intact: no setup-family detection, trigger generation, ranking, Telegram runtime, broker execution or live signal generation was added.

## Phase-2 LOCK

Phase 2 — Mathematical Feature Engine is LOCKED for the current normative specification.

Lock acceptance:
- all seven Phase-2 feature modules are implemented;
- every feature exposes value + availability state + provenance/as_of where applicable;
- deterministic EMA initialization and recursive update are implemented;
- deterministic ATR initialization and Wilder update are implemented;
- zero cumulative feed-volume VWAP is UNAVAILABLE;
- structural reference levels exclude the current candle;
- realized volatility uses the specified log-return formulation;
- ATR percentile capability is present;
- trend persistence, run length and structural HH/HL counts are present;
- causal-prefix regression coverage is present;
- Phase-2 CI validation is green.

Validation record:
- GitHub Actions run: 35778691916 — SUCCESS;
- validated commit: ed3f4187a2cbce92c9f07c09cc4d8725d6cb36b1.

Locked boundary:
- Phase 2 does not create setup candidates, triggers, trade plans, actionability decisions, ranking, Telegram notifications, broker orders, probabilities, or live trading.
- Provider timestamp semantics remain UNVERIFIED; production temporal signal generation remains disabled.
- No new mandatory feature or hard gate is introduced by this lock.

Change control:
Any modification to the locked Phase-2 mathematics or feature contract requires explicit change documentation, affected-test updates, and a new validation record before the Phase-2 lock can be considered changed.

## Phase 3 — Family contracts and setup detectors
Before detector code, create one versioned contract per family.

Modules:
- setups/sweep.py
- setups/pullback.py
- setups/breakout.py
- setups/rejection.py
- setups/continuation.py

Each detector returns a structured candidate and never a raw BUY/SELL string.


## Phase-3 implementation status

Phase 3 — Six Setup Families is COMPLETE AND VALIDATED for the current frozen contracts. The post-audit validation gate is closed.

Implemented:
- structured SetupCandidate model with family, direction, causal anchor, evidence, parameters and stable identity;
- LSR v1.0 detector;
- EPC v1.0 detector;
- BOA v1.0 detector;
- BOF v1.0 detector;
- RRE v1.0 detector;
- SPC v1.0 detector;
- explicit family lifetimes in candidate parameters;
- causal structural references using only supplied completed-candle history;
- insufficient-history behavior returns no candidate rather than fabricated evidence;
- detector parameter validation;
- independent family/direction test coverage;
- Phase-3 validation suite: fresh post-audit GitHub Actions validation passed 54 tests with zero failures;
- final validation PR #2 merged into main at commit aff3337ee88f0e1a1c8ad5193d25e3075a355bda;
- post-audit validation commit: 4efc274c243e1f9305e4f228079af122b9f976b7;
- GitHub Actions run 35781896563: SUCCESS, 54 passed.

Phase-3 boundary:
- detectors return structured candidates, not BUY/SELL strings;
- M1 trigger execution remains Phase 4;
- deterministic trade planning remains Phase 5;
- actionability, ranking, persistence, Telegram, outcomes and calibration remain later phases;
- provider timestamp semantics remain UNVERIFIED, so production temporal signal generation remains disabled.

Validation note:
- Fresh GitHub Actions validation is green: run 35781896563 completed successfully with 54 passed and 0 failed.
- The validation includes the post-audit LSR subsequent-candle correction, corrected fixtures, expanded negative-path coverage, and causal-prefix coverage.

## Phase 4 — M1 trigger engine
Module: trigger/m1.py

Trigger logic is family-specific and causal.

## Phase 5 — Trade-plan engine
Modules:
- risk/entries.py
- risk/stops.py
- risk/targets.py
- risk/horizon.py

Implement deterministic fallback chains and explicit INVALID_TRADE_PLAN reasons.

## Phase 6 — Actionability
Module: decision/actionability.py

Only minimum safety requirements determine ACTIONABLE.

No probability/rank/session/volatility universal gate.

## Phase 7 — Ranking
Module: decision/ranker.py

Rank actionable opportunities only.

No rank threshold may silently suppress a valid actionable opportunity.

## Phase 8 — State, persistence and telemetry
SQLite tables:
captures, candidates, opportunities, signals, alerts, outcomes, feature_snapshots, engine_state, suppression_events.

Persist decision before notification.

## Phase 9 — Liveness and architecture test suite
Test:
- every family independently;
- minimum setup;
- M1 trigger;
- optional feature unavailable;
- required family input unavailable;
- insufficient probability sample;
- neutral/conflicting MTF;
- session/volatility independence;
- event UNKNOWN;
- fallback plan;
- duplicate/re-arm;
- expiry;
- Telegram failure;
- execution-capacity separation;
- causal replay invariants.

## Phase 10 — Telegram
notifications/telegram.py

Structured notification only. Delivery is independent of signal existence.

## Phase 11 — Causal replay
research/replay.py

Never reveal later forming-candle final OHLC at earlier timestamps.

## Phase 12 — Outcome engine
research/outcomes.py

MFE, MAE, target/stop timing, horizon returns, R outcomes and holding time.

## Phase 13 — Probability and calibration
research/calibration.py
research/metrics.py

Only after sufficient outcome data.

## Phase 14 — Forward observation
Real-time feed + Telegram, no broker orders.

Measure market quiet vs detector starvation vs trigger starvation vs trade-plan starvation vs data failure.

## Phase 15 — Paper execution
Model broker execution, costs, latency, spread, slippage, rejection and partial fills.

## Phase 16 — External live execution
Only after validation and explicit deployment approval.

## Definition of Done
- verified data;
- causal calculations;
- all family contracts implemented;
- actionability/ranking/execution layers separated;
- every suppression explainable;
- liveness tests pass;
- replay is causal;
- outcomes recorded;
- probabilities calibrated where sample permits;
- out-of-sample expectancy survives realistic costs;
- deterministic risk;
- continuous runtime health;
- no silent starvation.


## Phase-0 exit gate
Phase 0 is GREEN only when:
- docs/SETUP_FAMILY_CONTRACTS.md exists and all six contracts are versioned;
- ACTIONABILITY vs EXECUTION_CAPACITY is explicit and tested;
- timestamp semantics have a defined implementation contract with UNVERIFIED/VERIFIED states; Phase 1 must implement this state before any production temporal signal calculation;
- observation-level capture schema is locked;
- causal replay invariant is specified;
- timeframe bucket alignment is deterministic;
- EMA/ATR/VWAP initialization behavior is deterministic;
- the final architecture audit passes with no unresolved blockers.

Phase 1 implementation may begin only after this gate is satisfied.


## Canonical source record
The authoritative Phase-0 source definition is locked in `docs/CANONICAL_DATA_SOURCE.md`. The implementation must use the documented RealMarketAPI endpoint, XAUUSD extraction path and schema from that record; source changes require the documented change-control process.

## Phase-1 implementation status

Phase 1 data-layer implementation is complete for the currently locked contract.

Implemented:
- canonical RealMarketAPI XAUUSD parser;
- strict canonical schema/type validation;
- optional bid/ask handling;
- feed-health metadata model;
- explicit UNVERIFIED timestamp state;
- verified-open-time forming/closed classification gate;
- M1 data-quality validation;
- duplicate/gap/order/freshness checks;
- absolute UTC M5/M15/M30 aggregation;
- complete-component-only higher-timeframe bars;
- append-only observation capture;
- Phase-1 automated test suite and GitHub Actions CI.

Validation:
- GitHub Actions CI: 24 passed;
- latest validated implementation commit: 503ca9034653f80bcc22441f6176cbc5b03a4eec

Important boundary:
- provider timestamp semantics remain UNVERIFIED;
- production temporal signal generation remains disabled;
- no setup-family, trigger, ranking, Telegram runtime, broker execution, macro/news or live-trading implementation is part of Phase 1.
