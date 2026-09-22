# PSYGRID WindowAU — Project Description

## One-line description
A Python XAUUSD intraday intelligence and signal engine that continuously evaluates independent structural setups while preserving a truthful path from valid setup to actionable signal.

## Canonical architecture
DATA → QUALITY → MTF BUILDER → FEATURES → INDEPENDENT SETUP FAMILIES → MINIMUM SETUP → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABLE → RANK → TELEGRAM → OUTCOME → CALIBRATION

Broker execution is deliberately a later external layer.

## Engineering promise
The engine can discover valid setups outside preferred sessions and without perfect indicator/MTF agreement.

Historical probability is evidence, not a universal prerequisite.

Missing optional features do not become false directional values and do not globally block the engine.

Every setup family has its own contract, trigger, trade-plan fallback, lifetime and re-arm rule.

Every suppressed candidate has an explicit reason.

## Main objective
Determine, with reproducible data, whether XAUUSD contains repeatable short-horizon opportunities under combinations of:
- setup family;
- structure;
- session;
- volatility;
- trigger;
- execution conditions.

## Actionability
Minimum path:
setup → M1 trigger → required data → executable entry → safe stop → target → horizon → duplicate check → risk/safety permission.

Then:
ACTIONABLE → RANK → TELEGRAM.

## Event data
Event status is explicit:
VERIFIED_EVENT, VERIFIED_NO_EVENT or UNKNOWN.

UNKNOWN is never treated as VERIFIED_NO_EVENT or automatic BLACKOUT.

## Guiding sentence
Observe the market that actually exists, preserve every truthful opportunity path, and let measured outcomes determine what survives.
