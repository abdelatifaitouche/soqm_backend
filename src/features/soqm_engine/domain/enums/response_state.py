from enum import StrEnum


class ResponseState(StrEnum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    IMPLEMENTED = "IMPLEMENTED"
    EFFECTIVE = "EFFECTIVE"
    RETIRED = "RETIRED"


class ResponseType(StrEnum):
    PREVENTIVE = "PREVENTIVE"
    CORRECTIVE = "CORRECTIVE"
    DETECTIVE = "DETECTIVE"


class ExecutionType(StrEnum):
    MANUAL = "MANUAL"
    AUTOMATED = "AUTOMATED"
    HYBRID = "HYBRID"


class Frequency(StrEnum):
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    BIMONTHLY = "bimonthly"
    QUARTERLY = "quarterly"
    SEMIANNUALLY = "semiannually"
    ANNUALLY = "annually"
    AD_HOC = "ad_hoc"
    EVENT_DRIVEN = "event_driven"
