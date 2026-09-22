# PSYGRID WindowAU — Versioned Setup Family Contracts
Version 1.0 — Phase 0 Architecture Lock

These contracts define the minimum causal path for the six initial setup families. They are detection contracts, not claims that any family has positive expectancy. Outcome data may later change thresholds/parameters only through documented version changes.

## Common contract rules
- A candidate is created from information available at the decision timestamp only.
- Optional evidence may be unavailable without suppressing the family.
- Required inputs are family-specific; absence/invalidity blocks only that family unless the entire feed is invalid.
- Every family reaches ACTIONABLE only through: minimum setup → valid M1 trigger → executable entry → safe stop/invalidation → target → horizon → duplicate/re-arm checks → strategy safety permission.
- Higher-timeframe context is evidence unless explicitly listed as intrinsic.
- Each family has an independent state machine and duplicate identity.
- Initial maximum research horizon is 30 minutes; exact family lifetimes are parameters below and must be outcome-validated.

## A. Liquidity Sweep Reversal — LSR v1.0
Definition: price takes a prior structural high/low, then demonstrates failure to sustain the break and returns through the swept level.
Required inputs: closed M1 OHLCV; causal structural reference level; valid ATR or equivalent range normalization only if used by the contract.
Minimum evidence: prior structural high/low exists; current completed M1 breaches it; subsequent completed M1 evidence returns through the level.
Optional evidence: wick/body geometry, displacement, VWAP location, M5/M15/M30 context, volatility/session state.
Timeframe dependencies: M1 intrinsic; M5/M15/M30 optional unless later version declares otherwise.
M1 trigger: completed M1 closes back across the swept level in the reversal direction.
Invalidation: price establishes continuation beyond the sweep level according to the configured structural buffer before trigger.
Entry hierarchy: trigger-close structural entry → next valid M1 retracement → documented safe fallback.
Stop hierarchy: beyond sweep extreme → structural buffer → volatility-adjusted structural buffer → safe fallback.
Target hierarchy: nearest opposing structure → next structure/range projection → volatility projection → empirical MFE target when validated.
Maximum lifetime: 15 minutes from setup anchor unless invalidated earlier.
Duplicate identity: symbol + LSR + direction + swept level identity + setup-start bucket.
Re-arm: only after invalidation/expiry or a new distinct sweep event.

## B. Expansion-Pullback Continuation — EPC v1.0
Definition: directional expansion/displacement establishes an impulse, followed by a controlled pullback that preserves the impulse structure.
Required inputs: closed M1 OHLCV; causal impulse and pullback structure.
Minimum evidence: qualifying expansion; identifiable impulse direction; pullback remains structurally consistent with continuation.
Optional evidence: ATR/displacement percentile, EMA/VWAP relationship, M5 structure, session/volatility.
Timeframe dependencies: M1 intrinsic; M5 optional formation context.
M1 trigger: completed M1 resumes impulse direction after pullback with qualifying close/body structure.
Invalidation: pullback breaks the setup's structural invalidation level.
Entry hierarchy: trigger continuation → shallow retracement entry → safe fallback.
Stop hierarchy: pullback structural invalidation → secondary structure → volatility-adjusted buffer → safe fallback.
Target hierarchy: prior impulse extension/structure → measured projection → volatility projection → empirical MFE.
Maximum lifetime: 20 minutes.
Duplicate identity: symbol + EPC + direction + impulse anchor + pullback anchor.
Re-arm: new impulse/pullback structure after expiry or invalidation.

