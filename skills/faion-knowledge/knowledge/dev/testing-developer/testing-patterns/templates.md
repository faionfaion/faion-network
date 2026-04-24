# Testing Patterns Templates

Copy-paste templates for common testing patterns. Ready to use with minimal modification.

## Test Structure Templates

### AAA Pattern Template (Python/pytest)

```python
import pytest


class TestClassName:
    """Test suite for ClassName functionality."""

    def test_method_happy_path(self):
        # Arrange
        sut = SystemUnderTest()
        input_data = {"key": "value"}

        # Act
        result = sut.method_name(input_data)

        # Assert
        assert result.status == "success"
        assert result.value == "expected"

    def test_method_edge_case_empty_input(self):
        # Arrange
        sut = SystemUnderTest()
        input_data = {}

        # Act
        result = sut.method_name(input_data)

        # Assert
        assert result is None

    def test_method_error_case_invalid_input(self):
        # Arrange
        sut = SystemUnderTest()
        input_data = {"invalid": True}

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            sut.method_name(input_data)

        assert "Invalid input" in str(exc_info.value)
```

### AAA Pattern Template (JavaScript/Jest)

```javascript
describe('ClassName', () => {
  describe('methodName', () => {
    it('should return success for valid input', () => {
      // Arrange
      const sut = new SystemUnderTest();
      const inputData = { key: 'value' };

      // Act
      const result = sut.methodName(inputData);

      // Assert
      expect(result.status).toBe('success');
      expect(result.value).toBe('expected');
    });

    it('should return null for empty input', () => {
      // Arrange
      const sut = new SystemUnderTest();
      const inputData = {};

      // Act
      const result = sut.methodName(inputData);

      // Assert
      expect(result).toBeNull();
    });

    it('should throw error for invalid input', () => {
      // Arrange
      const sut = new SystemUnderTest();
      const inputData = { invalid: true };

      // Act & Assert
      expect(() => sut.methodName(inputData)).toThrow('Invalid input');
    });
  });
});
```

### AAA Pattern Template (Go)

```go
package mypackage

import (
    "testing"
)

func TestMethodName_HappyPath(t *testing.T) {
    // Arrange
    sut := NewSystemUnderTest()
    input := Input{Key: "value"}

    // Act
    result, err := sut.MethodName(input)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result.Status != "success" {
        t.Errorf("expected status 'success', got '%s'", result.Status)
    }
}

func TestMethodName_EmptyInput(t *testing.T) {
    // Arrange
    sut := NewSystemUnderTest()
    input := Input{}

    // Act
    result, err := sut.MethodName(input)

    // Assert
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result != nil {
        t.Error("expected nil result for empty input")
    }
}

func TestMethodName_InvalidInput(t *testing.T) {
    // Arrange
    sut := NewSystemUnderTest()
    input := Input{Invalid: true}

    // Act
    _, err := sut.MethodName(input)

    // Assert
    if err == nil {
        t.Fatal("expected error for invalid input")
    }
    if err.Error() != "invalid input" {
        t.Errorf("expected 'invalid input' error, got '%s'", err.Error())
    }
}
```

## Test Data Builder Templates

### Python Builder Template

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Entity:
    """Domain entity to be built."""
    id: str
    name: str
    email: str
    status: str
    created_at: datetime
    metadata: Optional[dict] = None


