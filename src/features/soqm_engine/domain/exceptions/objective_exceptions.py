from src.core.shared.domain.exceptions import (
    BusinessRuleViolationException,
    DomainValidationException,
)


class InvalidObjectiveException(DomainValidationException):
    pass


class InvalidObjectiveStateException(BusinessRuleViolationException):
    pass
