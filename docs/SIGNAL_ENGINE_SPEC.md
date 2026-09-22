# PSYGRID WindowAU — Signal Engine Specification

Version 1.1 — Signal-Liveness Amendment

## 1. Runtime Loop

On every newly closed M1 candle:
1. validate feed;
2. update M1 series;
3. rebuild completed M5/M15/M30 views causally;
4. update session;
5. update volatility;
6. update structural levels;
7. evaluate every setup family independently;
8. update opportunity states;
9. evaluate M1 triggers;
10. construct a safe trade plan using family-specific fallback rules;
11. classify candidates as actionable or suppressed;
12. rank actionable opportunities;
13. send Telegram for a new actionable opportunity;
14. persist the full decision and suppression telemetry.

## 2. Decision Pipeline

SETUP FAMILY → MINIMUM VALID SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM

This order is mandatory.

## 3. Context

Context contains trend, slope, volatility, VWAP location, structure, range/trend state and session.

Context changes evidence. Context does not automatically veto a candidate.

M30/M15 may be unavailable, neutral or conflicting. These states must be represented explicitly.

## 4. Setup Evidence

Setup evidence can contain sweep, rejection, displacement, pullback, breakout, acceptance, failure and range location.

Each family uses only relevant features. No family may require unrelated indicators merely to increase model agreement.

## 5. Trigger Evidence

M1 timing evidence can include micro-structure break, reclaim, rejection, higher low/lower high, momentum return, retest and micro-range break.

M1 timing cannot create a trade thesis without a setup.

## 6. Minimum Viable Signal Contract

A candidate can become ACTIONABLE when:
- family-specific minimum setup definition is met;
- valid M1 trigger is present;
- feed/data quality is sufficient;
- entry is executable;
- safe stop/invalidation exists;
- at least one target exists;
- maximum horizon is defined;
- opportunity is not a duplicate;
- explicit safety/risk rules permit it.

Optional research evidence does not belong in this mandatory chain.

## 7. Historical Probability

If sample size is insufficient:
- preserve the candidate;
- mark evidence INSUFFICIENT_SAMPLE;
- do not fabricate a percentage;
- do not automatically suppress the candidate.

When enough observations exist, report sample size, estimate, uncertainty and calibration quality.

## 8. Trade-Plan Construction

Every setup family must define fallback hierarchies for entry, stop and target.

Preferred structural method → secondary structural method → volatility-adjusted structural method → documented safe fallback.

If all safe methods fail, suppress with INVALID_TRADE_PLAN and record the exact failed condition.

No silent suppression.

## 9. Ranking

Each actionable candidate receives evidence score, conflict score, empirical expectancy where available, uncertainty, execution quality and maturity.

The ranker orders actionable candidates.

There is no universal score requirement for actionability.

## 10. Setup Independence

All six setup families are evaluated independently.

One family returning no candidate, an error state or an expired opportunity must not suppress other families.

## 11. Session and Volatility

Session and volatility are conditioning variables and prioritization inputs.

They may change evaluation priority, evidence weight, expected behavior, ranking and research stratification.

They do not automatically disable signal generation.

## 12. Event Risk

Scheduled high-impact events may reduce confidence, require post-event confirmation or apply a configured temporary pause.

Any blackout must be explicit, time-bounded, instrument-relevant and logged as EXPLICIT_EVENT_BLACKOUT.

## 13. Duplicate Control

Opportunity identity uses symbol, setup family, structural anchor, setup start time and direction.

Identity must not be so broad that separate valid setups are accidentally treated as duplicates.

## 14. Invalidation

Candidate expires when structure is invalidated, setup exceeds its research lifetime, entry becomes materially stale, opportunity becomes unexecutable or required data quality fails.

Every invalidation is recorded.

## 15. Suppression Ledger

Every non-actionable candidate receives one explicit reason:
DATA_INVALID, DUPLICATE, NO_MINIMUM_SETUP, NO_TRIGGER, INVALID_TRADE_PLAN, RISK_LIMIT, EXPLICIT_EVENT_BLACKOUT, EXPIRED or OTHER_DOCUMENTED_REASON.

NO_HIGH_EDGE is prohibited as a suppression reason.

## 16. Telegram

Every actionable alert should show:
PSYGRID XAUUSD, Direction, Setup family, Entry, SL, TP1/TP2, R:R, Session, Volatility state, Structural reason, M1 trigger, Expected holding horizon, Historical sample size, Historical expectancy, Probability status, Timestamp and Data quality.

If historical probability is unavailable, show INSUFFICIENT_SAMPLE.

## 17. Frequency and Liveness Telemetry

Persist candidates by family, developing setups, triggers, actionable candidates, alerts, expired candidates, suppressed candidates, suppression reason, last valid candidate time, last actionable time, last Telegram delivery and data-quality state.

This distinguishes a quiet market from a broken or over-filtered engine.

## 18. Required Liveness Tests

Required before production:
- valid setup + neutral M30/M15 → actionable;
- valid setup + insufficient history → actionable;
- valid setup outside preferred session → actionable;
- one conflicting indicator → still actionable when minimum path is complete;
- low research rank → not blocked solely by ranking;
- preferred stop unavailable → safe fallback used;
- preferred target unavailable → safe fallback used;
- every suppression has a reason;
- all setup families run independently;
- one family failure does not suppress others;
- high volatility is not a universal blocker;
- low volatility is not a universal blocker;
- session is not a universal blocker.

## 19. Persistence

Persist the candidate before Telegram delivery.

Telegram delivery status is separate from signal existence.

A Telegram failure must not erase or suppress the underlying actionable opportunity.

## 20. Core Principle

Minimum safety path first. Ranking second.

Additional evidence should improve prioritization and research quality without silently destroying valid opportunity paths.
