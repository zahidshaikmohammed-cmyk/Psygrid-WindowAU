# PSYGRID WindowAU — Session and Volatility Framework

## 1. Principle

Time is a conditioning variable, not a trade signal.

The engine remains capable of evaluating opportunities across the day.

## 2. Timezone

Internal timestamps: UTC.

Display timezone: Asia/Kolkata.

Use IANA timezone data so daylight-saving changes are handled automatically for London and New York.

## 3. Session labels

Initial labels:

- ASIA
- LONDON
- LONDON_NY_OVERLAP
- NEW_YORK
- LATE_NEW_YORK
- TRANSITION

Exact clock boundaries are configuration and research parameters.

## 4. High-opportunity windows

High-liquidity/high-activity windows receive:

- more frequent opportunity evaluation;
- faster trigger monitoring;
- higher research priority;
- no forced trade.

The clock never creates a BUY or SELL.

## 5. Volatility state

Calculate:

- ATR percentile;
- realized-volatility percentile;
- range percentile;
- displacement percentile;
- current range vs rolling median;
- volatility expansion rate.

Initial labels:

QUIET  
NORMAL  
EXPANDING  
HIGH  
EXTREME

These are descriptive states.

## 6. Volatility transition

VolImpulse = current_ATR / prior_ATR_baseline

Also calculate percentile changes.

A transition from NORMAL to EXPANDING may be more informative than simply being HIGH.

## 7. Session × volatility

Eventually estimate:

P(outcome | setup, session, volatility_state)

This prevents assuming a setup behaves identically at every hour.

## 8. Low-activity periods

Do not implement:

if not preferred_session: no_signal

Instead, session is a feature that changes opportunity ranking.

## 9. Research rule

Session boundaries and volatility labels may be optimized only after enough out-of-sample data exists.
