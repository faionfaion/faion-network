# Unit Test Templates

Copy-paste templates for Python (pytest), JavaScript (Jest/Vitest), Go, and TypeScript.

## Python (pytest)

### Basic Test Class

```python
import pytest
from mymodule import MyClass


class TestMyClass:
    """Tests for MyClass."""

    @pytest.fixture
    def instance(self):
        """Create a fresh instance for each test."""
        return MyClass()

    def test_method_name_happy_path(self, instance):
        # Arrange
        input_data = "test input"

        # Act
        result = instance.method_name(input_data)

        # Assert
        assert result == "expected output"

    def test_method_name_edge_case(self, instance):
        # Arrange
        input_data = ""

        # Act
        result = instance.method_name(input_data)

        # Assert
        assert result is None

    def test_method_name_raises_on_invalid_input(self, instance):
        with pytest.raises(ValueError, match="Invalid input"):
            instance.method_name(None)
```

### Parametrized Test Template

```python
import pytest


@pytest.mark.parametrize("input_value,expected", [
    pytest.param("value1", "result1", id="happy_path"),
    pytest.param("", None, id="empty_string"),
    pytest.param(None, None, id="null_input"),
    pytest.param("edge", "edge_result", id="edge_case"),
])
def test_function_name(input_value, expected):
    result = function_name(input_value)
    assert result == expected
```

### Service with Mock Dependencies

```python
import pytest
from unittest.mock import Mock, AsyncMock
from myservice import UserService


class TestUserService:

    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def mock_email_service(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repository, mock_email_service):
        return UserService(
            repository=mock_repository,
            email_service=mock_email_service
        )

    def test_create_user_saves_and_sends_email(
        self, service, mock_repository, mock_email_service
    ):
        # Arrange
        mock_repository.save.return_value = User(id="123", email="test@example.com")

        # Act
        result = service.create_user("test@example.com", "Test User")

        # Assert
        assert result.id == "123"
        mock_repository.save.assert_called_once()
        mock_email_service.send_welcome.assert_called_once_with("test@example.com")

    def test_create_user_rollback_on_email_failure(
        self, service, mock_repository, mock_email_service
    ):
        # Arrange
        mock_repository.save.return_value = User(id="123", email="test@example.com")
        mock_email_service.send_welcome.side_effect = EmailError("SMTP failed")

        # Act & Assert
        with pytest.raises(EmailError):
            service.create_user("test@example.com", "Test User")

        mock_repository.delete.assert_called_once_with("123")
```

### Async Test Template

```python
import pytest


@pytest.mark.asyncio
async def test_async_function():
    # Arrange
    service = AsyncService()

    # Act
    result = await service.fetch_data("id-123")

    # Assert
    assert result is not None
    assert result.id == "id-123"


@pytest.mark.asyncio
async def test_async_with_mock():
    # Arrange
    mock_client = AsyncMock()
    mock_client.get.return_value = {"data": "value"}
    service = AsyncService(client=mock_client)

    # Act
    result = await service.process()

    # Assert
    assert result == "value"
    mock_client.get.assert_awaited_once()
```

## JavaScript/TypeScript (Jest)

### Basic Test Suite

```typescript
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { MyClass } from './my-class';

describe('MyClass', () => {
  let instance: MyClass;

  beforeEach(() => {
    instance = new MyClass();
  });

  afterEach(() => {
    // Cleanup if needed
  });

  describe('methodName', () => {
    it('should return expected result for valid input', () => {
      // Arrange
      const input = 'test input';

      // Act
      const result = instance.methodName(input);

      // Assert
      expect(result).toBe('expected output');
    });

    it('should return null for empty input', () => {
      // Arrange
      const input = '';

      // Act
      const result = instance.methodName(input);

      // Assert
      expect(result).toBeNull();
    });

    it('should throw error for invalid input', () => {
      // Act & Assert
      expect(() => instance.methodName(null)).toThrow('Invalid input');
    });
  });
});
```

### Service with Mocked Dependencies

