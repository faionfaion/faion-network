# Mocking Templates

Copy-paste templates for common mocking scenarios. Customize placeholders marked with `<...>`.

---

## Python Templates

### Basic Mock with pytest-mock

```python
import pytest
from <your_module> import <YourClass>


class Test<YourClass>:

    def test_<method>_success(self, mocker):
        # Arrange
        mock_dependency = mocker.patch('<your_module>.<Dependency>')
        mock_dependency.return_value.<method>.return_value = <expected_result>

        instance = <YourClass>()

        # Act
        result = instance.<method>(<args>)

        # Assert
        assert result == <expected_result>
        mock_dependency.return_value.<method>.assert_called_once_with(<args>)

    def test_<method>_failure(self, mocker):
        # Arrange
        mock_dependency = mocker.patch('<your_module>.<Dependency>')
        mock_dependency.return_value.<method>.side_effect = <ExceptionType>("<message>")

        instance = <YourClass>()

        # Act & Assert
        with pytest.raises(<ExceptionType>):
            instance.<method>(<args>)
```

### Stub with Return Values

```python
def test_with_stub(mocker):
    # Single return value
    mock = mocker.Mock()
    mock.get_data.return_value = {"id": "123", "name": "Test"}

    # Multiple return values (sequence)
    mock.get_next.side_effect = ["first", "second", "third"]

    # Conditional return based on input
    def conditional_return(arg):
        if arg == "valid":
            return {"status": "ok"}
        elif arg == "error":
            raise ValueError("Invalid input")
        return None

    mock.process.side_effect = conditional_return

    # Use in test
    service = Service(mock)
    result = service.do_something()
    assert result is not None
```

### Spy (Wrap Real Object)

```python
def test_with_spy(mocker):
    real_object = RealClass()

    # Spy wraps real object, tracks calls
    spy = mocker.Mock(wraps=real_object)

    # Real method executes, calls tracked
    result = spy.calculate(2, 3)

    assert result == 5  # Real behavior
    spy.calculate.assert_called_once_with(2, 3)  # Tracked
```

### Patch as Decorator

```python
from unittest.mock import patch


@patch('<module_path>.<function_or_class>')
def test_with_patch_decorator(mock_dependency):
    mock_dependency.return_value = <expected_result>

    result = function_under_test()

    assert result == <expected>
    mock_dependency.assert_called_once()


# Multiple patches (order: bottom-up to function args)
@patch('<module>.third_dep')
@patch('<module>.second_dep')
@patch('<module>.first_dep')
def test_multiple_patches(mock_first, mock_second, mock_third):
    mock_first.return_value = "first"
    mock_second.return_value = "second"
    mock_third.return_value = "third"

    result = function_under_test()
    assert result is not None
```

### Patch as Context Manager

```python
from unittest.mock import patch


def test_with_context_manager():
    with patch('<module>.<function>') as mock_func:
        mock_func.return_value = <expected_result>

        result = function_under_test()

        assert result == <expected>
        mock_func.assert_called_once()
```

### Patch Object Attribute

```python
from unittest.mock import patch


def test_patch_object_method(mocker):
    mocker.patch.object(
        <TargetClass>,
        '<method_name>',
        return_value=<expected_result>
    )

    instance = <TargetClass>()
    result = instance.<method_name>(<args>)

    assert result == <expected_result>
```

### Patch Dictionary (e.g., os.environ)

```python
from unittest.mock import patch


def test_with_env_vars(mocker):
    mocker.patch.dict('os.environ', {
        'API_KEY': 'test-key',
        'DATABASE_URL': 'sqlite:///:memory:',
        'DEBUG': 'true',
    })

    from <module> import load_config
    config = load_config()

    assert config['api_key'] == 'test-key'
```

---

## Python Async Templates

### AsyncMock Basic

```python
import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_async_function():
    # Arrange
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {"id": "123", "data": "test"}

    service = AsyncService(client=mock_client)

    # Act
    result = await service.get_data("123")

    # Assert
    assert result["id"] == "123"
    mock_client.fetch.assert_awaited_once_with("123")
```

### AsyncMock with Side Effect

```python
@pytest.mark.asyncio
async def test_async_error_handling():
    mock_client = AsyncMock()
    mock_client.fetch.side_effect = ConnectionError("Network error")

    service = AsyncService(client=mock_client)

    with pytest.raises(ServiceError):
        await service.get_data("123")
```

