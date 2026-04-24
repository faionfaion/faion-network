# Testing Patterns Examples

Real-world examples of testing patterns across Python, JavaScript, Go, and TypeScript.

## AAA Pattern Examples

### Python (pytest)

```python
# Example: Testing a shopping cart discount calculator

import pytest
from decimal import Decimal
from cart import Cart, Product, DiscountCalculator


class TestDiscountCalculator:
    """AAA pattern examples for discount calculation."""

    def test_percentage_discount_applied_to_subtotal(self):
        # Arrange
        cart = Cart()
        cart.add(Product("Widget", price=Decimal("100.00")))
        cart.add(Product("Gadget", price=Decimal("50.00")))
        calculator = DiscountCalculator()

        # Act
        result = calculator.apply_percentage_discount(cart, percent=10)

        # Assert
        assert result.discount_amount == Decimal("15.00")
        assert result.final_total == Decimal("135.00")

    def test_minimum_purchase_required_for_discount(self):
        # Arrange
        cart = Cart()
        cart.add(Product("Small Item", price=Decimal("5.00")))
        calculator = DiscountCalculator(minimum_purchase=Decimal("20.00"))

        # Act
        result = calculator.apply_percentage_discount(cart, percent=10)

        # Assert
        assert result.discount_amount == Decimal("0.00")
        assert result.final_total == Decimal("5.00")

    def test_empty_cart_returns_zero_total(self):
        # Arrange
        cart = Cart()
        calculator = DiscountCalculator()

        # Act
        result = calculator.apply_percentage_discount(cart, percent=10)

        # Assert
        assert result.discount_amount == Decimal("0.00")
        assert result.final_total == Decimal("0.00")
```

### JavaScript (Jest)

```javascript
// Example: Testing an authentication service

import { AuthService } from './auth-service';
import { User } from './user';

describe('AuthService', () => {
  describe('login', () => {
    it('should return token when credentials are valid', async () => {
      // Arrange
      const authService = new AuthService();
      const credentials = { email: 'user@example.com', password: 'valid123' };

      // Act
      const result = await authService.login(credentials);

      // Assert
      expect(result.token).toBeDefined();
      expect(result.expiresIn).toBe(3600);
    });

    it('should throw error when password is incorrect', async () => {
      // Arrange
      const authService = new AuthService();
      const credentials = { email: 'user@example.com', password: 'wrong' };

      // Act & Assert
      await expect(authService.login(credentials))
        .rejects
        .toThrow('Invalid credentials');
    });

    it('should lock account after 5 failed attempts', async () => {
      // Arrange
      const authService = new AuthService();
      const credentials = { email: 'user@example.com', password: 'wrong' };

      // Act
      for (let i = 0; i < 5; i++) {
        await authService.login(credentials).catch(() => {});
      }

      // Assert
      await expect(authService.login(credentials))
        .rejects
        .toThrow('Account locked');
    });
  });
});
```

### Go

```go
// Example: Testing a rate limiter

package ratelimiter

import (
    "testing"
    "time"
)

func TestRateLimiter_AllowsRequestsWithinLimit(t *testing.T) {
    // Arrange
    limiter := NewRateLimiter(Config{
        RequestsPerSecond: 10,
        BurstSize:         5,
    })
    clientID := "client-123"

    // Act
    allowed := limiter.Allow(clientID)

    // Assert
    if !allowed {
        t.Error("expected request to be allowed within rate limit")
    }
}

func TestRateLimiter_BlocksExcessiveRequests(t *testing.T) {
    // Arrange
    limiter := NewRateLimiter(Config{
        RequestsPerSecond: 1,
        BurstSize:         2,
    })
    clientID := "client-123"

    // Act - exhaust burst
    limiter.Allow(clientID)
    limiter.Allow(clientID)
    blocked := !limiter.Allow(clientID)

    // Assert
    if !blocked {
        t.Error("expected request to be blocked after exceeding burst")
    }
}

func TestRateLimiter_ReplenishesOverTime(t *testing.T) {
    // Arrange
    limiter := NewRateLimiter(Config{
        RequestsPerSecond: 10,
        BurstSize:         1,
    })
    clientID := "client-123"
    limiter.Allow(clientID) // exhaust token

    // Act
    time.Sleep(150 * time.Millisecond) // wait for replenishment
    allowed := limiter.Allow(clientID)

    // Assert
    if !allowed {
        t.Error("expected token to replenish after waiting")
    }
}
```

