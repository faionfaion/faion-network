# M-API-007: Error Handling

## Metadata
- **ID:** M-API-007
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, error-handling, http-status, rfc7807]
- **Agent:** faion-api-agent

---

## Problem

Without consistent error handling:
- Clients can't programmatically handle errors
- Debugging becomes difficult
- Same error returns different formats
- Security issues from verbose error messages
- No way to localize error messages

---

## Framework

### Step 1: Use Correct HTTP Status Codes

**2xx - Success:**

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | GET, PUT, PATCH success |
| 201 | Created | POST created new resource |
| 202 | Accepted | Async operation started |
| 204 | No Content | DELETE success, no body |

**4xx - Client Errors:**

| Code | Meaning | Use Case |
|------|---------|----------|
| 400 | Bad Request | Malformed request, invalid JSON |
| 401 | Unauthorized | Missing or invalid auth |
| 403 | Forbidden | Valid auth, no permission |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | Wrong HTTP method |
| 409 | Conflict | Duplicate, state conflict |
| 410 | Gone | Resource was deleted |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |

**5xx - Server Errors:**

| Code | Meaning | Use Case |
|------|---------|----------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service failed |
| 503 | Service Unavailable | Maintenance, overload |
| 504 | Gateway Timeout | Upstream timeout |

### Step 2: Design Error Response Format

**RFC 7807 Problem Details (Recommended):**

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body contains invalid data.",
  "instance": "/users/123",
  "errors": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "Must be a valid email address"
    },
    {
      "field": "password",
      "code": "TOO_SHORT",
      "message": "Must be at least 8 characters"
    }
  ]
}
```

**Simplified format:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains invalid data.",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

### Step 3: Define Error Codes

**Standard error codes:**

```python
# errors.py
class ErrorCode:
    # Authentication
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"

    # Authorization
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"

    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_FORMAT = "INVALID_FORMAT"
    REQUIRED_FIELD = "REQUIRED_FIELD"
    FIELD_TOO_LONG = "FIELD_TOO_LONG"
    FIELD_TOO_SHORT = "FIELD_TOO_SHORT"

    # Resources
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    CONFLICT = "CONFLICT"
    GONE = "GONE"

    # Rate limiting
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

    # Server
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
```

### Step 4: Implement Error Classes

**Python:**

```python
# exceptions.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class FieldError:
    field: str
    code: str
    message: str

@dataclass
class APIError(Exception):
    code: str
    message: str
    status: int = 400
    details: List[FieldError] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        result = {
            "error": {
                "code": self.code,
                "message": self.message
            }
        }
        if self.details:
            result["error"]["details"] = [
                {"field": d.field, "code": d.code, "message": d.message}
                for d in self.details
            ]
        if self.extra:
            result["error"].update(self.extra)
        return result

class ValidationError(APIError):
    def __init__(self, details: List[FieldError]):
        super().__init__(
            code="VALIDATION_ERROR",
            message="The request contains invalid data",
            status=422,
            details=details
        )

class NotFoundError(APIError):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource} with id '{resource_id}' not found",
            status=404
        )

class UnauthorizedError(APIError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status=401
        )

class ForbiddenError(APIError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status=403
        )

class ConflictError(APIError):
    def __init__(self, message: str):
        super().__init__(
            code="CONFLICT",
            message=message,
            status=409
        )

class RateLimitError(APIError):
    def __init__(self, retry_after: int):
        super().__init__(
            code="RATE_LIMIT_EXCEEDED",
            message="Too many requests",
            status=429,
            extra={"retryAfter": retry_after}
        )
```

**JavaScript:**

```javascript
// errors.js
class APIError extends Error {
  constructor(code, message, status = 400, details = [], extra = {}) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
    this.extra = extra;
  }

  toJSON() {
    const result = {
      error: {
        code: this.code,
        message: this.message,
        ...this.extra
      }
    };

    if (this.details.length > 0) {
      result.error.details = this.details;
    }

    return result;
  }
}