### AsyncMock Sequence

```python
@pytest.mark.asyncio
async def test_async_sequence():
    mock = AsyncMock()
    mock.get_next.side_effect = [
        {"page": 1, "data": [1, 2, 3]},
        {"page": 2, "data": [4, 5, 6]},
        {"page": 3, "data": []},
    ]

    results = []
    async for page in paginate(mock):
        results.extend(page["data"])

    assert results == [1, 2, 3, 4, 5, 6]
```

### Patch Async Function

```python
@pytest.mark.asyncio
async def test_patch_async(mocker):
    mock_fetch = mocker.patch(
        '<module>.fetch_data',
        new_callable=AsyncMock,
        return_value={"status": "ok"}
    )

    result = await function_that_calls_fetch()

    assert result["status"] == "ok"
    mock_fetch.assert_awaited_once()
```

---

## Python HTTP Mocking Templates

### responses Library (for requests)

```python
import responses
import requests


@responses.activate
def test_api_call():
    # Mock GET request
    responses.add(
        responses.GET,
        "https://api.example.com/users/123",
        json={"id": "123", "name": "John Doe"},
        status=200
    )

    # Mock POST request
    responses.add(
        responses.POST,
        "https://api.example.com/users",
        json={"id": "456", "created": True},
        status=201
    )

    # Mock error response
    responses.add(
        responses.GET,
        "https://api.example.com/users/999",
        json={"error": "Not found"},
        status=404
    )

    # Test your code
    client = APIClient("https://api.example.com")
    user = client.get_user("123")

    assert user["name"] == "John Doe"
    assert len(responses.calls) == 1
```

### pytest-httpx (for httpx/async)

```python
import pytest
import httpx
from pytest_httpx import HTTPXMock


@pytest.mark.asyncio
async def test_async_http(httpx_mock: HTTPXMock):
    # Mock response
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"result": "success"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    assert response.json()["result"] == "success"


@pytest.mark.asyncio
async def test_http_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.example.com/data",
        status_code=500,
        json={"error": "Internal server error"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    assert response.status_code == 500
```

---

## Python Time Mocking Templates

### freezegun

```python
from datetime import datetime
from freezegun import freeze_time


@freeze_time("2025-01-15 10:30:00")
def test_with_frozen_time():
    now = datetime.now()
    assert now == datetime(2025, 1, 15, 10, 30, 0)


@freeze_time("2025-01-15 10:30:00")
class TestTimeDependent:
    def test_current_time(self):
        assert datetime.now().year == 2025

    def test_time_comparison(self):
        deadline = datetime(2025, 1, 20)
        assert deadline > datetime.now()


def test_with_context_manager():
    with freeze_time("2025-06-01"):
        assert datetime.now().month == 6

    # Time unfrozen here
    assert datetime.now().month != 6  # Unless it actually is June
```

### time-machine (faster alternative)

```python
import time_machine
from datetime import datetime


@time_machine.travel("2025-01-15 10:30:00")
def test_with_time_machine():
    assert datetime.now() == datetime(2025, 1, 15, 10, 30, 0)


def test_travel_in_context():
    with time_machine.travel("2025-12-25"):
        assert datetime.now().month == 12
```

---

## Python Fake Implementation Template

```python
from typing import Dict, Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid


@dataclass
class Entity:
    id: str
    name: str
    # Add more fields...


class Repository(ABC):
    @abstractmethod
    def save(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        pass

    @abstractmethod
    def find_all(self) -> List[Entity]:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        pass


class FakeRepository(Repository):
    """In-memory fake for testing."""

    def __init__(self):
        self._storage: Dict[str, Entity] = {}

    def save(self, entity: Entity) -> Entity:
        if not entity.id:
            entity.id = str(uuid.uuid4())
        self._storage[entity.id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> Optional[Entity]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Entity]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    # Test helpers
    def clear(self):
        self._storage.clear()

    def count(self) -> int:
        return len(self._storage)


# Usage in tests
@pytest.fixture
def fake_repo():
    repo = FakeRepository()
    yield repo
    repo.clear()


def test_service_with_fake(fake_repo):
    service = EntityService(fake_repo)

    result = service.create(name="Test Entity")

    assert result.id is not None
    assert fake_repo.count() == 1
```

---

## JavaScript/TypeScript Templates

### Jest Mock Function