## Given-When-Then (BDD) Examples

### Python (pytest-bdd)

```python
# features/checkout.feature
Feature: Checkout Process
  As a customer
  I want to complete checkout
  So that I can receive my purchased items

  Scenario: Successful checkout with valid payment
    Given a cart with items totaling $99.99
    And a valid credit card on file
    When the customer completes checkout
    Then an order should be created
    And the payment should be processed
    And a confirmation email should be sent

# test_checkout.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('checkout.feature')


@given(parsers.parse('a cart with items totaling ${total:f}'))
def cart_with_items(total):
    cart = Cart()
    cart.add(Product("Test Item", price=Decimal(str(total))))
    return {'cart': cart, 'total': Decimal(str(total))}


@given('a valid credit card on file')
def valid_credit_card(context):
    context['payment_method'] = CreditCard(
        number="4111111111111111",
        expiry="12/25",
        cvv="123"
    )


@when('the customer completes checkout')
def complete_checkout(context):
    checkout_service = CheckoutService()
    context['order'] = checkout_service.process(
        cart=context['cart'],
        payment=context['payment_method']
    )


@then('an order should be created')
def order_created(context):
    assert context['order'].id is not None
    assert context['order'].status == 'confirmed'


@then('the payment should be processed')
def payment_processed(context):
    assert context['order'].payment_status == 'captured'


@then('a confirmation email should be sent')
def email_sent(context, email_service_mock):
    email_service_mock.send_confirmation.assert_called_once()
```

### JavaScript (Cucumber)

```javascript
// features/user-registration.feature
Feature: User Registration
  As a visitor
  I want to create an account
  So that I can access member features

  Scenario: Successful registration with valid email
    Given I am on the registration page
    When I enter "john@example.com" as email
    And I enter "SecurePass123!" as password
    And I submit the registration form
    Then I should see "Welcome, john@example.com"
    And I should receive a verification email

// step-definitions/registration.steps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('@playwright/test');

Given('I am on the registration page', async function() {
  await this.page.goto('/register');
});

When('I enter {string} as email', async function(email) {
  await this.page.fill('[data-testid="email-input"]', email);
  this.email = email;
});

When('I enter {string} as password', async function(password) {
  await this.page.fill('[data-testid="password-input"]', password);
});

When('I submit the registration form', async function() {
  await this.page.click('[data-testid="register-button"]');
  await this.page.waitForNavigation();
});

Then('I should see {string}', async function(text) {
  const content = await this.page.textContent('body');
  expect(content).toContain(text);
});

Then('I should receive a verification email', async function() {
  // Check email service mock or test mailbox
  const emails = await this.emailService.getEmailsFor(this.email);
  expect(emails).toHaveLength(1);
  expect(emails[0].subject).toContain('Verify');
});
```

## Test Data Builder Examples

### Python

```python
# builders.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
import uuid


@dataclass
class User:
    id: str
    email: str
    name: str
    role: str
    created_at: datetime
    is_verified: bool


class UserBuilder:
    """Fluent builder for creating User test objects."""

    def __init__(self):
        self._id = str(uuid.uuid4())
        self._email = "user@example.com"
        self._name = "Test User"
        self._role = "member"
        self._created_at = datetime.now()
        self._is_verified = True

    def with_id(self, id: str) -> 'UserBuilder':
        self._id = id
        return self

    def with_email(self, email: str) -> 'UserBuilder':
        self._email = email
        return self

    def with_name(self, name: str) -> 'UserBuilder':
        self._name = name
        return self

    def as_admin(self) -> 'UserBuilder':
        self._role = "admin"
        return self

    def as_guest(self) -> 'UserBuilder':
        self._role = "guest"
        self._is_verified = False
        return self

    def unverified(self) -> 'UserBuilder':
        self._is_verified = False
        return self

    def created_days_ago(self, days: int) -> 'UserBuilder':
        self._created_at = datetime.now() - timedelta(days=days)
        return self

    def build(self) -> User:
        return User(
            id=self._id,
            email=self._email,
            name=self._name,
            role=self._role,
            created_at=self._created_at,
            is_verified=self._is_verified
        )


# Usage in tests
class TestUserPermissions:
    def test_admin_can_delete_users(self):
        # Builder makes it clear what's important for this test
        admin = UserBuilder().as_admin().build()
        target = UserBuilder().with_email("target@example.com").build()

        result = permission_service.can_delete(admin, target)

        assert result is True

    def test_unverified_users_have_limited_access(self):
        user = UserBuilder().unverified().build()

        result = permission_service.can_post_content(user)

        assert result is False
```

