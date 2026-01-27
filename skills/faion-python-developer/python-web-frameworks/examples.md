# Python Web Frameworks - Examples

**Real-world usage examples for Django, FastAPI, and Flask.**

---

## Django Examples

### 1. Basic Project Setup

```bash
# Create project
django-admin startproject config .

# Create app
python manage.py startapp users

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

### 2. Model with Service Layer

```python
# apps/users/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.TextChoices):
    REGULAR = 'regular', 'Regular User'
    PREMIUM = 'premium', 'Premium User'
    ADMIN = 'admin', 'Administrator'


class User(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.REGULAR,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email
```

```python
# apps/users/services.py
from django.db import transaction
from .models import User, UserType


def create_user(
    email: str,
    name: str,
    *,
    user_type: str = UserType.REGULAR,
) -> User:
    """Create a new user."""
    return User.objects.create(
        email=email,
        name=name,
        user_type=user_type,
    )


def upgrade_to_premium(user: User) -> User:
    """Upgrade user to premium."""
    user.user_type = UserType.PREMIUM
    user.save(update_fields=['user_type', 'updated_at'])
    return user


@transaction.atomic
def transfer_ownership(from_user: User, to_user: User, item_id: int) -> None:
    """Transfer item ownership between users."""
    from apps.items import models as item_models

    item = item_models.Item.objects.select_for_update().get(id=item_id)
    item.owner = to_user
    item.save(update_fields=['owner', 'updated_at'])
```

---

### 3. REST API with Django REST Framework

```python
# apps/users/serializers.py
from rest_framework import serializers
from .models import User


class CreateUserRequest(serializers.Serializer):
    """Request serializer for user creation."""
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)


class UserResponse(serializers.ModelSerializer):
    """Response serializer for user data."""
    class Meta:
        model = User
        fields = ['uid', 'email', 'name', 'user_type', 'created_at']
        read_only_fields = fields
```

```python
# apps/users/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import services
from .serializers import CreateUserRequest, UserResponse


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = services.create_user(
            email=serializer.validated_data['email'],
            name=serializer.validated_data['name'],
        )

        return Response(
            UserResponse(user).data,
            status=status.HTTP_201_CREATED,
        )


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_active=True)
        return Response(UserResponse(users, many=True).data)
