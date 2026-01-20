---
id: M-DEV-055
name: "Error Handling"
domain: DEV
skill: faion-software-developer
category: "development"
---

# M-DEV-055: Error Handling

## Overview

Error handling ensures applications respond gracefully to unexpected conditions, providing meaningful feedback to users and developers while maintaining system stability. Proper error handling improves debugging, user experience, and system reliability.

## When to Use

- All production code should have error handling
- External service integrations (APIs, databases, files)
- User input processing
- Background job execution
- Critical business operations

## Key Principles

- **Fail fast**: Detect errors early, before they cause bigger problems
- **Fail loudly**: Make errors visible through logging and monitoring
- **Fail gracefully**: Don't expose internal details to users
- **Be specific**: Use appropriate exception types
- **Provide context**: Include enough information to debug

## Best Practices

### Exception Hierarchy Design

```python
# Custom exception hierarchy

class AppError(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code or "INTERNAL_ERROR"
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


# Domain-specific exceptions
class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str = None, details: dict = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={"field": field, **(details or {})}
        )


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            details={"resource": resource, "identifier": identifier}
        )


class ConflictError(AppError):
    """Raised when an operation conflicts with existing state."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            code="CONFLICT",
            details=details
        )


class AuthenticationError(AppError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, code="UNAUTHORIZED")


class AuthorizationError(AppError):
    """Raised when user lacks permission."""

    def __init__(self, action: str, resource: str = None):
        message = f"Not authorized to {action}"
        if resource:
            message += f" on {resource}"
        super().__init__(message=message, code="FORBIDDEN")


class ExternalServiceError(AppError):
    """Raised when an external service fails."""

    def __init__(self, service: str, message: str, original_error: Exception = None):
        super().__init__(
            message=f"{service} error: {message}",
            code="EXTERNAL_SERVICE_ERROR",
            details={"service": service}
        )
        self.original_error = original_error
```

### API Error Handling

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Global exception handlers
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle application-specific errors."""
    logger.warning(
        f"Application error: {exc.code} - {exc.message}",
        extra={"details": exc.details, "path": request.url.path}
    )

    status_codes = {
        "VALIDATION_ERROR": 400,
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "EXTERNAL_SERVICE_ERROR": 502,
        "INTERNAL_ERROR": 500,
    }

    return JSONResponse(
        status_code=status_codes.get(exc.code, 500),
        content=exc.to_dict()
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {"errors": errors}
            }
        }
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    """Handle unexpected errors - don't expose details."""
    logger.exception(
        f"Unhandled error on {request.method} {request.url.path}",
        exc_info=exc
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )


