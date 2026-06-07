# Path: src/domain/exceptions.py

class DomainError(Exception):
    pass

class BusinessRuleViolationError(DomainError):
    pass

class InvalidStateTransitionError(BusinessRuleViolationError):
    pass

class InvalidValueError(DomainError):
    pass
