# Test Fixtures Templates

Copy-paste templates for common fixture scenarios.

---

## pytest Fixtures

### Basic Fixture

```python
import pytest


@pytest.fixture
def sample_data():
    """Provides sample data for testing."""
    return {
        "key": "value",
        "number": 42,
        "items": ["a", "b", "c"],
    }
```

### Fixture with Teardown

```python
import pytest


@pytest.fixture
def resource():
    """Provides a resource with automatic cleanup."""
    # Setup
    resource = acquire_resource()

    yield resource

    # Teardown - runs even if test fails
    resource.cleanup()
```

### Fixture with Parameters

```python
import pytest


@pytest.fixture
def configurable_fixture(request):
    """Fixture that accepts parameters via indirect parametrization."""
    config = getattr(request, "param", {"default": True})
    return create_resource(config)


# Usage:
# @pytest.mark.parametrize("configurable_fixture", [{"mode": "fast"}], indirect=True)
```

### Parametrized Fixture

```python
import pytest


@pytest.fixture(params=[
    pytest.param("sqlite", id="sqlite"),
    pytest.param("postgresql", id="postgres"),
    pytest.param("mysql", id="mysql"),
])
def database_type(request):
    """Run tests against multiple database backends."""
    return request.param
```

### Scoped Fixture

```python
import pytest


@pytest.fixture(scope="session")
def expensive_resource():
    """Session-scoped fixture for expensive setup."""
    resource = create_expensive_resource()

    yield resource

    resource.teardown()


@pytest.fixture(scope="module")
def module_resource():
    """Module-scoped fixture."""
    return create_module_resource()


@pytest.fixture(scope="class")
def class_resource():
    """Class-scoped fixture."""
    return create_class_resource()
```

### Autouse Fixture

```python
import pytest


@pytest.fixture(autouse=True)
def reset_state():
    """Automatically runs before each test."""
    # Reset any global state
    GlobalConfig.reset()

    yield

    # Cleanup after test
    GlobalConfig.reset()
```

---

## conftest.py Templates

### Root conftest.py

```python
# tests/conftest.py
import pytest


# Session-scoped fixtures
@pytest.fixture(scope="session")
def app_config():
    """Application configuration for tests."""
    return {
        "TESTING": True,
        "DATABASE_URL": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key",
        "DEBUG": True,
    }


@pytest.fixture(scope="session")
def app(app_config):
    """Create application instance."""
    from myapp import create_app

    app = create_app(app_config)
    return app


# Function-scoped fixtures
@pytest.fixture
def client(app):
    """Test client for HTTP requests."""
    return app.test_client()


# Fixture for async tests
@pytest.fixture
def anyio_backend():
    """Backend for anyio/pytest-anyio."""
    return "asyncio"
```

### Unit Test conftest.py

```python
# tests/unit/conftest.py
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_repository():
    """Mock repository for unit tests."""
    repo = Mock()
    repo.find_by_id = Mock(return_value=None)
    repo.save = Mock(return_value=True)
    repo.delete = Mock(return_value=True)
    return repo


@pytest.fixture
def mock_service():
    """Mock external service."""
    service = MagicMock()
    service.process.return_value = {"status": "success"}
    return service
```

### Integration Test conftest.py

```python
# tests/integration/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def test_engine():
    """Test database engine."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Transactional database session."""
    from myapp.models import Base

    Base.metadata.create_all(test_engine)

    Session = sessionmaker(bind=test_engine)
    session = Session()
    session.begin_nested()

    yield session

    session.rollback()
    session.close()
```

---

## Factory Boy Templates

### Django Model Factory

```python
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from myapp.models import User, Profile, Order

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False

    class Params:
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True,
        )
        inactive = factory.Trait(
            is_active=False,
        )

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "testpass123"
        self.set_password(password)
        if create:
            self.save()


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("paragraph")
    location = factory.Faker("city")
```

### SQLAlchemy Model Factory

