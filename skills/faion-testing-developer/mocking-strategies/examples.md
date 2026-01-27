# Mocking Strategies Examples

Real-world examples demonstrating good and bad mocking practices across Python, JavaScript/TypeScript, and Go.

---

## Case Study 1: Mocking External APIs

### Scenario

A `UserService` fetches user data from an external API and caches results.

### Python: Good Example

```python
import pytest
import responses
from unittest.mock import AsyncMock
from myapp.services import UserService
from myapp.cache import RedisCache


class TestUserService:
    """Good: Mock at HTTP boundary, not internal methods."""

    @responses.activate
    def test_get_user_success(self):
        """Test successful API response."""
        # Arrange: Mock HTTP response
        responses.add(
            responses.GET,
            "https://api.users.com/v1/users/123",
            json={"id": "123", "name": "John Doe", "email": "john@example.com"},
            status=200
        )

        service = UserService(base_url="https://api.users.com/v1")

        # Act
        user = service.get_user("123")

        # Assert: Verify result, not internals
        assert user.id == "123"
        assert user.name == "John Doe"
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_user_not_found(self):
        """Test 404 handling."""
        responses.add(
            responses.GET,
            "https://api.users.com/v1/users/999",
            json={"error": "User not found"},
            status=404
        )

        service = UserService(base_url="https://api.users.com/v1")

        # Assert: Verify exception handling
        with pytest.raises(UserNotFoundError):
            service.get_user("999")

    @responses.activate
    def test_get_user_retries_on_500(self):
        """Test retry logic on server errors."""
        # First call fails, second succeeds
        responses.add(responses.GET, "https://api.users.com/v1/users/123", status=500)
        responses.add(
            responses.GET,
            "https://api.users.com/v1/users/123",
            json={"id": "123", "name": "John"},
            status=200
        )

        service = UserService(base_url="https://api.users.com/v1", max_retries=2)
        user = service.get_user("123")

        assert user.name == "John"
        assert len(responses.calls) == 2  # Verify retry happened
```

### Python: Bad Example

```python
# BAD: Over-mocking internal implementation
def test_get_user_bad(mocker):
    # Mocking internal methods couples test to implementation
    mock_build_url = mocker.patch.object(UserService, '_build_url')
    mock_build_url.return_value = "https://api.users.com/v1/users/123"

    mock_parse_response = mocker.patch.object(UserService, '_parse_response')
    mock_parse_response.return_value = User(id="123", name="John")

    mock_validate = mocker.patch.object(UserService, '_validate_user')
    mock_validate.return_value = True

    # This test will break on any refactoring!
    service = UserService(base_url="https://api.users.com/v1")
    user = service.get_user("123")

    # Asserting on implementation details, not behavior
    mock_build_url.assert_called_once_with("/users/123")
    mock_parse_response.assert_called_once()
    mock_validate.assert_called_once()
```

**Why it's bad:**
- Mocks internal methods, not external boundaries
- Test breaks on refactoring even if behavior is correct
- Doesn't test actual HTTP handling
- Complex setup for simple functionality

---

## Case Study 2: Mocking Database Operations

### Scenario

An `OrderRepository` saves orders to a database and publishes events.

### Python: Using Fakes (Preferred for Repositories)

