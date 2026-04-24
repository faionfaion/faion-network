# Unit Test Examples by Language

Practical examples for Python (pytest), JavaScript (Jest/Vitest), Go, and TypeScript.

## Python (pytest)

### Basic Test Structure

```python
import pytest
from decimal import Decimal

class TestPriceCalculator:
    """Tests for PriceCalculator class."""

    def test_calculate_total_single_item(self):
        # Arrange
        calculator = PriceCalculator(tax_rate=Decimal("0.10"))

        # Act
        result = calculator.calculate_total(
            price=Decimal("100.00"),
            quantity=1
        )

        # Assert
        assert result == Decimal("110.00")

    def test_calculate_total_zero_tax(self):
        # Arrange
        calculator = PriceCalculator(tax_rate=Decimal("0.00"))

        # Act
        result = calculator.calculate_total(Decimal("50.00"), 2)

        # Assert
        assert result == Decimal("100.00")
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("user.name@domain.co.uk", True),
    ("invalid", False),
    ("@no-local.com", False),
    ("no-at-sign.com", False),
    ("user@", False),
])
def test_email_validation(email, is_valid):
    result = validate_email(email)
    assert result == is_valid


# Named test cases for better output
@pytest.mark.parametrize("a,b,expected", [
    pytest.param(1, 2, 3, id="positive_numbers"),
    pytest.param(-1, 1, 0, id="mixed_signs"),
    pytest.param(0, 0, 0, id="zeros"),
    pytest.param(-5, -3, -8, id="negative_numbers"),
])
def test_addition(a, b, expected):
    assert add(a, b) == expected
```

### Testing Exceptions

```python
def test_withdraw_insufficient_funds_raises_error():
    account = BankAccount(balance=Decimal("100.00"))

    with pytest.raises(InsufficientFundsError) as exc_info:
        account.withdraw(Decimal("150.00"))

    assert exc_info.value.balance == Decimal("100.00")
    assert exc_info.value.amount == Decimal("150.00")
```

### Fixtures

```python
@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(
        id="user-123",
        email="test@example.com",
        name="Test User"
    )

@pytest.fixture
def user_service(sample_user):
    """Create user service with sample data."""
    repo = InMemoryUserRepository()
    repo.add(sample_user)
    return UserService(repo)

def test_find_user_by_id(user_service, sample_user):
    result = user_service.find_by_id(sample_user.id)
    assert result == sample_user
```

### Mocking

```python
from unittest.mock import Mock, patch

def test_with_stub():
    repo = Mock()
    repo.find_by_id.return_value = User(id="123", name="Test")

    service = UserService(repo)
    result = service.get_user("123")

    assert result.name == "Test"

def test_with_mock():
    notifier = Mock()
    service = OrderService(notifier=notifier)

    service.complete_order("order-123")

    notifier.send_notification.assert_called_once_with(
        "order-123", "Order completed"
    )

@patch("mymodule.external_api")
def test_with_patch(mock_api):
    mock_api.fetch.return_value = {"status": "ok"}

    result = process_data()

    assert result.status == "ok"
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch_user():
    service = AsyncUserService()

    result = await service.get_user("user-123")

    assert result.id == "user-123"

@pytest.mark.asyncio
async def test_async_timeout():
    service = SlowService()

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(
            service.slow_operation(),
            timeout=0.1
        )
```

## JavaScript/TypeScript (Jest)

### Basic Test Structure

```typescript
import { describe, it, expect, beforeEach } from '@jest/globals';

describe('OrderService', () => {
  let service: OrderService;

  beforeEach(() => {
    service = new OrderService();
  });

  describe('placeOrder', () => {
    it('should calculate total with tax', () => {
      // Arrange
      const order = { items: [{ price: 100, qty: 2 }] };

      // Act
      const result = service.calculateTotal(order);

      // Assert
      expect(result).toBe(220); // 200 + 10% tax
    });
  });
});
```

### Mocking

```typescript
describe('OrderService', () => {
  let service: OrderService;
  let mockRepository: jest.Mocked<OrderRepository>;
  let mockPaymentGateway: jest.Mocked<PaymentGateway>;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
    };
    mockPaymentGateway = {
      charge: jest.fn(),
    };
    service = new OrderService(mockRepository, mockPaymentGateway);
  });

  it('should save order and process payment', async () => {
    // Arrange
    const order = { items: [], total: 100 };
    mockRepository.save.mockResolvedValue({ id: 'order-1', ...order });
    mockPaymentGateway.charge.mockResolvedValue({ id: 'payment-1' });

    // Act
    const result = await service.placeOrder(order);

    // Assert
    expect(result.orderId).toBe('order-1');
    expect(result.paymentId).toBe('payment-1');
    expect(mockRepository.save).toHaveBeenCalledWith(order);
    expect(mockPaymentGateway.charge).toHaveBeenCalledWith(100);
  });

  it('should throw when payment fails', async () => {
    // Arrange
    mockRepository.save.mockResolvedValue({ id: 'order-1' });
    mockPaymentGateway.charge.mockRejectedValue(new Error('Payment declined'));

    // Act & Assert
    await expect(service.placeOrder({ items: [], total: 100 }))
      .rejects.toThrow('Payment declined');
  });
});
```

