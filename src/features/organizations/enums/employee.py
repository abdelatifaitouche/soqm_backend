from enum import StrEnum


class EmployeeState(StrEnum):
    ACTIVE = "ACTIVE"
    INVITED = "INVITED"
    ON_LEAVE = "ON_LEAVE"
    IN_ACTIVE = "IN_ACTIVE"
    TERMINATED = "TERMINATED"


class EmployeeLevel(StrEnum):
    INTERN = "INTERN"
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    MANAGER = "MANAGER"
    SENIOR_MANAGER = "SENIOR_MANAGER"
    DIRECTOR = "DIRECTOR"
    PARTNER = "PARTNER"