```python
import factory
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime
from decimal import Decimal
from myapp.models import User, Order, OrderItem
from myapp.database import Session


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    created_at = factory.LazyFunction(datetime.utcnow)
    is_active = True


class OrderFactory(BaseFactory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    status = "pending"
    total = Decimal("0.00")
    created_at = factory.LazyFunction(datetime.utcnow)

    @factory.lazy_attribute
    def total(self):
        return sum(
            item.price * item.quantity
            for item in self.items
        ) if hasattr(self, 'items') else Decimal("0.00")


class OrderItemFactory(BaseFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    sku = factory.Sequence(lambda n: f"SKU-{n:05d}")
    name = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=5)
    price = factory.Faker(
        "pydecimal",
        min_value=1,
        max_value=100,
        left_digits=3,
        right_digits=2,
    )
```

### pytest-factoryboy Integration

```python
# tests/conftest.py
import pytest
from pytest_factoryboy import register
from .factories import UserFactory, OrderFactory, ProfileFactory

# Register factories as fixtures
register(UserFactory)
register(OrderFactory)
register(ProfileFactory)

# Creates fixtures:
# - user (UserFactory instance)
# - user_factory (factory function)
# - order
# - order_factory
# - profile
# - profile_factory


# Override attributes with pytest.mark.parametrize
@pytest.mark.parametrize("user__email", ["custom@test.com"])
def test_custom_email(user):
    assert user.email == "custom@test.com"
```

---

## Builder Pattern Templates

### Python Builder

```python
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List
from uuid import uuid4
from datetime import datetime


@dataclass
class OrderBuilder:
    """Builder for test orders."""

    _id: str = field(default_factory=lambda: str(uuid4()))
    _user_id: str = "default-user"
    _items: List = field(default_factory=list)
    _status: str = "pending"
    _discount: Optional[Decimal] = None
    _shipping_address: Optional[dict] = None

    def with_id(self, order_id: str) -> "OrderBuilder":
        self._id = order_id
        return self

    def for_user(self, user_id: str) -> "OrderBuilder":
        self._user_id = user_id
        return self

    def with_item(
        self,
        sku: str = "SKU-001",
        quantity: int = 1,
        price: Decimal = Decimal("10.00"),
    ) -> "OrderBuilder":
        self._items.append({
            "sku": sku,
            "quantity": quantity,
            "price": price,
        })
        return self

    def with_discount(self, amount: Decimal) -> "OrderBuilder":
        self._discount = amount
        return self

    def with_status(self, status: str) -> "OrderBuilder":
        self._status = status
        return self

    def shipped_to(self, address: dict) -> "OrderBuilder":
        self._shipping_address = address
        return self

    def completed(self) -> "OrderBuilder":
        return self.with_status("completed")

    def cancelled(self) -> "OrderBuilder":
        return self.with_status("cancelled")

    def build(self) -> "Order":
        return Order(
            id=self._id,
            user_id=self._user_id,
            items=self._items.copy(),
            status=self._status,
            discount=self._discount,
            shipping_address=self._shipping_address,
        )


# Fixture
@pytest.fixture
def order_builder():
    return OrderBuilder()
```

### TypeScript Builder

```typescript
// builders/OrderBuilder.ts
import { Order, OrderItem, OrderStatus } from '../types';

export class OrderBuilder {
  private order: Partial<Order> = {
    id: `order-${Date.now()}`,
    status: OrderStatus.Pending,
    items: [],
    createdAt: new Date(),
  };

  forUser(userId: string): this {
    this.order.userId = userId;
    return this;
  }

  withItem(item: Partial<OrderItem>): this {
    const fullItem: OrderItem = {
      id: `item-${Date.now()}`,
      sku: 'SKU-001',
      name: 'Product',
      quantity: 1,
      price: 10,
      ...item,
    };
    this.order.items = [...(this.order.items || []), fullItem];
    return this;
  }

  withStatus(status: OrderStatus): this {
    this.order.status = status;
    return this;
  }

  completed(): this {
    return this.withStatus(OrderStatus.Completed);
  }

  cancelled(): this {
    return this.withStatus(OrderStatus.Cancelled);
  }

  build(): Order {
    const items = this.order.items || [];
    return {
      ...this.order,
      total: items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    } as Order;
  }
}
```

