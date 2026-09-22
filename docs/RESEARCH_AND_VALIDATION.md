# PSYGRID WindowAU — Research and Validation Protocol

## 1. Objective

Prevent attractive-looking signals from being mistaken for a real edge.

## 2. Raw capture

Store:

- fetch timestamp;
- provider timestamp;
- symbol;
- M1 candles;
- feed status;
- freshness;
- connection state.

## 3. Causal replay

Replay must reproduce only what was knowable at each historical decision time.

A later snapshot containing the final value of a forming candle must never be visible earlier.

If forming-candle snapshots cannot reconstruct the intrabar path, expose the candle only after it closes.

## 4. Chronological validation

Never randomly shuffle time series.

Use:

- development/training;
- validation;
- untouched forward/out-of-sample period.

## 5. Walk-forward

Estimate parameters on a past window and test on the next unseen window.

Record parameter stability.

## 6. Required metrics

- trade count;
- win rate;
- expectancy in R;
- median R;
- profit factor;
- drawdown;
- MFE;
- MAE;
- time to target;
- time to stop;
- holding time;
- slippage sensitivity;
- session results;
- volatility results;
- setup-family results.

## 7. Calibration

Record:

- Brier score;
- predicted vs realized probability;
- calibration buckets;
- sample size;
- confidence intervals.

## 8. Multiple testing

Record every experiment.

Do not report only the best variation.

Prefer robust rules that survive unseen data.

## 9. Cost sensitivity

Test realistic and adverse spread/slippage scenarios.

A strategy that only works at theoretical mid-price is not proven.

## 10. Forward test

Run observation mode first, then paper mode.

Compare live observations against replay expectations.

## 11. Live deployment prerequisites

Require:

1. verified feed;
2. causal replay;
3. tested risk engine;
4. stable paper evidence;
5. no known look-ahead bias;
6. deterministic Telegram delivery;
7. persistent state.

## 12. No invented results

No performance number enters documentation unless it comes from recorded data and a reproducible run.

## 13. Daily report

Eventually report:

- candidates;
- alerts;
- missed opportunities;
- invalidations;
- outcomes;
- MFE/MAE;
- setup statistics;
- session statistics;
- volatility statistics;
- data quality.