```python
from typing import Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pytest


@dataclass
class Order:
    id: str
    user_id: str
    total: float
    status: str = "pending"


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def find_by_user(self, user_id: str) -> list[Order]:
        pass


class FakeOrderRepository(OrderRepository):
    """Fake implementation for testing - has real behavior."""

    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._user_orders: Dict[str, list[str]] = {}

    def save(self, order: Order) -> Order:
        self._orders[order.id] = order
        if order.user_id not in self._user_orders:
            self._user_orders[order.user_id] = []
        if order.id not in self._user_orders[order.user_id]:
            self._user_orders[order.user_id].append(order.id)
        return order

    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def find_by_user(self, user_id: str) -> list[Order]:
        order_ids = self._user_orders.get(user_id, [])
        return [self._orders[oid] for oid in order_ids]

    def clear(self):
        """Helper for test cleanup."""
        self._orders.clear()
        self._user_orders.clear()


class OrderService:
    def __init__(self, repository: OrderRepository, event_publisher):
        self._repo = repository
        self._publisher = event_publisher

    def create_order(self, user_id: str, total: float) -> Order:
        order = Order(id=f"order_{len(self._repo._orders)}", user_id=user_id, total=total)
        saved = self._repo.save(order)
        self._publisher.publish("order.created", {"order_id": saved.id})
        return saved


@pytest.fixture
def fake_repo():
    return FakeOrderRepository()


@pytest.fixture
def mock_publisher(mocker):
    return mocker.Mock()


class TestOrderService:
    """Good: Fake for repository (state), Mock for events (behavior)."""

    def test_create_order_saves_to_repository(self, fake_repo, mock_publisher):
        service = OrderService(fake_repo, mock_publisher)

        order = service.create_order(user_id="user_123", total=99.99)

        # Assert on state (fake repository)
        saved_order = fake_repo.find_by_id(order.id)
        assert saved_order is not None
        assert saved_order.total == 99.99
        assert saved_order.user_id == "user_123"

    def test_create_order_publishes_event(self, fake_repo, mock_publisher):
        service = OrderService(fake_repo, mock_publisher)

        order = service.create_order(user_id="user_123", total=99.99)

        # Assert on behavior (event publishing)
        mock_publisher.publish.assert_called_once_with(
            "order.created",
            {"order_id": order.id}
        )

    def test_find_orders_by_user(self, fake_repo, mock_publisher):
        # Arrange: Pre-populate fake
        fake_repo.save(Order(id="order_1", user_id="user_123", total=50.0))
        fake_repo.save(Order(id="order_2", user_id="user_123", total=75.0))
        fake_repo.save(Order(id="order_3", user_id="user_456", total=100.0))

        # Act
        orders = fake_repo.find_by_user("user_123")

        # Assert
        assert len(orders) == 2
        assert all(o.user_id == "user_123" for o in orders)
```

**Why fakes are better here:**
- Real query logic tested (find_by_user)
- No need to set up mock return values for every test
- Catches logic errors that mocks would miss

---

## Case Study 3: Mocking Time-Dependent Code

### Scenario

A `SubscriptionService` checks if subscriptions are expired.

### Python: Using freezegun

```python
from datetime import datetime, timedelta
from dataclasses import dataclass
from freezegun import freeze_time
import pytest


@dataclass
class Subscription:
    id: str
    user_id: str
    plan: str
    expires_at: datetime


class SubscriptionService:
    def __init__(self, repository):
        self._repo = repository

    def is_active(self, subscription_id: str) -> bool:
        sub = self._repo.find_by_id(subscription_id)
        if not sub:
            return False
        return sub.expires_at > datetime.now()

    def days_until_expiry(self, subscription_id: str) -> int:
        sub = self._repo.find_by_id(subscription_id)
        if not sub:
            return 0
        delta = sub.expires_at - datetime.now()
        return max(0, delta.days)

    def renew(self, subscription_id: str, days: int = 30) -> Subscription:
        sub = self._repo.find_by_id(subscription_id)
        sub.expires_at = datetime.now() + timedelta(days=days)
        return self._repo.save(sub)


class TestSubscriptionService:
    """Good: Freeze time for deterministic tests."""

    @freeze_time("2025-01-15 10:00:00")
    def test_subscription_is_active(self, mocker):
        mock_repo = mocker.Mock()
        mock_repo.find_by_id.return_value = Subscription(
            id="sub_123",
            user_id="user_456",
            plan="pro",
            expires_at=datetime(2025, 2, 15, 10, 0, 0)  # 1 month in future
        )

        service = SubscriptionService(mock_repo)

        assert service.is_active("sub_123") is True

    @freeze_time("2025-01-15 10:00:00")
    def test_subscription_is_expired(self, mocker):
        mock_repo = mocker.Mock()
        mock_repo.find_by_id.return_value = Subscription(
            id="sub_123",
            user_id="user_456",
            plan="pro",
            expires_at=datetime(2025, 1, 10, 10, 0, 0)  # 5 days in past
        )

        service = SubscriptionService(mock_repo)

        assert service.is_active("sub_123") is False

    @freeze_time("2025-01-15 10:00:00")
    def test_days_until_expiry(self, mocker):
        mock_repo = mocker.Mock()
        mock_repo.find_by_id.return_value = Subscription(
            id="sub_123",
            user_id="user_456",
            plan="pro",
            expires_at=datetime(2025, 1, 25, 10, 0, 0)  # 10 days in future
        )

        service = SubscriptionService(mock_repo)

        assert service.days_until_expiry("sub_123") == 10

    @freeze_time("2025-01-15 10:00:00")
    def test_renew_extends_subscription(self, mocker):
        mock_repo = mocker.Mock()
        original_sub = Subscription(
            id="sub_123",
            user_id="user_456",
            plan="pro",
            expires_at=datetime(2025, 1, 20, 10, 0, 0)
        )
        mock_repo.find_by_id.return_value = original_sub
        mock_repo.save.return_value = original_sub

        service = SubscriptionService(mock_repo)
        renewed = service.renew("sub_123", days=30)

        # New expiry should be 30 days from frozen "now"
        expected_expiry = datetime(2025, 2, 14, 10, 0, 0)
        assert renewed.expires_at == expected_expiry
```

