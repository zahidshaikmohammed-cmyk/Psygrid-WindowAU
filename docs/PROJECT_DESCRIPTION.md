# PSYGRID WindowAU — Project Description

## One-line description

A Python XAUUSD intraday research and signal engine that hunts continuously for statistically supported setups without suppressing genuine opportunities through excessive hard filtering.

## What this project is

WindowAU is a dedicated Gold engine.

It is not a generic multi-instrument scanner.

Its job is to observe XAUUSD, understand the current market state, identify several possible structural behaviors, wait for a precise trigger, calculate a complete trade plan, and notify the user through Telegram.

## What this project is not

It is not:

- a candle-direction guessing machine;
- an indicator-crossing bot;
- a fixed 90% probability generator;
- a system that must produce exactly 3 or 4 trades every day;
- a system that avoids all volatility;
- a system that assumes every breakout works;
- a backtest that uses future candle information.

## Engineering promise

The engine must be capable of finding opportunities whenever a high-quality setup genuinely develops, including outside preferred session windows.

Preferred/high-activity windows improve search priority but never create a trade.

Weak evidence is allowed to remain a candidate instead of being destroyed by a rigid gate.

Strong evidence is allowed to reach the trigger stage even if one indicator disagrees.

## Main objective

Find out, with reproducible data, whether XAUUSD offers repeatable short-horizon opportunities under specific combinations of:

- setup family;
- market structure;
- session;
- volatility;
- trigger behavior;
- execution conditions.

Then trade only the behavior that survives research.

## Core architecture

DATA → QUALITY → MTF CONTEXT → SETUP FAMILIES → M1 TRIGGER → RISK PLAN → TELEGRAM → OUTCOME → CALIBRATION

## Guiding sentence

**Observe the market that actually exists, not the market we wish existed.**