class ValidationError extends APIError {
  constructor(details) {
    super('VALIDATION_ERROR', 'The request contains invalid data', 422, details);
  }
}

class NotFoundError extends APIError {
  constructor(resource, id) {
    super('NOT_FOUND', `${resource} with id '${id}' not found`, 404);
  }
}

class UnauthorizedError extends APIError {
  constructor(message = 'Authentication required') {
    super('UNAUTHORIZED', message, 401);
  }
}

class ForbiddenError extends APIError {
  constructor(message = 'Insufficient permissions') {
    super('FORBIDDEN', message, 403);
  }
}

class ConflictError extends APIError {
  constructor(message) {
    super('CONFLICT', message, 409);
  }
}

class RateLimitError extends APIError {
  constructor(retryAfter) {
    super('RATE_LIMIT_EXCEEDED', 'Too many requests', 429, [], { retryAfter });
  }
}

module.exports = {
  APIError,
  ValidationError,
  NotFoundError,
  UnauthorizedError,
  ForbiddenError,
  ConflictError,
  RateLimitError
};
```

### Step 5: Create Error Handler Middleware

**Django:**

```python
# middleware.py
import logging
import traceback
from django.http import JsonResponse
from .exceptions import APIError

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, APIError):
            return JsonResponse(
                exception.to_dict(),
                status=exception.status
            )

        # Log unexpected errors
        logger.error(
            f"Unexpected error: {exception}",
            exc_info=True,
            extra={
                'request_path': request.path,
                'request_method': request.method,
                'user_id': getattr(request.user, 'id', None)
            }
        )

        # Don't expose internal errors in production
        if settings.DEBUG:
            return JsonResponse({
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(exception),
                    "traceback": traceback.format_exc()
                }
            }, status=500)

        return JsonResponse({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }, status=500)
```

**Express.js:**

```javascript
// errorHandler.js
const { APIError } = require('./errors');

const errorHandler = (err, req, res, next) => {
  // Log all errors
  console.error('Error:', {
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    userId: req.user?.id
  });

  // Handle known API errors
  if (err instanceof APIError) {
    return res.status(err.status).json(err.toJSON());
  }

  // Handle validation errors from express-validator
  if (err.array && typeof err.array === 'function') {
    const details = err.array().map(e => ({
      field: e.path,
      code: 'VALIDATION_ERROR',
      message: e.msg
    }));

    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'The request contains invalid data',
        details
      }
    });
  }

  // Handle Mongoose validation errors
  if (err.name === 'ValidationError') {
    const details = Object.entries(err.errors).map(([field, error]) => ({
      field,
      code: 'VALIDATION_ERROR',
      message: error.message
    }));

    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'The request contains invalid data',
        details
      }
    });
  }

  // Handle JWT errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      error: {
        code: 'INVALID_TOKEN',
        message: 'Invalid authentication token'
      }
    });
  }

  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({
      error: {
        code: 'TOKEN_EXPIRED',
        message: 'Authentication token has expired'
      }
    });
  }

  // Don't expose internal errors in production
  const errorResponse = {
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : err.message
    }
  };

  if (process.env.NODE_ENV !== 'production') {
    errorResponse.error.stack = err.stack;
  }

  res.status(500).json(errorResponse);
};

module.exports = errorHandler;