### Parametrized Tests (Jest)

```typescript
describe.each([
  { input: 'hello', expected: 'HELLO' },
  { input: 'World', expected: 'WORLD' },
  { input: '', expected: '' },
])('uppercase($input)', ({ input, expected }) => {
  it(`should return ${expected}`, () => {
    expect(input.toUpperCase()).toBe(expected);
  });
});
```

### Vitest Example

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('UserService', () => {
  it('should fetch user from API', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({ id: 1, name: 'John' })
    });
    vi.stubGlobal('fetch', mockFetch);

    const service = new UserService();
    const user = await service.getUser(1);

    expect(user.name).toBe('John');
    expect(mockFetch).toHaveBeenCalledWith('/api/users/1');
  });
});
```

## Go

### Basic Test Structure

```go
package calculator

import "testing"

func TestAdd(t *testing.T) {
    // Arrange
    calc := NewCalculator()

    // Act
    result := calc.Add(2, 3)

    // Assert
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

func TestAdd_NegativeNumbers(t *testing.T) {
    calc := NewCalculator()

    result := calc.Add(-1, -2)

    if result != -3 {
        t.Errorf("Add(-1, -2) = %d; want -3", result)
    }
}
```

### Table-Driven Tests

```go
func TestCalculator_Add(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -2, -3},
        {"mixed signs", -1, 5, 4},
        {"zeros", 0, 0, 0},
    }

    calc := NewCalculator()

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := calc.Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Testing with Testify

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestUserService_GetUser(t *testing.T) {
    // Arrange
    repo := &MockUserRepository{}
    repo.On("FindByID", "123").Return(&User{ID: "123", Name: "John"}, nil)

    service := NewUserService(repo)

    // Act
    user, err := service.GetUser("123")

    // Assert
    require.NoError(t, err)
    assert.Equal(t, "123", user.ID)
    assert.Equal(t, "John", user.Name)
    repo.AssertExpectations(t)
}

func TestUserService_GetUser_NotFound(t *testing.T) {
    repo := &MockUserRepository{}
    repo.On("FindByID", "999").Return(nil, ErrNotFound)

    service := NewUserService(repo)

    user, err := service.GetUser("999")

    assert.Nil(t, user)
    assert.ErrorIs(t, err, ErrNotFound)
}
```

### Mocking with gomock

```go
//go:generate mockgen -source=repository.go -destination=mock_repository.go -package=user

func TestUserService_Create(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := NewMockUserRepository(ctrl)
    mockRepo.EXPECT().
        Save(gomock.Any()).
        Return(&User{ID: "new-123"}, nil)

    service := NewUserService(mockRepo)

    user, err := service.Create("John", "john@example.com")

    require.NoError(t, err)
    assert.Equal(t, "new-123", user.ID)
}
```

## Rust

### Basic Test Structure

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive_numbers() {
        // Arrange
        let calc = Calculator::new();

        // Act
        let result = calc.add(2, 3);

        // Assert
        assert_eq!(result, 5);
    }

    #[test]
    fn test_add_negative_numbers() {
        let calc = Calculator::new();

        let result = calc.add(-1, -2);

        assert_eq!(result, -3);
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_divide_by_zero_panics() {
        let calc = Calculator::new();
        calc.divide(10, 0);
    }
}
```

### Using rstest for Parametrized Tests

```rust
use rstest::rstest;

#[rstest]
#[case(2, 3, 5)]
#[case(-1, -2, -3)]
#[case(0, 0, 0)]
fn test_add(#[case] a: i32, #[case] b: i32, #[case] expected: i32) {
    let calc = Calculator::new();
    assert_eq!(calc.add(a, b), expected);
}
```

## Common Patterns Across Languages

### Factory Functions for Test Data

```python
# Python
def make_user(**overrides):
    defaults = {"id": "123", "name": "Test", "email": "test@example.com"}
    return User(**{**defaults, **overrides})

# Use in tests
user = make_user(name="Custom Name")
```

```typescript
// TypeScript
const makeUser = (overrides: Partial<User> = {}): User => ({
  id: '123',
  name: 'Test',
  email: 'test@example.com',
  ...overrides,
});

// Use in tests
const user = makeUser({ name: 'Custom Name' });
```

### Asserting Collections

```python
# Python
assert set(result) == {1, 2, 3}  # Order doesn't matter
assert result == [1, 2, 3]       # Order matters
assert len(result) == 3
assert 2 in result
```

```typescript
// Jest
expect(result).toEqual([1, 2, 3]);           // Order matters
expect(result).toEqual(expect.arrayContaining([1, 2])); // Subset
expect(result).toHaveLength(3);
expect(result).toContain(2);
```

```go
// Go with testify
assert.ElementsMatch(t, []int{1, 2, 3}, result)  // Order doesn't matter
assert.Equal(t, []int{1, 2, 3}, result)          // Order matters
assert.Len(t, result, 3)
assert.Contains(t, result, 2)
```
