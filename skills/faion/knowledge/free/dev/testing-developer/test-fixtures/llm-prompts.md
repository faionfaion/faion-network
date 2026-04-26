# LLM Prompts for Test Fixtures

Effective prompts for AI-assisted fixture creation, factory design, and test data generation.

---

## Context Setting Prompts

### Project Context

```
I'm working on a [Python/TypeScript/Go] project using [pytest/Jest/testing package].

Tech stack:
- Framework: [Django/FastAPI/Express/etc.]
- ORM: [SQLAlchemy/Django ORM/Prisma/GORM]
- Database: [PostgreSQL/MySQL/SQLite]

I need help creating test fixtures for [describe domain].
```

### Model Definition

```
Here are my models that need fixtures:

```python
# models.py
class User:
    id: str
    email: str
    name: str
    role: str
    created_at: datetime
    is_active: bool

class Order:
    id: str
    user_id: str  # FK to User
    status: str  # pending, completed, cancelled
    items: List[OrderItem]
    total: Decimal
```

Create factories/fixtures for these models with sensible defaults.
```

---

## Factory Creation Prompts

### Basic Factory

```
Create a Factory Boy factory for this Django model:

```python
class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Requirements:
- Use Sequence for unique fields
- Use LazyAttribute for computed fields
- Use SubFactory for relationships
- Include traits for common scenarios (out_of_stock, inactive, premium)
```

### Factory with Relationships

```
Create interconnected factories for an e-commerce domain:

Models:
- User (id, email, name)
- Order (id, user_id, status, created_at)
- OrderItem (id, order_id, product_id, quantity, price)
- Product (id, sku, name, price)

Requirements:
1. OrderFactory should auto-create a User via SubFactory
2. OrderItemFactory should create Order and Product
3. Include a factory method to create "Order with N items"
4. Handle total calculation based on items
```

### pytest-factoryboy Integration

```
I have these Factory Boy factories:

```python
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    # ... fields

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
    user = SubFactory(UserFactory)
    # ... fields
```

Show me:
1. How to register these with pytest-factoryboy
2. How to use them as fixtures in tests
3. How to override attributes using pytest.mark.parametrize
4. How to create related objects in tests
```

---

## pytest Fixture Prompts

### Basic Fixtures

```
Create pytest fixtures for a FastAPI application:

1. `app` - FastAPI application instance (session scope)
2. `client` - TestClient for HTTP requests
3. `async_client` - httpx.AsyncClient for async tests
4. `db_session` - SQLAlchemy session with transaction rollback
5. `authenticated_client` - Client with auth token

Include proper setup/teardown using yield.
```

### Database Fixtures

```
Create a complete database fixture setup for SQLAlchemy with pytest:

Requirements:
1. Session-scoped engine connected to test database
2. Session-scoped table creation
3. Function-scoped session with nested transaction (savepoint)
4. Automatic rollback after each test
5. Support for both sync and async tests

Database: PostgreSQL
ORM: SQLAlchemy 2.0 with async support
```

### Parametrized Fixtures

```
Create parametrized fixtures for testing different user roles:

Roles:
- anonymous (no user)
- user (basic permissions)
- editor (read + write)
- admin (all permissions)
- superadmin (all + system settings)

Each fixture should provide:
- User object (or None for anonymous)
- Expected permissions list
- HTTP client with appropriate auth

Tests should run once for each role.
```

---

## Builder Pattern Prompts

### Basic Builder

```
Create a test builder for this complex Order entity:

```python
@dataclass
class Order:
    id: str
    user_id: str
    items: List[OrderItem]
    status: str
    discount: Optional[Decimal]
    shipping_address: Optional[Address]
    billing_address: Optional[Address]
    notes: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

Builder requirements:
1. Fluent interface (method chaining)
2. Sensible defaults for all fields
3. Convenience methods: completed(), cancelled(), with_free_shipping()
4. Method to add items with automatic total calculation
5. Address builder or integration
```

### TypeScript Builder

```
Create a TypeScript test builder for:

```typescript
interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  discount?: number;
  shippingAddress?: Address;
  total: number;
  createdAt: Date;
}

interface OrderItem {
  id: string;
  productId: string;
  name: string;
  quantity: number;
  price: number;
}
```

Include:
1. Type-safe builder with proper TypeScript types
2. Method chaining with `this` return type
3. Automatic ID generation
4. Total calculation in build()
```

---

## Object Mother Prompts

```
Create Object Mother classes for common test scenarios:

Domain: E-commerce platform

UserMother scenarios:
- admin() - full admin user
- customer() - regular customer
- guest() - anonymous user representation
- banned_user() - user with banned status
- user_with_cart() - user with items in cart
- user_with_orders() - user with order history
- new_signup() - user without completed profile

OrderMother scenarios:
- pending_order()
- paid_order()
- shipped_order()
- delivered_order()
- cancelled_order()
- refunded_order()
- order_with_discount()
- large_order() - many items
- international_order() - non-US shipping

Make each method return fully valid objects ready for testing.
```

---

## Fixture Organization Prompts

### conftest.py Structure

```
Design a conftest.py hierarchy for a medium-sized Python project:

Project structure:
```
tests/
├── conftest.py           # Root
├── unit/
│   ├── conftest.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_database.py
└── e2e/
    ├── conftest.py
    └── test_flows.py
```

Define which fixtures go where:
- Root: app config, database engine
- Unit: mocks, simple fixtures
- Integration: real db session, test containers
- E2E: browser, full app setup

Include fixture scopes and dependency chains.
```

