# PSYGRID WindowAU — Mathematical Specification

## 1. Base M1 candle

C_t = (O_t, H_t, L_t, C_t, V_t, T_t)

T_t is the candle opening timestamp unless the provider contract proves otherwise.

## 2. Returns

Simple return:

r_t = C_t / C_(t-1) - 1

Log return:

g_t = ln(C_t / C_(t-1))

## 3. True Range and ATR

TR_t = max(H_t-L_t, |H_t-C_(t-1)|, |L_t-C_(t-1)|)

ATR_n = mean(TR over the last n completed candles)

Also calculate ATR percentile against a rolling historical distribution.

No single absolute ATR number is a universal volatility gate.

## 4. Realized volatility

RV_n = sqrt(n) × std(g over n observations)

Store both absolute and percentile-normalized volatility.

## 5. EMA

EMA_t = alpha*C_t + (1-alpha)*EMA_(t-1)

alpha = 2/(n+1)

Initial periods: 9, 20, 50, 200.

EMA slope:

slope_n(t,k) = [EMA_n(t)-EMA_n(t-k)] / k

## 6. VWAP

Typical price:

P_i = (H_i + L_i + C_i) / 3

Session VWAP:

VWAP_t = sum(P_i V_i) / sum(V_i)

If feed volume is not centralized exchange volume, label it feed-volume VWAP.

## 7. Candle geometry

Range:

R_t = H_t - L_t

Body:

B_t = |C_t - O_t|

Body ratio:

BodyRatio = B_t / R_t

Upper wick:

UW = H_t - max(O_t,C_t)

Lower wick:

LW = min(O_t,C_t) - L_t

Normalize wick values by R_t.

## 8. Structural levels

For lookback n:

HH_n(t) = max(H from t-n through t-1)

LL_n(t) = min(L from t-n through t-1)

The current candle is excluded from the reference level.

## 9. Liquidity sweep

For prior high H*:

sweep_up = max(0, H_t-H*)

For prior low L*:

sweep_down = max(0, L*-L_t)

Normalize:

SweepNorm = sweep_distance / ATR_n

Failed upside break requires price to return below the relevant level.

Failed downside break requires price to return above the relevant level.

## 10. Pullback depth

Bullish impulse from L to H, retracement price P:

Retracement = (H-P)/(H-L)

Bearish impulse:

Retracement = (P-L)/(H-L)

## 11. Displacement

Let R_base be a rolling robust baseline range.

DisplacementRatio = R_t / R_base

BodyDisplacement = B_t / median(B_baseline)

Displacement is evidence, not a trade signal.

## 12. Trend persistence

TrendPersistence = [count(positive returns) - count(negative returns)] / n

Also store directional run length and structural higher-high/higher-low counts.

## 13. Compression

CompressionRatio = current_range / median(previous_ranges)

Compression may precede expansion but has no predetermined direction.

## 14. Breakout acceptance

BreakDistance = |C_t - Level|

BreakNorm = BreakDistance / ATR_n

Acceptance is evaluated using:

- closes beyond level;
- persistence;
- retest behavior;
- distance maintained;
- rejection/re-entry.

## 15. Multi-timeframe context

Each timeframe stores:

- directional pressure;
- slope;
- VWAP location;
- structural location;
- volatility;
- range/trend state.

Alignment is a soft evidence vector.

## 16. Opportunity score

Initial diagnostic score:

S = sum(w_i*x_i) - sum(p_j*c_j)

x_i = positive evidence  
c_j = conflict evidence

Weights are research parameters and must be validated.

The score is not automatically a permanent hard gate.

## 17. Empirical conditional probability

For setup s, direction d, context z and horizon h:

p = P(target before stop | s,d,z,h)

Estimate:

p_hat = wins / N

Use Wilson or Bayesian intervals.

Wilson center:

(p_hat + z^2/(2N)) / (1 + z^2/N)

Wilson half-width:

z*sqrt[p_hat(1-p_hat)/N + z^2/(4N^2)] / (1+z^2/N)

Displayed probability must include N and uncertainty.

## 18. Expectancy

For win payoff W, loss L and cost K:

E_net = pW - (1-p)L - K

R-multiple expectancy:

E_R = mean(realized R)

Expectancy is more important than raw win rate.

## 19. Risk/reward

RR = |TP-Entry| / |Entry-SL|

Targets must come from structure/volatility/research rather than being chosen only to make RR look attractive.

## 20. Position sizing

Account risk:

R_$ = Equity × RiskFraction

If stop distance is D and contract value per price unit is V:

PositionSize = R_$ / (D × V)

Broker contract specifications must be verified before live sizing.

## 21. MFE / MAE

MFE = maximum favorable price excursion after entry.

MAE = maximum adverse price excursion after entry.

Store both in price and R units.

## 22. Holding horizon

Initial buckets:

1–3 min  
3–5 min  
5–10 min  
10–15 min  
15–20 min  
20–30 min

Initial maximum research horizon: 30 minutes.

## 23. Probability calibration

Brier score:

BS = mean[(p_i-y_i)^2]

Compare predicted probability buckets against realized frequencies.

## 24. Data-leakage rule

At decision time t, calculations may not use:

- future candles;
- final OHLC of a still-forming candle;
- future spread;
- future event outcome;
- future target/stop path.

Every feature must be reproducible from information available at t.

## 25. Priority

1. Causal correctness
2. Realistic execution
3. Stable expectancy
4. Calibration
5. Opportunity frequency
6. Efficiency