class EntityBuilder:
    """
    Fluent builder for Entity test objects.

    Usage:
        entity = EntityBuilder().with_name("Test").as_active().build()
    """

    def __init__(self):
        self._id = str(uuid.uuid4())
        self._name = "Default Name"
        self._email = "default@example.com"
        self._status = "pending"
        self._created_at = datetime.now()
        self._metadata = None

    def with_id(self, id: str) -> 'EntityBuilder':
        self._id = id
        return self

    def with_name(self, name: str) -> 'EntityBuilder':
        self._name = name
        return self

    def with_email(self, email: str) -> 'EntityBuilder':
        self._email = email
        return self

    def as_active(self) -> 'EntityBuilder':
        self._status = "active"
        return self

    def as_inactive(self) -> 'EntityBuilder':
        self._status = "inactive"
        return self

    def with_status(self, status: str) -> 'EntityBuilder':
        self._status = status
        return self

    def created_at(self, dt: datetime) -> 'EntityBuilder':
        self._created_at = dt
        return self

    def with_metadata(self, metadata: dict) -> 'EntityBuilder':
        self._metadata = metadata
        return self

    def build(self) -> Entity:
        return Entity(
            id=self._id,
            name=self._name,
            email=self._email,
            status=self._status,
            created_at=self._created_at,
            metadata=self._metadata
        )
```

### TypeScript Builder Template

```typescript
import { v4 as uuidv4 } from 'uuid';

interface Entity {
  id: string;
  name: string;
  email: string;
  status: 'pending' | 'active' | 'inactive';
  createdAt: Date;
  metadata?: Record<string, unknown>;
}

export class EntityBuilder {
  private entity: Entity;

  constructor() {
    this.entity = {
      id: uuidv4(),
      name: 'Default Name',
      email: 'default@example.com',
      status: 'pending',
      createdAt: new Date(),
    };
  }

  withId(id: string): EntityBuilder {
    this.entity.id = id;
    return this;
  }

  withName(name: string): EntityBuilder {
    this.entity.name = name;
    return this;
  }

  withEmail(email: string): EntityBuilder {
    this.entity.email = email;
    return this;
  }

  asActive(): EntityBuilder {
    this.entity.status = 'active';
    return this;
  }

  asInactive(): EntityBuilder {
    this.entity.status = 'inactive';
    return this;
  }

  createdAt(date: Date): EntityBuilder {
    this.entity.createdAt = date;
    return this;
  }

  withMetadata(metadata: Record<string, unknown>): EntityBuilder {
    this.entity.metadata = metadata;
    return this;
  }

  build(): Entity {
    return { ...this.entity };
  }
}
```

### Go Builder Template

```go
package builders

import (
    "time"

    "github.com/google/uuid"
)

type Entity struct {
    ID        string
    Name      string
    Email     string
    Status    string
    CreatedAt time.Time
    Metadata  map[string]interface{}
}

type EntityBuilder struct {
    entity Entity
}

func NewEntityBuilder() *EntityBuilder {
    return &EntityBuilder{
        entity: Entity{
            ID:        uuid.New().String(),
            Name:      "Default Name",
            Email:     "default@example.com",
            Status:    "pending",
            CreatedAt: time.Now(),
            Metadata:  nil,
        },
    }
}

func (b *EntityBuilder) WithID(id string) *EntityBuilder {
    b.entity.ID = id
    return b
}

func (b *EntityBuilder) WithName(name string) *EntityBuilder {
    b.entity.Name = name
    return b
}

func (b *EntityBuilder) WithEmail(email string) *EntityBuilder {
    b.entity.Email = email
    return b
}

func (b *EntityBuilder) AsActive() *EntityBuilder {
    b.entity.Status = "active"
    return b
}

func (b *EntityBuilder) AsInactive() *EntityBuilder {
    b.entity.Status = "inactive"
    return b
}

func (b *EntityBuilder) CreatedAt(t time.Time) *EntityBuilder {
    b.entity.CreatedAt = t
    return b
}

func (b *EntityBuilder) WithMetadata(metadata map[string]interface{}) *EntityBuilder {
    b.entity.Metadata = metadata
    return b
}

func (b *EntityBuilder) Build() Entity {
    return b.entity
}
```

## Object Mother Templates

### Python Object Mother Template

```python
from builders import EntityBuilder, UserBuilder, OrderBuilder


