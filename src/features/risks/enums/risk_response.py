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
