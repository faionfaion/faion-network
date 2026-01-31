# REST API Design Templates

Production-ready templates for REST API development.

## OpenAPI Specification Template

```yaml
openapi: 3.1.0
info:
  title: {API_NAME} API
  version: 1.0.0
  description: |
    {API_DESCRIPTION}

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

security:
  - bearerAuth: []

paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    $ref: '#/components/schemas/Pagination'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          headers:
            Location:
              schema:
                type: string
              description: URL of created resource
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '422':
          $ref: '#/components/responses/ValidationError'

  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      summary: Get a user
      operationId: getUser
      tags: [Users]
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      summary: Update a user
      operationId: updateUser
      tags: [Users]
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
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete a user
      operationId: deleteUser
      tags: [Users]
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        status:
          type: string
          enum: [active, inactive]
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
      required: [id, email, name, status]

    CreateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 255
        password:
          type: string
          minLength: 8
      required: [email, name, password]

    UpdateUserRequest:
      type: object
      properties:
        name:
          type: string
        status:
          type: string
          enum: [active, inactive]

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        requestId:
          type: string
      required: [code, message]

    ValidationError:
      allOf:
        - $ref: '#/components/schemas/Error'
        - type: object
          properties:
            errors:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ValidationError'
```

## FastAPI Implementation Template

```python
# app/api/users.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, EmailStr
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    status: str | None = None


class User(UserBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    data: list[User]
    meta: dict


@router.get("", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
):
    """List all users with pagination and filtering."""
    # Implementation
    pass


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, response: Response):
    """Create a new user."""
    # Implementation
    # Set Location header
    response.headers["Location"] = f"/users/{created_user.id}"
    return created_user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    """Get a user by ID."""
    # Implementation
    pass


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: UserUpdate):
    """Update a user."""
    # Implementation
    pass


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID):
    """Delete a user."""
    # Implementation
    pass
```

## Django REST Framework Template

```python
# app/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    filterset_fields = ['status']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Add Location header
        headers['Location'] = f"/users/{serializer.data['id']}"
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
```

## Error Response Template

```python
# app/exceptions.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import uuid


class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "requestId": str(uuid.uuid4()),
        }
    )


# Usage
raise APIError(
    code="USER_NOT_FOUND",
    message="User with specified ID does not exist",
    status_code=404
)
```

---

*REST API Design Templates v1.0*
