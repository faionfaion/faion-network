"""
Domain exception hierarchy for Django services.

Rules:
- Never raise Http404 or DRF APIException inside services.
- Raise domain exceptions; let the view/serializer layer translate them.
- Use a two-level hierarchy: ApplicationError → domain-specific errors.
- All domain exceptions are catchable as ApplicationError in middleware.
"""


class ApplicationError(Exception):
    """
    Base exception for all domain errors.

    Attributes:
        message: Human-readable error description.
        extra: Optional dict for structured error context.
    """

    def __init__(self, message: str, extra: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


# --- Order domain ---

class OrderNotFoundError(ApplicationError):
    pass


class OrderAlreadyCancelledError(ApplicationError):
    pass


class OrderCannotBeModifiedError(ApplicationError):
    pass


# --- Product domain ---

class ProductNotFoundError(ApplicationError):
    pass


class ProductOutOfStockError(ApplicationError):
    pass


# --- User domain ---

class UserNotFoundError(ApplicationError):
    pass


class UserPermissionDeniedError(ApplicationError):
    pass
