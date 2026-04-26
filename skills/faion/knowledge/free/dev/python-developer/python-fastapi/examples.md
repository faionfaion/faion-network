# FastAPI Examples

Complete, production-ready examples for common FastAPI patterns.

## Complete CRUD API

### Main Application

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.engine import async_engine
from app.models.base import Base
from app.routers import users, items

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: create tables (dev only, use Alembic in prod)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose engine
    await async_engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Configuration

```python
# app/config.py
from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "FastAPI App"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost/db"
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # Auth
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Database Engine

```python
# app/db/engine.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

async_engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    echo=settings.debug,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

### Base Model

```python
# app/models/base.py
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
```

### User Model

```python
# app/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin

class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
```

### Schemas

```python
# app/schemas/base.py
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

# app/schemas/users.py
from datetime import datetime
from uuid import UUID
from pydantic import EmailStr, Field, field_validator

from app.schemas.base import BaseSchema

class UserCreate(BaseSchema):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

class UserUpdate(BaseSchema):
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=100)

class UserResponse(BaseSchema):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

class UserListResponse(BaseSchema):
    items: list[UserResponse]
    total: int
    page: int
    size: int

    @property
    def pages(self) -> int:
        return (self.total + self.size - 1) // self.size
```

### Dependencies

```python
# app/dependencies.py
from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.config import settings
from app.db.engine import async_session
from app.models.user import User
from app.services import users as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

# Type aliases
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
```

### Service Layer

```python
# app/services/users.py
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_by_id(db: AsyncSession, user_id: UUID | str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_list(
    db: AsyncSession,
    *,
    page: int = 1,
    size: int = 20,
) -> tuple[list[User], int]:
    # Count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar_one()

    # Fetch
    offset = (page - 1) * size
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    users = list(result.scalars().all())

    return users, total

async def create(db: AsyncSession, data: UserCreate) -> User:
    user = User(
        email=data.email,
        name=data.name,
        hashed_password=pwd_context.hash(data.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def update(
    db: AsyncSession,
    user_id: UUID,
    data: UserUpdate,
) -> User | None:
    user = await get_by_id(db, user_id)
    if not user:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return user

async def delete(db: AsyncSession, user_id: UUID) -> bool:
    user = await get_by_id(db, user_id)
    if not user:
        return False
    await db.delete(user)
    return True
```

### Router

```python
# app/routers/users.py
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import DBSession, CurrentUser
from app.schemas.users import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.services import users as user_service

router = APIRouter()

@router.get("", response_model=UserListResponse)
async def list_users(
    db: DBSession,
    _: CurrentUser,  # Require auth
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """List users with pagination."""
    users, total = await user_service.get_list(db, page=page, size=size)
    return UserListResponse(items=users, total=total, page=page, size=size)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: DBSession, data: UserCreate):
    """Create a new user."""
    existing = await user_service.get_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    return await user_service.create(db, data)

@router.get("/me", response_model=UserResponse)
async def get_current_user(user: CurrentUser):
    """Get current authenticated user."""
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(db: DBSession, _: CurrentUser, user_id: UUID):
    """Get user by ID."""
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    db: DBSession,
    current_user: CurrentUser,
    user_id: UUID,
    data: UserUpdate,
):
    """Update user fields."""
    # Only allow self-update or admin
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    user = await user_service.update(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: DBSession, current_user: CurrentUser, user_id: UUID):
    """Delete user."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if not await user_service.delete(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
```

## Authentication Example

```python
# app/routers/auth.py
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel

from app.config import settings
from app.dependencies import DBSession
from app.services import users as user_service
from app.services.users import pwd_context

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

@router.post("/token", response_model=Token)
async def login(
    db: DBSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token login."""
    user = await user_service.get_by_email(db, form_data.username)

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    access_token = create_access_token(str(user.id))
    return Token(access_token=access_token)
```

## Testing Example

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.models.base import Base
from app.dependencies import get_db

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL)
test_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)

@pytest.fixture(scope="function")
async def db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()

# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "Password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "Password123",
    }
    await client.post("/api/v1/users", json=user_data)
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 409
```

## Background Tasks Example

```python
# app/tasks/email.py
import httpx
from app.config import settings

async def send_email(to: str, subject: str, body: str):
    """Send email via external service."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.email_service_url}/send",
            json={"to": to, "subject": subject, "body": body},
        )

# app/routers/orders.py
from fastapi import BackgroundTasks

@router.post("", response_model=OrderResponse)
async def create_order(
    db: DBSession,
    user: CurrentUser,
    data: OrderCreate,
    background_tasks: BackgroundTasks,
):
    order = await order_service.create(db, user.id, data)

    # Send confirmation in background
    background_tasks.add_task(
        send_email,
        to=user.email,
        subject="Order Confirmation",
        body=f"Your order {order.id} has been placed.",
    )

    return order
```

## WebSocket Example

```python
# app/routers/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import list

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```
