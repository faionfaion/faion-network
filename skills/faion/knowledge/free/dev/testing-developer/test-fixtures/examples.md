# Test Fixtures Examples

Real-world fixture implementations across languages and frameworks.

---

## Python - pytest Fixtures

### Basic Fixture with Teardown

```python
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_directory():
    """Provides a temporary directory that is cleaned up after test."""
    temp_dir = Path(tempfile.mkdtemp())

    yield temp_dir

    # Teardown - runs even if test fails
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_file_creation(temp_directory):
    test_file = temp_directory / "test.txt"
    test_file.write_text("hello")

    assert test_file.exists()
    assert test_file.read_text() == "hello"
```

### Parametrized Fixture

```python
import pytest


@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_url(request):
    """Runs tests against multiple database backends."""
    urls = {
        "sqlite": "sqlite:///:memory:",
        "postgresql": "postgresql://test:test@localhost/test",
        "mysql": "mysql://test:test@localhost/test",
    }
    return urls[request.param]


@pytest.fixture(params=[
    pytest.param({"role": "admin", "can_delete": True}, id="admin"),
    pytest.param({"role": "editor", "can_delete": False}, id="editor"),
    pytest.param({"role": "viewer", "can_delete": False}, id="viewer"),
])
def user_permissions(request):
    """Test with different permission configurations."""
    return request.param


def test_delete_permission(user_permissions):
    user = User(role=user_permissions["role"])
    assert user.can_delete == user_permissions["can_delete"]
```

### Fixture Composition

```python
import pytest
from datetime import datetime, timedelta


@pytest.fixture
def base_user():
    """Minimal user for most tests."""
    return User(
        id="user-123",
        email="test@example.com",
        name="Test User",
        created_at=datetime(2024, 1, 15),
    )


@pytest.fixture
def admin_user(base_user):
    """Admin user built from base."""
    base_user.role = "admin"
    base_user.permissions = ["read", "write", "delete", "admin"]
    return base_user


@pytest.fixture
def expired_subscription_user(base_user):
    """User with expired subscription."""
    base_user.subscription = Subscription(
        plan="pro",
        expires_at=datetime.now() - timedelta(days=30),
    )
    return base_user


def test_admin_can_delete(admin_user):
    assert "delete" in admin_user.permissions


def test_expired_user_downgraded(expired_subscription_user):
    assert expired_subscription_user.effective_plan == "free"
```

### Autouse Fixture

```python
import pytest
import logging


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset all singletons before each test."""
    ConfigManager._instance = None
    CacheManager._instance = None

    yield

    # Cleanup after test
    ConfigManager._instance = None
    CacheManager._instance = None


@pytest.fixture(autouse=True)
def capture_logs(caplog):
    """Automatically capture logs for all tests."""
    caplog.set_level(logging.DEBUG)
    yield
    # Logs available in caplog.records


@pytest.fixture(autouse=True, scope="session")
def setup_test_environment():
    """One-time environment setup for entire test session."""
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"

    yield

    del os.environ["TESTING"]
    del os.environ["LOG_LEVEL"]
```

---

## Python - Factory Boy

### Django Model Factory

```python
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from myapp.models import Profile, Order, OrderItem


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        # Set password after user creation
        password = extracted or "testpass123"
        self.set_password(password)
        if create:
            self.save()


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("paragraph")
    avatar_url = factory.Faker("image_url")
    timezone = "UTC"


# Usage in tests
def test_user_creation():
    user = UserFactory()
    assert user.username.startswith("user")
    assert user.check_password("testpass123")


def test_custom_user():
    user = UserFactory(
        username="custom",
        email="custom@test.com",
        is_active=False,
    )
    assert user.username == "custom"
    assert not user.is_active
```

### SQLAlchemy Model Factory

