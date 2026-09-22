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

## Phase 3 — Family contracts and setup detectors
Before detector code, create one versioned contract per family.

Modules:
- setups/sweep.py
- setups/pullback.py
- setups/breakout.py
- setups/rejection.py
- setups/continuation.py

Each detector returns a structured candidate and never a raw BUY/SELL string.

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
