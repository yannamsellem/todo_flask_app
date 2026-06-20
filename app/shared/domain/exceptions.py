class DomainException(Exception):
    """Base class for domain exceptions"""

    pass


class EntityNotFoundException(DomainException):
    """Raised when an entity is not found"""

    pass


class UnauthorizedException(DomainException):
    """Raised when an action is unauthorized"""

    pass