```python
import factory
from factory.alchemy import SQLAlchemyModelFactory
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


class OrderFactory(BaseFactory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    status = "pending"
    total = factory.LazyAttribute(
        lambda o: sum(item.price * item.quantity for item in o.items)
    )

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.items.append(item)


class OrderItemFactory(BaseFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    sku = factory.Sequence(lambda n: f"SKU-{n:05d}")
    name = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=10)
    price = factory.Faker("pydecimal", min_value=1, max_value=100, left_digits=3)


# Usage
def test_order_with_items(db_session):
    order = OrderFactory(
        items=[
            OrderItemFactory(quantity=2, price=Decimal("10.00")),
            OrderItemFactory(quantity=1, price=Decimal("25.00")),
        ]
    )
    assert order.total == Decimal("45.00")
```

### Factory Traits

```python
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    is_active = True
    is_staff = False
    is_superuser = False

    class Params:
        # Traits for common configurations
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True,
        )
        inactive = factory.Trait(
            is_active=False,
        )
        with_profile = factory.Trait(
            profile=factory.RelatedFactory(
                ProfileFactory,
                factory_related_name="user",
            )
        )


# Usage
def test_admin_user():
    admin = UserFactory(admin=True)
    assert admin.is_staff
    assert admin.is_superuser


def test_inactive_user():
    user = UserFactory(inactive=True)
    assert not user.is_active


def test_user_with_profile():
    user = UserFactory(with_profile=True)
    assert user.profile is not None
```

---

## Python - Database Fixtures

### SQLAlchemy Transactional Fixture

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from myapp.models import Base


@pytest.fixture(scope="session")
def engine():
    """Create database engine for entire test session."""
    engine = create_engine(
        "postgresql://test:test@localhost/test_db",
        echo=False,
    )
    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    """Session factory scoped to test session."""
    return sessionmaker(bind=engine)


@pytest.fixture
def db_session(session_factory):
    """
    Transactional database session.

    Each test runs in a nested transaction (savepoint) that is
    rolled back after the test, ensuring test isolation.
    """
    connection = session_factory().connection()
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(bind=connection, join_transaction_mode="create_savepoint")
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# Usage
def test_user_creation(db_session):
    user = User(email="test@example.com", name="Test")
    db_session.add(user)
    db_session.commit()

    found = db_session.query(User).filter_by(email="test@example.com").first()
    assert found is not None
    # Rolled back after test - database is clean
```

### Django Database Fixture

```python
import pytest
from django.contrib.auth.models import User
from myapp.models import Order


