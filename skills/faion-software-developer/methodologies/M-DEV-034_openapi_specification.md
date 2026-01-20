---
id: M-DEV-034
name: "OpenAPI Specification"
domain: DEV
skill: faion-software-developer
category: "development"
---

# M-DEV-034: OpenAPI Specification

## Overview

OpenAPI (formerly Swagger) is a specification for describing REST APIs. It enables documentation generation, code generation, testing, and API validation. This methodology covers schema design, documentation, and tooling.

## When to Use

- Public APIs requiring documentation
- API-first development
- Generating client SDKs
- Contract-driven development
- API testing and validation

## Key Principles

1. **API-first design** - Define spec before implementation
2. **Complete documentation** - All endpoints documented
3. **Consistent naming** - Follow conventions throughout
4. **Reusable components** - DRY with $ref
5. **Version control** - Spec versioned with code

## Best Practices

### OpenAPI 3.1 Structure

```yaml
# openapi.yaml
openapi: 3.1.0

info:
  title: User Management API
  description: |
    API for managing users and organizations.

    ## Authentication
    All endpoints require Bearer token authentication.

    ## Rate Limiting
    - 100 requests per minute for standard users
    - 1000 requests per minute for premium users

    ## Pagination
    List endpoints support cursor-based pagination with `first` and `after` parameters.
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com
    url: https://api.example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:8000/v1
    description: Local development

tags:
  - name: Users
    description: User management operations
  - name: Organizations
    description: Organization management
  - name: Orders
    description: Order operations

security:
  - bearerAuth: []

paths:
  /users:
    get:
      tags:
        - Users
      summary: List users
      description: Returns a paginated list of users with optional filtering.
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/PageSize'
        - $ref: '#/components/parameters/PageCursor'
        - name: status
          in: query
          description: Filter by user status
          schema:
            type: string
            enum: [active, inactive]
        - name: role
          in: query
          description: Filter by user role
          schema:
            type: array
            items:
              $ref: '#/components/schemas/UserRole'
          style: form
          explode: true
        - name: search
          in: query
          description: Search by name or email
          schema:
            type: string
            minLength: 2
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
              example:
                data:
                  - id: "550e8400-e29b-41d4-a716-446655440000"
                    email: "user@example.com"
                    name: "John Doe"
                    role: member
                    isActive: true
                    createdAt: "2024-01-15T10:30:00Z"
                meta:
                  total: 100
                  pageSize: 20
                  hasNextPage: true
                  endCursor: "cursor123"
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/TooManyRequests'

    post:
      tags:
        - Users
      summary: Create user
      description: Creates a new user in the system.
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            examples:
              basic:
                summary: Basic user
                value:
                  email: "newuser@example.com"
                  name: "Jane Doe"
              admin:
                summary: Admin user
                value:
                  email: "admin@example.com"
                  name: "Admin User"
                  role: admin
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
          headers:
            Location:
              description: URL of created resource
              schema:
                type: string
                format: uri
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'
        '422':
          $ref: '#/components/responses/ValidationError'

  /users/{userId}:
    parameters:
      - $ref: '#/components/parameters/UserId'

    get:
      tags:
        - Users
      summary: Get user
      description: Returns a single user by ID.
      operationId: getUser
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      tags:
        - Users
      summary: Update user
      description: Partially updates a user.
      operationId: updateUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '404':
          $ref: '#/components/responses/NotFound'
        '422':
          $ref: '#/components/responses/ValidationError'

    delete:
      tags:
        - Users
      summary: Delete user
      description: Soft deletes a user.
      operationId: deleteUser
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'

  /users/{userId}/orders:
    parameters:
      - $ref: '#/components/parameters/UserId'

    get:
      tags:
        - Users
        - Orders
      summary: Get user's orders
      description: Returns orders for a specific user.
      operationId: getUserOrders
      parameters:
        - $ref: '#/components/parameters/PageSize'
        - $ref: '#/components/parameters/PageCursor'
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/OrderStatus'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT access token

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for service-to-service communication

  parameters:
    UserId:
      name: userId
      in: path
      required: true
      description: User unique identifier
      schema:
        type: string
        format: uuid
      example: "550e8400-e29b-41d4-a716-446655440000"

    PageSize:
      name: first
      in: query
      description: Number of items to return
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    PageCursor:
      name: after
      in: query
      description: Cursor for pagination
      schema:
        type: string

  schemas:
    # Enums
    UserRole:
      type: string
      enum: [admin, moderator, member]
      description: User role in the system

    OrderStatus:
      type: string
      enum: [draft, placed, paid, shipped, delivered, cancelled]

    # Base schemas
    BaseEntity:
      type: object
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true
      required:
        - id
        - createdAt
        - updatedAt

    # User schemas
    User:
      allOf:
        - $ref: '#/components/schemas/BaseEntity'
        - type: object
          properties:
            email:
              type: string
              format: email
            name:
              type: string
              minLength: 1
              maxLength: 100
            role:
              $ref: '#/components/schemas/UserRole'
            isActive:
              type: boolean
          required:
            - email
            - name
            - role
            - isActive

    CreateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
          description: User's email address
        name:
          type: string
          minLength: 2
          maxLength: 100
          description: User's full name
        role:
          $ref: '#/components/schemas/UserRole'
          default: member
        organizationId:
          type: string
          format: uuid
          description: Organization to assign user to
      required:
        - email
        - name
        - organizationId

    UpdateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 2
          maxLength: 100
        role:
          $ref: '#/components/schemas/UserRole'
      minProperties: 1

    UserResponse:
      type: object
      properties:
        data:
          $ref: '#/components/schemas/User'
        links:
          $ref: '#/components/schemas/ResourceLinks'

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'
        links:
          $ref: '#/components/schemas/PaginationLinks'

    # Common schemas
    PaginationMeta:
      type: object
      properties:
        total:
          type: integer
        pageSize:
          type: integer
        hasNextPage:
          type: boolean
        hasPreviousPage:
          type: boolean
        startCursor:
          type: string
          nullable: true
        endCursor:
          type: string
          nullable: true

    PaginationLinks:
      type: object
      properties:
        self:
          type: string
          format: uri
        first:
          type: string
          format: uri
        last:
          type: string
          format: uri
        next:
          type: string
          format: uri
          nullable: true
        prev:
          type: string
          format: uri
          nullable: true

    ResourceLinks:
      type: object
      properties:
        self:
          type: string
          format: uri
      additionalProperties:
        type: string
        format: uri

    # Error schemas
    Error:
      type: object
      properties:
        code:
          type: string
          description: Error code
        message:
          type: string
          description: Human-readable error message
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'
        requestId:
          type: string
          description: Request ID for tracking
      required:
        - code
        - message

    ErrorDetail:
      type: object
      properties:
        field:
          type: string
        message:
          type: string
      required:
        - message

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: BAD_REQUEST
            message: Invalid request body
            requestId: "abc-123"

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required
            requestId: "abc-123"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: Resource not found
            requestId: "abc-123"

    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: CONFLICT
            message: User with this email already exists
            requestId: "abc-123"

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VALIDATION_ERROR
            message: Request validation failed
            details:
              - field: email
                message: Invalid email format
              - field: name
                message: Name is required
            requestId: "abc-123"

    TooManyRequests:
      description: Rate limit exceeded
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: RATE_LIMIT_EXCEEDED
            message: Too many requests
            requestId: "abc-123"
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
          description: Rate limit ceiling
        X-RateLimit-Remaining:
          schema:
            type: integer
          description: Remaining requests
        X-RateLimit-Reset:
          schema:
            type: integer
          description: Reset timestamp
```