```typescript
import { myFunction } from './my-module';

describe('myFunction', () => {
  it('should handle success case', () => {
    const mockCallback = jest.fn();
    mockCallback.mockReturnValue('expected result');

    const result = myFunction(mockCallback);

    expect(result).toBe('expected result');
    expect(mockCallback).toHaveBeenCalledTimes(1);
  });
});
```

### Jest Module Mock

```typescript
// Mock entire module
jest.mock('./api-client');
import { ApiClient } from './api-client';

// Type the mock
const MockedApiClient = ApiClient as jest.MockedClass<typeof ApiClient>;

describe('Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch data', async () => {
    // Configure mock
    MockedApiClient.prototype.fetch.mockResolvedValue({ data: 'test' });

    const service = new Service(new ApiClient());
    const result = await service.getData();

    expect(result.data).toBe('test');
  });
});
```

### Jest Spy

```typescript
describe('with spy', () => {
  it('should spy on method', () => {
    const obj = new RealClass();
    const spy = jest.spyOn(obj, 'method');

    obj.method('arg');

    expect(spy).toHaveBeenCalledWith('arg');

    spy.mockRestore(); // Restore original
  });

  it('should override method with spy', () => {
    const obj = new RealClass();
    const spy = jest.spyOn(obj, 'method').mockReturnValue('mocked');

    const result = obj.method('arg');

    expect(result).toBe('mocked');
    spy.mockRestore();
  });
});
```

### Jest Async Mock

```typescript
describe('async operations', () => {
  it('should mock async function', async () => {
    const mockFetch = jest.fn();
    mockFetch.mockResolvedValue({ id: '123', name: 'Test' });

    const result = await fetchUser(mockFetch, '123');

    expect(result.name).toBe('Test');
    expect(mockFetch).toHaveBeenCalledWith('123');
  });

  it('should mock async rejection', async () => {
    const mockFetch = jest.fn();
    mockFetch.mockRejectedValue(new Error('Network error'));

    await expect(fetchUser(mockFetch, '123')).rejects.toThrow('Network error');
  });
});
```

### Jest Timer Mock

```typescript
describe('timer operations', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should call callback after delay', () => {
    const callback = jest.fn();

    scheduleCallback(callback, 5000);

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(5000);

    expect(callback).toHaveBeenCalledTimes(1);
  });

  it('should handle setInterval', () => {
    const callback = jest.fn();

    startInterval(callback, 1000);

    jest.advanceTimersByTime(3000);

    expect(callback).toHaveBeenCalledTimes(3);
  });
});
```

### Jest Partial Mock

```typescript
jest.mock('./module', () => {
  const actual = jest.requireActual('./module');
  return {
    ...actual,
    // Only mock this function
    problematicFunction: jest.fn().mockReturnValue('mocked'),
  };
});
```

---

## Go Templates

### Interface-Based Mock

```go
package <package>

import (
    "context"
    "testing"

    "github.com/stretchr/testify/assert"
)

// Interface definition (at consumer)
type DataStore interface {
    Get(ctx context.Context, key string) (string, error)
    Set(ctx context.Context, key, value string) error
    Delete(ctx context.Context, key string) error
}

// Mock implementation
type MockDataStore struct {
    GetFn    func(ctx context.Context, key string) (string, error)
    SetFn    func(ctx context.Context, key, value string) error
    DeleteFn func(ctx context.Context, key string) error

    GetCalls    []string
    SetCalls    []SetCall
    DeleteCalls []string
}

type SetCall struct {
    Key   string
    Value string
}

func (m *MockDataStore) Get(ctx context.Context, key string) (string, error) {
    m.GetCalls = append(m.GetCalls, key)
    if m.GetFn != nil {
        return m.GetFn(ctx, key)
    }
    return "", nil
}

func (m *MockDataStore) Set(ctx context.Context, key, value string) error {
    m.SetCalls = append(m.SetCalls, SetCall{Key: key, Value: value})
    if m.SetFn != nil {
        return m.SetFn(ctx, key, value)
    }
    return nil
}

func (m *MockDataStore) Delete(ctx context.Context, key string) error {
    m.DeleteCalls = append(m.DeleteCalls, key)
    if m.DeleteFn != nil {
        return m.DeleteFn(ctx, key)
    }
    return nil
}

// Test
func TestServiceWithMock(t *testing.T) {
    mock := &MockDataStore{
        GetFn: func(ctx context.Context, key string) (string, error) {
            if key == "existing" {
                return "value", nil
            }
            return "", ErrNotFound
        },
    }

    service := NewService(mock)
    result, err := service.GetData(context.Background(), "existing")

    assert.NoError(t, err)
    assert.Equal(t, "value", result)
    assert.Equal(t, []string{"existing"}, mock.GetCalls)
}
```

