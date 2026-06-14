from enum import StrEnum


class ObjectiveState(StrEnum):
    DRAFT = "draft"  # Being formulated by quality team
    APPROVED = "approved"  # Approved by leadership/management
    ACTIVE = "active"  # Currently in effect, being monitored
    UNDER_REVIEW = "under_review"  # Annual/periodic review in progress
    REVISED = "revised"  # Updated based on risk/findings
    ACHIEVED = "achieved"  # Goals met (quality objective realized)
    SUPERSEDED = "superseded"  # Replaced by new objective
    SUSPENDED = "suspended"  # Temporarily paused
    ARCHIVED = "archived"
