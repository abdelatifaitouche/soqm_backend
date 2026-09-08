class DomainException(Exception):
    pass


class DomainValidationException(DomainException):
    pass


class BusinessRuleViolationException(DomainException):
    pass
