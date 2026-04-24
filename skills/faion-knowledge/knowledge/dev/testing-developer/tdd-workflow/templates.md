# Test Templates

Ready-to-use test templates for pytest, Jest, and Go testing. Copy and adapt for your TDD workflow.

## pytest Templates

### Basic Unit Test

```python
# tests/test_{module}.py
import pytest
from {module} import {Class}


class Test{Class}:
    """Test suite for {Class}."""

    def test_{method}_with_{scenario}(self):
        """Given {precondition}, when {action}, then {expected}."""
        # Arrange
        instance = {Class}()
        input_value = "test_input"

        # Act
        result = instance.{method}(input_value)

        # Assert
        assert result == expected_value
```

### Parametrized Test

```python
import pytest


class TestCalculator:
    """Parametrized test example."""

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1, 1, 2),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
        ],
        ids=["positive", "zeros", "negative_positive", "large_numbers"],
    )
    def test_add(self, a: int, b: int, expected: int):
        """Given two numbers, when added, then return sum."""
        calc = Calculator()

        result = calc.add(a, b)

        assert result == expected
```

### Fixture Template

```python
# tests/conftest.py
import pytest
from database import Database
from user_service import UserService


@pytest.fixture
def db():
    """Provide clean database connection."""
    database = Database(":memory:")
    database.migrate()
    yield database
    database.close()


@pytest.fixture
def user_service(db):
    """Provide UserService with database."""
    return UserService(db)


@pytest.fixture
def sample_user():
    """Provide sample user data."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "user",
    }
```

### Exception Test

```python
import pytest
from validator import Validator, ValidationError


class TestValidator:
    """Exception handling tests."""

    def test_validate_raises_on_empty_input(self):
        """Given empty input, when validated, then raise ValidationError."""
        validator = Validator()

        with pytest.raises(ValidationError) as exc_info:
            validator.validate("")

        assert "cannot be empty" in str(exc_info.value)
        assert exc_info.value.field == "input"

    def test_validate_raises_on_invalid_format(self):
        """Given invalid format, when validated, then raise with details."""
        validator = Validator()

        with pytest.raises(ValidationError, match="invalid format"):
            validator.validate("bad-data")
```

### Mock Template

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from payment_service import PaymentService


class TestPaymentService:
    """Mocking external dependencies."""

    def test_process_payment_calls_gateway(self):
        """Given valid payment, when processed, then call gateway."""
        # Arrange
        mock_gateway = Mock()
        mock_gateway.charge.return_value = {"status": "success", "id": "txn_123"}
        service = PaymentService(gateway=mock_gateway)

        # Act
        result = service.process(amount=100.00, card_token="tok_visa")

        # Assert
        mock_gateway.charge.assert_called_once_with(
            amount=100.00,
            token="tok_visa",
        )
        assert result.transaction_id == "txn_123"

    @patch("payment_service.requests.post")
    def test_process_handles_gateway_timeout(self, mock_post):
        """Given gateway timeout, when processed, then raise PaymentError."""
        mock_post.side_effect = TimeoutError("Connection timed out")
        service = PaymentService()

        with pytest.raises(PaymentError, match="gateway unavailable"):
            service.process(amount=50.00, card_token="tok_visa")
```

### Async Test

```python
import pytest
from async_client import AsyncClient


class TestAsyncClient:
    """Async test examples."""

    @pytest.mark.asyncio
    async def test_fetch_returns_data(self):
        """Given valid URL, when fetched, then return data."""
        client = AsyncClient()

        result = await client.fetch("https://api.example.com/data")

        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_fetch_with_mock(self, mocker):
        """Given mocked response, when fetched, then return mock data."""
        mock_response = {"data": "mocked"}
        mocker.patch.object(
            AsyncClient,
            "_make_request",
            return_value=mock_response,
        )
        client = AsyncClient()

        result = await client.fetch("https://api.example.com/data")

        assert result == mock_response
