# purpose: Pydantic v2 schema hierarchy template — Base/Create/Update/Response.
# consumes: domain field list.
# produces: 4 schema classes per entity; Response has from_attributes=True.
# depends-on: pydantic>=2.
# token-budget-impact: ~40 lines per entity.
"""
Pydantic v2 schema hierarchy for User resource.
Copy and adapt for other resources: rename User → YourResource.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Request schema for user creation. Includes password (not in response)."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Request schema for partial update (PATCH). All fields optional."""
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """Response schema. Excludes password. from_attributes for ORM serialization."""
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    """Paginated user list response."""
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