### httptest for HTTP Handlers

```go
package handlers

import (
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestGetUserHandler(t *testing.T) {
    // Arrange
    handler := NewUserHandler(mockUserService)

    req := httptest.NewRequest(http.MethodGet, "/users/123", nil)
    rr := httptest.NewRecorder()

    // Act
    handler.ServeHTTP(rr, req)

    // Assert
    assert.Equal(t, http.StatusOK, rr.Code)

    var response UserResponse
    err := json.Unmarshal(rr.Body.Bytes(), &response)
    require.NoError(t, err)
    assert.Equal(t, "123", response.ID)
}

func TestCreateUserHandler(t *testing.T) {
    body := `{"name": "John Doe", "email": "john@example.com"}`
    req := httptest.NewRequest(http.MethodPost, "/users", strings.NewReader(body))
    req.Header.Set("Content-Type", "application/json")

    rr := httptest.NewRecorder()
    handler.ServeHTTP(rr, req)

    assert.Equal(t, http.StatusCreated, rr.Code)
}
```

### httptest.Server for HTTP Clients

```go
func TestAPIClient(t *testing.T) {
    // Create test server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        switch r.URL.Path {
        case "/users/123":
            w.Header().Set("Content-Type", "application/json")
            w.WriteHeader(http.StatusOK)
            json.NewEncoder(w).Encode(map[string]string{
                "id":   "123",
                "name": "Test User",
            })
        case "/users/999":
            w.WriteHeader(http.StatusNotFound)
            w.Write([]byte(`{"error": "not found"}`))
        default:
            w.WriteHeader(http.StatusNotFound)
        }
    }))
    defer server.Close()

    // Use test server URL
    client := NewAPIClient(server.URL)

    user, err := client.GetUser("123")

    assert.NoError(t, err)
    assert.Equal(t, "Test User", user.Name)
}
```

### Table-Driven Tests with Mocks

```go
func TestCalculator(t *testing.T) {
    tests := []struct {
        name     string
        mockFn   func(ctx context.Context, a, b int) (int, error)
        a, b     int
        expected int
        wantErr  bool
    }{
        {
            name: "addition success",
            mockFn: func(ctx context.Context, a, b int) (int, error) {
                return a + b, nil
            },
            a: 2, b: 3,
            expected: 5,
            wantErr:  false,
        },
        {
            name: "overflow error",
            mockFn: func(ctx context.Context, a, b int) (int, error) {
                return 0, ErrOverflow
            },
            a: 1 << 62, b: 1 << 62,
            expected: 0,
            wantErr:  true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            mock := &MockCalculator{AddFn: tt.mockFn}
            service := NewService(mock)

            result, err := service.Add(context.Background(), tt.a, tt.b)

            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
                assert.Equal(t, tt.expected, result)
            }
        })
    }
}
```

---

## pytest Fixtures for Mocking

```python
# conftest.py
import pytest
from unittest.mock import AsyncMock, Mock


@pytest.fixture
def mock_db_session(mocker):
    """Mock database session."""
    session = mocker.Mock()
    session.commit = mocker.Mock()
    session.rollback = mocker.Mock()
    session.close = mocker.Mock()
    return session


@pytest.fixture
def mock_http_client(mocker):
    """Mock HTTP client for API calls."""
    client = AsyncMock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.put = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.fixture
def mock_cache(mocker):
    """Mock cache with basic get/set."""
    cache = {}

    async def mock_get(key):
        return cache.get(key)

    async def mock_set(key, value, ttl=None):
        cache[key] = value

    async def mock_delete(key):
        cache.pop(key, None)

    mock = AsyncMock()
    mock.get = AsyncMock(side_effect=mock_get)
    mock.set = AsyncMock(side_effect=mock_set)
    mock.delete = AsyncMock(side_effect=mock_delete)
    mock._cache = cache  # For inspection in tests
    return mock


@pytest.fixture
def frozen_time():
    """Provide frozen time context."""
    from freezegun import freeze_time
    return freeze_time("2025-01-15 10:00:00")
```

---

*Copy and adapt these templates for your specific testing needs.*