### Code Generation

```bash
# Generate Python client
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o ./clients/python \
  --additional-properties=packageName=myapi_client

# Generate TypeScript client
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./clients/typescript

# Generate server stub (FastAPI)
openapi-generator generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server

# Validate spec
openapi-generator validate -i openapi.yaml

# Using spectral for linting
spectral lint openapi.yaml
```

### FastAPI Integration

```python
# Generate OpenAPI from FastAPI
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="User Management API",
    description="API for managing users",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "User operations"},
        {"name": "Orders", "description": "Order operations"},
    ],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Add global security
    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Endpoint with documentation
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID


class CreateUserRequest(BaseModel):
    """Request body for creating a user."""

    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's full name",
    )
    role: Optional[str] = Field(
        "member",
        description="User's role",
        json_schema_extra={"enum": ["admin", "moderator", "member"]},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "role": "member",
            }
        }


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create user",
    description="Creates a new user in the system.",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "email": "user@example.com",
                            "name": "John Doe",
                        }
                    }
                }
            },
        },
        409: {"description": "User with email already exists"},
        422: {"description": "Validation error"},
    },
    tags=["Users"],
)
async def create_user(request: CreateUserRequest):
    """
    Create a new user.

    - **email**: Valid email address (must be unique)
    - **name**: User's full name (2-100 characters)
    - **role**: User's role (default: member)
    """
    ...
```

### API Versioning

```yaml
# Multiple versions in single spec
openapi: 3.1.0
info:
  title: API with Versioning
  version: 2.0.0

paths:
  # V1 endpoints
  /v1/users:
    get:
      deprecated: true
      summary: List users (deprecated)
      description: Use /v2/users instead

  # V2 endpoints
  /v2/users:
    get:
      summary: List users
      description: Returns paginated list with cursor-based pagination
```

## Anti-patterns

### Avoid: Inconsistent Naming

```yaml
# BAD - inconsistent naming
paths:
  /users:
    get: ...
  /get-orders: ...
  /Products: ...

# GOOD - consistent naming
paths:
  /users:
    get: ...
  /orders:
    get: ...
  /products:
    get: ...
```

### Avoid: Missing Examples

```yaml
# BAD - no examples
schemas:
  User:
    type: object
    properties:
      id:
        type: string

# GOOD - with examples
schemas:
  User:
    type: object
    properties:
      id:
        type: string
        format: uuid
        example: "550e8400-e29b-41d4-a716-446655440000"
```

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Spectral Linter](https://stoplight.io/open-source/spectral)
- [Swagger Editor](https://editor.swagger.io/)
