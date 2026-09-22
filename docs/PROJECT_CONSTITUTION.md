# PSYGRID WindowAU — Permanent Project Constitution

Version 1.1 — Signal-Liveness Amendment
Instrument: XAUUSD

## 1. Mission

Create a precise, empirical XAUUSD intraday engine that acts when a valid setup and trigger exist, while never manufacturing trades and never suppressing genuine opportunities through excessive conjunctive filtering.

## 2. Signal-Liveness Contract

Canonical flow:

SETUP FAMILY → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM

Ranking is prioritization. It is not a hidden elimination gate.

Historical probability, higher-timeframe agreement, preferred session, volatility state, indicator agreement and research scores are normally evidence, not mandatory prerequisites.

## 3. Anti-Starvation Rule

No universal AND-gate may require every model, timeframe and indicator to agree.

Each setup family gets an independent detection path and is evaluated independently on every eligible closed M1 update.

One family's failure must not suppress another family.

Context is evidence, not a veto by default.

## 4. Minimum Actionable Path

A candidate may become ACTIONABLE when:
1. minimum setup evidence for that family exists;
2. a valid M1 trigger exists;
3. the feed is valid and sufficiently fresh;
4. entry is executable;
5. a safe stop/invalidation level exists;
6. at least one valid target exists;
7. the research maximum holding horizon is defined;
8. the opportunity is not a duplicate;
9. explicit risk/safety rules permit the action.

This is the minimum safety path. It is not a requirement for every indicator or model to agree.

## 5. Hard-Gate Doctrine

Hard gates may block only objective conditions such as:
- invalid or stale data;
- impossible prices or OHLC;
- timestamp corruption;
- data required intrinsically by that setup family is unavailable;
- duplicate opportunity;
- invalid trade geometry;
- explicit risk-limit violation;
- explicit configured safety blackout;
- execution-safety failure.

Strategy evidence must normally be soft-scored.

Prohibited blanket gates:
- all indicators must agree;
- arbitrary model-agreement percentage;
- one universal score cutoff;
- one universal ATR cutoff;
- one universal probability cutoff;
- insufficient historical sample = no signal;
- non-preferred session = no signal;
- high volatility = no signal;
- low volatility = no signal;
- neutral/conflicting M30 or M15 = no signal;
- preferred stop/target unavailable = no signal when a documented safe fallback exists.

## 6. Context Doctrine

M30/M15 provide context. M5 primarily describes setup formation. M1 provides timing.

Higher-timeframe context can strengthen, weaken or conflict with a setup.

Neutral or conflicting context must not automatically veto a setup unless that context is intrinsically required by the definition of that specific setup family.

Missing optional context is represented explicitly as unavailable/neutral, never silently converted into a directional value.

## 7. Probability Doctrine

A probability must identify:
- event definition;
- sample;
- horizon;
- conditioning variables;
- outcome;
- uncertainty;
- calibration quality.

Insufficient historical sample produces an INSUFFICIENT_SAMPLE state or label. It does not fabricate a probability and does not automatically suppress a structurally valid signal.

Probability is research evidence. It is not a universal live gate unless a later version explicitly proves and documents such a rule for a defined setup family.

## 8. Trade-Plan Fallback Doctrine

Every setup family must have a deterministic hierarchy for entry, stop/invalidation, target and maximum horizon.

If the preferred method is unavailable, the engine tries the documented fallback.

If every safe method fails, the candidate is suppressed with an explicit reason such as INVALID_TRADE_PLAN.

The engine must never silently convert preferred method unavailable into no signal.

## 9. Setup Families

A. Liquidity sweep reversal
B. Expansion-pullback continuation
C. Breakout acceptance
D. Breakout failure
E. Range rejection
F. Structural pullback continuation

Each family must be independently testable and independently observable in telemetry.

## 10. Opportunity States

OBSERVE → CANDIDATE → DEVELOPING → TRIGGERED → ACTIVE → CLOSED

Or:

DEVELOPING → EXPIRED

All transitions must be causal and recorded.

## 11. Suppression Ledger

Every candidate that fails to become actionable must carry an explicit reason.

Canonical reasons:
- DATA_INVALID
- DUPLICATE
- NO_MINIMUM_SETUP
- NO_TRIGGER
- INVALID_TRADE_PLAN
- RISK_LIMIT
- EXPLICIT_EVENT_BLACKOUT
- EXPIRED
- OTHER_DOCUMENTED_REASON

NO_HIGH_EDGE is not a valid final suppression reason.

## 12. Ranking Doctrine

The ranker orders already-actionable opportunities.

It must not require a universal score threshold to permit a signal.

Evidence scores, conflict scores, empirical expectancy, uncertainty, execution quality and maturity are ranking/research variables unless a setup-specific validated rule explicitly states otherwise.

## 13. Sessions and Volatility

Session classification and volatility state affect search priority, evidence and ranking.

They do not automatically disable the engine.

The engine must remain capable of identifying valid opportunities outside preferred windows.

High or extreme volatility does not universally mean no trade.

Low or quiet volatility does not universally mean no trade.

## 14. Daily Quota

The engine does not trade to satisfy a target number of trades.

It also does not suppress a valid setup because the daily count is already high.

Actual opportunity frequency is measured.

## 15. Liveness Requirements

Before production strategy code is considered complete, tests must prove:
1. valid setup can alert with neutral M30/M15 context;
2. insufficient historical sample does not block a valid setup;
3. valid setup can alert outside preferred sessions;
4. one conflicting indicator does not kill a valid setup;
5. candidate below a research ranking benchmark can still become actionable when its minimum path is complete;
6. stop/target fallbacks work;
7. every blocked candidate has a suppression reason;
8. every setup family is evaluated independently;
9. failure of one family does not stop another;
10. high volatility does not universally suppress signals;
11. low volatility does not universally suppress signals;
12. session classification does not universally suppress signals.

Runtime telemetry must expose candidates, developing setups, triggers, actionable opportunities, alerts and suppression reasons by family.

## 16. Change Control

Any new hard gate must document its exact condition, reason, affected setup families, false-negative risk and a test proving it does not create unintended starvation.

## 17. Success

Success requires evidence of repeatable positive expectancy after realistic costs and out-of-sample validation.

Win rate alone is insufficient. Signal count alone is insufficient. Model agreement alone is insufficient.

## 18. Final Rule

Do not optimize the engine to look intelligent. Optimize it to be falsifiable, measurable, robust, live and useful while preserving every truthful path from a valid setup to an actionable signal.
