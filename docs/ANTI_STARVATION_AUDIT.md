# PSYGRID WindowAU — Anti-Starvation Audit

## Audit purpose

This document is a permanent engineering control.

The highest-priority failure mode is:

> A sophisticated engine that technically works but produces almost no signals because independent conditions accidentally become one giant AND-gate.

## Findings from the v1 specification audit

### Risk 1 — Historical probability becoming a hidden gate

The engine eventually uses empirical conditional probability. If implementation requires a calibrated probability before a signal can be emitted, the engine can produce zero signals during the early research period.

**Rule:**

Historical probability is optional evidence.

If sample size is insufficient:

- mark LOW_SAMPLE or INSUFFICIENT_SAMPLE;
- do not fabricate probability;
- do not reject the setup solely for lack of history.

### Risk 2 — M30/M15 context becoming a veto

The architecture says M30/M15 = context, M5 = setup, M1 = trigger.

If code implements:

M30 bullish AND M15 bullish AND M5 bullish AND M1 bullish

then many valid reversal setups disappear.

**Rule:**

M30/M15 are normally evidence.

A neutral or conflicting higher timeframe can reduce quality but cannot automatically veto a setup unless that requirement is intrinsic to that specific setup family.

### Risk 3 — Ranking becoming another hard gate

A ranker can accidentally implement:

if score < threshold: no signal

This recreates the old starvation problem under a different name.

**Rule:**

First determine whether a candidate is ACTIONABLE using safety, setup, trigger and trade-plan requirements.

Only then rank actionable candidates.

A research score is not a universal signal cutoff.

### Risk 4 — Trade-plan construction silently killing signals

A strategy can identify a valid setup and then disappear because its preferred target or stop formula returns None.

**Rule:**

Every setup family must have a deterministic fallback hierarchy for entry, stop, target and maximum holding time.

If all safe methods fail, record the exact suppression reason.

Never silently return NO SIGNAL.

## Mandatory minimum viable signal path

Every setup family must define:

1. minimum setup evidence;
2. M1 trigger;
3. valid feed;
4. executable entry;
5. safe stop/invalidation;
6. at least one valid target method;
7. maximum holding horizon;
8. duplicate check;
9. explicit risk/safety check.

Optional context and research statistics are not part of the minimum path.

## Suppression ledger

Every candidate that fails to alert must receive an explicit reason:

- DATA_INVALID
- DUPLICATE
- NO_MINIMUM_SETUP
- NO_TRIGGER
- INVALID_TRADE_PLAN
- RISK_LIMIT
- EXPLICIT_EVENT_BLACKOUT
- EXPIRED
- OTHER_DOCUMENTED_REASON

NO_HIGH_EDGE is prohibited as a final suppression reason.

## Liveness tests

The test suite must prove:

1. A valid setup can alert with neutral M30/M15 context.
2. A valid setup can alert with insufficient historical sample.
3. A valid setup can alert outside preferred sessions.
4. One conflicting indicator does not kill a valid setup.
5. A candidate below a research score benchmark can still alert if its minimum viable path is complete.
6. A fallback stop/target can construct a valid plan.
7. Every blocked candidate produces a suppression reason.
8. The engine evaluates all enabled setup families independently.
9. One family failing does not prevent another family from producing a signal.
10. A high-volatility state does not automatically suppress all setups.
11. A low-volatility state does not automatically suppress all setups.
12. Session classification does not automatically suppress all setups.

## Required runtime telemetry

Every minute the engine should be able to answer:

- How many setup candidates exist?
- Which family generated them?
- How many are developing?
- How many reached M1 trigger?
- How many became actionable?
- How many were suppressed?
- Why was each suppressed?
- Which feature or rule was responsible?

If the engine reports zero signals, we must be able to distinguish:

- the market produced no setup;
- setup detector missed it;
- trigger detector missed it;
- trade plan failed;
- risk blocked it;
- data blocked it;
- duplicate blocked it.

## Final audit conclusion

The architecture is acceptable only when the implementation preserves these rules.

The project must never become:

CONTEXT × INDICATORS × SCORE × PROBABILITY × SESSION × VOLATILITY × TRADE PLAN

with every factor required.

The intended structure is:

SETUP FAMILY
→ MINIMUM VALID SETUP
→ M1 TRIGGER
→ SAFE TRADE PLAN
→ ACTIONABLE
→ RANK
→ TELEGRAM

Additional information improves ranking and research quality; it does not silently turn into another mandatory gate.

**Primary engineering objective: maximize truthful opportunity detection without manufacturing trades.**