```

---

## Jest Templates

### Basic Unit Test

```typescript
// __tests__/{module}.test.ts
import { ClassName } from '../src/{module}';

describe('ClassName', () => {
  let instance: ClassName;

  beforeEach(() => {
    instance = new ClassName();
  });

  describe('methodName', () => {
    it('should return expected result when given valid input', () => {
      // Arrange
      const input = 'test_input';

      // Act
      const result = instance.methodName(input);

      // Assert
      expect(result).toBe('expected_output');
    });

    it('should throw error when given invalid input', () => {
      // Arrange
      const invalidInput = '';

      // Act & Assert
      expect(() => instance.methodName(invalidInput)).toThrow('Invalid input');
    });
  });
});
```

### Parametrized Test (test.each)

```typescript
describe('Calculator', () => {
  const calculator = new Calculator();

  describe('add', () => {
    test.each([
      { a: 1, b: 1, expected: 2, scenario: 'positive numbers' },
      { a: 0, b: 0, expected: 0, scenario: 'zeros' },
      { a: -1, b: 1, expected: 0, scenario: 'negative and positive' },
      { a: 100, b: 200, expected: 300, scenario: 'large numbers' },
    ])('should return $expected when $scenario ($a + $b)', ({ a, b, expected }) => {
      expect(calculator.add(a, b)).toBe(expected);
    });
  });

  describe('divide', () => {
    test.each`
      a      | b    | expected
      ${10}  | ${2} | ${5}
      ${9}   | ${3} | ${3}
      ${100} | ${4} | ${25}
    `('$a / $b = $expected', ({ a, b, expected }) => {
      expect(calculator.divide(a, b)).toBe(expected);
    });
  });
});
```

### Mock Template

```typescript
import { UserService } from '../src/userService';
import { UserRepository } from '../src/userRepository';
import { EmailService } from '../src/emailService';

// Mock the entire module
jest.mock('../src/userRepository');
jest.mock('../src/emailService');

describe('UserService', () => {
  let userService: UserService;
  let mockRepository: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    mockRepository = new UserRepository() as jest.Mocked<UserRepository>;
    mockEmailService = new EmailService() as jest.Mocked<EmailService>;
    userService = new UserService(mockRepository, mockEmailService);
  });

  describe('createUser', () => {
    it('should save user and send welcome email', async () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };
      const savedUser = { id: '123', ...userData };

      mockRepository.save.mockResolvedValue(savedUser);
      mockEmailService.sendWelcome.mockResolvedValue(undefined);

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(mockRepository.save).toHaveBeenCalledWith(userData);
      expect(mockEmailService.sendWelcome).toHaveBeenCalledWith(savedUser.email);
      expect(result).toEqual(savedUser);
    });

    it('should not send email if save fails', async () => {
      // Arrange
      mockRepository.save.mockRejectedValue(new Error('Database error'));

      // Act & Assert
      await expect(userService.createUser({ name: 'John', email: 'john@example.com' }))
        .rejects.toThrow('Database error');

      expect(mockEmailService.sendWelcome).not.toHaveBeenCalled();
    });
  });
});
```

### Spy Template

```typescript
describe('Logger', () => {
  let consoleSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation();
  });

  afterEach(() => {
    consoleSpy.mockRestore();
  });

  it('should log message with timestamp', () => {
    const logger = new Logger();

    logger.info('Test message');

    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringMatching(/^\[\d{4}-\d{2}-\d{2}.*\] INFO: Test message$/)
    );
  });
});
```

### Async Test

```typescript
describe('ApiClient', () => {
  let client: ApiClient;

  beforeEach(() => {
    client = new ApiClient('https://api.example.com');
  });

  describe('fetchData', () => {
    it('should return data on successful request', async () => {
      // Arrange
      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: 'test' }),
      });

      // Act
      const result = await client.fetchData('/endpoint');

      // Assert
      expect(result).toEqual({ data: 'test' });
      expect(fetch).toHaveBeenCalledWith('https://api.example.com/endpoint');
    });

    it('should throw on network error', async () => {
      // Arrange
      global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));

      // Act & Assert
      await expect(client.fetchData('/endpoint')).rejects.toThrow('Network error');
    });

    it('should timeout after specified duration', async () => {
      // Arrange
      jest.useFakeTimers();
      global.fetch = jest.fn().mockImplementation(
        () => new Promise((resolve) => setTimeout(resolve, 10000))
      );

      // Act
      const fetchPromise = client.fetchData('/endpoint', { timeout: 5000 });
      jest.advanceTimersByTime(5000);

      // Assert
      await expect(fetchPromise).rejects.toThrow('Request timeout');
      jest.useRealTimers();
    });
  });
});
```

### React Component Test

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from '../src/components/LoginForm';

describe('LoginForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('should render email and password inputs', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('should call onSubmit with credentials when form submitted', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(mockOnSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('should show validation error for invalid email', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'invalid-email');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

---

## Go Test Templates

### Basic Unit Test

```go
// {package}_test.go
package {package}