# Usage in endpoints
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await user_repository.find_by_id(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user


@app.post("/users")
async def create_user(data: UserCreate):
    existing = await user_repository.find_by_email(data.email)
    if existing:
        raise ConflictError(
            "Email already registered",
            details={"email": data.email}
        )
    return await user_repository.create(data)
```

### Result Type Pattern

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Ok(Generic[T]):
    """Represents a successful result."""
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value


@dataclass
class Err(Generic[E]):
    """Represents an error result."""
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self):
        raise ValueError(f"Called unwrap on Err: {self.error}")

    def unwrap_or(self, default: T) -> T:
        return default


Result = Union[Ok[T], Err[E]]


# Usage
def parse_user_id(value: str) -> Result[int, str]:
    try:
        user_id = int(value)
        if user_id <= 0:
            return Err("User ID must be positive")
        return Ok(user_id)
    except ValueError:
        return Err(f"Invalid user ID format: {value}")


def get_user_safely(user_id_str: str) -> Result[User, str]:
    # Chain results
    result = parse_user_id(user_id_str)
    if result.is_err():
        return result

    user_id = result.unwrap()
    user = user_repository.find_by_id(user_id)

    if not user:
        return Err(f"User not found: {user_id}")

    return Ok(user)


# Usage
result = get_user_safely("123")
if result.is_ok():
    user = result.unwrap()
    print(f"Found user: {user.name}")
else:
    print(f"Error: {result.error}")
```

### Error Recovery Patterns

```python
import time
from functools import wraps
from typing import Callable, Type

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception

        return wrapper
    return decorator


# Usage
@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
def fetch_from_api(url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


# Circuit breaker pattern
class CircuitBreaker:
    """Prevents repeated calls to failing services."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "open":
                if self._should_attempt_reset():
                    self.state = "half-open"
                else:
                    raise CircuitOpenError("Circuit breaker is open")

            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise

        return wrapper

    def _should_attempt_reset(self) -> bool:
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )

    def _on_success(self):
        self.failures = 0
        self.state = "closed"

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"


# Usage
payment_circuit = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

@payment_circuit
def process_payment(amount: float) -> PaymentResult:
    return payment_gateway.charge(amount)
```

### Contextual Error Information

```python
import traceback
from contextvars import ContextVar
from typing import Optional

# Request context for error tracking
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar("user_id", default=None)


class ErrorContext:
    """Capture context for better error debugging."""

    @staticmethod
    def capture() -> dict:
        return {
            "request_id": request_id_var.get(),
            "user_id": user_id_var.get(),
            "timestamp": datetime.utcnow().isoformat(),
        }


class DetailedError(Exception):
    """Exception with detailed context for debugging."""

    def __init__(
        self,
        message: str,
        cause: Exception = None,
        context: dict = None
    ):
        self.message = message
        self.cause = cause
        self.context = {
            **ErrorContext.capture(),
            **(context or {})
        }
        super().__init__(message)

    def __str__(self):
        parts = [self.message]
        if self.cause:
            parts.append(f"Caused by: {type(self.cause).__name__}: {self.cause}")
        if self.context:
            parts.append(f"Context: {self.context}")
        return "\n".join(parts)


# Usage
def process_order(order_id: str):
    try:
        order = fetch_order(order_id)
        payment = charge_payment(order)
        return complete_order(order, payment)
    except PaymentGatewayError as e:
        raise DetailedError(
            message=f"Failed to process order {order_id}",
            cause=e,
            context={
                "order_id": order_id,
                "order_total": order.total,
                "payment_method": order.payment_method
            }
        )
```

### TypeScript Error Handling

```typescript
// Custom error classes
abstract class AppError extends Error {
  abstract readonly code: string;
  abstract readonly statusCode: number;
  readonly details?: Record<string, unknown>;

  constructor(message: string, details?: Record<string, unknown>) {
    super(message);
    this.name = this.constructor.name;
    this.details = details;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        details: this.details,
      },
    };
  }
}

class ValidationError extends AppError {
  readonly code = 'VALIDATION_ERROR';
  readonly statusCode = 400;
}

class NotFoundError extends AppError {
  readonly code = 'NOT_FOUND';
  readonly statusCode = 404;

  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, { resource, id });
  }
}

// Result type for TypeScript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Usage
async function getUser(id: string): Promise<Result<User, AppError>> {
  try {
    const user = await userRepository.findById(id);
    if (!user) {
      return err(new NotFoundError('User', id));
    }
    return ok(user);
  } catch (e) {
    return err(new AppError('Failed to fetch user'));
  }
}

// Handle result
const result = await getUser('123');
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error.message);
}
```

### Error Logging Best Practices

```python
import logging
import structlog
from typing import Any

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Logging errors with context
def log_error(
    error: Exception,
    message: str,
    **context: Any
) -> None:
    logger.error(
        message,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
        exc_info=True
    )

# Usage
try:
    process_payment(order)
except PaymentError as e:
    log_error(
        e,
        "Payment processing failed",
        order_id=order.id,
        amount=order.total,
        payment_method=order.payment_method
    )
    raise
```

## Anti-patterns

- **Swallowing exceptions**: `except: pass`
- **Catching too broadly**: `except Exception` without re-raising
- **Leaking implementation details**: Exposing stack traces to users
- **Inconsistent error formats**: Different structures for different errors
- **Missing error context**: Errors without enough information to debug
- **Not logging errors**: Silent failures
- **Overusing exceptions**: Using exceptions for control flow

## References

- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Error Handling in Node.js](https://nodejs.org/api/errors.html)
- [Effective Error Handling Strategies](https://www.toptal.com/python/python-error-handling-guide)
