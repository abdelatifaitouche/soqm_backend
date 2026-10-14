from dataclasses import dataclass


@dataclass
class RiskMatrixCell:
    occurence: int
    significance: int
    percent: float


@dataclass
class RiskMatrix:
    cells: list[RiskMatrixCell] | None = None