### TypeScript

```typescript
// builders/OrderBuilder.ts
import { v4 as uuidv4 } from 'uuid';

interface OrderItem {
  productId: string;
  name: string;
  quantity: number;
  price: number;
}

interface Order {
  id: string;
  customerId: string;
  items: OrderItem[];
  status: 'pending' | 'paid' | 'shipped' | 'delivered';
  total: number;
  createdAt: Date;
}

export class OrderBuilder {
  private order: Order;

  constructor() {
    this.order = {
      id: uuidv4(),
      customerId: uuidv4(),
      items: [],
      status: 'pending',
      total: 0,
      createdAt: new Date(),
    };
  }

  withId(id: string): OrderBuilder {
    this.order.id = id;
    return this;
  }

  forCustomer(customerId: string): OrderBuilder {
    this.order.customerId = customerId;
    return this;
  }

  withItem(item: Partial<OrderItem>): OrderBuilder {
    const fullItem: OrderItem = {
      productId: item.productId ?? uuidv4(),
      name: item.name ?? 'Test Product',
      quantity: item.quantity ?? 1,
      price: item.price ?? 10.00,
    };
    this.order.items.push(fullItem);
    this.order.total += fullItem.price * fullItem.quantity;
    return this;
  }

  withItems(count: number): OrderBuilder {
    for (let i = 0; i < count; i++) {
      this.withItem({ name: `Product ${i + 1}`, price: 10 + i });
    }
    return this;
  }

  asPaid(): OrderBuilder {
    this.order.status = 'paid';
    return this;
  }

  asShipped(): OrderBuilder {
    this.order.status = 'shipped';
    return this;
  }

  createdDaysAgo(days: number): OrderBuilder {
    this.order.createdAt = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
    return this;
  }

  build(): Order {
    return { ...this.order, items: [...this.order.items] };
  }
}

// Usage in tests
describe('OrderService', () => {
  it('should calculate shipping for paid orders', () => {
    // Builder clearly shows: paid order with 3 items
    const order = new OrderBuilder()
      .withItems(3)
      .asPaid()
      .build();

    const shipping = orderService.calculateShipping(order);

    expect(shipping).toBe(5.99);
  });

  it('should apply discount for orders over $100', () => {
    const order = new OrderBuilder()
      .withItem({ price: 60 })
      .withItem({ price: 50 })
      .asPaid()
      .build();

    const discount = orderService.calculateDiscount(order);

    expect(discount).toBe(11); // 10% of $110
  });
});
```

## Object Mother Examples

### Python

```python
# mothers.py
from builders import UserBuilder, OrderBuilder
from datetime import datetime, timedelta


class UserMother:
    """Factory for common user scenarios."""

    @staticmethod
    def admin() -> UserBuilder:
        return UserBuilder().as_admin().with_name("Admin User")

    @staticmethod
    def regular_member() -> UserBuilder:
        return UserBuilder().with_name("Regular Member")

    @staticmethod
    def new_unverified_user() -> UserBuilder:
        return UserBuilder().unverified().created_days_ago(0)

    @staticmethod
    def long_time_customer() -> UserBuilder:
        return UserBuilder().created_days_ago(365).with_name("Loyal Customer")

    @staticmethod
    def suspended_user() -> UserBuilder:
        return (UserBuilder()
                .with_role("suspended")
                .with_name("Suspended User"))


class OrderMother:
    """Factory for common order scenarios."""

    @staticmethod
    def pending_order() -> OrderBuilder:
        return OrderBuilder().with_items(2)

    @staticmethod
    def paid_order() -> OrderBuilder:
        return OrderBuilder().with_items(2).as_paid()

    @staticmethod
    def high_value_order() -> OrderBuilder:
        """Order qualifying for free shipping (>$100)."""
        return (OrderBuilder()
                .with_item({"name": "Premium Product", "price": 150})
                .as_paid())

    @staticmethod
    def old_unshipped_order() -> OrderBuilder:
        """Order that's been pending for too long."""
        return OrderBuilder().with_items(1).created_days_ago(30)


# Usage in tests - combining Object Mother with Builder
class TestOrderShipping:
    def test_free_shipping_for_high_value_orders(self):
        order = OrderMother.high_value_order().build()

        shipping = shipping_service.calculate(order)

        assert shipping == Decimal("0.00")

    def test_expedited_shipping_available_for_members(self):
        customer = UserMother.long_time_customer().build()
        order = OrderMother.paid_order().for_customer(customer.id).build()

        options = shipping_service.get_options(order, customer)

        assert "expedited" in [o.type for o in options]
```

