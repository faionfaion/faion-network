# Error code constants for RFC 7807 error responses.
# Use these in the "code" field of error items and in error type URIs.


class ErrorCode:
    # Client errors (4xx)
    VALIDATION_ERROR = "validation_error"
    INVALID_FORMAT = "invalid_format"
    MISSING_FIELD = "missing_field"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    RATE_LIMITED = "rate_limited"

    # Server errors (5xx)
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    TIMEOUT = "timeout"