---

## Case Study 4: TypeScript/Jest Mocking

### Scenario

A `PaymentService` processes payments via Stripe API.

### TypeScript: Good Example

```typescript
import { PaymentService } from './payment-service';
import { StripeClient } from './stripe-client';
import { OrderRepository } from './order-repository';

// Mock the module
jest.mock('./stripe-client');

describe('PaymentService', () => {
  let paymentService: PaymentService;
  let mockStripeClient: jest.Mocked<StripeClient>;
  let mockOrderRepo: jest.Mocked<OrderRepository>;

  beforeEach(() => {
    jest.clearAllMocks();

    mockStripeClient = {
      createPaymentIntent: jest.fn(),
      confirmPayment: jest.fn(),
      refund: jest.fn(),
    } as jest.Mocked<StripeClient>;

    mockOrderRepo = {
      findById: jest.fn(),
      save: jest.fn(),
    } as jest.Mocked<OrderRepository>;

    paymentService = new PaymentService(mockStripeClient, mockOrderRepo);
  });

  describe('processPayment', () => {
    it('should create payment intent and update order', async () => {
      // Arrange
      const order = { id: 'order_123', total: 99.99, status: 'pending' };
      mockOrderRepo.findById.mockResolvedValue(order);
      mockStripeClient.createPaymentIntent.mockResolvedValue({
        id: 'pi_123',
        status: 'succeeded',
        amount: 9999,
      });
      mockOrderRepo.save.mockResolvedValue({ ...order, status: 'paid' });

      // Act
      const result = await paymentService.processPayment('order_123');

      // Assert on outcome
      expect(result.status).toBe('paid');

      // Assert on critical behavior (payment was made)
      expect(mockStripeClient.createPaymentIntent).toHaveBeenCalledWith({
        amount: 9999,  // Cents
        currency: 'usd',
        metadata: { orderId: 'order_123' },
      });
    });

    it('should handle payment failure gracefully', async () => {
      // Arrange
      const order = { id: 'order_123', total: 99.99, status: 'pending' };
      mockOrderRepo.findById.mockResolvedValue(order);
      mockStripeClient.createPaymentIntent.mockRejectedValue(
        new Error('Card declined')
      );

      // Act & Assert
      await expect(paymentService.processPayment('order_123'))
        .rejects.toThrow('Payment failed: Card declined');

      // Order should NOT be marked as paid
      expect(mockOrderRepo.save).not.toHaveBeenCalled();
    });

    it('should throw if order not found', async () => {
      mockOrderRepo.findById.mockResolvedValue(null);

      await expect(paymentService.processPayment('nonexistent'))
        .rejects.toThrow('Order not found');

      expect(mockStripeClient.createPaymentIntent).not.toHaveBeenCalled();
    });
  });

  describe('refundPayment', () => {
    it('should refund and update order status', async () => {
      const order = {
        id: 'order_123',
        total: 99.99,
        status: 'paid',
        paymentIntentId: 'pi_123',
      };
      mockOrderRepo.findById.mockResolvedValue(order);
      mockStripeClient.refund.mockResolvedValue({ id: 'ref_123', status: 'succeeded' });
      mockOrderRepo.save.mockResolvedValue({ ...order, status: 'refunded' });

      const result = await paymentService.refundPayment('order_123');

      expect(result.status).toBe('refunded');
      expect(mockStripeClient.refund).toHaveBeenCalledWith('pi_123');
    });
  });
});
```

