# Mocking Strategies Checklist

## Pre-Mocking Decision Checklist

Before writing a mock, verify these conditions:

### Should I Mock This?

- [ ] Is this an **external boundary** (API, database, file system, time)?
- [ ] Does calling the real dependency cause **slowness** (>100ms)?
- [ ] Does calling the real dependency cause **flakiness** (network, timing)?
- [ ] Does calling the real dependency have **costs** (API calls, resources)?
- [ ] Is the dependency **non-deterministic** (time, random, external state)?

**If none of these apply, consider testing with the real implementation.**

### Red Flags: Should I Refactor Instead?

- [ ] Am I mocking more than 2-3 dependencies?
- [ ] Is my mock setup longer than my test logic?
- [ ] Am I mocking internal classes, not boundaries?
- [ ] Am I creating mocks that return mocks?
- [ ] Would this test break on refactoring without behavior change?

**If any apply, refactor the code for better testability.**

---

## Python Mocking Checklist

### Setup Phase

- [ ] **Choose the right tool:**
  - `unittest.mock` for unittest projects
  - `pytest-mock` for pytest projects (preferred)
  - `freezegun` for time mocking
  - `responses` for HTTP mocking (requests)
  - `pytest-httpx` for HTTP mocking (httpx)

- [ ] **Import correctly:**
  ```python
  # pytest-mock (preferred)
  def test_example(mocker):
      mock = mocker.patch('module.function')

  # unittest.mock
  from unittest.mock import Mock, patch, MagicMock, AsyncMock
  ```

- [ ] **Patch in the right place:**
  - Patch where the function is **used**, not where it's **defined**
  - Example: If `my_module.py` imports `requests.get`, patch `my_module.requests.get`

### Mock Configuration

- [ ] **Use `autospec=True` for signature validation:**
  ```python
  mock = mocker.patch('module.function', autospec=True)
  ```

- [ ] **Set return values appropriately:**
  ```python
  mock.return_value = expected_result  # Single call
  mock.side_effect = [val1, val2, val3]  # Multiple calls
  mock.side_effect = CustomException()  # Raise exception
  ```

- [ ] **Use `side_effect` for conditional returns:**
  ```python
  def conditional_return(arg):
      if arg == "valid":
          return {"status": "ok"}
      raise ValueError("Invalid")
  mock.side_effect = conditional_return
  ```

### Async Mocking

- [ ] **Use `AsyncMock` for async functions:**
  ```python
  mock = mocker.patch('module.async_function', new_callable=AsyncMock)
  mock.return_value = expected_result
  ```

- [ ] **Use async-specific assertions:**
  ```python
  mock.assert_awaited_once()
  mock.assert_awaited_with(expected_arg)
  ```

- [ ] **Mark test as async:**
  ```python
  @pytest.mark.asyncio
  async def test_async_function():
      ...
  ```

### Verification Phase

- [ ] **Assert on behavior (when appropriate):**
  ```python
  mock.assert_called_once()
  mock.assert_called_with(expected_arg)
  mock.assert_not_called()
  ```

- [ ] **Prefer state verification over behavior:**
  ```python
  # Better: Assert on outcome
  assert result == expected_value

  # Avoid: Assert on every interaction
  mock.assert_called_with(...)  # Only when interaction IS the behavior
  ```

### Cleanup

- [ ] **pytest-mock auto-cleans** - No manual cleanup needed
- [ ] **unittest.mock context manager auto-cleans:**
  ```python
  with patch('module.function') as mock:
      ...  # Mock automatically cleaned after block
  ```
- [ ] **For manual cleanup:**
  ```python
  mock.reset_mock()  # Reset call history
  patch.stopall()    # Stop all patches
  ```

---

## JavaScript/TypeScript Mocking Checklist

### Setup Phase

- [ ] **Choose the right approach:**
  - `jest.fn()` for function mocks
  - `jest.mock()` for module mocks
  - `jest.spyOn()` for spies on existing functions

- [ ] **Clear mocks between tests:**
  ```typescript
  beforeEach(() => {
      jest.clearAllMocks();  // Clear call history
      // OR
      jest.resetAllMocks();  // Clear calls + reset implementations
      // OR
      jest.restoreAllMocks();  // Restore original implementations
  });
  ```

- [ ] **Understand mock hoisting:**
  - `jest.mock()` is hoisted to top of file
  - Runs before imports
  - Add `// Mocked module` comment for clarity

### Mock Configuration

- [ ] **Use type-safe mocks:**
  ```typescript
  const mockFn = jest.fn<ReturnType, [ArgType1, ArgType2]>();
  // OR with jest.mocked()
  jest.mock('./module');
  const mockedModule = jest.mocked(module);
  ```

- [ ] **Set return values:**
  ```typescript
  mockFn.mockReturnValue(value);           // Sync
  mockFn.mockResolvedValue(value);         // Async success
  mockFn.mockRejectedValue(new Error());   // Async error
  mockFn.mockImplementation((arg) => ...); // Custom logic
  ```

- [ ] **For partial mocks, use `spyOn`:**
  ```typescript
  const spy = jest.spyOn(object, 'method');
  spy.mockReturnValue(value);  // Override
  // Real method still available via spy.mockRestore()
  ```

### Timer Mocking

- [ ] **Enable fake timers:**
  ```typescript
  beforeEach(() => jest.useFakeTimers());
  afterEach(() => jest.useRealTimers());
  ```

