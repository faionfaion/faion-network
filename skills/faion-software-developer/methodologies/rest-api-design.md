---
id: rest-api-design
name: "API Design (REST)"
domain: DEV
skill: faion-software-developer
category: "development"
---

# API Design (REST)

## Overview

REST (Representational State Transfer) is an architectural style for designing networked applications. This methodology covers resource-oriented design, HTTP semantics, and best practices for building scalable REST APIs.

## When to Use

- Public APIs for external consumers
- CRUD-heavy applications
- Systems requiring cacheability
- APIs that should be discoverable
- Integration between services

## Key Principles

1. **Resource-oriented** - Everything is a resource with a unique URI
2. **Stateless** - Each request contains all needed information
3. **Uniform interface** - Standard HTTP methods and status codes
4. **HATEOAS** - Hypermedia as the Engine of Application State
5. **Layered system** - Client cannot tell if connected directly to server

## Best Practices

### URL Design

```
# Resources as nouns (plural)
GET    /users                 # List users
POST   /users                 # Create user
GET    /users/{id}           # Get user
PUT    /users/{id}           # Replace user
PATCH  /users/{id}           # Update user
DELETE /users/{id}           # Delete user

# Nested resources (relationships)
GET    /users/{id}/orders    # Get user's orders
POST   /users/{id}/orders    # Create order for user
GET    /orders/{id}/items    # Get order items

# Filtering, sorting, pagination
GET /users?status=active&role=admin
GET /users?sort=-created_at
GET /users?page=2&per_page=20
GET /users?limit=20&offset=40

# Search
GET /users?q=john
GET /products/search?name=phone&min_price=100

# Actions (when CRUD doesn't fit)
POST /orders/{id}/cancel
POST /users/{id}/verify-email
POST /payments/{id}/refund

# Versioning in URL
GET /api/v1/users
GET /api/v2/users
```

### HTTP Methods and Status Codes

```python
# HTTP Methods
GET     # Read resource (idempotent, safe)
POST    # Create resource
PUT     # Replace resource (idempotent)
PATCH   # Partial update (idempotent)
DELETE  # Remove resource (idempotent)
HEAD    # Get headers only
OPTIONS # Get allowed methods

# Success Codes
200 OK            # Request succeeded
201 Created       # Resource created
204 No Content    # Success, no body (DELETE, PUT)
206 Partial       # Partial response (pagination)

# Client Error Codes
400 Bad Request      # Malformed request
401 Unauthorized     # Authentication required
403 Forbidden        # Authenticated but not authorized
404 Not Found        # Resource doesn't exist
405 Method Not Allowed
409 Conflict         # Resource conflict (duplicate)
422 Unprocessable    # Validation failed
429 Too Many Requests

# Server Error Codes
500 Internal Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

### Request/Response Design

```python
# FastAPI implementation
from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

app = FastAPI()


# Request schemas
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: Optional[str] = "member"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "role": "member",
            }
        }


class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)


# Response schemas
class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # HATEOAS links
    links: dict = {}

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    data: List[UserResponse]
    meta: dict
    links: dict


# Endpoints
@app.get("/api/v1/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    sort: str = Query("-created_at", description="Sort field"),
):
    """List all users with pagination."""
    users, total = await user_service.list(
        page=page,
        per_page=per_page,
        status=status,
        sort=sort,
    )

    return PaginatedResponse(
        data=[UserResponse.from_orm(u) for u in users],
        meta={
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
        },
        links={
            "self": f"/api/v1/users?page={page}&per_page={per_page}",
            "first": f"/api/v1/users?page=1&per_page={per_page}",
            "last": f"/api/v1/users?page={total // per_page + 1}&per_page={per_page}",
            "next": f"/api/v1/users?page={page + 1}&per_page={per_page}" if page * per_page < total else None,
            "prev": f"/api/v1/users?page={page - 1}&per_page={per_page}" if page > 1 else None,
        },
    )


@app.post(
    "/api/v1/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(request: CreateUserRequest):
    """Create a new user."""
    user = await user_service.create(
        email=request.email,
        name=request.name,
        role=request.role,
    )

    response = UserResponse.from_orm(user)
    response.links = {
        "self": f"/api/v1/users/{user.id}",
        "orders": f"/api/v1/users/{user.id}/orders",
    }

    return response


@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID = Path(..., description="User ID"),
):
    """Get user by ID."""
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "USER_NOT_FOUND",
                "message": f"User with id {user_id} not found",
            },
        )

    response = UserResponse.from_orm(user)
    response.links = {
        "self": f"/api/v1/users/{user_id}",
        "orders": f"/api/v1/users/{user_id}/orders",
        "collection": "/api/v1/users",
    }

    return response


@app.patch("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
):
    """Partially update a user."""
    update_data = request.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    user = await user_service.update(user_id, update_data)
    return UserResponse.from_orm(user)


