# M-PY-003: FastAPI Patterns

## Metadata
- **Category:** Development/Python
- **Difficulty:** Intermediate
- **Tags:** #dev, #python, #fastapi, #methodology
- **Agent:** faion-code-agent

---

## Problem

FastAPI is fast and modern, but its flexibility can lead to inconsistent code. Without patterns, projects become a mess of scattered endpoints and duplicate logic. You need structure.

## Promise

After this methodology, you will build FastAPI applications with clean architecture, proper dependency injection, and maintainable code structure.

## Overview

FastAPI patterns leverage Python type hints, Pydantic models, and dependency injection for clean, documented APIs.

---

## Framework

### Step 1: Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # Settings
│   ├── dependencies.py      # Shared dependencies
│   ├── database.py          # Database connection
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # API dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # Main router
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── products.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # Auth helpers
│   │   └── exceptions.py    # Custom exceptions
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── user.py
│   └── repositories/        # Database access
│       ├── __init__.py
│       └── user.py
├── tests/
├── alembic/                 # Migrations
├── pyproject.toml
└── Dockerfile
```

### Step 2: Application Setup

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1.router import api_router
from app.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # await database.connect()
    yield
    # Shutdown
    # await database.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
```

### Step 3: Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "My API"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Step 4: Pydantic Schemas

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

# Base schema - shared fields
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

# Create schema - for POST requests
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Update schema - for PATCH requests
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)

# Response schema - for API responses
class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode

# Internal schema - with sensitive data
class UserInDB(UserResponse):
    hashed_password: str
```

### Step 5: SQLAlchemy Models

```python
# app/models/base.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

# app/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
```

### Step 6: Repository Pattern

```python
# app/repositories/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate, hashed_password: str) -> User:
        user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
```

### Step 7: Service Layer

```python
# app/services/user.py
from uuid import UUID
from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user(self, user_id: UUID) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)

    async def create_user(self, user_in: UserCreate) -> UserResponse:
        existing = await self.repository.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_in.password)
        user = await self.repository.create(user_in, hashed_password)
        return UserResponse.model_validate(user)

    async def authenticate(self, email: str, password: str) -> UserResponse | None:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return UserResponse.model_validate(user)
```

### Step 8: Dependency Injection

```python
# app/api/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.database import get_session
from app.config import settings
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserRepository:
    return UserRepository(session)

async def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(repository)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await service.get_user(user_id)
    return user

# Type aliases for cleaner endpoints
CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

### Step 9: Endpoints

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, status
from uuid import UUID

from app.api.deps import CurrentUser, UserServiceDep
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserServiceDep,
):
    """Create new user."""
    return await service.create_user(user_in)

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUser):
    """Get current user."""
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
    current_user: CurrentUser,
):
    """Get user by ID."""
    return await service.get_user(user_id)
```

---

## Templates

### Database Setup

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### Exception Handlers

```python
# app/core/exceptions.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# In main.py
app.add_exception_handler(AppException, app_exception_handler)
```

---

## Examples

### Background Tasks

```python
from fastapi import BackgroundTasks

async def send_email(email: str, message: str):
    # Send email logic
    pass

@router.post("/notify")
async def notify_user(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification scheduled"}
```

### File Upload

```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

---

## Common Mistakes

1. **Sync database calls** - Always use async SQLAlchemy
2. **Missing response_model** - Always specify for automatic validation
3. **Business logic in endpoints** - Move to service layer
4. **No dependency injection** - Use Depends for testability
5. **Missing error handling** - Add custom exception handlers

---

## Checklist

- [ ] Project structure follows pattern
- [ ] Pydantic schemas for all I/O
- [ ] Repository pattern for database
- [ ] Service layer for business logic
- [ ] Dependency injection configured
- [ ] Authentication middleware
- [ ] Exception handlers added
- [ ] CORS configured

---

## Next Steps

- M-PY-004: Pytest Testing
- M-PY-005: Asyncio Patterns
- M-API-001: REST API Design

---

*Methodology M-PY-003 v1.0*
