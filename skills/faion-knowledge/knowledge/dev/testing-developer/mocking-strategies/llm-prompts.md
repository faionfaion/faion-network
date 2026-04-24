# LLM Prompts for Mocking

Effective prompts for generating high-quality mocks using LLMs (Claude, GPT-4, etc.).

---

## General Principles for LLM Mocking Prompts

1. **Provide the interface/signature** - LLMs need exact method signatures
2. **Specify the framework** - pytest-mock, Jest, gomock, etc.
3. **Include context** - What the mock replaces, why it's being mocked
4. **Request error cases** - Both success and failure scenarios
5. **Ask for cleanup** - Proper mock teardown and reset

---

## Python Mocking Prompts

### Generate Mock for External API Client

```
Generate a pytest test with mocks for this class:

```python
class PaymentClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    async def create_payment(self, amount: float, currency: str, customer_id: str) -> dict:
        """Returns: {"id": "pay_xxx", "status": "pending", "amount": amount}"""
        pass

    async def get_payment(self, payment_id: str) -> dict:
        """Returns payment details or raises PaymentNotFoundError"""
        pass

    async def refund(self, payment_id: str, amount: Optional[float] = None) -> dict:
        """Full or partial refund. Returns: {"id": "ref_xxx", "status": "succeeded"}"""
        pass
```

Requirements:
- Use pytest-mock with AsyncMock
- Test success cases for all methods
- Test error handling (PaymentNotFoundError, NetworkError)
- Use autospec=True for type safety
- Include proper cleanup
```

### Generate Fake Repository

```
Create a fake repository implementation for testing:

Interface:
```python
from abc import ABC, abstractmethod
from typing import Optional, List

class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User: pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: pass

    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[User]: pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool: pass
```

Requirements:
- In-memory implementation using dict
- Support for email uniqueness constraint
- Include pagination in find_all
- Add test helper methods (clear, count)
- Make it async-compatible
```

### Generate HTTP Mocking Tests

```
Generate tests using the responses library for this function:

```python
def fetch_user_profile(user_id: str) -> dict:
    """
    Fetches user profile from external API.
    - GET https://api.users.com/v2/users/{user_id}
    - Returns user dict on success
    - Raises UserNotFoundError on 404
    - Raises APIError on 5xx
    - Retries 3 times on network errors
    """
    pass
```

Test scenarios needed:
1. Successful fetch
2. User not found (404)
3. Server error (500)
4. Network error with retry success
5. Network error exhausting retries
```

### Generate Time Mocking Tests

```
Generate pytest tests with freezegun for this subscription checker:

```python
class SubscriptionChecker:
    def is_trial_expired(self, trial_start: datetime) -> bool:
        """Trial lasts 14 days from start"""
        pass

    def days_until_renewal(self, renewal_date: datetime) -> int:
        """Returns days until renewal, 0 if past due"""
        pass

    def should_send_reminder(self, renewal_date: datetime) -> bool:
        """Send reminder 7, 3, and 1 day before renewal"""
        pass
```

Test cases:
- Trial active (day 1, day 13)
- Trial expired (day 14, day 15)
- Renewal in future (30 days, 7 days, 1 day)
- Renewal in past
- Reminder boundaries (exactly 7, 3, 1 days before)
```

---

## TypeScript/Jest Prompts

### Generate Jest Mock for Service

```
Generate Jest tests with mocks for this TypeScript service:

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<boolean>;
}

interface EmailService {
  sendWelcome(email: string, name: string): Promise<void>;
  sendPasswordReset(email: string, token: string): Promise<void>;
}

class UserService {
  constructor(
    private repo: UserRepository,
    private emailService: EmailService
  ) {}

  async register(email: string, name: string): Promise<User> { ... }
  async requestPasswordReset(email: string): Promise<void> { ... }
  async deleteAccount(userId: string): Promise<void> { ... }
}
```

Requirements:
- Type-safe mocks using jest.Mocked<T>
- Test all three methods
- Include success and error cases
- Clear mocks between tests
- Use toHaveBeenCalledWith for interaction verification
```

### Generate Jest Timer Mocks

```
Generate Jest tests with fake timers for this debounce utility:

```typescript
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  // Implementation uses setTimeout
}
```

Test cases:
- Single call executes after delay
- Multiple rapid calls only execute once
- Delay resets on each call
- Arguments from last call are used
```

### Generate API Mock with MSW

```
Generate tests using Mock Service Worker (MSW) for this API client:

```typescript
class ProductAPI {
  constructor(private baseUrl: string) {}

  async getProducts(category?: string): Promise<Product[]> {
    // GET /products?category=...
  }

  async getProduct(id: string): Promise<Product> {
    // GET /products/:id
  }

  async createProduct(data: CreateProductDTO): Promise<Product> {
    // POST /products
  }
}
```

Requirements:
- Use MSW for request interception
- Mock success responses
- Mock error responses (404, 500)
- Verify request bodies for POST
```

---

## Go Prompts

### Generate Interface Mock

```
Generate a mock implementation for this Go interface:

```go
type OrderService interface {
    Create(ctx context.Context, order *Order) (*Order, error)
    GetByID(ctx context.Context, id string) (*Order, error)
    GetByUser(ctx context.Context, userID string, page, limit int) ([]*Order, error)
    UpdateStatus(ctx context.Context, id string, status OrderStatus) error
    Cancel(ctx context.Context, id string, reason string) error
}
```

Requirements:
- Manual mock with function properties for customization
- Track all calls for verification
- Include helper to reset call tracking
- Provide example tests using the mock
```

### Generate HTTP Handler Tests

```
Generate tests using httptest for this Go handler:

```go
type UserHandler struct {
    service UserService
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    // GET /users/{id}
    // Returns JSON user or 404
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    // POST /users
    // Body: {"name": "...", "email": "..."}
    // Returns 201 with created user
    // Returns 400 on validation error
    // Returns 409 on duplicate email
}
```

Requirements:
- Use httptest.NewRequest and httptest.NewRecorder
- Test success cases
- Test error cases (404, 400, 409)
- Verify response headers and body
- Use table-driven tests
```

### Generate HTTP Client Tests

```
Generate tests using httptest.Server for this Go HTTP client:

```go
type APIClient struct {
    baseURL    string
    httpClient *http.Client
}

func (c *APIClient) GetUser(ctx context.Context, id string) (*User, error) {
    // GET {baseURL}/users/{id}
}

func (c *APIClient) CreateUser(ctx context.Context, user *CreateUserRequest) (*User, error) {
    // POST {baseURL}/users
}
```

Requirements:
- Create httptest.Server with custom handler
- Route different paths appropriately
- Test success responses
- Test error responses
- Test timeout handling
```

---

## Complex Scenario Prompts

### Generate Integration Test with Multiple Mocks

```
Generate an integration test for this order flow:

Components:
1. OrderService - creates orders
2. InventoryClient - checks/reserves stock (external API)
3. PaymentClient - processes payment (external API)
4. NotificationService - sends emails (external API)
5. OrderRepository - stores orders (database)

Flow to test:
1. User submits order
2. System checks inventory
3. System reserves stock
4. System processes payment
5. System saves order
6. System sends confirmation email
7. If payment fails, release reserved stock

Requirements:
- Mock external APIs (Inventory, Payment, Notification)
- Use fake for OrderRepository
- Test happy path
- Test payment failure with rollback
- Test inventory check failure
- Verify correct order of operations
```

### Generate Test for Retry Logic

```
Generate tests for this retry mechanism:

```python
async def with_retry(
    fn: Callable[[], Awaitable[T]],
    max_attempts: int = 3,
    backoff_base: float = 1.0,
    retryable_exceptions: tuple = (ConnectionError, TimeoutError)
) -> T:
    """
    Retries fn with exponential backoff.
    - First retry after backoff_base seconds
    - Second retry after backoff_base * 2 seconds
    - Raises last exception if all attempts fail
    """
    pass
```

Test scenarios:
1. Succeeds on first attempt
2. Fails once, succeeds on retry
3. Fails twice, succeeds on third attempt
4. Fails all attempts, raises exception
5. Non-retryable exception raises immediately
6. Verify backoff timing (use freezegun)
```

### Generate Mock for Event-Driven System

```
Generate tests for this event publisher:

```python
class EventPublisher:
    def __init__(self, broker: MessageBroker):
        self.broker = broker

    async def publish(self, event: Event) -> None:
        """Publishes event to message broker"""
        pass

    async def publish_batch(self, events: List[Event]) -> PublishResult:
        """
        Publishes multiple events.
        Returns PublishResult with success_count and failed_events.
        Continues on individual failures.
        """
        pass
```

Requirements:
- Mock MessageBroker
- Test single event publish
- Test batch with all success
- Test batch with partial failure
- Verify event serialization
- Verify correct topic routing based on event type
```

---

## Prompt Templates for Common Patterns

### Template: Mock External Service

```
Generate mocks for this external service client:

[Paste interface/class here]

Framework: [pytest-mock/Jest/gomock/testify]
Language: [Python/TypeScript/Go]

Test scenarios:
- Success case with typical response
- Not found (404 or equivalent)
- Server error (5xx)
- Network timeout
- Rate limiting (429)

Additional requirements:
- [Type safety/autospec]
- [Async support if needed]
- [Response timing verification if needed]
```

### Template: Fake Data Store

```
Create a fake implementation for this repository:

[Paste interface here]

Requirements:
- In-memory storage
- Support for [specific queries]
- Unique constraints on [fields]
- Thread-safe: [yes/no]
- Test helper methods: [clear, count, seed, etc.]
```

### Template: Time-Dependent Tests

```
Generate time-mocking tests for:

[Paste function/class here]

Test cases:
- [List specific time scenarios]

Time mocking library: [freezegun/time-machine/Jest fake timers]
```

---

## Tips for Better LLM Mock Generation

### Do Provide

1. **Complete interface/signature** - Not just method names
2. **Expected behaviors** - What each method should return/throw
3. **Error types** - Specific exceptions to handle
4. **Framework preference** - pytest-mock vs unittest.mock
5. **Test scenario list** - What cases to cover

### Do Not Provide

1. **Implementation details** - LLM doesn't need internal logic
2. **Database schemas** - Unless mocking ORM
3. **Configuration values** - Keep tests focused

### Example of Good vs Bad Prompt

**Bad prompt:**
```
Write tests for my user service
```

**Good prompt:**
```
Generate pytest tests with mocks for this UserService:

```python
class UserService:
    def __init__(self, repo: UserRepository, cache: Cache):
        ...

    async def get_user(self, user_id: str) -> User:
        """
        1. Check cache first
        2. If cache miss, fetch from repo
        3. Cache result for 5 minutes
        4. Raises UserNotFoundError if not in repo
        """
        pass
```

Requirements:
- Use pytest-mock with AsyncMock
- Test cache hit scenario
- Test cache miss with repo fetch
- Test user not found
- Verify cache is set on cache miss
- Use freezegun if testing cache TTL
```

---

## Fixing Common LLM Mock Mistakes

### Wrong Patch Target

LLM output:
```python
@patch('external_module.requests.get')  # Wrong!
```

Fix:
```python
@patch('my_module.requests.get')  # Patch where it's used, not where it's defined
```

Prompt addition:
```
Remember to patch where the function is USED (in my_module), not where it's DEFINED (in requests).
```

### Missing Async Handling

LLM output:
```python
mock = Mock()
mock.fetch.return_value = {"data": "test"}
```

Fix:
```python
mock = AsyncMock()
mock.fetch.return_value = {"data": "test"}
```

Prompt addition:
```
This is an async function. Use AsyncMock and mark tests with @pytest.mark.asyncio.
```

### Over-Complicated Setup

LLM output:
```python
mock = Mock()
mock.client.session.connection.execute.return_value = ...
```

Fix:
```
The code has too many layers. Consider asking LLM to suggest refactoring for better testability.
```

Prompt addition:
```
If the mock setup becomes complex (more than 2 levels deep), suggest how to refactor the code for better testability instead.
```

---

*Use these prompts as starting points. Adjust based on your specific frameworks, patterns, and requirements.*