---

## Database Fixture Templates

### SQLAlchemy Transactional Fixture

```python
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session


@pytest.fixture(scope="session")
def engine():
    """Create database engine."""
    engine = create_engine(
        "postgresql://test:test@localhost/test_db",
        echo=False,
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables."""
    from myapp.models import Base

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """
    Transactional database session.

    Uses nested transactions for isolation.
    Rolls back after each test.
    """
    connection = engine.connect()
    transaction = connection.begin()

    # Bind session to connection
    session = Session(bind=connection)

    # Begin nested transaction (savepoint)
    session.begin_nested()

    # Handle session commits by starting new nested transaction
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    # Rollback and cleanup
    session.close()
    transaction.rollback()
    connection.close()
```

### Django Transactional Fixture

```python
import pytest
from django.db import connection


@pytest.fixture
def db_session(db):
    """Transactional Django database session."""
    # db fixture from pytest-django provides database access

    yield

    # Cleanup handled by pytest-django


@pytest.fixture
def populated_db(db):
    """Database with pre-populated data."""
    from myapp.models import User, Category

    admin = User.objects.create_user(
        username="admin",
        email="admin@test.com",
        password="adminpass",
        is_staff=True,
    )

    categories = [
        Category.objects.create(name="Electronics", slug="electronics"),
        Category.objects.create(name="Books", slug="books"),
        Category.objects.create(name="Clothing", slug="clothing"),
    ]

    yield {
        "admin": admin,
        "categories": categories,
    }

    # Cleanup handled by pytest-django transaction rollback
```

### Testcontainers Fixture

```python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine


@pytest.fixture(scope="session")
def postgres_container():
    """PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """SQLAlchemy engine connected to container."""
    engine = create_engine(postgres_container.get_connection_url())
    yield engine
    engine.dispose()
```

---

## TypeScript/JavaScript Templates

### Jest Factory Function

```typescript
// __fixtures__/users.ts
import { User, UserRole } from '../types';

let counter = 0;

export function createUser(overrides: Partial<User> = {}): User {
  counter++;
  return {
    id: `user-${counter}`,
    email: `user${counter}@example.com`,
    name: 'Test User',
    role: UserRole.User,
    isActive: true,
    createdAt: new Date('2024-01-15'),
    ...overrides,
  };
}

export function createAdmin(overrides: Partial<User> = {}): User {
  return createUser({
    role: UserRole.Admin,
    permissions: ['read', 'write', 'delete', 'admin'],
    ...overrides,
  });
}

export function resetFixtures(): void {
  counter = 0;
}
```

### Jest Setup File

```typescript
// jest.setup.ts
import { resetFixtures } from './__fixtures__/users';

beforeEach(() => {
  resetFixtures();
  jest.clearAllMocks();
});

afterEach(() => {
  jest.restoreAllMocks();
});
```

### Vitest Fixture

```typescript
// tests/fixtures.ts
import { test as base } from 'vitest';
import { createUser, createOrder } from './__fixtures__';

interface Fixtures {
  user: User;
  order: Order;
}

export const test = base.extend<Fixtures>({
  user: async ({}, use) => {
    const user = createUser();
    await use(user);
    // Cleanup if needed
  },
  order: async ({ user }, use) => {
    const order = createOrder({ userId: user.id });
    await use(order);
  },
});

// Usage
test('order belongs to user', ({ user, order }) => {
  expect(order.userId).toBe(user.id);
});
```

---

## Go Templates

### Factory Function

