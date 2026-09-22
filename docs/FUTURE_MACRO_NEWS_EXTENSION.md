# PSYGRID WindowAU — Future Macro & News Extension Scope

Version 1.0 — Phase-0 Scope Reservation

## 1. Purpose

WindowAU is currently a **technical-only XAUUSD intraday engine**.

This document reserves a controlled extension point for future macroeconomic, market-context and news intelligence without making those inputs dependencies of the current technical signal engine.

This is a scope reservation, not an implementation of macro/news functionality.

## 2. Current Production Scope

The current WindowAU decision engine uses technical market data only:

DATA → QUALITY → MTF BUILDER → TECHNICAL FEATURES → INDEPENDENT TECHNICAL SETUP FAMILIES → M1 TRIGGER → SAFE TRADE PLAN → ACTIONABILITY → RANK → TELEGRAM

The current canonical market source remains the RealMarketAPI M1 XAUUSD feed defined in `docs/CANONICAL_DATA_SOURCE.md`.

No macro or news provider is required for the current technical engine.

## 3. Reserved Future Inputs

A future extension may ingest, where independently verified and documented:

- economic-calendar events;
- central-bank decisions and communications;
- inflation and employment releases;
- interest-rate and monetary-policy context;
- USD/DXY context;
- Treasury-yield context;
- geopolitical/news events;
- broader risk-on/risk-off context;
- other documented macro variables relevant to XAUUSD.

No provider is selected or implied by this document.

## 4. Architectural Extension Point

Future macro/news information should enter through a separate context layer:

TECHNICAL ENGINE
+
FUTURE MACRO/NEWS CONTEXT
↓
EVIDENCE / RESEARCH / RANKING / OPTIONAL EXPLICIT SAFETY RULES

The future context layer must not be embedded directly into individual technical setup detectors unless a later versioned family contract explicitly requires a specific input.

## 5. Availability Semantics

Future macro/news data must use explicit availability states.

Examples:

- AVAILABLE
- UNAVAILABLE
- INVALID
- UNKNOWN

Unavailable or unknown macro/news data must not automatically suppress a technically valid setup.

A future provider outage must not silently become:

`NO_SIGNAL`

unless a separately documented, tested and explicitly configured safety rule makes that particular information intrinsically required.

## 6. Anti-Starvation Requirement

Macro/news integration must preserve the WindowAU anti-starvation constitution.

The following blanket gates are prohibited:

- no news feed = no technical signal;
- no macro confirmation = no technical signal;
- preferred macro condition absent = no signal;
- all macro factors must agree with technical direction;
- arbitrary macro score threshold as a universal prerequisite.

Macro/news evidence may improve context, research stratification, ranking or a specifically validated safety rule without becoming a universal technical prerequisite.

## 7. Future Provider Change Control

When macro/news functionality is actually implemented, it requires:

1. a dedicated source record;
2. provider/schema verification;
3. timestamp and event-time semantics verification;
4. observation-level capture;
5. causal replay treatment;
6. data-quality rules;
7. availability-state handling;
8. explicit provenance;
9. tests for provider failure and missing data;
10. architecture/liveness regression tests.

The provider must never be silently substituted.

## 8. Separation of Concerns

Technical signal existence must remain distinguishable from macro/news context.

At minimum, future signal records should be able to distinguish:

- technical setup evidence;
- macro context;
- news/event context;
- actionability;
- ranking;
- execution capacity.

This prevents future contextual information from becoming an undocumented hidden gate.

## 9. Current Status

Technical engine: **IN SCOPE**

Macro/news provider: **NOT SELECTED**

Macro/news implementation: **NOT IMPLEMENTED**

Macro/news data dependency for technical signals: **NONE**

Future extension point: **RESERVED**

This document must be updated through normal project change control when macro/news functionality is introduced.