```typescript
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { UserService } from './user-service';
import type { UserRepository, EmailService } from './types';

describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn(),
      delete: jest.fn(),
    };
    mockEmailService = {
      sendWelcome: jest.fn(),
    };
    service = new UserService(mockRepository, mockEmailService);
  });

  describe('createUser', () => {
    it('should save user and send welcome email', async () => {
      // Arrange
      mockRepository.save.mockResolvedValue({ id: '123', email: 'test@example.com' });
      mockEmailService.sendWelcome.mockResolvedValue(undefined);

      // Act
      const result = await service.createUser('test@example.com', 'Test User');

      // Assert
      expect(result.id).toBe('123');
      expect(mockRepository.save).toHaveBeenCalledTimes(1);
      expect(mockEmailService.sendWelcome).toHaveBeenCalledWith('test@example.com');
    });

    it('should rollback on email failure', async () => {
      // Arrange
      mockRepository.save.mockResolvedValue({ id: '123', email: 'test@example.com' });
      mockEmailService.sendWelcome.mockRejectedValue(new Error('SMTP failed'));

      // Act & Assert
      await expect(service.createUser('test@example.com', 'Test User'))
        .rejects.toThrow('SMTP failed');
      expect(mockRepository.delete).toHaveBeenCalledWith('123');
    });
  });
});
```

### Parametrized Tests (Jest)

```typescript
describe('validateEmail', () => {
  it.each([
    ['user@example.com', true],
    ['user.name@domain.co.uk', true],
    ['invalid', false],
    ['@no-local.com', false],
    ['no-at-sign.com', false],
  ])('validateEmail(%s) should return %s', (email, expected) => {
    expect(validateEmail(email)).toBe(expected);
  });
});

// With named test cases
describe('Calculator', () => {
  it.each`
    a     | b     | expected | scenario
    ${1}  | ${2}  | ${3}     | ${'positive numbers'}
    ${-1} | ${1}  | ${0}     | ${'mixed signs'}
    ${0}  | ${0}  | ${0}     | ${'zeros'}
  `('add($a, $b) = $expected ($scenario)', ({ a, b, expected }) => {
    expect(add(a, b)).toBe(expected);
  });
});
```

### React Component Test

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

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

  it('should call onSubmit with form data', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('should show validation error for invalid email', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/email/i), 'invalid');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

## Go

### Basic Test File

```go
package mypackage

import (
    "testing"
)

func TestMyFunction_HappyPath(t *testing.T) {
    // Arrange
    input := "test input"

    // Act
    result := MyFunction(input)

    // Assert
    if result != "expected output" {
        t.Errorf("MyFunction(%q) = %q; want %q", input, result, "expected output")
    }
}

func TestMyFunction_EdgeCase(t *testing.T) {
    // Arrange
    input := ""

    // Act
    result := MyFunction(input)

    // Assert
    if result != "" {
        t.Errorf("MyFunction(%q) = %q; want empty string", input, result)
    }
}
```

### Table-Driven Test Template

```go
func TestMyFunction(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
        wantErr  bool
    }{
        {
            name:     "happy path",
            input:    "valid input",
            expected: "expected output",
            wantErr:  false,
        },
        {
            name:     "empty input",
            input:    "",
            expected: "",
            wantErr:  false,
        },
        {
            name:     "invalid input",
            input:    "invalid",
            expected: "",
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := MyFunction(tt.input)

            if (err != nil) != tt.wantErr {
                t.Errorf("MyFunction() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if result != tt.expected {
                t.Errorf("MyFunction() = %v, want %v", result, tt.expected)
            }
        })
    }
}
```

### Service with Mocked Interface

