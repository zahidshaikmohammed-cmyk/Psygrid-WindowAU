# PSYGRID WindowAU — XAUUSD Intraday Trading Engine

PSYGRID WindowAU is a dedicated Python research and signal engine for XAUUSD (Gold).

## Mission

Build a precise, empirical, session-aware intraday engine that can detect multiple types of opportunity without relying on a single rigid pattern or a giant collection of hard gates.

The core rule is:

> **Do not force Gold into a rigid prediction model. Quantify its current behavior and act when a statistically supported opportunity develops.**

## Anti-starvation constitution

The engine must NOT become a giant AND-gate such as:

M30 agrees + M15 agrees + M5 agrees + M1 agrees + every indicator agrees + score > 90 = trade.

That architecture can produce zero useful signals.

Instead:

- Context contributes evidence.
- Each setup family has an independent detection path.
- Evidence is scored continuously.
- Conflicting evidence reduces confidence; it does not automatically kill a setup.
- Thresholds are calibrated from outcomes.
- Multiple valid opportunities are allowed in one session.
- No artificial daily trade quota exists.

### Hard gates allowed

Hard gates are reserved for objective safety/data conditions:

- invalid or stale feed;
- impossible OHLC;
- timestamp corruption;
- missing price required for a decision;
- unrecoverable data gap;
- invalid stop/target geometry;
- duplicate opportunity;
- explicit risk-limit violation;
- explicit configured trading blackout.

### Strategy hard gates prohibited

Do not add permanent blanket rules such as:

- all indicators must agree;
- model agreement must exceed an arbitrary percentage;
- one universal ATR threshold;
- one universal probability threshold;
- one universal score threshold;
- non-preferred session means no trade;
- high volatility means no trade;
- low volatility means no trade.

## Architecture

M30 / M15 context
→ M5 setup formation
→ M1 trigger
→ trade plan
→ Telegram alert
→ outcome tracking

## Initial setup families

1. Liquidity sweep / failed-break reversal
2. Expansion → pullback → continuation
3. Breakout → acceptance → continuation
4. Breakout → failure → reversal
5. Range extreme rejection / mean reversion
6. Structural pullback continuation

These families compete independently.

## Time windows

The engine remains capable of evaluating setups throughout the day.

Session windows are opportunity multipliers, not automatic trade signals.

The initial configuration will classify Asian, London, London/New York overlap, New York, late New York and transition periods. Exact windows are timezone-aware and DST-safe.

High-activity windows receive more intensive opportunity hunting. The clock never forces a trade.

## Data

Initial source: RealMarketAPI M1 XAUUSD feed.

The engine will:

1. validate timestamps;
2. deduplicate;
3. detect gaps;
4. identify forming vs closed candles;
5. construct M5/M15/M30 causally from M1;
6. never expose a future candle value to an earlier decision;
7. persist raw captures for replay.

## Mathematical feature layer

The initial feature set includes:

- True Range and ATR;
- ATR percentile;
- realized volatility;
- rolling return volatility;
- EMA 9/20/50/200;
- EMA slope;
- VWAP and price-to-VWAP distance;
- candle body/range and wick ratios;
- rolling highs/lows;
- session highs/lows;
- previous day levels;
- local swing structure;
- displacement;
- pullback depth;
- breakout distance;
- acceptance/rejection;
- compression/expansion;
- trend persistence;
- momentum/velocity;
- M1/M5/M15/M30 relationships.

Full formulas are locked in docs/MATHEMATICAL_SPECIFICATION.md.

## Probability philosophy

The engine will not invent a probability because a model outputs one.

For each setup, direction, session, volatility state and horizon, we eventually estimate:

P(target before stop | setup, direction, context, horizon)

Every probability must carry sample size and uncertainty and must be tested for calibration.

## Trade plan

Every actionable signal contains:

- direction;
- entry;
- stop;
- target(s);
- R:R;
- risk;
- session;
- volatility state;
- setup family;
- trigger reason;
- expected holding horizon;
- data timestamp.

Initial research horizon is 30 minutes maximum, with 1–3, 3–5, 5–10, 10–15, 15–20 and 20–30 minute outcome buckets.

## Research before real money

The project progresses:

1. Feed verification
2. Causal candle construction
3. Feature calculations
4. Setup detection
5. Trigger detection
6. Trade-plan calculation
7. Capture
8. Replay
9. Outcome measurement
10. Calibration
11. Forward observation
12. Paper trading
13. Live only after validation

The engine is not considered successful because it sends attractive Telegram messages.

## Documents

- docs/PROJECT_CONSTITUTION.md
- docs/MATHEMATICAL_SPECIFICATION.md
- docs/SIGNAL_ENGINE_SPEC.md
- docs/SESSION_AND_VOLATILITY.md
- docs/RISK_AND_TRADE_PLAN.md
- docs/RESEARCH_AND_VALIDATION.md
- docs/DATA_CONTRACT.md
- docs/IMPLEMENTATION_ROADMAP.md

## Primary principle

> **We are not building a machine that must produce trades. We are building a machine that discovers whether XAUUSD contains repeatable, measurable intraday opportunities — without suppressing genuine opportunities through excessive filtering.**


## Canonical liveness contract

The permanent decision path is:

SETUP FAMILY → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM

Ranking is prioritization, not a universal signal cutoff.

Historical probability, perfect M30/M15 agreement, preferred session, preferred volatility state, or full indicator agreement must not become hidden prerequisites.

Each setup family is evaluated independently. Optional evidence may be unavailable or conflicting without automatically suppressing a structurally valid setup.

Every non-actionable candidate receives an explicit suppression reason. The engine never silently converts low confidence, low research rank, insufficient sample, or unavailable preferred methods into a generic no-signal decision.

See docs/PROJECT_CONSTITUTION.md, docs/SIGNAL_ENGINE_SPEC.md and docs/ANTI_STARVATION_AUDIT.md for the canonical rules.


## Phase-0 architecture lock
The six setup family contracts are frozen in docs/SETUP_FAMILY_CONTRACTS.md. Actionability is separate from account execution capacity. Provider timestamp semantics begin UNVERIFIED and require explicit verification before production temporal decisions. Raw capture is observation-level and replay is causal. M5/M15/M30 use absolute UTC bucket alignment, with deterministic EMA/ATR initialization and zero-volume VWAP handling.

Phase 1 begins only after the Phase-0 exit gate in docs/IMPLEMENTATION_ROADMAP.md passes.


## Canonical source record
The authoritative Phase-0 source definition is locked in `docs/CANONICAL_DATA_SOURCE.md`. The implementation must use the documented RealMarketAPI endpoint, XAUUSD extraction path and schema from that record; source changes require the documented change-control process.