## Page Object Model Examples

### Playwright (TypeScript)

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
    this.forgotPasswordLink = page.locator('[data-testid="forgot-password"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/login');
  }

  async login(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async getErrorText(): Promise<string> {
    return await this.errorMessage.textContent() ?? '';
  }

  async clickForgotPassword(): Promise<ForgotPasswordPage> {
    await this.forgotPasswordLink.click();
    return new ForgotPasswordPage(this.page);
  }
}

// pages/DashboardPage.ts
import { Page, Locator } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.locator('[data-testid="welcome-message"]');
    this.userMenu = page.locator('[data-testid="user-menu"]');
    this.logoutButton = page.locator('[data-testid="logout-button"]');
  }

  async getWelcomeText(): Promise<string> {
    return await this.welcomeMessage.textContent() ?? '';
  }

  async logout(): Promise<LoginPage> {
    await this.userMenu.click();
    await this.logoutButton.click();
    return new LoginPage(this.page);
  }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

test.describe('Login Flow', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    await loginPage.login('user@example.com', 'validpassword');

    const dashboardPage = new DashboardPage(page);
    const welcome = await dashboardPage.getWelcomeText();
    expect(welcome).toContain('Welcome');
  });

  test('invalid credentials show error message', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    await loginPage.login('user@example.com', 'wrongpassword');

    const error = await loginPage.getErrorText();
    expect(error).toBe('Invalid email or password');
  });
});
```

### Cypress

```typescript
// cypress/pages/CheckoutPage.ts
export class CheckoutPage {
  visit() {
    cy.visit('/checkout');
    return this;
  }

  fillShippingAddress(address: {
    name: string;
    street: string;
    city: string;
    zip: string;
  }) {
    cy.get('[data-testid="shipping-name"]').type(address.name);
    cy.get('[data-testid="shipping-street"]').type(address.street);
    cy.get('[data-testid="shipping-city"]').type(address.city);
    cy.get('[data-testid="shipping-zip"]').type(address.zip);
    return this;
  }

  selectPaymentMethod(method: 'credit' | 'paypal') {
    cy.get(`[data-testid="payment-${method}"]`).click();
    return this;
  }

  enterCreditCard(card: { number: string; expiry: string; cvv: string }) {
    cy.get('[data-testid="card-number"]').type(card.number);
    cy.get('[data-testid="card-expiry"]').type(card.expiry);
    cy.get('[data-testid="card-cvv"]').type(card.cvv);
    return this;
  }

  placeOrder() {
    cy.get('[data-testid="place-order-button"]').click();
    return new OrderConfirmationPage();
  }

  getTotal(): Cypress.Chainable<string> {
    return cy.get('[data-testid="order-total"]').invoke('text');
  }
}

// cypress/e2e/checkout.cy.ts
import { CheckoutPage } from '../pages/CheckoutPage';

describe('Checkout Process', () => {
  it('completes checkout with credit card', () => {
    const checkout = new CheckoutPage();

    checkout
      .visit()
      .fillShippingAddress({
        name: 'John Doe',
        street: '123 Main St',
        city: 'New York',
        zip: '10001',
      })
      .selectPaymentMethod('credit')
      .enterCreditCard({
        number: '4111111111111111',
        expiry: '12/25',
        cvv: '123',
      });

    const confirmation = checkout.placeOrder();

    confirmation.getOrderNumber().should('match', /^ORD-\d+$/);
    confirmation.getStatus().should('eq', 'confirmed');
  });
});
```

## Property-Based Testing Examples

### Python (Hypothesis)

```python
# test_serialization.py
from hypothesis import given, strategies as st, settings
import json


class JsonSerializer:
    @staticmethod
    def serialize(data):
        return json.dumps(data)

    @staticmethod
    def deserialize(text):
        return json.loads(text)


# Round-trip property: deserialize(serialize(x)) == x
@given(st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=20
))
def test_json_roundtrip(data):
    """Any valid JSON data should survive a serialize-deserialize cycle."""
    serialized = JsonSerializer.serialize(data)
    deserialized = JsonSerializer.deserialize(serialized)
    assert data == deserialized


