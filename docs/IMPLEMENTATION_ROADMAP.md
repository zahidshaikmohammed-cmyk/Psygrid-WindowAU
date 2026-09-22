# PSYGRID WindowAU — Python Implementation Roadmap

## Phase 0 — Constitution

Documentation first.

Deliver the complete project rules, formulas, data contract, session framework, signal state machine, risk rules and validation protocol.

## Phase 1 — Data layer

Modules:

- data/client.py
- data/models.py
- data/quality.py
- data/aggregator.py
- data/capture.py

Tests:

- schema;
- timestamp semantics;
- duplicates;
- gaps;
- M5/M15/M30 aggregation;
- forming candle behavior.

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

## Phase 3 — Setup detectors

Modules:

- setups/sweep.py
- setups/pullback.py
- setups/breakout.py
- setups/rejection.py
- setups/continuation.py

Each detector returns a structured candidate, not a BUY/SELL string.

## Phase 4 — M1 trigger

Module:

trigger/m1.py

Purpose:

- identify the actionable transition;
- timestamp it;
- prevent repeated alerts;
- preserve causality.

## Phase 5 — Opportunity ranking

Module:

decision/ranker.py

Inputs:

- context;
- setup evidence;
- trigger evidence;
- volatility;
- session;
- empirical expectancy;
- execution quality.

Output:

- candidate ranking;
- action state;
- explanation.

No universal hard strategy gate.

## Phase 6 — Risk engine

Modules:

- risk/stops.py
- risk/targets.py
- risk/sizing.py
- risk/limits.py

## Phase 7 — Persistence

SQLite initially.

Tables:

- captures;
- opportunities;
- signals;
- alerts;
- outcomes;
- feature snapshots;
- engine state.

## Phase 8 — Telegram

notifications/telegram.py

Telegram receives structured signals only.

## Phase 9 — Replay

research/replay.py

Replay must be causal and deterministic.

## Phase 10 — Outcome engine

research/outcomes.py

Calculate MFE, MAE, target/stop timing, horizon returns and R outcomes.

## Phase 11 — Calibration

research/calibration.py  
research/metrics.py

## Phase 12 — Forward observation

Real-time data, real Telegram, no broker orders.

## Phase 13 — Paper trading

Simulate realistic broker execution and costs.

## Phase 14 — Live

Only after validation.

## Definition of done

The engine is done only when:

- data is trustworthy;
- calculations are reproducible;
- signals are explainable;
- outcomes are recorded;
- probabilities are calibrated;
- expectancy survives out-of-sample testing;
- risk is deterministic;
- no look-ahead bias exists;
- the engine can run continuously without silently dying.