class UserMother:
    """Factory for common user test scenarios."""

    @staticmethod
    def admin() -> UserBuilder:
        """Admin user with full permissions."""
        return UserBuilder().with_role("admin").with_name("Admin User")

    @staticmethod
    def regular() -> UserBuilder:
        """Standard member user."""
        return UserBuilder().with_role("member")

    @staticmethod
    def guest() -> UserBuilder:
        """Unverified guest user."""
        return UserBuilder().as_guest().unverified()

    @staticmethod
    def premium() -> UserBuilder:
        """Premium subscription user."""
        return UserBuilder().with_role("premium").with_subscription("premium")


class OrderMother:
    """Factory for common order test scenarios."""

    @staticmethod
    def empty() -> OrderBuilder:
        """Empty cart/order."""
        return OrderBuilder()

    @staticmethod
    def with_single_item() -> OrderBuilder:
        """Order with one item."""
        return OrderBuilder().with_item({"name": "Widget", "price": 29.99})

    @staticmethod
    def with_multiple_items() -> OrderBuilder:
        """Order with several items."""
        return (OrderBuilder()
                .with_item({"name": "Widget", "price": 29.99})
                .with_item({"name": "Gadget", "price": 49.99})
                .with_item({"name": "Gizmo", "price": 19.99}))

    @staticmethod
    def high_value() -> OrderBuilder:
        """Order qualifying for free shipping (>$100)."""
        return OrderBuilder().with_item({"name": "Premium Item", "price": 149.99})

    @staticmethod
    def paid() -> OrderBuilder:
        """Completed payment."""
        return OrderMother.with_single_item().as_paid()

    @staticmethod
    def shipped() -> OrderBuilder:
        """Order in transit."""
        return OrderMother.paid().as_shipped()
```

### TypeScript Object Mother Template

```typescript
import { UserBuilder } from './UserBuilder';
import { OrderBuilder } from './OrderBuilder';

export class UserMother {
  static admin(): UserBuilder {
    return new UserBuilder().withRole('admin').withName('Admin User');
  }

  static regular(): UserBuilder {
    return new UserBuilder().withRole('member');
  }

  static guest(): UserBuilder {
    return new UserBuilder().asGuest().unverified();
  }

  static premium(): UserBuilder {
    return new UserBuilder().withRole('premium').withSubscription('premium');
  }
}

export class OrderMother {
  static empty(): OrderBuilder {
    return new OrderBuilder();
  }

  static withSingleItem(): OrderBuilder {
    return new OrderBuilder().withItem({ name: 'Widget', price: 29.99 });
  }

  static withMultipleItems(): OrderBuilder {
    return new OrderBuilder()
      .withItem({ name: 'Widget', price: 29.99 })
      .withItem({ name: 'Gadget', price: 49.99 })
      .withItem({ name: 'Gizmo', price: 19.99 });
  }

  static highValue(): OrderBuilder {
    return new OrderBuilder().withItem({ name: 'Premium Item', price: 149.99 });
  }

  static paid(): OrderBuilder {
    return OrderMother.withSingleItem().asPaid();
  }

  static shipped(): OrderBuilder {
    return OrderMother.paid().asShipped();
  }
}
```

## Page Object Model Templates

### Playwright Page Object Template (TypeScript)

```typescript
import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
  protected readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }
}

export class LoginPage extends BasePage {
  // Locators
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly signUpLink: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
    this.forgotPasswordLink = page.locator('[data-testid="forgot-password"]');
    this.signUpLink = page.locator('[data-testid="signup-link"]');
  }

  // Navigation
  async goto(): Promise<void> {
    await this.page.goto('/login');
    await this.waitForPageLoad();
  }

  // Actions
  async login(email: string, password: string): Promise<DashboardPage> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
    return new DashboardPage(this.page);
  }

  async loginExpectingError(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
    await this.errorMessage.waitFor({ state: 'visible' });
  }

  // Getters
  async getErrorText(): Promise<string> {
    return (await this.errorMessage.textContent()) ?? '';
  }

  // Assertions (optional - can also be in tests)
  async expectErrorMessage(message: string): Promise<void> {
    await expect(this.errorMessage).toHaveText(message);
  }
}