### Factory Organization

```
How should I organize factories for a large Django project?

Current structure:
```
myproject/
├── apps/
│   ├── users/
│   │   └── models.py
│   ├── orders/
│   │   └── models.py
│   └── products/
│       └── models.py
└── tests/
    ├── conftest.py
    └── ???
```

Questions:
1. Where to put factories? (One file? Per app? Separate package?)
2. How to share factories across test types (unit/integration)?
3. How to handle factory dependencies across apps?
4. How to register all factories with pytest-factoryboy?
```

---

## Specific Scenario Prompts

### API Testing Fixtures

```
Create fixtures for testing a REST API:

Endpoints:
- GET /users - list users
- POST /users - create user
- GET /users/{id} - get user
- PUT /users/{id} - update user
- DELETE /users/{id} - delete user

Need fixtures for:
1. Test client with auth headers
2. Sample users in database
3. Invalid request payloads
4. Expected response schemas

Framework: FastAPI with pytest
```

### Authentication Fixtures

```
Create fixtures for testing authentication flows:

Auth system: JWT with refresh tokens

Scenarios to test:
1. Valid access token
2. Expired access token
3. Invalid token signature
4. Missing token
5. Refresh token flow
6. Different user roles

Provide:
- Token generation fixtures
- Authenticated client fixtures
- User fixtures with tokens
```

### File Upload Fixtures

```
Create fixtures for testing file uploads:

Accepted files:
- Images (jpg, png, gif) - max 5MB
- Documents (pdf, docx) - max 10MB
- CSV files - max 50MB

Need fixtures that provide:
1. Valid files of each type
2. Invalid files (wrong format, too large, corrupted)
3. Cleanup after tests
4. Mock S3 storage for integration tests

Framework: Django with pytest
```

### Time-Dependent Fixtures

```
Create fixtures for testing time-dependent behavior:

Scenarios:
1. Subscription expiry (expires in past, today, future)
2. Scheduled tasks (due now, overdue, future)
3. Rate limiting (requests per minute)
4. Token expiration

Requirements:
- Use freezegun or time-machine for time control
- Fixtures should work with frozen time
- Clear naming indicating time scenario
```

---

## Debugging and Optimization Prompts

### Fixture Debugging

```
My fixtures are causing issues. Help me debug:

Problem: Tests pass individually but fail when run together.

Current fixtures:
```python
@pytest.fixture(scope="module")
def shared_user():
    return User(id="user-1", name="Test")

@pytest.fixture
def order(shared_user):
    return Order(user_id=shared_user.id, status="pending")
```

Tests are modifying the shared_user. How do I:
1. Identify which test is modifying state?
2. Fix the isolation issue?
3. Keep module scope for performance?
```

### Fixture Performance

```
My test suite is slow due to fixture setup. Help optimize:

Current situation:
- 500 tests
- Database fixtures recreated for each test
- Full app setup per test
- Suite takes 15 minutes

Current fixtures:
```python
@pytest.fixture
def db():
    engine = create_engine(...)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
```

How can I:
1. Reuse database schema across tests?
2. Use transactions instead of full setup/teardown?
3. Identify slowest fixtures?
4. Target: under 3 minutes
```

---

## Migration Prompts

### From Unittest to pytest

```
Help me migrate unittest fixtures to pytest:

Current unittest setup:
```python
class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(...)
        Base.metadata.create_all(cls.engine)

    def setUp(self):
        self.session = Session(self.engine)
        self.user = User(email="test@test.com")
        self.session.add(self.user)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
```

Convert to pytest fixtures with:
1. Proper scopes matching unittest lifecycle
2. Yield-based teardown
3. Shared conftest.py organization
```

### From Static Fixtures to Factories

```
I have JSON fixture files. Help me convert to factories:

Current: tests/fixtures/users.json
```json
{
  "user_1": {
    "id": 1,
    "email": "user1@test.com",
    "name": "User One",
    "role": "admin"
  },
  "user_2": {
    "id": 2,
    "email": "user2@test.com",
    "name": "User Two",
    "role": "user"
  }
}
```

Problems with current approach:
- Hard to customize per test
- IDs conflict between tests
- No relationship handling

Create Factory Boy factories that:
1. Generate unique IDs
2. Allow easy customization
3. Handle relationships (user has orders)
4. Maintain same "personas" as Object Mother methods
```

---

## Best Practices Review Prompts

```
Review my fixture setup for best practices:

```python
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="session")
def Session(db_engine):
    return sessionmaker(bind=db_engine)

@pytest.fixture
def db(Session):
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def user(db):
    user = User(email="test@test.com")
    db.add(user)
    db.commit()
    return user
```

Check for:
1. Scope appropriateness
2. Cleanup completeness
3. Test isolation
4. Naming conventions
5. Potential issues with parallel execution
```

---

## Tips for Effective Prompting

1. **Always provide model definitions** - LLMs need to see the data structure

2. **Specify the framework** - pytest vs unittest, Factory Boy vs custom factories

3. **Include relationships** - Show foreign keys and related models

4. **State the test type** - Unit tests need mocks, integration tests need real data

5. **Mention constraints** - Unique fields, validation rules, required relationships

6. **Describe scenarios** - What states/configurations need to be tested

7. **Ask for specific patterns** - Factory, Builder, Object Mother

8. **Include existing code** - Show your conftest.py for context