### TypeScript: Using jest.spyOn for Partial Mocking

```typescript
import { EmailService } from './email-service';

describe('EmailService with partial mocking', () => {
  it('should format email but skip actual sending', async () => {
    const service = new EmailService();

    // Spy on send method, mock its implementation
    const sendSpy = jest.spyOn(service, 'send').mockResolvedValue({ sent: true });

    // formatAndSend is the method under test (real implementation)
    const result = await service.formatAndSend({
      to: 'user@example.com',
      template: 'welcome',
      data: { name: 'John' },
    });

    // Real formatting logic ran
    expect(sendSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        to: 'user@example.com',
        subject: 'Welcome, John!',  // Formatted by real code
        html: expect.stringContaining('John'),
      })
    );

    // Restore after test
    sendSpy.mockRestore();
  });
});
```

---

## Case Study 5: Go Interface Mocking

### Scenario

A `NotificationService` sends notifications via different channels.

### Go: Good Example with Interfaces

```go
package notification

import (
    "context"
    "errors"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

// Define interfaces at consumer
type EmailSender interface {
    Send(ctx context.Context, to, subject, body string) error
}

type SMSSender interface {
    Send(ctx context.Context, phone, message string) error
}

type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

// Notification service
type NotificationService struct {
    email EmailSender
    sms   SMSSender
    users UserRepository
}

func NewNotificationService(email EmailSender, sms SMSSender, users UserRepository) *NotificationService {
    return &NotificationService{email: email, sms: sms, users: users}
}

func (s *NotificationService) NotifyUser(ctx context.Context, userID, message string) error {
    user, err := s.users.FindByID(ctx, userID)
    if err != nil {
        return err
    }

    if user.EmailVerified {
        if err := s.email.Send(ctx, user.Email, "Notification", message); err != nil {
            return err
        }
    }

    if user.PhoneVerified && user.Phone != "" {
        if err := s.sms.Send(ctx, user.Phone, message); err != nil {
            return err
        }
    }

    return nil
}

// Manual mocks with function properties
type MockEmailSender struct {
    SendFn func(ctx context.Context, to, subject, body string) error
    Calls  []EmailCall
}

type EmailCall struct {
    To, Subject, Body string
}

func (m *MockEmailSender) Send(ctx context.Context, to, subject, body string) error {
    m.Calls = append(m.Calls, EmailCall{To: to, Subject: subject, Body: body})
    if m.SendFn != nil {
        return m.SendFn(ctx, to, subject, body)
    }
    return nil
}

type MockSMSSender struct {
    SendFn func(ctx context.Context, phone, message string) error
    Calls  []SMSCall
}

type SMSCall struct {
    Phone, Message string
}

func (m *MockSMSSender) Send(ctx context.Context, phone, message string) error {
    m.Calls = append(m.Calls, SMSCall{Phone: phone, Message: message})
    if m.SendFn != nil {
        return m.SendFn(ctx, phone, message)
    }
    return nil
}

type MockUserRepository struct {
    Users map[string]*User
}

func (m *MockUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    user, ok := m.Users[id]
    if !ok {
        return nil, errors.New("user not found")
    }
    return user, nil
}

// Tests
func TestNotificationService_NotifyUser(t *testing.T) {
    t.Run("sends email when email verified", func(t *testing.T) {
        mockEmail := &MockEmailSender{}
        mockSMS := &MockSMSSender{}
        mockUsers := &MockUserRepository{
            Users: map[string]*User{
                "user_123": {
                    ID:            "user_123",
                    Email:         "john@example.com",
                    EmailVerified: true,
                    PhoneVerified: false,
                },
            },
        }

        service := NewNotificationService(mockEmail, mockSMS, mockUsers)
        err := service.NotifyUser(context.Background(), "user_123", "Hello!")

        require.NoError(t, err)
        assert.Len(t, mockEmail.Calls, 1)
        assert.Equal(t, "john@example.com", mockEmail.Calls[0].To)
        assert.Equal(t, "Hello!", mockEmail.Calls[0].Body)
        assert.Len(t, mockSMS.Calls, 0)  // SMS not sent
    })

    t.Run("sends both when both verified", func(t *testing.T) {
        mockEmail := &MockEmailSender{}
        mockSMS := &MockSMSSender{}
        mockUsers := &MockUserRepository{
            Users: map[string]*User{
                "user_123": {
                    ID:            "user_123",
                    Email:         "john@example.com",
                    EmailVerified: true,
                    Phone:         "+1234567890",
                    PhoneVerified: true,
                },
            },
        }

        service := NewNotificationService(mockEmail, mockSMS, mockUsers)
        err := service.NotifyUser(context.Background(), "user_123", "Hello!")

        require.NoError(t, err)
        assert.Len(t, mockEmail.Calls, 1)
        assert.Len(t, mockSMS.Calls, 1)
        assert.Equal(t, "+1234567890", mockSMS.Calls[0].Phone)
    })

    t.Run("handles email failure", func(t *testing.T) {
        mockEmail := &MockEmailSender{
            SendFn: func(ctx context.Context, to, subject, body string) error {
                return errors.New("SMTP error")
            },
        }
        mockSMS := &MockSMSSender{}
        mockUsers := &MockUserRepository{
            Users: map[string]*User{
                "user_123": {ID: "user_123", Email: "john@example.com", EmailVerified: true},
            },
        }

        service := NewNotificationService(mockEmail, mockSMS, mockUsers)
        err := service.NotifyUser(context.Background(), "user_123", "Hello!")

        assert.Error(t, err)
        assert.Contains(t, err.Error(), "SMTP error")
    })

    t.Run("returns error when user not found", func(t *testing.T) {
        mockEmail := &MockEmailSender{}
        mockSMS := &MockSMSSender{}
        mockUsers := &MockUserRepository{Users: map[string]*User{}}

        service := NewNotificationService(mockEmail, mockSMS, mockUsers)
        err := service.NotifyUser(context.Background(), "nonexistent", "Hello!")

        assert.Error(t, err)
        assert.Contains(t, err.Error(), "not found")
        assert.Len(t, mockEmail.Calls, 0)  // No email attempted
    })
}
```