export class DashboardPage extends BasePage {
  readonly welcomeMessage: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;
  readonly navigationMenu: Locator;

  constructor(page: Page) {
    super(page);
    this.welcomeMessage = page.locator('[data-testid="welcome-message"]');
    this.userMenu = page.locator('[data-testid="user-menu"]');
    this.logoutButton = page.locator('[data-testid="logout-button"]');
    this.navigationMenu = page.locator('[data-testid="nav-menu"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/dashboard');
    await this.waitForPageLoad();
  }

  async getWelcomeText(): Promise<string> {
    return (await this.welcomeMessage.textContent()) ?? '';
  }

  async logout(): Promise<LoginPage> {
    await this.userMenu.click();
    await this.logoutButton.click();
    return new LoginPage(this.page);
  }

  async navigateTo(section: string): Promise<void> {
    await this.navigationMenu.locator(`text=${section}`).click();
  }
}
```

### Cypress Page Object Template

```typescript
// cypress/support/pages/BasePage.ts
export class BasePage {
  visit(path: string): this {
    cy.visit(path);
    return this;
  }

  waitForPageLoad(): this {
    cy.get('body').should('be.visible');
    return this;
  }
}

// cypress/support/pages/LoginPage.ts
import { BasePage } from './BasePage';
import { DashboardPage } from './DashboardPage';

export class LoginPage extends BasePage {
  // Selectors
  private selectors = {
    emailInput: '[data-testid="email-input"]',
    passwordInput: '[data-testid="password-input"]',
    loginButton: '[data-testid="login-button"]',
    errorMessage: '[data-testid="error-message"]',
    forgotPassword: '[data-testid="forgot-password"]',
  };

  goto(): this {
    return this.visit('/login');
  }

  typeEmail(email: string): this {
    cy.get(this.selectors.emailInput).clear().type(email);
    return this;
  }

  typePassword(password: string): this {
    cy.get(this.selectors.passwordInput).clear().type(password);
    return this;
  }

  clickLogin(): DashboardPage {
    cy.get(this.selectors.loginButton).click();
    return new DashboardPage();
  }

  login(email: string, password: string): DashboardPage {
    return this.typeEmail(email).typePassword(password).clickLogin();
  }

  getErrorMessage(): Cypress.Chainable<string> {
    return cy.get(this.selectors.errorMessage).invoke('text');
  }

  assertErrorMessage(message: string): this {
    cy.get(this.selectors.errorMessage).should('have.text', message);
    return this;
  }
}
```

## Fixture Templates

### pytest Fixtures Template

```python
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


# Database session fixture with transaction rollback
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create fresh database session with automatic rollback."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.rollback()
    session.close()


# Service fixtures with dependencies
@pytest.fixture
def user_repository(db_session: Session):
    """User repository with database session."""
    return UserRepository(db_session)


@pytest.fixture
def user_service(user_repository, email_service_mock):
    """User service with mocked dependencies."""
    return UserService(
        repository=user_repository,
        email_service=email_service_mock
    )


# Mock fixtures
@pytest.fixture
def email_service_mock():
    """Mocked email service."""
    mock = Mock(spec=EmailService)
    mock.send.return_value = True
    return mock


# Test data fixtures
@pytest.fixture
def sample_user(db_session) -> User:
    """Create and persist a sample user."""
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def admin_user(db_session) -> User:
    """Create and persist an admin user."""
    user = User(email="admin@example.com", name="Admin", role="admin")
    db_session.add(user)
    db_session.commit()
    return user


# Parameterized fixture
@pytest.fixture(params=["pending", "active", "inactive"])
def user_status(request) -> str:
    """Parameterized fixture for testing all user statuses."""
    return request.param
