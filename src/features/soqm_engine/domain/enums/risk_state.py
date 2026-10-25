from enum import StrEnum


class RiskStatus(StrEnum):
    IDENTIFIED = "identified"
    ASSESSED = "assessed"
    TREATMENT_PLANNED = "treatment_planned"
    MITIGATED = "mitigated"
    ACCEPTED = "accepted"
    CLOSED = "closed"
    UNDER_REVIEW = "under_review"
    VOIDED = "voided"


class RiskLevel(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