---

## Case Study 6: Async Python Mocking

### Scenario

An async `SearchService` queries multiple backends in parallel.

### Python: AsyncMock with pytest-asyncio

```python
import pytest
from unittest.mock import AsyncMock, patch
from myapp.services import SearchService


class TestSearchService:
    """Good: Proper async mocking with AsyncMock."""

    @pytest.mark.asyncio
    async def test_search_aggregates_results(self, mocker):
        # Arrange: Mock async backends
        mock_db = AsyncMock()
        mock_db.search.return_value = [
            {"id": "1", "title": "DB Result 1", "source": "db"},
            {"id": "2", "title": "DB Result 2", "source": "db"},
        ]

        mock_api = AsyncMock()
        mock_api.search.return_value = [
            {"id": "3", "title": "API Result 1", "source": "api"},
        ]

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None  # Cache miss
        mock_cache.set.return_value = None

        service = SearchService(
            db_client=mock_db,
            api_client=mock_api,
            cache=mock_cache
        )

        # Act
        results = await service.search("python testing")

        # Assert: Results aggregated from both sources
        assert len(results) == 3
        assert any(r["source"] == "db" for r in results)
        assert any(r["source"] == "api" for r in results)

        # Assert: Both backends were queried
        mock_db.search.assert_awaited_once_with("python testing")
        mock_api.search.assert_awaited_once_with("python testing")

        # Assert: Results were cached
        mock_cache.set.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_search_returns_cached_results(self, mocker):
        cached_results = [
            {"id": "1", "title": "Cached Result", "source": "cache"},
        ]

        mock_cache = AsyncMock()
        mock_cache.get.return_value = cached_results

        mock_db = AsyncMock()
        mock_api = AsyncMock()

        service = SearchService(
            db_client=mock_db,
            api_client=mock_api,
            cache=mock_cache
        )

        results = await service.search("python testing")

        # Assert: Cached results returned
        assert results == cached_results

        # Assert: Backends NOT queried (cache hit)
        mock_db.search.assert_not_awaited()
        mock_api.search.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_search_handles_backend_failure(self, mocker):
        mock_db = AsyncMock()
        mock_db.search.side_effect = ConnectionError("DB unavailable")

        mock_api = AsyncMock()
        mock_api.search.return_value = [
            {"id": "1", "title": "API Result", "source": "api"},
        ]

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        service = SearchService(
            db_client=mock_db,
            api_client=mock_api,
            cache=mock_cache
        )

        # Act: Should handle failure gracefully
        results = await service.search("python testing")

        # Assert: Returns results from working backend
        assert len(results) == 1
        assert results[0]["source"] == "api"

    @pytest.mark.asyncio
    async def test_search_with_timeout(self, mocker):
        import asyncio

        mock_db = AsyncMock()
        # Simulate slow response
        async def slow_search(query):
            await asyncio.sleep(5)
            return []
        mock_db.search.side_effect = slow_search

        mock_api = AsyncMock()
        mock_api.search.return_value = [{"id": "1", "title": "Fast API Result"}]

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        service = SearchService(
            db_client=mock_db,
            api_client=mock_api,
            cache=mock_cache,
            timeout=1.0  # 1 second timeout
        )

        # Act: Should timeout slow backend
        results = await service.search("python testing")

        # Assert: Only fast results returned
        assert len(results) == 1
        assert results[0]["title"] == "Fast API Result"
```