# Property: sorting should be idempotent
@given(st.lists(st.integers()))
def test_sorting_idempotent(numbers):
    """Sorting twice should give same result as sorting once."""
    once = sorted(numbers)
    twice = sorted(sorted(numbers))
    assert once == twice


# Property: sorted list maintains all elements
@given(st.lists(st.integers()))
def test_sorting_preserves_elements(numbers):
    """Sorting should not add or remove elements."""
    result = sorted(numbers)
    assert len(result) == len(numbers)
    assert sorted(result) == sorted(numbers)


# Business logic property
@given(
    balance=st.decimals(min_value=0, max_value=10000),
    withdrawal=st.decimals(min_value=0, max_value=10000)
)
def test_withdrawal_never_exceeds_balance(balance, withdrawal):
    """Account balance should never go negative from a withdrawal."""
    account = Account(balance=balance)

    account.withdraw(withdrawal)

    assert account.balance >= 0


# Custom strategy for domain objects
@st.composite
def valid_email(draw):
    """Generate valid email addresses."""
    local = draw(st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N')),
        min_size=1,
        max_size=20
    ))
    domain = draw(st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N')),
        min_size=1,
        max_size=10
    ))
    tld = draw(st.sampled_from(['com', 'org', 'net', 'io']))
    return f"{local}@{domain}.{tld}"


@given(email=valid_email())
def test_email_validation_accepts_valid_emails(email):
    """Email validator should accept all valid email formats."""
    assert validate_email(email) is True
```

### JavaScript (fast-check)

```javascript
// test/property-based.test.js
import fc from 'fast-check';

describe('Array utilities', () => {
  it('reverse of reverse equals original', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const reversed = [...arr].reverse().reverse();
        expect(reversed).toEqual(arr);
      })
    );
  });

  it('filter does not increase length', () => {
    fc.assert(
      fc.property(
        fc.array(fc.integer()),
        fc.func(fc.boolean()),
        (arr, predicate) => {
          const filtered = arr.filter(predicate);
          return filtered.length <= arr.length;
        }
      )
    );
  });

  it('map preserves length', () => {
    fc.assert(
      fc.property(
        fc.array(fc.integer()),
        fc.func(fc.integer()),
        (arr, mapper) => {
          const mapped = arr.map(mapper);
          return mapped.length === arr.length;
        }
      )
    );
  });
});

describe('String utilities', () => {
  it('trim is idempotent', () => {
    fc.assert(
      fc.property(fc.string(), (str) => {
        expect(str.trim().trim()).toBe(str.trim());
      })
    );
  });

  it('split then join restores original for single char delimiter', () => {
    fc.assert(
      fc.property(
        fc.string(),
        fc.char().filter(c => c !== ''),
        (str, delimiter) => {
          // Only valid when string doesn't contain delimiter at edges
          if (!str.startsWith(delimiter) && !str.endsWith(delimiter)) {
            const restored = str.split(delimiter).join(delimiter);
            expect(restored).toBe(str);
          }
        }
      )
    );
  });
});

describe('Calculator', () => {
  it('addition is commutative', () => {
    fc.assert(
      fc.property(fc.integer(), fc.integer(), (a, b) => {
        expect(add(a, b)).toBe(add(b, a));
      })
    );
  });

  it('multiplication distributes over addition', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: -1000, max: 1000 }),
        fc.integer({ min: -1000, max: 1000 }),
        fc.integer({ min: -1000, max: 1000 }),
        (a, b, c) => {
          // a * (b + c) === a * b + a * c
          expect(multiply(a, add(b, c))).toBe(add(multiply(a, b), multiply(a, c)));
        }
      )
    );
  });
});
```

## Test Isolation Examples

### Database Isolation (Python/pytest)

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test with transaction rollback."""
    engine = create_engine("postgresql://test@localhost/testdb")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start transaction
    session.begin_nested()

    yield session

    # Rollback transaction - no data persists
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def clean_tables(db_session):
    """Alternative: truncate tables between tests."""
    yield

    # Clean up after test
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


# Usage in tests
class TestUserRepository:
    def test_create_user(self, db_session):
        repo = UserRepository(db_session)

        user = repo.create({"email": "test@example.com", "name": "Test"})

        assert user.id is not None
        # Data is automatically rolled back after test

    def test_find_by_email(self, db_session):
        repo = UserRepository(db_session)
        repo.create({"email": "find@example.com", "name": "Find Me"})

        found = repo.find_by_email("find@example.com")

        assert found is not None
        assert found.name == "Find Me"
```

