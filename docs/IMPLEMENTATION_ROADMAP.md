# PSYGRID WindowAU — Python Implementation Roadmap

## Phase 0 — Constitution and liveness contract

Lock the project constitution, mathematical specification, data contract, session/volatility framework, signal state machine, anti-starvation rules, risk rules, validation protocol, suppression ledger and trade-plan fallback doctrine.

The anti-starvation rules are canonical project rules, not advisory notes.

## Phase 1 — Data layer

Modules:
- data/client.py
- data/models.py
- data/quality.py
- data/aggregator.py
- data/capture.py

Requirements:
- genuine M1 OHLCV;
- verified timestamp semantics;
- closed/forming state;
- causal M5/M15/M30 aggregation;
- no look-ahead;
- graceful optional-field handling;
- raw capture for deterministic replay.

Tests include schema, timestamps, duplicates, gaps, aggregation and forming-candle behavior.

## Phase 2 — Feature engine

Modules:
- features/returns.py
- features/volatility.py
- features/trend.py
- features/vwap.py
- features/structure.py
- features/candle_geometry.py
- features/momentum.py

Every feature is causal and unit-tested.

Optional or missing features must be represented as unavailable, not silently converted into a directional value.

## Phase 3 — Setup detectors

Modules:
- setups/sweep.py
- setups/pullback.py
- setups/breakout.py
- setups/rejection.py
- setups/continuation.py

Each detector returns a structured candidate.

Every family has an independent evaluation path.

## Phase 4 — M1 trigger

Module: trigger/m1.py

Identify the actionable transition, timestamp it, prevent repeated alerts and preserve causality.

## Phase 5 — Safe trade-plan engine

Modules:
- risk/stops.py
- risk/targets.py
- risk/horizon.py

Each setup family gets a deterministic fallback hierarchy:
preferred structural method → secondary structural method → volatility-adjusted structural method → documented safe fallback.

If no safe plan exists, suppress explicitly with INVALID_TRADE_PLAN.

## Phase 6 — Actionability classifier

Module: decision/actionability.py

Required path:
minimum setup → valid M1 trigger → valid data → executable entry → safe stop → at least one target → defined horizon → duplicate check → explicit risk/safety check → ACTIONABLE

It must not require historical probability, perfect M30/M15 agreement, preferred session, preferred volatility state, universal score threshold or all indicators.

## Phase 7 — Opportunity ranking

Module: decision/ranker.py

The ranker orders actionable opportunities. It does not decide whether an otherwise valid opportunity is allowed to exist.

## Phase 8 — Persistence and suppression telemetry

SQLite initially.

Tables:
captures, opportunities, signals, alerts, outcomes, feature snapshots, engine state and suppression events.

Required telemetry includes candidates by family, actionable count, alert count, suppression reason, last valid candidate, last actionable and data-quality state.

## Phase 9 — Liveness test suite

Before strategy optimization, implement tests proving:
1. valid setup + neutral M30/M15 can become actionable;
2. insufficient historical sample does not block;
3. outside preferred session can become actionable;
4. one conflicting indicator does not block;
5. low research rank does not block actionability;
6. stop fallback works;
7. target fallback works;
8. every suppression has an explicit reason;
9. all setup families are evaluated independently;
10. one family failure does not suppress another;
11. high volatility is not a universal blocker;
12. low volatility is not a universal blocker;
13. session is not a universal blocker;
14. duplicate control blocks only genuine duplicates;
15. Telegram failure does not erase an actionable signal.

A runtime starvation dashboard is required.

## Phase 10 — Telegram

notifications/telegram.py

Telegram receives structured actionable signals only.

Signal persistence occurs before delivery. Delivery success/failure is tracked separately.

## Phase 11 — Replay

research/replay.py

Replay must be causal and deterministic. A forming M1 candle's final OHLC must never appear at an earlier replay timestamp.

## Phase 12 — Outcome engine

research/outcomes.py

Calculate MFE, MAE, target/stop timing, horizon returns, R outcomes and holding time.

## Phase 13 — Calibration

research/calibration.py
research/metrics.py

Measure predicted vs realized, Brier score, sample size, uncertainty, stratification, multiple-testing effects and cost sensitivity.

## Phase 14 — Forward observation

Real-time data, real Telegram, no broker orders.

Use telemetry to distinguish genuine market quiet, feed problems, over-filtering, family starvation, trigger starvation and trade-plan starvation.

## Phase 15 — Paper trading

Simulate realistic broker execution, spread, slippage, latency and rejection.

## Phase 16 — Live

Only after validation and explicit deployment approval.

## Definition of done

The engine is done only when data is trustworthy, calculations are reproducible, signals are explainable, every suppression is explainable, liveness tests pass, outcomes are recorded, probabilities are calibrated where sample permits, expectancy survives out-of-sample testing, risk is deterministic, no look-ahead bias exists and the engine can run continuously without silently dying or silently starving valid opportunity paths.