```

### Jest Fixtures Template

```javascript
// test/fixtures/setup.js
import { jest } from '@jest/globals';

// Database setup
export const setupTestDatabase = () => {
  let db;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.beginTransaction();
  });

  afterEach(async () => {
    await db.rollback();
  });

  return () => db;
};

// Mock factory
export const createMockService = (overrides = {}) => ({
  find: jest.fn().mockResolvedValue(null),
  create: jest.fn().mockResolvedValue({ id: 'mock-id' }),
  update: jest.fn().mockResolvedValue(true),
  delete: jest.fn().mockResolvedValue(true),
  ...overrides,
});

// test/fixtures/users.js
export const testUsers = {
  regular: {
    id: 'user-1',
    email: 'user@example.com',
    name: 'Test User',
    role: 'member',
  },
  admin: {
    id: 'admin-1',
    email: 'admin@example.com',
    name: 'Admin User',
    role: 'admin',
  },
  guest: {
    id: 'guest-1',
    email: 'guest@example.com',
    name: 'Guest User',
    role: 'guest',
    isVerified: false,
  },
};

// test/fixtures/orders.js
export const testOrders = {
  pending: {
    id: 'order-1',
    status: 'pending',
    items: [{ productId: 'prod-1', quantity: 1, price: 29.99 }],
    total: 29.99,
  },
  paid: {
    id: 'order-2',
    status: 'paid',
    items: [{ productId: 'prod-1', quantity: 2, price: 29.99 }],
    total: 59.98,
  },
};
```

### Playwright Fixtures Template

```typescript
// fixtures/index.ts
import { test as base, Page } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

// Define custom fixtures
type CustomFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<CustomFixtures>({
  // Page object fixtures
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  // Pre-authenticated page fixture
  authenticatedPage: async ({ page }, use) => {
    // Login via API to skip UI
    await page.request.post('/api/auth/login', {
      data: {
        email: 'test@example.com',
        password: 'testpassword',
      },
    });

    // Set auth state
    await page.context().storageState({ path: 'auth-state.json' });

    await use(page);
  },
});

export { expect } from '@playwright/test';

// Usage in tests
// import { test, expect } from '../fixtures';
//
// test('dashboard shows user data', async ({ authenticatedPage, dashboardPage }) => {
//   await dashboardPage.goto();
//   await expect(dashboardPage.welcomeMessage).toBeVisible();
// });
```

## Property-Based Testing Templates

### Hypothesis (Python) Template

```python
from hypothesis import given, strategies as st, settings, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant


# Basic property test template
@given(st.integers())
def test_property_name(value):
    """Property: describe what should always be true."""
    result = function_under_test(value)
    assert property_holds(result)


# Round-trip property template
@given(st.binary())
def test_encode_decode_roundtrip(data):
    """Property: decoding encoded data returns original."""
    encoded = encode(data)
    decoded = decode(encoded)
    assert decoded == data


# Invariant property template
@given(st.lists(st.integers()))
def test_sort_invariant_length_preserved(items):
    """Property: sorting preserves length."""
    sorted_items = sorted(items)
    assert len(sorted_items) == len(items)


# Conditional property template
@given(st.integers(), st.integers())
def test_division_property(a, b):
    """Property: a / b * b approximately equals a (for non-zero b)."""
    assume(b != 0)  # Skip if precondition not met
    result = (a / b) * b
    assert abs(result - a) < 0.0001


# Custom strategy template
@st.composite
def valid_user(draw):
    """Generate valid User objects."""
    name = draw(st.text(min_size=1, max_size=50))
    email = draw(st.emails())
    age = draw(st.integers(min_value=18, max_value=120))
    return User(name=name, email=email, age=age)


@given(valid_user())
def test_user_property(user):
    """Property: valid users can be saved and retrieved."""
    save(user)
    retrieved = find_by_email(user.email)
    assert retrieved.name == user.name