@pytest.fixture
def user(db):
    """Create a user (requires db fixture)."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def authenticated_client(client, user):
    """Django test client with logged-in user."""
    client.login(username="testuser", password="testpass123")
    return client


@pytest.fixture
def order_with_items(db, user):
    """Order with items for testing."""
    order = Order.objects.create(user=user, status="pending")
    order.items.create(sku="SKU-001", quantity=2, price=10.00)
    order.items.create(sku="SKU-002", quantity=1, price=25.00)
    return order


@pytest.mark.django_db
def test_order_total(order_with_items):
    assert order_with_items.total == 45.00


@pytest.mark.django_db(transaction=True)
def test_concurrent_order_update(order_with_items):
    """Test with real transactions."""
    # This test uses actual commits, not savepoints
    pass
```

---

## Python - Builder Pattern

### Fluent Test Builder

```python
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List
from uuid import uuid4
from datetime import datetime


@dataclass
class OrderBuilder:
    """Builder for creating test orders."""

    _id: str = field(default_factory=lambda: str(uuid4()))
    _user_id: str = "default-user"
    _items: List["OrderItem"] = field(default_factory=list)
    _status: str = "pending"
    _discount: Optional[Decimal] = None
    _shipping_address: Optional["Address"] = None
    _notes: Optional[str] = None
    _created_at: datetime = field(default_factory=datetime.utcnow)

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
        self._items.append(
            OrderItem(sku=sku, quantity=quantity, price=price)
        )
        return self

    def with_discount(self, amount: Decimal) -> "OrderBuilder":
        self._discount = amount
        return self

    def with_discount_percent(self, percent: int) -> "OrderBuilder":
        """Apply percentage discount (calculated at build time)."""
        self._discount_percent = percent
        return self

    def shipped_to(self, address: "Address") -> "OrderBuilder":
        self._shipping_address = address
        return self

    def with_status(self, status: str) -> "OrderBuilder":
        self._status = status
        return self

    def with_note(self, note: str) -> "OrderBuilder":
        self._notes = note
        return self

    def created_at(self, dt: datetime) -> "OrderBuilder":
        self._created_at = dt
        return self

    # Convenience methods for common scenarios
    def completed(self) -> "OrderBuilder":
        return self.with_status("completed")

    def cancelled(self) -> "OrderBuilder":
        return self.with_status("cancelled")

    def build(self) -> "Order":
        order = Order(
            id=self._id,
            user_id=self._user_id,
            items=self._items.copy(),
            status=self._status,
            discount=self._discount,
            shipping_address=self._shipping_address,
            notes=self._notes,
            created_at=self._created_at,
        )
        return order


# Usage as pytest fixture
@pytest.fixture
def order_builder():
    return OrderBuilder()


def test_order_with_multiple_items(order_builder):
    order = (
        order_builder
        .for_user("user-123")
        .with_item(sku="SHIRT-M", quantity=2, price=Decimal("29.99"))
        .with_item(sku="PANTS-L", quantity=1, price=Decimal("49.99"))
        .with_discount(Decimal("10.00"))
        .shipped_to(Address(city="New York", country="US"))
        .build()
    )

    assert order.subtotal == Decimal("109.97")
    assert order.total == Decimal("99.97")


def test_cancelled_order(order_builder):
    order = (
        order_builder
        .for_user("user-456")
        .with_item()
        .cancelled()
        .build()
    )

    assert order.status == "cancelled"
    assert not order.can_be_modified
```

---

## TypeScript - Jest Fixtures

### Factory Functions

```typescript
// __fixtures__/users.ts
import { User, UserRole } from '../types';

let userIdCounter = 0;

export function createUser(overrides: Partial<User> = {}): User {
  userIdCounter++;
  return {
    id: `user-${userIdCounter}`,
    email: `user${userIdCounter}@example.com`,
    name: 'Test User',
    role: UserRole.User,
    createdAt: new Date('2024-01-15'),
    isActive: true,
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

// Reset counter between test files
export function resetUserFactory(): void {
  userIdCounter = 0;
}
```

```typescript
// __fixtures__/orders.ts
import { Order, OrderItem, OrderStatus } from '../types';
import { createUser } from './users';

let orderIdCounter = 0;

export function createOrderItem(overrides: Partial<OrderItem> = {}): OrderItem {
  return {
    id: `item-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    sku: `SKU-${String(orderIdCounter).padStart(5, '0')}`,
    name: 'Test Product',
    quantity: 1,
    price: 29.99,
    ...overrides,
  };
}

export function createOrder(overrides: Partial<Order> = {}): Order {
  orderIdCounter++;
  const items = overrides.items || [createOrderItem()];

  return {
    id: `order-${orderIdCounter}`,
    userId: createUser().id,
    items,
    status: OrderStatus.Pending,
    total: items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    createdAt: new Date(),
    ...overrides,
  };
}
```

### Builder Pattern in TypeScript

```typescript
// __fixtures__/OrderBuilder.ts
import { Order, OrderItem, OrderStatus, Address } from '../types';

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
      id: `item-${Date.now()}-${Math.random().toString(36).slice(2)}`,
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

  shippedTo(address: Address): this {
    this.order.shippingAddress = address;
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

// Usage
describe('OrderService', () => {
  it('calculates total with discount', () => {
    const order = new OrderBuilder()
      .forUser('user-123')
      .withItem({ sku: 'A', quantity: 2, price: 15 })
      .withItem({ sku: 'B', quantity: 1, price: 30 })
      .build();

    expect(order.total).toBe(60);
  });
});
```

### Jest Setup/Teardown

```typescript
// jest.setup.ts
import { resetUserFactory } from './__fixtures__/users';

beforeEach(() => {
  // Reset factories before each test
  resetUserFactory();
});

// tests/order.test.ts
import { createOrder, createOrderItem } from '../__fixtures__/orders';
import { createUser } from '../__fixtures__/users';

describe('OrderService', () => {
  let testUser: User;

  beforeEach(() => {
    testUser = createUser({ name: 'Order Test User' });
  });

  afterEach(() => {
    // Cleanup if needed
  });

  it('creates order for user', () => {
    const order = createOrder({ userId: testUser.id });
    expect(order.userId).toBe(testUser.id);
  });
});
```

---

## Go - Table-Driven Tests with Fixtures

### Test Fixtures in Go

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

func NewUser(opts ...UserOption) *models.User {
    id := atomic.AddUint64(&userCounter, 1)

    user := &models.User{
        ID:        fmt.Sprintf("user-%d", id),
        Email:     fmt.Sprintf("user%d@example.com", id),
        Name:      "Test User",
        Role:      models.RoleUser,
        IsActive:  true,
        CreatedAt: time.Date(2024, 1, 15, 10, 0, 0, 0, time.UTC),
    }

    for _, opt := range opts {
        opt(user)
    }

    return user
}

// Functional options pattern
type UserOption func(*models.User)

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
        u.Permissions = []string{"read", "write", "delete", "admin"}
    }
}

func Inactive() UserOption {
    return func(u *models.User) {
        u.IsActive = false
    }
}
```

### Table-Driven Tests

```go
// user_service_test.go
package services_test

import (
    "testing"

    "myapp/fixtures"
    "myapp/models"
    "myapp/services"
)

func TestUserService_CanDelete(t *testing.T) {
    tests := []struct {
        name       string
        user       *models.User
        targetUser *models.User
        want       bool
    }{
        {
            name:       "admin can delete any user",
            user:       fixtures.NewUser(fixtures.AsAdmin()),
            targetUser: fixtures.NewUser(),
            want:       true,
        },
        {
            name:       "user can delete self",
            user:       fixtures.NewUser(fixtures.WithEmail("same@test.com")),
            targetUser: fixtures.NewUser(fixtures.WithEmail("same@test.com")),
            want:       true,
        },
        {
            name:       "user cannot delete others",
            user:       fixtures.NewUser(fixtures.WithEmail("user1@test.com")),
            targetUser: fixtures.NewUser(fixtures.WithEmail("user2@test.com")),
            want:       false,
        },
        {
            name:       "inactive user cannot delete",
            user:       fixtures.NewUser(fixtures.Inactive(), fixtures.AsAdmin()),
            targetUser: fixtures.NewUser(),
            want:       false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := services.NewUserService()
            got := svc.CanDelete(tt.user, tt.targetUser)
            if got != tt.want {
                t.Errorf("CanDelete() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Database Fixtures with testcontainers-go

```go
// fixtures/database.go
package fixtures

import (
    "context"
    "testing"

    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
)

type TestDB struct {
    Container testcontainers.Container
    DB        *gorm.DB
}

func NewTestDB(t *testing.T) *TestDB {
    t.Helper()

    ctx := context.Background()

    container, err := postgres.RunContainer(ctx,
        testcontainers.WithImage("postgres:15"),
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
    )
    if err != nil {
        t.Fatalf("failed to start container: %v", err)
    }

    connStr, err := container.ConnectionString(ctx, "sslmode=disable")
    if err != nil {
        t.Fatalf("failed to get connection string: %v", err)
    }

    db, err := gorm.Open(postgres.Open(connStr), &gorm.Config{})
    if err != nil {
        t.Fatalf("failed to connect to database: %v", err)
    }

    // Run migrations
    db.AutoMigrate(&models.User{}, &models.Order{})

    t.Cleanup(func() {
        container.Terminate(ctx)
    })

    return &TestDB{
        Container: container,
        DB:        db,
    }
}

// Usage
func TestUserRepository(t *testing.T) {
    testDB := fixtures.NewTestDB(t)

    repo := repositories.NewUserRepository(testDB.DB)

    user := fixtures.NewUser()
    err := repo.Create(user)
    if err != nil {
        t.Fatalf("failed to create user: %v", err)
    }

    found, err := repo.FindByID(user.ID)
    if err != nil {
        t.Fatalf("failed to find user: %v", err)
    }

    if found.Email != user.Email {
        t.Errorf("expected email %s, got %s", user.Email, found.Email)
    }
}
```

---

## Rust - Test Fixtures

### Builder Pattern in Rust

```rust
// tests/fixtures/user.rs
use myapp::models::{User, Role};
use chrono::{DateTime, Utc};
use uuid::Uuid;

pub struct UserBuilder {
    id: String,
    email: String,
    name: String,
    role: Role,
    is_active: bool,
    created_at: DateTime<Utc>,
}

impl Default for UserBuilder {
    fn default() -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            email: format!("user-{}@example.com", Uuid::new_v4()),
            name: "Test User".to_string(),
            role: Role::User,
            is_active: true,
            created_at: Utc::now(),
        }
    }
}

impl UserBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn with_email(mut self, email: &str) -> Self {
        self.email = email.to_string();
        self
    }

    pub fn with_role(mut self, role: Role) -> Self {
        self.role = role;
        self
    }

    pub fn as_admin(self) -> Self {
        self.with_role(Role::Admin)
    }

    pub fn inactive(mut self) -> Self {
        self.is_active = false;
        self
    }

    pub fn build(self) -> User {
        User {
            id: self.id,
            email: self.email,
            name: self.name,
            role: self.role,
            is_active: self.is_active,
            created_at: self.created_at,
        }
    }
}

// tests/user_service_test.rs
#[cfg(test)]
mod tests {
    use super::*;
    use crate::fixtures::UserBuilder;

    #[test]
    fn admin_can_delete_any_user() {
        let admin = UserBuilder::new().as_admin().build();
        let target = UserBuilder::new().build();

        let service = UserService::new();
        assert!(service.can_delete(&admin, &target));
    }

    #[test]
    fn inactive_admin_cannot_delete() {
        let admin = UserBuilder::new()
            .as_admin()
            .inactive()
            .build();
        let target = UserBuilder::new().build();

        let service = UserService::new();
        assert!(!service.can_delete(&admin, &target));
    }
}
```

### rstest Fixtures

```rust
use rstest::*;
use myapp::models::User;

#[fixture]
fn user() -> User {
    User {
        id: "user-1".to_string(),
        email: "test@example.com".to_string(),
        name: "Test User".to_string(),
        role: Role::User,
        is_active: true,
    }
}

#[fixture]
fn admin(#[from(user)] mut user: User) -> User {
    user.role = Role::Admin;
    user
}

#[rstest]
fn test_user_is_not_admin(user: User) {
    assert_ne!(user.role, Role::Admin);
}

#[rstest]
fn test_admin_has_admin_role(admin: User) {
    assert_eq!(admin.role, Role::Admin);
}

// Parametrized fixture
#[rstest]
#[case("user@test.com", true)]
#[case("invalid", false)]
#[case("", false)]
fn test_email_validation(#[case] email: &str, #[case] expected: bool) {
    assert_eq!(is_valid_email(email), expected);
}
```

---

## Summary

| Language | Framework | Fixture Approach |
|----------|-----------|------------------|
| Python | pytest | `@pytest.fixture` with yield |
| Python | Factory Boy | `DjangoModelFactory`, `SQLAlchemyModelFactory` |
| TypeScript | Jest | Factory functions + beforeEach |
| Go | testing | Functional options + table-driven |
| Rust | rstest | `#[fixture]` attribute |

**Universal patterns:**
1. Factory functions with sensible defaults
2. Builder pattern for complex objects
3. Composition over inheritance
4. Explicit cleanup/teardown
