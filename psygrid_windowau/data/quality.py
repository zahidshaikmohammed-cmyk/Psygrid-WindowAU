from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import Candle, DataQualityState, QualityIssue, QualityReport, finite_number

XAUUSD_MIN_PRICE = 0.0


def validate_candle(candle: Candle) -> QualityReport:
    issues: list[QualityIssue] = []
    if candle.open <= XAUUSD_MIN_PRICE or candle.high <= XAUUSD_MIN_PRICE or candle.low <= XAUUSD_MIN_PRICE or candle.close <= XAUUSD_MIN_PRICE:
        issues.append(QualityIssue("INVALID_PRICE", "OHLC prices must be positive", candle.timestamp))
    if candle.low > candle.high:
        issues.append(QualityIssue("INVALID_RANGE", "low exceeds high", candle.timestamp))
    if candle.open < candle.low or candle.open > candle.high:
        issues.append(QualityIssue("INVALID_OPEN", "open lies outside high/low", candle.timestamp))
    if candle.close < candle.low or candle.close > candle.high:
        issues.append(QualityIssue("INVALID_CLOSE", "close lies outside high/low", candle.timestamp))
    if candle.volume < 0:
        issues.append(QualityIssue("INVALID_VOLUME", "volume cannot be negative", candle.timestamp))
    for name in ("open", "high", "low", "close", "volume"):
        if not finite_number(getattr(candle, name)):
            issues.append(QualityIssue("NON_FINITE", f"{name} is not finite", candle.timestamp))
    for name in ("bid", "ask"):
        value = getattr(candle, name)
        if value is not None and not finite_number(value):
            issues.append(QualityIssue("NON_FINITE_QUOTE", f"{name} is not finite", candle.timestamp))
    if issues:
        return QualityReport(DataQualityState.INVALID, tuple(issues))
    return QualityReport(DataQualityState.VALID, ())


def validate_series(candles: tuple[Candle, ...], *, expected_interval_minutes: int = 1) -> QualityReport:
    issues: list[QualityIssue] = []
    previous: Candle | None = None
    seen: set[datetime] = set()
    delta = timedelta(minutes=expected_interval_minutes)
    for candle in candles:
        if candle.timestamp in seen:
            issues.append(QualityIssue("DUPLICATE", "duplicate candle timestamp", candle.timestamp))
        seen.add(candle.timestamp)
        report = validate_candle(candle)
        issues.extend(report.issues)
        if previous is not None:
            if candle.timestamp < previous.timestamp:
                issues.append(QualityIssue("NON_MONOTONIC", "timestamps are not monotonic", candle.timestamp))
            elif candle.timestamp - previous.timestamp > delta:
                issues.append(QualityIssue("GAP", "M1 interval gap detected", candle.timestamp))
        previous = candle
    state = DataQualityState.VALID
    if any(i.code == "DUPLICATE" for i in issues):
        state = DataQualityState.DUPLICATE
    elif any(i.code == "GAP" for i in issues):
        state = DataQualityState.GAP
    elif issues:
        state = DataQualityState.INVALID
    return QualityReport(state, tuple(issues))


def freshness_seconds(*, observation_time: datetime, provider_time: datetime) -> float:
    obs = observation_time.astimezone(timezone.utc)
    prov = provider_time.astimezone(timezone.utc)
    value = (obs - prov).total_seconds()
    if value < 0:
        raise ValueError("provider timestamp cannot be in the future relative to observation")
    return value


def is_fresh(freshness: float, max_age_seconds: float) -> bool:
    if freshness < 0 or max_age_seconds < 0:
        raise ValueError("freshness values must be non-negative")
    return freshness <= max_age_seconds