@app.delete(
    "/api/v1/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: UUID):
    """Delete a user."""
    await user_service.delete(user_id)
    return None
```

### Error Handling

```python
# Standardized error response format
from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = None


# Exception handlers
from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=[
                ErrorDetail(field=err["loc"][-1], message=err["msg"])
                for err in exc.errors()
            ],
            request_id=request.state.request_id,
        ).model_dump(),
    )


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            code="NOT_FOUND",
            message=str(exc),
            request_id=request.state.request_id,
        ).model_dump(),
    )


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content=ErrorResponse(
            code="CONFLICT",
            message=str(exc),
            request_id=request.state.request_id,
        ).model_dump(),
    )


# Example error responses
"""
400 Bad Request:
{
    "code": "BAD_REQUEST",
    "message": "Invalid JSON in request body",
    "request_id": "abc123"
}

422 Unprocessable Entity:
{
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
        {"field": "email", "message": "Invalid email format"},
        {"field": "name", "message": "Field is required"}
    ],
    "request_id": "abc123"
}

409 Conflict:
{
    "code": "CONFLICT",
    "message": "User with email user@example.com already exists",
    "request_id": "abc123"
}
"""
```

### Filtering and Search

```python
from typing import Optional, List
from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class UserFilter(BaseModel):
    status: Optional[str] = None
    role: Optional[List[str]] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    search: Optional[str] = None


@app.get("/api/v1/users")
async def list_users(
    # Pagination
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),

    # Filtering
    status: Optional[str] = Query(None),
    role: Optional[List[str]] = Query(None),
    created_after: Optional[datetime] = Query(None),
    created_before: Optional[datetime] = Query(None),

    # Search
    q: Optional[str] = Query(None, min_length=2),

    # Sorting
    sort: str = Query("created_at"),
    order: SortOrder = Query(SortOrder.DESC),

    # Field selection
    fields: Optional[List[str]] = Query(None),
):
    """
    List users with filtering, sorting, and pagination.

    Filters:
    - status: Filter by user status (active, inactive)
    - role: Filter by roles (can specify multiple)
    - created_after/before: Date range filter

    Sorting:
    - sort: Field to sort by (created_at, name, email)
    - order: Sort order (asc, desc)

    Field selection:
    - fields: Comma-separated list of fields to include
    """
    filters = UserFilter(
        status=status,
        role=role,
        created_after=created_after,
        created_before=created_before,
        search=q,
    )

    users, total = await user_service.list(
        filters=filters,
        page=page,
        per_page=per_page,
        sort_by=sort,
        sort_order=order.value,
    )

    # Field selection
    if fields:
        users = [
            {k: v for k, v in user.dict().items() if k in fields}
            for user in users
        ]

    return {"data": users, "meta": {"total": total}}
```

### Caching

```python
from fastapi import Response
from datetime import datetime


@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: UUID, response: Response):
    user = await user_service.get(user_id)

    # Set cache headers
    response.headers["Cache-Control"] = "private, max-age=60"
    response.headers["ETag"] = f'"{user.updated_at.timestamp()}"'
    response.headers["Last-Modified"] = user.updated_at.strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    return user


# Conditional requests
from fastapi import Header


@app.get("/api/v1/users/{user_id}")
async def get_user(
    user_id: UUID,
    response: Response,
    if_none_match: Optional[str] = Header(None),
    if_modified_since: Optional[str] = Header(None),
):
    user = await user_service.get(user_id)
    etag = f'"{user.updated_at.timestamp()}"'

    # Check ETag
    if if_none_match and if_none_match == etag:
        return Response(status_code=304)

    # Check Last-Modified
    if if_modified_since:
        modified_since = datetime.strptime(
            if_modified_since, "%a, %d %b %Y %H:%M:%S GMT"
        )
        if user.updated_at <= modified_since:
            return Response(status_code=304)

    response.headers["ETag"] = etag
    return user
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/api/v1/users")
@limiter.limit("100/minute")
async def list_users(request: Request):
    ...


@app.post("/api/v1/users")
@limiter.limit("10/minute")
async def create_user(request: Request):
    ...


# Add rate limit headers
@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    response = await call_next(request)

    # Add standard rate limit headers
    response.headers["X-RateLimit-Limit"] = "100"
    response.headers["X-RateLimit-Remaining"] = "99"
    response.headers["X-RateLimit-Reset"] = "1640000000"

    return response
```

## Anti-patterns

### Avoid: Verbs in URLs

```
# BAD
GET  /getUsers
POST /createUser
POST /deleteUser/123

# GOOD
GET    /users
POST   /users
DELETE /users/123
```

### Avoid: Ignoring HTTP Semantics

```python
# BAD - using POST for everything
POST /api/users/get
POST /api/users/delete

# GOOD - use appropriate methods
GET    /api/users
DELETE /api/users/{id}
```

### Avoid: Exposing Internal IDs

```python
# BAD - exposes auto-increment ID
GET /api/users/1234567

# GOOD - use UUIDs
GET /api/users/550e8400-e29b-41d4-a716-446655440000
```

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [JSON:API Specification](https://jsonapi.org/)
- [HTTP Status Codes](https://httpstatuses.com/)
