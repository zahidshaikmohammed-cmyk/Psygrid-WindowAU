# PSYGRID WindowAU — Signal Engine Specification

## 1. Runtime loop

On every newly closed M1 candle:

1. validate feed;
2. update M1 series;
3. rebuild completed M5/M15/M30 views causally;
4. update session;
5. update volatility;
6. update structural levels;
7. evaluate every setup family;
8. update opportunity states;
9. evaluate M1 triggers;
10. calculate trade plan;
11. rank opportunities;
12. send Telegram only for a new actionable opportunity;
13. persist everything.

## 2. Context vector

Context contains:

- trend;
- slope;
- volatility;
- VWAP location;
- structure;
- range/trend state;
- session.

Context changes evidence. It is not a universal veto.

## 3. Setup vector

Setup evidence can contain:

- sweep;
- rejection;
- displacement;
- pullback;
- breakout;
- acceptance;
- failure;
- range location.

Each family uses only the relevant features.

## 4. Trigger vector

M1 timing evidence can include:

- micro-structure break;
- reclaim;
- rejection;
- higher low/lower high;
- momentum return;
- retest;
- micro-range break.

M1 timing cannot create a trade thesis without a setup.

## 5. Decision design

Each candidate gets:

- evidence score;
- conflict score;
- empirical expectancy estimate;
- uncertainty;
- execution quality;
- maturity.

Use an opportunity ranking queue rather than one universal hard threshold.

A strong setup may trigger even if one indicator disagrees.

## 6. Telegram signal

Every actionable alert should show:

PSYGRID XAUUSD

Direction  
Setup family  
Entry  
SL  
TP1 / TP2  
R:R  
Session  
Volatility state  
Structural reason  
M1 trigger  
Expected holding horizon  
Historical sample size  
Historical expectancy  
Timestamp  
Data quality

## 7. Duplicate control

Opportunity identity is derived from:

- symbol;
- setup family;
- structural anchor;
- setup start time;
- direction.

An opportunity cannot repeatedly alert unless it is explicitly re-armed after invalidation.

## 8. Invalidation

Candidate expires when:

- structure is invalidated;
- setup exceeds its research lifetime;
- entry becomes materially stale;
- opportunity becomes unexecutable;
- required data quality fails.

Every invalidation is recorded.

## 9. Event risk

Scheduled high-impact events are a conditioning variable.

The engine may reduce confidence, require post-event confirmation, or apply a configured temporary pause.

Event risk is not a universal permanent no-trade rule.

## 10. Frequency

No daily trade quota.

The engine measures:

- candidates;
- developing setups;
- triggers;
- alerts;
- expired setups;
- outcomes.

This is how we determine whether the system is genuinely too restrictive.
