from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SetupFamily(str, Enum):
    LSR = "LSR"
    EPC = "EPC"
    BOA = "BOA"
    BOF = "BOF"
    RRE = "RRE"
    SPC = "SPC"


class SetupDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass(frozen=True)
class SetupCandidate:
    family: SetupFamily
    direction: SetupDirection
    anchor_timestamp: datetime
    observed_timestamp: datetime
    anchor_index: int
    reference_level: float | None
    invalidation_level: float | None
    evidence: tuple[str, ...]
    parameters: tuple[tuple[str, float], ...]

    def __post_init__(self) -> None:
        if self.anchor_index < 0:
            raise ValueError("anchor_index must be non-negative")
        if self.anchor_timestamp.tzinfo is None or self.observed_timestamp.tzinfo is None:
            raise ValueError("candidate timestamps must be timezone-aware")
        if self.observed_timestamp < self.anchor_timestamp:
            raise ValueError("observed_timestamp cannot precede anchor_timestamp")
        if not self.evidence:
            raise ValueError("candidate must record minimum evidence")
        if any(not isinstance(x, str) or not x for x in self.evidence):
            raise ValueError("candidate evidence must contain non-empty strings")

    @property
    def identity(self) -> tuple[str, str, str, int]:
        level = "none" if self.reference_level is None else f"{self.reference_level:.10f}"
        return (self.family.value, self.direction.value, level, self.anchor_index)