```go
// fixtures/users.go
package fixtures

import (
    "fmt"
    "sync/atomic"
    "time"

    "myapp/models"
)

var userCounter uint64

type UserOption func(*models.User)

func NewUser(opts ...UserOption) *models.User {
    id := atomic.AddUint64(&userCounter, 1)

    user := &models.User{
        ID:        fmt.Sprintf("user-%d", id),
        Email:     fmt.Sprintf("user%d@example.com", id),
        Name:      "Test User",
        Role:      models.RoleUser,
        IsActive:  true,
        CreatedAt: time.Now(),
    }

    for _, opt := range opts {
        opt(user)
    }

    return user
}

func WithEmail(email string) UserOption {
    return func(u *models.User) {
        u.Email = email
    }
}

func WithRole(role models.Role) UserOption {
    return func(u *models.User) {
        u.Role = role
    }
}

func AsAdmin() UserOption {
    return func(u *models.User) {
        u.Role = models.RoleAdmin
    }
}

func Inactive() UserOption {
    return func(u *models.User) {
        u.IsActive = false
    }
}
```

### Table-Driven Test Template

```go
func TestFeature(t *testing.T) {
    tests := []struct {
        name    string
        input   InputType
        want    OutputType
        wantErr bool
    }{
        {
            name:  "valid input",
            input: fixtures.NewInput(),
            want:  expectedOutput,
        },
        {
            name:    "invalid input",
            input:   fixtures.NewInput(fixtures.Invalid()),
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ProcessInput(tt.input)

            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if !tt.wantErr && !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

---

## Object Mother Template

```python
# fixtures/mothers.py
from datetime import datetime, timedelta
from decimal import Decimal


class UserMother:
    """Pre-configured users for common test scenarios."""

    @staticmethod
    def admin():
        return User(
            id="admin-1",
            email="admin@company.com",
            name="Admin User",
            role="admin",
            permissions=["read", "write", "delete", "admin"],
            is_active=True,
        )

    @staticmethod
    def regular_user():
        return User(
            id="user-1",
            email="user@example.com",
            name="Regular User",
            role="user",
            permissions=["read"],
            is_active=True,
        )

    @staticmethod
    def inactive_user():
        return User(
            id="inactive-1",
            email="inactive@example.com",
            name="Inactive User",
            role="user",
            is_active=False,
        )

    @staticmethod
    def user_with_expired_subscription():
        user = UserMother.regular_user()
        user.subscription = Subscription(
            plan="pro",
            expires_at=datetime.now() - timedelta(days=30),
        )
        return user

    @staticmethod
    def new_user_without_profile():
        return User(
            id="new-1",
            email="new@example.com",
            name="New User",
            role="user",
            is_active=True,
            profile=None,
        )


class OrderMother:
    """Pre-configured orders for common test scenarios."""

    @staticmethod
    def pending_order():
        return Order(
            id="order-1",
            user_id="user-1",
            status="pending",
            items=[
                OrderItem(sku="SKU-001", quantity=1, price=Decimal("29.99")),
            ],
            total=Decimal("29.99"),
        )

    @staticmethod
    def completed_order():
        order = OrderMother.pending_order()
        order.status = "completed"
        order.completed_at = datetime.now()
        return order

    @staticmethod
    def order_with_discount():
        order = OrderMother.pending_order()
        order.discount = Decimal("5.00")
        order.total = Decimal("24.99")
        return order

    @staticmethod
    def large_order():
        return Order(
            id="large-order-1",
            user_id="user-1",
            status="pending",
            items=[
                OrderItem(sku=f"SKU-{i:03d}", quantity=2, price=Decimal("10.00"))
                for i in range(10)
            ],
            total=Decimal("200.00"),
        )
```

---

## Async Fixture Template

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def async_client(app):
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def async_db_session(async_engine):
    """Async database session with rollback."""
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession(async_engine) as session:
        await session.begin_nested()

        yield session

        await session.rollback()


@pytest.mark.anyio
async def test_create_user(async_client, async_db_session):
    response = await async_client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test"},
    )
    assert response.status_code == 201
```
