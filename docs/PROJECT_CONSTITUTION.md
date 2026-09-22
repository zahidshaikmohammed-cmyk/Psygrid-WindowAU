# PSYGRID WindowAU — Permanent Project Constitution

Version 1.0  
Instrument: XAUUSD

## 1. Mission

Create a precise, empirical XAUUSD intraday engine that is willing to act when evidence supports a setup and unwilling to manufacture trades when evidence does not.

## 2. Anti-starvation rule

No universal AND-gate may require every model, timeframe and indicator to agree.

Each setup family gets an independent path to action.

Context is evidence, not a veto by default.

## 3. Hard-gate doctrine

Hard gates may block only for:

- invalid/stale data;
- impossible prices;
- timestamp corruption;
- required missing data;
- duplicate opportunity;
- invalid trade geometry;
- explicit risk-limit violation;
- explicit configured safety blackout.

Strategy evidence must normally be soft-scored.

Prohibited blanket gates include arbitrary model-agreement percentages, one universal score threshold, one universal ATR threshold, or "wrong session = no trade".

## 4. Three-layer architecture

M30/M15 = context  
M5 = setup  
M1 = trigger

M1 cannot create a thesis by itself.

## 5. Setup families

A. Liquidity sweep reversal  
B. Expansion-pullback continuation  
C. Breakout acceptance  
D. Breakout failure  
E. Range rejection  
F. Structural pullback continuation

Each family must be independently testable.

## 6. Opportunity states

OBSERVE → CANDIDATE → DEVELOPING → TRIGGERED → ACTIVE → CLOSED

Or:

DEVELOPING → EXPIRED

All transitions must be causal.

## 7. No daily quota

The engine does not trade to satisfy a target number of trades.

It also does not suppress a valid setup because the daily count is already high.

The research system measures actual opportunity frequency.

## 8. Probability doctrine

A probability must identify:

- event definition;
- sample;
- horizon;
- conditioning variables;
- outcome;
- uncertainty;
- calibration quality.

## 9. Change control

Any change to setup definitions, formulas, thresholds, risk, sessions, outcome definitions or data semantics must be documented and versioned before it becomes production logic.

## 10. Success

Success requires evidence of repeatable positive expectancy after realistic costs and out-of-sample validation.

Win rate alone is insufficient.

Signal count alone is insufficient.

Model agreement alone is insufficient.

## 11. Final rule

**Do not optimize the engine to look intelligent. Optimize it to be falsifiable, measurable, robust and useful.**