import (
    "testing"
)

func TestFunctionName(t *testing.T) {
    // Arrange
    input := "test_input"
    expected := "expected_output"

    // Act
    result := FunctionName(input)

    // Assert
    if result != expected {
        t.Errorf("FunctionName(%q) = %q; want %q", input, result, expected)
    }
}
```

### Table-Driven Test

```go
package calculator

import "testing"

func TestAdd(t *testing.T) {
    tests := map[string]struct {
        a, b     int
        expected int
    }{
        "positive numbers":     {a: 1, b: 2, expected: 3},
        "zeros":                {a: 0, b: 0, expected: 0},
        "negative and positive":{a: -1, b: 1, expected: 0},
        "large numbers":        {a: 1000000, b: 2000000, expected: 3000000},
    }

    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            result := Add(tc.a, tc.b)

            if result != tc.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tc.a, tc.b, result, tc.expected)
            }
        })
    }
}
```

### Parallel Table-Driven Test

```go
func TestDivide(t *testing.T) {
    tests := map[string]struct {
        a, b     int
        expected int
        wantErr  bool
    }{
        "normal division":  {a: 10, b: 2, expected: 5, wantErr: false},
        "division by zero": {a: 10, b: 0, expected: 0, wantErr: true},
    }

    for name, tc := range tests {
        tc := tc // capture range variable
        t.Run(name, func(t *testing.T) {
            t.Parallel() // run subtests in parallel

            result, err := Divide(tc.a, tc.b)

            if tc.wantErr {
                if err == nil {
                    t.Error("expected error, got nil")
                }
                return
            }

            if err != nil {
                t.Errorf("unexpected error: %v", err)
            }
            if result != tc.expected {
                t.Errorf("Divide(%d, %d) = %d; want %d", tc.a, tc.b, result, tc.expected)
            }
        })
    }
}
```

### Test with Setup/Teardown

```go
func TestUserRepository(t *testing.T) {
    // Setup
    db := setupTestDB(t)
    repo := NewUserRepository(db)

    // Teardown
    t.Cleanup(func() {
        db.Close()
    })

    t.Run("Create", func(t *testing.T) {
        user := User{Name: "John", Email: "john@example.com"}

        err := repo.Create(user)

        if err != nil {
            t.Fatalf("failed to create user: %v", err)
        }
    })

    t.Run("FindByEmail", func(t *testing.T) {
        // Uses user created in previous test (if tests run sequentially)
        // Or set up own test data
        user, err := repo.FindByEmail("john@example.com")

        if err != nil {
            t.Fatalf("failed to find user: %v", err)
        }
        if user.Name != "John" {
            t.Errorf("user.Name = %q; want %q", user.Name, "John")
        }
    })
}