```

---

### 4. Admin Configuration

```python
# apps/users/admin.py
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'user_type', 'is_active', 'created_at']
    list_filter = ['user_type', 'is_active', 'created_at']
    search_fields = ['email', 'name']
    readonly_fields = ['uid', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = [
        (None, {'fields': ['email', 'name']}),
        ('Status', {'fields': ['user_type', 'is_active']}),
        ('Metadata', {'fields': ['uid', 'created_at', 'updated_at']}),
    ]
```

---

### 5. Async View (Django 5.x)

```python
# apps/products/views.py
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import Product


async def product_list(request):
    """Async view for listing products."""
    # Option 1: sync_to_async wrapper
    products = await sync_to_async(list)(
        Product.objects.filter(is_active=True).values('id', 'name', 'price')
    )

    return JsonResponse({'products': products})


async def product_detail(request, pk):
    """Async view with async ORM methods (Django 4.1+)."""
    # Option 2: Async ORM methods (a-prefix)
    try:
        product = await Product.objects.aget(pk=pk)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
```

---

### 6. Django Channels WebSocket

```python
# apps/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
```

```python
# apps/chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
```

---

### 7. Testing with pytest-django

```python
# apps/users/tests/test_services.py
import pytest
from apps.users import services
from apps.users.models import User, UserType


@pytest.fixture
def user(db):
    return services.create_user(
        email='test@example.com',
        name='Test User',
    )


class TestUserServices:
    def test_create_user(self, db):
        user = services.create_user(
            email='new@example.com',
            name='New User',
        )

        assert user.email == 'new@example.com'
        assert user.name == 'New User'
        assert user.user_type == UserType.REGULAR

    def test_upgrade_to_premium(self, user):
        services.upgrade_to_premium(user)

        user.refresh_from_db()
        assert user.user_type == UserType.PREMIUM
```

```python
# apps/users/tests/test_views.py
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


class TestUserViews:
    def test_create_user_requires_auth(self, api_client):
        response = api_client.post('/api/users/', {
            'email': 'new@example.com',
            'name': 'New User',
        })
        assert response.status_code == 401

    def test_create_user_success(self, authenticated_client):
        response = authenticated_client.post('/api/users/', {
            'email': 'new@example.com',
            'name': 'New User',
        })
        assert response.status_code == 201
        assert response.data['email'] == 'new@example.com'
```

---

## FastAPI Examples

### 1. Basic Application Setup

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import users, items
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    await init_db()
    yield


app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API documentation",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

### 2. Pydantic Schemas

```python
# app/schemas/users.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """User creation request."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update request - all fields optional."""
    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Paginated user list response."""
    items: list[UserResponse]
    total: int
    page: int
    size: int
```

---

### 3. Routes with Dependency Injection

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.schemas.users import UserCreate, UserResponse, UserListResponse
from app.services import users as user_service
from app.models.users import User

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new user."""
    existing = await user_service.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = await user_service.create_user(db, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List users with pagination."""
    users, total = await user_service.list_users(db, page=page, size=size)
    return UserListResponse(
        items=users,
        total=total,
        page=page,
        size=size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get user by ID."""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
```

---

### 4. Dependencies

```python
# app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.models.users import User
from app.services import auth as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_db():
    """Database session dependency."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current authenticated user."""
    user = await auth_service.get_user_from_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


# Type aliases for cleaner signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
```

---

### 5. Async Service Layer

```python
# app/services/users.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.users import UserCreate
from app.core.security import hash_password


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user."""
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Get user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def list_users(
    db: AsyncSession,
    page: int = 1,
    size: int = 20,
) -> tuple[list[User], int]:
    """List users with pagination."""
    # Get total count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar()

    # Get paginated results
    offset = (page - 1) * size
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    users = list(result.scalars().all())

    return users, total
```

---

### 6. WebSocket Implementation

```python
# app/routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = set()
        self.active_connections[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].discard(websocket)

    async def broadcast(self, room: str, message: dict):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                try:
                    await connection.send_json(message)
                except:
                    pass


manager = ConnectionManager()


@router.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.broadcast(room, {
                "type": "message",
                "data": message,
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(room, {
            "type": "disconnect",
            "data": {"message": "User disconnected"},
        })
```

---

### 7. Background Tasks

```python
# app/routers/notifications.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr

router = APIRouter()


class NotificationRequest(BaseModel):
    email: EmailStr
    message: str


def send_email(email: str, message: str) -> None:
    """Send email in background (sync function)."""
    # Simulate email sending
    import time
    time.sleep(2)
    print(f"Email sent to {email}: {message}")


async def send_push_notification(user_id: int, message: str) -> None:
    """Send push notification (async function)."""
    import asyncio
    await asyncio.sleep(1)
    print(f"Push sent to user {user_id}: {message}")


@router.post("/email")
async def send_email_notification(
    notification: NotificationRequest,
    background_tasks: BackgroundTasks,
):
    """Queue email notification."""
    background_tasks.add_task(
        send_email,
        notification.email,
        notification.message,
    )
    return {"status": "queued", "type": "email"}


@router.post("/push/{user_id}")
async def send_push(
    user_id: int,
    message: str,
    background_tasks: BackgroundTasks,
):
    """Queue push notification."""
    background_tasks.add_task(
        send_push_notification,
        user_id,
        message,
    )
    return {"status": "queued", "type": "push"}
```

---

### 8. Testing with pytest

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/api/v1/users/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

---

## Flask Examples

### 1. Application Factory Pattern

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)

    # Load config
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.users import bp as users_bp
    from app.items import bp as items_bp

    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(items_bp, url_prefix='/api/items')

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}

    return app
```

```python
# config.py
import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

---

### 2. Blueprint with Views

```python
# app/users/__init__.py
from flask import Blueprint

bp = Blueprint('users', __name__)

from app.users import views  # noqa
```

```python
# app/users/views.py
from flask import jsonify, request
from app.users import bp
from app.users import services
from app.users.schemas import UserSchema, CreateUserSchema
from app.auth import login_required


@bp.route('/', methods=['GET'])
@login_required
def list_users():
    """List all users."""
    users = services.get_all_users()
    return jsonify(UserSchema(many=True).dump(users))


@bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get user by ID."""
    user = services.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(UserSchema().dump(user))


@bp.route('/', methods=['POST'])
@login_required
def create_user():
    """Create a new user."""
    schema = CreateUserSchema()
    errors = schema.validate(request.json)
    if errors:
        return jsonify({'errors': errors}), 400

    data = schema.load(request.json)
    user = services.create_user(**data)
    return jsonify(UserSchema().dump(user)), 201
```

---

### 3. Models

```python
# app/users/models.py
from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f'<User {self.email}>'
```

---

### 4. Marshmallow Schemas

```python
# app/users/schemas.py
from marshmallow import Schema, fields, validate, post_load


class UserSchema(Schema):
    """User response schema."""
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class CreateUserSchema(Schema):
    """User creation schema."""
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
```

---

### 5. Service Layer

```python
# app/users/services.py
from app import db
from app.users.models import User
from werkzeug.security import generate_password_hash


def get_all_users():
    """Get all active users."""
    return User.query.filter_by(is_active=True).order_by(User.created_at.desc()).all()


def get_user_by_id(user_id):
    """Get user by ID."""
    return User.query.get(user_id)


def get_user_by_email(email):
    """Get user by email."""
    return User.query.filter_by(email=email).first()


def create_user(email, name, password):
    """Create a new user."""
    user = User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, **kwargs):
    """Update user attributes."""
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.session.commit()
    return user
```

---

### 6. Authentication Decorator

```python
# app/auth.py
from functools import wraps
from flask import request, jsonify, g
import jwt
from app.users import services


def login_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
            )
            g.current_user = services.get_user_by_id(payload['user_id'])
            if not g.current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function
