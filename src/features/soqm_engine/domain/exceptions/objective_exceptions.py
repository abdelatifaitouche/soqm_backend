from src.core.shared.domain.exceptions import (
    DomainValidationException,
    BusinessRuleViolationException,
)


class InvalidObjectiveException(DomainValidationException):
    pass


class InvalidObjectiveStateException(BusinessRuleViolationException):
    pass