- [ ] **Advance time:**
  ```typescript
  jest.advanceTimersByTime(1000);  // Advance 1 second
  jest.runAllTimers();              // Run all pending timers
  ```

### Verification

- [ ] **Use matchers for flexibility:**
  ```typescript
  expect(mockFn).toHaveBeenCalledWith(expect.objectContaining({ id: '123' }));
  expect(mockFn).toHaveBeenCalledTimes(1);
  ```

---

## Go Mocking Checklist

### Design Phase

- [ ] **Define interfaces at the consumer:**
  ```go
  // Define in the file that USES the dependency
  type UserStore interface {
      FindByID(id string) (*User, error)
  }
  ```

- [ ] **Keep interfaces small:**
  - 1-3 methods per interface
  - Larger interfaces are harder to mock

- [ ] **Use dependency injection:**
  ```go
  type Service struct {
      store UserStore  // Interface, not concrete type
  }

  func NewService(store UserStore) *Service {
      return &Service{store: store}
  }
  ```

### Mock Implementation

- [ ] **Manual mock (simple cases):**
  ```go
  type MockUserStore struct {
      FindByIDFn func(id string) (*User, error)
  }

  func (m *MockUserStore) FindByID(id string) (*User, error) {
      return m.FindByIDFn(id)
  }
  ```

- [ ] **gomock (complex cases):**
  ```bash
  mockgen -source=interface.go -destination=mock_interface.go
  ```

- [ ] **testify/mock (alternative):**
  ```go
  type MockStore struct {
      mock.Mock
  }

  func (m *MockStore) FindByID(id string) (*User, error) {
      args := m.Called(id)
      return args.Get(0).(*User), args.Error(1)
  }
  ```

### HTTP Testing

- [ ] **Use `httptest` for handlers:**
  ```go
  req := httptest.NewRequest("GET", "/users/123", nil)
  rr := httptest.NewRecorder()
  handler.ServeHTTP(rr, req)
  assert.Equal(t, http.StatusOK, rr.Code)
  ```

- [ ] **Use `httptest.Server` for clients:**
  ```go
  server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
      w.WriteHeader(http.StatusOK)
      w.Write([]byte(`{"id": "123"}`))
  }))
  defer server.Close()
  ```

---

## Time Mocking Checklist

### Python (freezegun)

- [ ] **Install:** `pip install freezegun`
- [ ] **Use decorator:**
  ```python
  @freeze_time("2025-01-15 10:30:00")
  def test_time_sensitive():
      assert datetime.now() == datetime(2025, 1, 15, 10, 30, 0)
  ```
- [ ] **Use context manager:**
  ```python
  with freeze_time("2025-01-15"):
      ...
  ```

### Python (time-machine) - Faster Alternative

- [ ] **Install:** `pip install time-machine`
- [ ] **Use decorator:**
  ```python
  @time_machine.travel("2025-01-15 10:30:00")
  def test_time_sensitive():
      ...
  ```

### JavaScript (Jest)

- [ ] **Enable fake timers:**
  ```typescript
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2025-01-15'));
  ```
- [ ] **Restore after tests:**
  ```typescript
  afterEach(() => jest.useRealTimers());
  ```

### Best Practice: Clock Injection

- [ ] **Define a Clock interface:**
  ```python
  class Clock(Protocol):
      def now(self) -> datetime: ...

  class RealClock:
      def now(self) -> datetime:
          return datetime.now()

  class FakeClock:
      def __init__(self, fixed_time: datetime):
          self._time = fixed_time
      def now(self) -> datetime:
          return self._time
  ```

---

## HTTP/API Mocking Checklist

### Python (responses library)

- [ ] **Install:** `pip install responses`
- [ ] **Mock request:**
  ```python
  @responses.activate
  def test_api_call():
      responses.add(
          responses.GET,
          "https://api.example.com/users/123",
          json={"id": "123", "name": "John"},
          status=200
      )
      result = api_client.get_user("123")
      assert result["name"] == "John"
  ```

### Python (pytest-httpx for async)

- [ ] **Install:** `pip install pytest-httpx`
- [ ] **Mock httpx:**
  ```python
  @pytest.mark.asyncio
  async def test_async_api(httpx_mock):
      httpx_mock.add_response(
          url="https://api.example.com/users/123",
          json={"id": "123"}
      )
      async with httpx.AsyncClient() as client:
          response = await client.get("https://api.example.com/users/123")
  ```

### JavaScript (nock)

- [ ] **Install:** `npm install nock`
- [ ] **Mock request:**
  ```typescript
  import nock from 'nock';

  nock('https://api.example.com')
      .get('/users/123')
      .reply(200, { id: '123', name: 'John' });
  ```

### Integration Tests (Testcontainers + WireMock)

- [ ] **Use for realistic API mocking in integration tests**
- [ ] **Configure via JSON or code:**
  ```python
  from testcontainers.mockserver import MockServerContainer

  with MockServerContainer() as container:
      client = container.get_client()
      client.expect(...)
  ```

---

## Final Verification Checklist

Before committing test code:

- [ ] Test passes with mock
- [ ] Test fails when expected behavior is removed
- [ ] Mock setup is minimal and focused
- [ ] No mocking of internal implementation details
- [ ] Proper cleanup/reset between tests
- [ ] `autospec=True` used where applicable (Python)
- [ ] Type safety maintained (TypeScript)
- [ ] Interfaces used for testability (Go)
- [ ] Error scenarios covered
- [ ] No hardcoded values that should be configurable

---

*Use this checklist to ensure consistent, maintainable mocking practices across your test suite.*