```

---

### 7. Error Handlers

```python
# app/errors.py
from flask import jsonify


def register_error_handlers(app):
    """Register application error handlers."""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
```

---

### 8. Testing

```python
# tests/conftest.py
import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app, client):
    """Create user and return auth headers."""
    from app.users import services

    with app.app_context():
        user = services.create_user(
            email='test@example.com',
            name='Test User',
            password='password123',
        )
        token = create_access_token(user.id)
        return {'Authorization': f'Bearer {token}'}
```

```python
# tests/test_users.py
def test_list_users_requires_auth(client):
    response = client.get('/api/users/')
    assert response.status_code == 401


def test_list_users_success(client, auth_headers):
    response = client.get('/api/users/', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_user(client, auth_headers):
    response = client.post('/api/users/',
        headers=auth_headers,
        json={
            'email': 'new@example.com',
            'name': 'New User',
            'password': 'password123',
        }
    )
    assert response.status_code == 201
    assert response.json['email'] == 'new@example.com'


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}
```

---

## Cross-Framework Comparison

### Same Feature: User Creation

**Django:**
```python
# View -> Serializer -> Service -> Model
user = services.create_user(
    email=serializer.validated_data['email'],
    name=serializer.validated_data['name'],
)
```

**FastAPI:**
```python
# Route -> Pydantic schema -> Service -> SQLAlchemy model
user = await user_service.create_user(db, user_data)
```

**Flask:**
```python
# View -> Marshmallow schema -> Service -> SQLAlchemy model
data = schema.load(request.json)
user = services.create_user(**data)
```

---

*Python Web Frameworks Examples v1.0*
*Django | FastAPI | Flask*