func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open test db: %v", err)
    }
    // Run migrations
    return db
}
```

### Mock with Interface

```go
// payment_service.go
type PaymentGateway interface {
    Charge(amount float64, token string) (string, error)
}

type PaymentService struct {
    gateway PaymentGateway
}

func (s *PaymentService) ProcessPayment(amount float64, token string) (string, error) {
    return s.gateway.Charge(amount, token)
}

// payment_service_test.go
type mockGateway struct {
    chargeFunc func(amount float64, token string) (string, error)
}

func (m *mockGateway) Charge(amount float64, token string) (string, error) {
    return m.chargeFunc(amount, token)
}

func TestPaymentService_ProcessPayment(t *testing.T) {
    tests := map[string]struct {
        setupMock func() *mockGateway
        amount    float64
        token     string
        wantTxn   string
        wantErr   bool
    }{
        "successful charge": {
            setupMock: func() *mockGateway {
                return &mockGateway{
                    chargeFunc: func(amount float64, token string) (string, error) {
                        return "txn_123", nil
                    },
                }
            },
            amount:  100.00,
            token:   "tok_visa",
            wantTxn: "txn_123",
            wantErr: false,
        },
        "gateway error": {
            setupMock: func() *mockGateway {
                return &mockGateway{
                    chargeFunc: func(amount float64, token string) (string, error) {
                        return "", errors.New("gateway unavailable")
                    },
                }
            },
            amount:  100.00,
            token:   "tok_visa",
            wantTxn: "",
            wantErr: true,
        },
    }

    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            service := &PaymentService{gateway: tc.setupMock()}

            txn, err := service.ProcessPayment(tc.amount, tc.token)

            if tc.wantErr && err == nil {
                t.Error("expected error, got nil")
            }
            if !tc.wantErr && err != nil {
                t.Errorf("unexpected error: %v", err)
            }
            if txn != tc.wantTxn {
                t.Errorf("txn = %q; want %q", txn, tc.wantTxn)
            }
        })
    }
}
```

### HTTP Handler Test

```go
import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestUserHandler_Create(t *testing.T) {
    tests := map[string]struct {
        body           string
        wantStatusCode int
        wantBody       string
    }{
        "valid user": {
            body:           `{"name":"John","email":"john@example.com"}`,
            wantStatusCode: http.StatusCreated,
            wantBody:       `"id":`,
        },
        "invalid json": {
            body:           `{invalid}`,
            wantStatusCode: http.StatusBadRequest,
            wantBody:       "invalid JSON",
        },
        "missing name": {
            body:           `{"email":"john@example.com"}`,
            wantStatusCode: http.StatusBadRequest,
            wantBody:       "name is required",
        },
    }

    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            // Arrange
            handler := NewUserHandler(NewMockUserService())
            req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(tc.body))
            req.Header.Set("Content-Type", "application/json")
            rec := httptest.NewRecorder()

            // Act
            handler.Create(rec, req)

            // Assert
            if rec.Code != tc.wantStatusCode {
                t.Errorf("status code = %d; want %d", rec.Code, tc.wantStatusCode)
            }
            if !strings.Contains(rec.Body.String(), tc.wantBody) {
                t.Errorf("body = %q; want to contain %q", rec.Body.String(), tc.wantBody)
            }
        })
    }
}
```

---

## Quick Reference

| Framework | Test File | Run Command |
|-----------|-----------|-------------|
| pytest | `tests/test_*.py` | `pytest` |
| Jest | `__tests__/*.test.ts` | `npm test` |
| Go | `*_test.go` | `go test ./...` |

| Pattern | pytest | Jest | Go |
|---------|--------|------|-----|
| Setup | `@pytest.fixture` | `beforeEach` | `t.Cleanup` |
| Parametrize | `@pytest.mark.parametrize` | `test.each` | table-driven |
| Mock | `unittest.mock` | `jest.mock()` | interface |
| Async | `@pytest.mark.asyncio` | `async/await` | N/A |
