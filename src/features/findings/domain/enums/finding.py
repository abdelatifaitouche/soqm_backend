from enum import StrEnum


class FindingSource(StrEnum):
    GTAR = "Gtar"
    EXTERNAL_QUALITY_REVIEW = "external_quality_review"
    EXTERNAL_ENGAGEMENT_SYSTEM_REVIEW = "external_engagement_system_review"
    INTERNAL_QUALITY_MANAMGEMENT_SYSTEM_REVIEW = (
        "internal_quality_management_system_review"
    )
    INTERNAL_ENGAGEMENT_REVIEW = "internal_engagement_review"
    RESTATEMENTS = "restatements"
    OTHER_QUALITY_EVENTS = "other_quality_events"


class FindingStatus(StrEnum):
    OPEN = "open"
    UNDER_ASSESSMENT = "under_assessment"
    REMEDIATION_IN_PROGRESS = "remediation_in_progress"
    PENDING_VERIFICATION = "pending_verification"
    CLOSED = "closed"


class DeficiencySeverity(StrEnum):
    DEFICIENCY = "deficiency"
    SIGNIFICANT_DEFICIENCY = "significant_deficiency"
    MATERIAL_DEFICIENCY = "material_deficiency"