### Mock Isolation (JavaScript)

```javascript
// tests/service.test.js
import { jest } from '@jest/globals';
import { OrderService } from '../services/OrderService';
import { PaymentGateway } from '../gateways/PaymentGateway';
import { EmailService } from '../services/EmailService';

describe('OrderService', () => {
  let orderService;
  let paymentGateway;
  let emailService;

  beforeEach(() => {
    // Fresh mocks for each test - complete isolation
    paymentGateway = {
      charge: jest.fn(),
      refund: jest.fn(),
    };
    emailService = {
      sendConfirmation: jest.fn(),
      sendRefundNotification: jest.fn(),
    };
    orderService = new OrderService(paymentGateway, emailService);
  });

  afterEach(() => {
    // Explicit cleanup (optional with beforeEach recreation)
    jest.clearAllMocks();
  });

  it('should process payment and send confirmation', async () => {
    paymentGateway.charge.mockResolvedValue({ transactionId: 'tx-123' });
    emailService.sendConfirmation.mockResolvedValue(true);

    await orderService.complete(orderId);

    expect(paymentGateway.charge).toHaveBeenCalledTimes(1);
    expect(emailService.sendConfirmation).toHaveBeenCalledTimes(1);
  });

  it('should not send email if payment fails', async () => {
    paymentGateway.charge.mockRejectedValue(new Error('Card declined'));

    await expect(orderService.complete(orderId)).rejects.toThrow();

    expect(emailService.sendConfirmation).not.toHaveBeenCalled();
  });
});
```

## Flaky Test Prevention Examples

### Waiting Strategies (Playwright)

```typescript
// BAD: Fixed sleep (flaky)
test('bad example with sleep', async ({ page }) => {
  await page.click('[data-testid="load-data"]');
  await page.waitForTimeout(3000); // Don't do this!
  const data = await page.textContent('[data-testid="data-container"]');
  expect(data).toContain('Loaded');
});

// GOOD: Wait for element
test('good example with explicit wait', async ({ page }) => {
  await page.click('[data-testid="load-data"]');
  await page.waitForSelector('[data-testid="data-container"]:has-text("Loaded")');
  const data = await page.textContent('[data-testid="data-container"]');
  expect(data).toContain('Loaded');
});

// GOOD: Wait for network
test('wait for API response', async ({ page }) => {
  const responsePromise = page.waitForResponse(
    (resp) => resp.url().includes('/api/data') && resp.status() === 200
  );

  await page.click('[data-testid="fetch-button"]');
  await responsePromise;

  // Now safe to check UI
  await expect(page.locator('[data-testid="result"]')).toBeVisible();
});

// GOOD: Custom polling
test('wait for condition with polling', async ({ page }) => {
  await page.click('[data-testid="start-process"]');

  await expect(async () => {
    const status = await page.textContent('[data-testid="status"]');
    expect(status).toBe('Complete');
  }).toPass({ timeout: 10000 });
});
```

### Deterministic Data (Python)

```python
# BAD: Non-deterministic (flaky)
def test_bad_random_data():
    import random
    value = random.randint(1, 100)
    result = process(value)
    # This might fail randomly!
    assert result > 0

# GOOD: Seeded random for reproducibility
def test_good_seeded_random():
    import random
    random.seed(42)  # Fixed seed = reproducible
    value = random.randint(1, 100)
    result = process(value)
    assert result == expected_for_seed_42

# GOOD: Use property-based testing with shrinking
from hypothesis import given, strategies as st, settings

@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=1, max_value=100))
def test_property_based(value):
    result = process(value)
    assert result > 0  # Hypothesis will find counterexample if exists
```

### Time-Independent Tests

```python
# BAD: Depends on current time (flaky at midnight)
def test_bad_time_dependent():
    user = User(created_at=datetime.now())
    assert user.is_new()  # Might fail at 23:59:59!

# GOOD: Inject time dependency
def test_good_injected_time():
    fixed_time = datetime(2024, 1, 15, 12, 0, 0)
    user = User(created_at=fixed_time)

    # Use freezegun or manual injection
    with freeze_time(fixed_time + timedelta(hours=1)):
        assert user.is_new()  # Created < 24 hours ago

# GOOD: Use relative assertions
def test_relative_time_assertion():
    before = datetime.now()
    user = create_user()
    after = datetime.now()

    assert before <= user.created_at <= after
```