// app.js
app.use(errorHandler);
```

### Step 6: Validate Input and Return Clear Errors

**Django REST Framework:**

```python
# serializers.py
from rest_framework import serializers
from .exceptions import ValidationError, FieldError

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128)
    name = serializers.CharField(max_length=100, required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

# views.py
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            details = [
                FieldError(
                    field=field,
                    code="VALIDATION_ERROR",
                    message=errors[0] if errors else "Invalid value"
                )
                for field, errors in serializer.errors.items()
            ]
            raise ValidationError(details)

        user = User.objects.create(**serializer.validated_data)
        return Response(UserSerializer(user).data, status=201)
```

**Express.js with express-validator:**

```javascript
// validators.js
const { body, validationResult } = require('express-validator');
const { ValidationError } = require('./errors');

const validateUser = [
  body('email')
    .isEmail()
    .withMessage('Must be a valid email address')
    .normalizeEmail(),

  body('password')
    .isLength({ min: 8 })
    .withMessage('Must be at least 8 characters')
    .matches(/\d/)
    .withMessage('Must contain a number'),

  body('name')
    .optional()
    .isLength({ max: 100 })
    .withMessage('Must not exceed 100 characters')
];

const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    const details = errors.array().map(err => ({
      field: err.path,
      code: 'VALIDATION_ERROR',
      message: err.msg
    }));

    throw new ValidationError(details);
  }

  next();
};

// routes.js
app.post('/users',
  validateUser,
  handleValidationErrors,
  async (req, res) => {
    const user = await User.create(req.body);
    res.status(201).json({ data: user });
  }
);
```

### Step 7: Handle Not Found and Conflicts

```python
# Django
from .exceptions import NotFoundError, ConflictError

class UserViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFoundError("User", pk)

        return Response(UserSerializer(user).data)

    def create(self, request):
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            raise ConflictError(f"User with email '{email}' already exists")

        # Create user...
```

```javascript
// Express.js
const { NotFoundError, ConflictError } = require('./errors');

app.get('/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }

  res.json({ data: user });
});

app.post('/users', async (req, res) => {
  const existing = await User.findOne({ email: req.body.email });

  if (existing) {
    throw new ConflictError(`User with email '${req.body.email}' already exists`);
  }

  const user = await User.create(req.body);
  res.status(201).json({ data: user });
});
```

---

## Templates

### Error Response Schema (OpenAPI)

```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              example: VALIDATION_ERROR
            message:
              type: string
              example: The request contains invalid data
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  code:
                    type: string
                  message:
                    type: string

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: BAD_REQUEST
              message: Invalid JSON in request body

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: VALIDATION_ERROR
              message: The request contains invalid data
              details:
                - field: email
                  code: INVALID_FORMAT
                  message: Must be a valid email address

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: UNAUTHORIZED
              message: Authentication required

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: NOT_FOUND
              message: User with id '123' not found
```

---

## Examples

### Complete Error Response Examples

**Validation Error (422):**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Must be at least 8 characters"
      }
    ]
  }
}
```

**Not Found (404):**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User with id '550e8400-e29b-41d4-a716-446655440000' not found"
  }
}
```

**Unauthorized (401):**

```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token has expired"
  }
}
```

**Rate Limit (429):**

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 45
  }
}
```

---

## Common Mistakes

1. **Generic error messages**
   - Wrong: "Error occurred"
   - Right: "User with email 'test@example.com' already exists"

2. **Wrong status codes**
   - Wrong: 200 with error in body
   - Right: Appropriate 4xx/5xx status

3. **Exposing internal details**
   - Wrong: SQL error message in response
   - Right: Generic message, log details

4. **Inconsistent format**
   - Wrong: Different error structures per endpoint
   - Right: Same format everywhere

5. **Missing field-level errors**
   - Wrong: "Validation failed"
   - Right: List of specific field errors

---

## Next Steps

1. **Define error codes** - Create comprehensive list
2. **Implement error classes** - Reusable exceptions
3. **Add global handler** - Consistent formatting
4. **Document errors** - Include in OpenAPI spec
5. **Log appropriately** - Details for debugging, not in response

---

## Related Methodologies

- [M-API-001: REST API Design](./M-API-001_rest_api_design.md)
- [M-API-004: OpenAPI Specification](./M-API-004_openapi_specification.md)
- [M-API-010: API Monitoring](./M-API-010_api_monitoring.md)

---

*Methodology: Error Handling*
*Version: 1.0*
*Agent: faion-api-agent*