# Stateful testing template
class AccountStateMachine(RuleBasedStateMachine):
    """Stateful test for bank account operations."""

    def __init__(self):
        super().__init__()
        self.account = Account(balance=0)
        self.model_balance = 0

    @rule(amount=st.integers(min_value=1, max_value=1000))
    def deposit(self, amount):
        self.account.deposit(amount)
        self.model_balance += amount

    @rule(amount=st.integers(min_value=1, max_value=1000))
    def withdraw(self, amount):
        if amount <= self.model_balance:
            self.account.withdraw(amount)
            self.model_balance -= amount

    @invariant()
    def balance_matches_model(self):
        assert self.account.balance == self.model_balance

    @invariant()
    def balance_never_negative(self):
        assert self.account.balance >= 0


TestAccount = AccountStateMachine.TestCase
```

### fast-check (JavaScript) Template

```javascript
import fc from 'fast-check';

describe('Property-Based Tests', () => {
  // Basic property
  it('property: array reverse is involutory', () => {
    fc.assert(
      fc.property(fc.array(fc.anything()), (arr) => {
        const reversed = [...arr].reverse().reverse();
        expect(reversed).toEqual(arr);
      })
    );
  });

  // Round-trip property
  it('property: JSON parse/stringify roundtrip', () => {
    fc.assert(
      fc.property(fc.jsonValue(), (value) => {
        const serialized = JSON.stringify(value);
        const parsed = JSON.parse(serialized);
        expect(parsed).toEqual(value);
      })
    );
  });

  // Conditional property
  it('property: division then multiplication restores value', () => {
    fc.assert(
      fc.property(
        fc.integer(),
        fc.integer().filter((n) => n !== 0),
        (a, b) => {
          const result = Math.round((a / b) * b);
          expect(result).toBe(a);
        }
      )
    );
  });

  // Custom arbitrary
  const validEmail = fc
    .tuple(
      fc.stringOf(fc.constantFrom(...'abcdefghijklmnopqrstuvwxyz0123456789'), {
        minLength: 1,
        maxLength: 20,
      }),
      fc.constantFrom('gmail.com', 'example.com', 'test.org')
    )
    .map(([local, domain]) => `${local}@${domain}`);

  it('property: email validation accepts valid emails', () => {
    fc.assert(
      fc.property(validEmail, (email) => {
        expect(isValidEmail(email)).toBe(true);
      })
    );
  });

  // Model-based testing
  it('property: Set operations match model', () => {
    fc.assert(
      fc.property(
        fc.commands(
          [
            fc.integer().map((v) => ({ type: 'add', value: v })),
            fc.integer().map((v) => ({ type: 'remove', value: v })),
            fc.integer().map((v) => ({ type: 'has', value: v })),
          ],
          { maxCommands: 100 }
        ),
        (commands) => {
          const set = new Set();
          const mySet = new MyCustomSet();

          for (const cmd of commands) {
            if (cmd.type === 'add') {
              set.add(cmd.value);
              mySet.add(cmd.value);
            } else if (cmd.type === 'remove') {
              set.delete(cmd.value);
              mySet.remove(cmd.value);
            } else if (cmd.type === 'has') {
              expect(mySet.has(cmd.value)).toBe(set.has(cmd.value));
            }
          }

          expect(mySet.size()).toBe(set.size);
        }
      )
    );
  });
});
```

## CI/CD Test Configuration Templates

### GitHub Actions Template

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run unit tests
        run: pytest tests/unit -v --cov=src --cov-report=xml --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run integration tests
        run: pytest tests/integration -v
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### pytest.ini Template

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, external deps)
    e2e: End-to-end tests (slowest, full stack)
    slow: Tests that take more than 1 second

# Coverage
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-fail-under=80

# Async
asyncio_mode = auto

# Filtering
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### playwright.config.ts Template

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```