```go
package user

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "github.com/stretchr/testify/require"
)

// Mock implementation
type MockRepository struct {
    mock.Mock
}

func (m *MockRepository) FindByID(id string) (*User, error) {
    args := m.Called(id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockRepository) Save(user *User) (*User, error) {
    args := m.Called(user)
    return args.Get(0).(*User), args.Error(1)
}

// Tests
func TestUserService_GetUser(t *testing.T) {
    // Arrange
    mockRepo := new(MockRepository)
    mockRepo.On("FindByID", "123").Return(&User{ID: "123", Name: "John"}, nil)

    service := NewUserService(mockRepo)

    // Act
    user, err := service.GetUser("123")

    // Assert
    require.NoError(t, err)
    assert.Equal(t, "123", user.ID)
    assert.Equal(t, "John", user.Name)
    mockRepo.AssertExpectations(t)
}

func TestUserService_GetUser_NotFound(t *testing.T) {
    // Arrange
    mockRepo := new(MockRepository)
    mockRepo.On("FindByID", "999").Return(nil, ErrNotFound)

    service := NewUserService(mockRepo)

    // Act
    user, err := service.GetUser("999")

    // Assert
    assert.Nil(t, user)
    assert.ErrorIs(t, err, ErrNotFound)
    mockRepo.AssertExpectations(t)
}
```

### HTTP Handler Test

```go
func TestGetUserHandler(t *testing.T) {
    tests := []struct {
        name           string
        userID         string
        mockReturn     *User
        mockErr        error
        expectedStatus int
        expectedBody   string
    }{
        {
            name:           "user found",
            userID:         "123",
            mockReturn:     &User{ID: "123", Name: "John"},
            mockErr:        nil,
            expectedStatus: http.StatusOK,
            expectedBody:   `{"id":"123","name":"John"}`,
        },
        {
            name:           "user not found",
            userID:         "999",
            mockReturn:     nil,
            mockErr:        ErrNotFound,
            expectedStatus: http.StatusNotFound,
            expectedBody:   `{"error":"user not found"}`,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Arrange
            mockService := new(MockUserService)
            mockService.On("GetUser", tt.userID).Return(tt.mockReturn, tt.mockErr)

            handler := NewUserHandler(mockService)

            req := httptest.NewRequest(http.MethodGet, "/users/"+tt.userID, nil)
            rec := httptest.NewRecorder()

            // Act
            handler.ServeHTTP(rec, req)

            // Assert
            assert.Equal(t, tt.expectedStatus, rec.Code)
            assert.JSONEq(t, tt.expectedBody, rec.Body.String())
        })
    }
}
```

## Vitest Template

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { UserService } from './user-service';

describe('UserService', () => {
  let service: UserService;
  let mockFetch: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockFetch = vi.fn();
    vi.stubGlobal('fetch', mockFetch);
    service = new UserService();
  });

  it('should fetch user by id', async () => {
    // Arrange
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ id: '123', name: 'John' }),
    });

    // Act
    const user = await service.getUser('123');

    // Assert
    expect(user.name).toBe('John');
    expect(mockFetch).toHaveBeenCalledWith('/api/users/123');
  });

  it('should throw on API error', async () => {
    // Arrange
    mockFetch.mockResolvedValue({
      ok: false,
      status: 404,
    });

    // Act & Assert
    await expect(service.getUser('999')).rejects.toThrow('User not found');
  });
});
```

## Fixture Template (conftest.py)

```python
import pytest
from datetime import datetime, timedelta


@pytest.fixture
def freeze_time(monkeypatch):
    """Fixture to freeze time at a specific moment."""
    frozen_time = datetime(2024, 1, 15, 12, 0, 0)

    class FrozenDatetime:
        @classmethod
        def now(cls, tz=None):
            return frozen_time

        @classmethod
        def utcnow(cls):
            return frozen_time

    monkeypatch.setattr("datetime.datetime", FrozenDatetime)
    return frozen_time


@pytest.fixture
def sample_user():
    """Factory for creating test users."""
    def _make_user(**overrides):
        defaults = {
            "id": "user-123",
            "email": "test@example.com",
            "name": "Test User",
            "created_at": datetime.utcnow(),
        }
        return User(**{**defaults, **overrides})
    return _make_user


@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)

    yield session

    session.close()
    engine.dispose()
```
