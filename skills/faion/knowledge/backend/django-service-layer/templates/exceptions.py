# purpose: domain exception hierarchy used by services (no HTTP coupling)
# consumes: nothing (root of the hierarchy)
# produces: ApplicationError + concrete subtypes raised by services and mapped to HTTP by views
# depends-on: stdlib only
# token-budget-impact: ~80 tokens


class ApplicationError(Exception):
    """Base class for every domain-level exception."""


class NotFoundError(ApplicationError):
    """Resource does not exist or is not visible to the caller."""


class ValidationError(ApplicationError):
    """Business invariant violated. Distinct from DRF's ValidationError."""


class PermissionDeniedError(ApplicationError):
    """Caller is authenticated but not authorised for this resource."""


class ConflictError(ApplicationError):
    """Resource state conflicts with the requested change (uniqueness, race)."""