## C. Breakout Acceptance — BOA v1.0
Definition: price breaks a defined structural level and demonstrates acceptance beyond it rather than immediate rejection.
Required inputs: closed M1 OHLCV; defined structural level.
Minimum evidence: completed M1 close beyond level plus persistence/acceptance evidence from subsequent price behavior.
Optional evidence: retest, displacement, VWAP/EMA location, M5 context, volatility/session.
Timeframe dependencies: M1 intrinsic; higher timeframes optional unless the level itself is family-specific.
M1 trigger: completed M1 confirms maintained acceptance beyond level or successful retest-and-hold.
Invalidation: decisive re-entry through the breakout level before trigger.
Entry hierarchy: acceptance close → retest hold → safe fallback.
Stop hierarchy: breakout-level invalidation → retest structure → volatility buffer → safe fallback.
Target hierarchy: next structural level → measured range projection → volatility projection → empirical MFE.
Maximum lifetime: 15 minutes.
Duplicate identity: symbol + BOA + direction + breakout-level identity + setup-start bucket.
Re-arm: only after failed/expired event followed by a new breakout event.

## D. Breakout Failure — BOF v1.0
Definition: price breaks a structural level but fails to sustain acceptance and returns through the level, creating reversal evidence.
Required inputs: closed M1 OHLCV; defined structural level.
Minimum evidence: break beyond level; failure/re-entry through level.
Optional evidence: rejection wick/body, displacement, VWAP, M5/M15 context, volatility/session.
Timeframe dependencies: M1 intrinsic.
M1 trigger: completed M1 closes back through the failed breakout level in reversal direction.
Invalidation: renewed acceptance beyond the failed-break extreme/level before trigger.
Entry hierarchy: re-entry close → first valid retracement → safe fallback.
Stop hierarchy: failed-break extreme → structural buffer → volatility buffer → safe fallback.
Target hierarchy: opposite range boundary/structure → next opposing level → volatility projection → empirical MFE.
Maximum lifetime: 15 minutes.
Duplicate identity: symbol + BOF + direction + failed-level identity + setup-start bucket.
Re-arm: new distinct failed-break event after expiry/invalidation.

## E. Range Rejection — RRE v1.0
Definition: price reaches a validated local range extreme and rejects it back toward the range interior.
Required inputs: closed M1 OHLCV; causal range boundaries with sufficient observations.
Minimum evidence: range is established; price reaches/penetrates an extreme; completed M1 shows rejection toward interior.
Optional evidence: wick/body geometry, compression, VWAP, M5 range context, session/volatility.
Timeframe dependencies: M1 intrinsic; higher timeframe range context optional.
M1 trigger: completed M1 rejection close away from the extreme.
Invalidation: sustained acceptance outside the range boundary.
Entry hierarchy: rejection close → retracement toward boundary → safe fallback.
Stop hierarchy: beyond range extreme → structural buffer → volatility buffer → safe fallback.
Target hierarchy: range midpoint → opposite internal structure → opposite range extreme when independently valid → empirical MFE.
Maximum lifetime: 20 minutes.
Duplicate identity: symbol + RRE + direction + range-boundary identity + setup-start bucket.
Re-arm: new range test/rejection after explicit expiry or invalidation.

## F. Structural Pullback Continuation — SPC v1.0
Definition: established directional structure experiences a controlled retracement and resumes without requiring a large expansion impulse.
Required inputs: closed M1 OHLCV; causal swing structure.
Minimum evidence: directional structural sequence; pullback to a valid structural area; no structural invalidation.
Optional evidence: EMA slope, VWAP, momentum, M5/M15 context, volatility/session.
Timeframe dependencies: M1 intrinsic; M5 may be optional structural confirmation.
M1 trigger: completed M1 resumes directional structure after pullback.
Invalidation: structural sequence breaks before trigger.
Entry hierarchy: trigger close → retracement entry → safe fallback.
Stop hierarchy: structural swing invalidation → secondary structure → volatility buffer → safe fallback.
Target hierarchy: next structural swing → measured projection → volatility projection → empirical MFE.
Maximum lifetime: 20 minutes.
Duplicate identity: symbol + SPC + direction + structural anchor + setup-start bucket.
Re-arm: new structurally distinct pullback after expiry/invalidation.

## Contract change control
Changing required inputs, minimum evidence, trigger, invalidation, lifetime, duplicate identity, re-arm, or fallback hierarchy creates a new contract version and requires liveness tests plus causal replay tests.