---

## Anti-Pattern Examples

### What NOT to do

```python
# BAD: Testing mocks instead of behavior
def test_user_service_bad(mocker):
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.return_value = {"id": "123", "name": "John"}

    mock_validator = mocker.Mock()
    mock_validator.validate.return_value = True

    mock_mapper = mocker.Mock()
    mock_mapper.to_dto.return_value = {"id": "123", "displayName": "John"}

    service = UserService(mock_repo, mock_validator, mock_mapper)
    result = service.get_user("123")

    # BAD: Only testing that mocks were called in order
    mock_repo.find_by_id.assert_called_with("123")
    mock_validator.validate.assert_called_once()
    mock_mapper.to_dto.assert_called_once()

    # This test passes but doesn't verify:
    # - Correct data flows through the pipeline
    # - Error handling
    # - Edge cases
```

```python
# BAD: Mocking data structures
def test_with_mocked_list_bad(mocker):
    mock_list = mocker.Mock()
    mock_list.__len__ = mocker.Mock(return_value=3)
    mock_list.__iter__ = mocker.Mock(return_value=iter([1, 2, 3]))

    # Why not just use a real list?
    result = process_items(mock_list)

    # Tests nothing useful
```

```python
# BAD: Mock chain hell
def test_mock_chain_bad(mocker):
    mock = mocker.Mock()
    mock.client.session.request.json.return_value = {"data": "value"}

    # Deeply nested mocks are a code smell
    # Indicates tight coupling in production code
```

---

## Summary: Good vs Bad Mocking

| Good | Bad |
|------|-----|
| Mock external boundaries | Mock internal methods |
| Simple mock setup | Complex mock configuration |
| Assert on outcomes | Assert on every call |
| Use fakes for repositories | Mock data access |
| Freeze time with libraries | Mock datetime manually |
| Interface-based DI | Patching global imports |
| Real data structures | Mocked lists/dicts |
| Cover error scenarios | Only happy path |

---

*These examples demonstrate practical mocking patterns. Adapt them to your specific frameworks and requirements.*
