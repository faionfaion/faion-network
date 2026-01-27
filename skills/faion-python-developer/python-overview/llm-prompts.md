# LLM Prompts for Python Development

Effective prompts for LLM-assisted Python development with Claude, GPT-4, Cursor, and Copilot.

---

## Prompting Principles

### Context Is Critical

LLMs perform best with relevant context:
- Include relevant imports and types
- Show existing code patterns
- Specify Python version (3.12+)
- Mention framework versions
- Reference coding standards

### Effective Prompt Structure

```
[CONTEXT] What exists / what you're working with
[TASK] What you want to accomplish
[CONSTRAINTS] Requirements, standards, limitations
[OUTPUT] Expected format/structure
```

### Iteration Strategy

1. **Start small:** Break complex tasks into focused requests
2. **Review output:** Check generated code against patterns
3. **Refine:** Iterate with specific corrections
4. **Test:** Always verify with tests

---

## Project Setup Prompts

### Initialize New Project

```
Create a Python project structure for a FastAPI REST API.

Requirements:
- Python 3.12+
- uv for package management
- ruff for linting/formatting
- pytest for testing
- src layout with package name "my_api"

Include:
- pyproject.toml with all tool configurations
- .pre-commit-config.yaml
- Basic directory structure
- README.md with setup instructions
```

### Add Dependencies

```
Update the pyproject.toml to add:
- SQLAlchemy 2.0+ for async database operations
- Alembic for migrations
- Redis for caching

Include dev dependencies:
- pytest-asyncio
- factory-boy for test factories

Keep existing configurations intact.
```

### Configure Code Quality

```
Create a comprehensive pyproject.toml configuration for:

Tools:
- ruff (linting + formatting)
- mypy (strict mode)
- pytest (with asyncio support)

Requirements:
- Line length: 100
- Python 3.12+
- Strict type checking
- Full coverage reporting

Include sensible defaults for a FastAPI project.
```

---

## Code Generation Prompts

### FastAPI Endpoint

```
Create a FastAPI endpoint for user registration.

Existing models:
```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str
```

Requirements:
- POST /api/v1/users
- Input validation with Pydantic
- Return 201 on success, 400 if email exists
- Use dependency injection for service
- Include comprehensive type hints
- Follow thin controller pattern (business logic in service)
```

### Service Layer

```
Create a UserService class for user management.

Interface:
- create_user(data: UserCreate) -> User
- get_user(user_id: int) -> User | None
- update_user(user_id: int, data: UserUpdate) -> User | None
- delete_user(user_id: int) -> bool

Requirements:
- Async methods
- Type hints for all parameters and returns
- Proper error handling
- Use repository pattern for data access
- Include docstrings (Google style)
```

### Database Model

```
Create a SQLAlchemy 2.0 model for a User entity.

Fields:
- id (UUID, primary key)
- email (unique, indexed)
- name
- hashed_password
- is_active (default True)
- created_at (auto-set)
- updated_at (auto-update)

Requirements:
- Use mapped_column with Mapped type hints
- Include relationships placeholder
- Add __repr__ method
- Follow naming conventions (snake_case)
```

### Async Operations

```
Implement concurrent API calls to fetch data from multiple endpoints.

Endpoints:
- /api/users/{id}
- /api/orders/{user_id}
- /api/preferences/{user_id}

Requirements:
- Use asyncio.gather for concurrent execution
- Handle individual failures gracefully
- Use Semaphore for rate limiting (max 5 concurrent)
- Return aggregated results
- Timeout: 30 seconds per request
- Use httpx.AsyncClient
```

---

## Testing Prompts

### Unit Tests

```
Write pytest unit tests for this function:

```python
def calculate_discount(
    price: float,
    discount_percent: float,
    max_discount: float | None = None,
) -> float:
    """Calculate discounted price."""
    discount = price * (discount_percent / 100)
    if max_discount is not None:
        discount = min(discount, max_discount)
    return round(price - discount, 2)
```

Test cases:
- Normal discount calculation
- Discount capped by max_discount
- Zero discount
- 100% discount
- Edge cases (negative values, boundary values)

Use pytest.mark.parametrize for multiple test cases.
```

### Integration Tests

```
Write integration tests for the UserService.

Service interface:
- async create_user(data: UserCreate) -> User
- async get_user(user_id: int) -> User | None

Requirements:
- Test with real database (use pytest fixture for test DB)
- Test successful creation
- Test duplicate email handling
- Test get existing user
- Test get non-existent user
- Use factory-boy for test data
- Clean up after tests
```

### API Tests

```
Write FastAPI endpoint tests for POST /api/v1/users.

Endpoint behavior:
- 201: User created successfully
- 400: Email already exists
- 422: Validation error

Test scenarios:
- Valid user creation
- Duplicate email
- Invalid email format
- Missing required fields
- Name too long (max 100 chars)

Use httpx.AsyncClient with ASGITransport.
Include fixtures in conftest.py.
```

---

## Refactoring Prompts

### Extract Service

```
Refactor this view to extract business logic into a service:

```python
@router.post("/orders")
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_db)):
    # Check inventory
    product = await db.get(Product, data.product_id)
    if not product or product.stock < data.quantity:
        raise HTTPException(400, "Insufficient stock")

    # Calculate total
    total = product.price * data.quantity
    if data.coupon_code:
        coupon = await db.execute(
            select(Coupon).where(Coupon.code == data.coupon_code)
        )
        if coupon:
            total *= (1 - coupon.discount / 100)

    # Create order
    order = Order(product_id=data.product_id, quantity=data.quantity, total=total)
    db.add(order)

    # Update stock
    product.stock -= data.quantity

    await db.commit()
    return order
```

Requirements:
- Create OrderService with proper type hints
- Keep view thin (HTTP handling only)
- Use dependency injection
- Handle transactions properly
- Add error handling
```

### Add Type Hints

```
Add comprehensive type hints to this module:

```python
def process_data(items, config=None):
    results = []
    for item in items:
        if config and config.get("filter"):
            if not config["filter"](item):
                continue
        processed = transform(item)
        results.append(processed)
    return results

def transform(item):
    return {
        "id": item["id"],
        "name": item["name"].upper(),
        "value": item.get("value", 0) * 2
    }
```

Requirements:
- Use TypedDict for structured dicts
- Use Protocol or Callable for filter function
- Import from collections.abc (not typing)
- Use X | None instead of Optional[X]
- Make types as specific as possible
```

### Improve Error Handling

```
Improve error handling in this code:

```python
async def fetch_user_data(user_id: int) -> dict:
    response = await client.get(f"/users/{user_id}")
    data = response.json()
    profile = await client.get(f"/profiles/{data['profile_id']}")
    return {
        "user": data,
        "profile": profile.json()
    }
```

Requirements:
- Handle HTTP errors (4xx, 5xx)
- Handle JSON parsing errors
- Handle missing keys
- Use custom exceptions
- Add logging
- Provide meaningful error messages
- Don't expose internal details to callers
```

---

## Documentation Prompts

### Add Docstrings

```
Add Google-style docstrings to these functions:

```python
async def create_user(
    email: str,
    name: str,
    password: str,
    role: UserRole = UserRole.USER,
) -> User:
    ...

async def authenticate(
    email: str,
    password: str,
) -> tuple[User, str] | None:
    ...
```

Include:
- One-line summary
- Args with types and descriptions
- Returns description
- Raises section for exceptions
- Example usage
```

### Generate API Documentation

```
Create OpenAPI documentation metadata for this FastAPI app:

Endpoints:
- POST /api/v1/auth/login
- POST /api/v1/auth/register
- GET /api/v1/users/me
- PUT /api/v1/users/me

Include:
- App title, description, version
- Tags with descriptions
- Response schemas
- Example requests/responses
- Authentication requirements
```

---

## Performance Prompts

### Optimize Query

```
Optimize this database query for better performance:

```python
async def get_orders_with_details(user_id: int) -> list[Order]:
    orders = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    result = []
    for order in orders.scalars():
        # N+1 query problem
        items = await db.execute(
            select(OrderItem).where(OrderItem.order_id == order.id)
        )
        order.items = items.scalars().all()
        result.append(order)
    return result
```

Requirements:
- Eliminate N+1 queries
- Use proper joins or eager loading
- Maintain async compatibility
- Include index recommendations
```

### Profile and Optimize

```
Analyze this code for performance issues and suggest optimizations:

```python
def process_large_dataset(data: list[dict]) -> list[dict]:
    results = []
    for item in data:
        if item["status"] == "active":
            processed = expensive_transform(item)
            if processed["value"] > 100:
                results.append(processed)

    # Sort by value
    results.sort(key=lambda x: x["value"], reverse=True)

    # Remove duplicates
    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)

    return unique
```

Suggest:
- Memory optimizations
- Algorithm improvements
- Parallelization opportunities
- Generator usage where appropriate
```

---

## Migration Prompts

### Upgrade Python Version

```
Update this code from Python 3.9 to Python 3.12 patterns:

```python
from typing import Dict, List, Optional, Union

def process(
    items: List[Dict[str, Union[str, int]]],
    config: Optional[Dict[str, str]] = None,
) -> List[str]:
    results: List[str] = []
    for item in items:
        if config is not None:
            ...
    return results
```

Apply:
- Use built-in generic types (list, dict)
- Use X | Y instead of Union
- Use X | None instead of Optional
- Use match statement where appropriate
- Import from collections.abc
```

### Migrate to Async

```
Convert this synchronous code to async:

```python
import requests

def get_user_data(user_ids: list[int]) -> list[dict]:
    results = []
    for user_id in user_ids:
        response = requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 200:
            results.append(response.json())
    return results
```

Requirements:
- Use httpx.AsyncClient
- Implement concurrent fetching with asyncio.gather
- Add error handling
- Add rate limiting (max 10 concurrent)
- Maintain type safety
```

---

## Project-Specific Rules

### Cursor Rules (.cursorrules)

```
# Python Project Rules

## Code Style
- Python 3.12+ features only
- Type hints required for all functions
- Google-style docstrings
- Line length: 100 characters
- Use ruff for formatting

## Imports
- Sort with isort rules
- Prefer collections.abc over typing
- No relative imports in src/

## Patterns
- Thin views/controllers
- Business logic in services
- Repository pattern for data access
- Dependency injection via FastAPI Depends

## Testing
- pytest with pytest-asyncio
- Factory-boy for test data
- Minimum 80% coverage

## Error Handling
- Custom exception classes
- No bare except
- Log all errors with context

## Async
- Use async/await for I/O
- httpx for HTTP clients
- asyncpg/aiosqlite for databases
```

### Claude Project Instructions

```
You are helping with a Python FastAPI project.

Tech stack:
- Python 3.12
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (async)
- pytest + pytest-asyncio
- uv for package management
- ruff for linting/formatting

Coding standards:
- All functions must have type hints
- Use Google-style docstrings
- Follow repository pattern
- Business logic in service layer
- Keep views/routes thin

When generating code:
- Include all necessary imports
- Use modern Python syntax (3.12+)
- Handle errors appropriately
- Add tests for new functionality

File structure:
src/app/
  models/      # Pydantic schemas
  entities/    # SQLAlchemy models
  routes/      # FastAPI routers
  services/    # Business logic
  repositories/ # Data access
```

---

## Common Tasks Quick Reference

| Task | Prompt Pattern |
|------|----------------|
| New endpoint | "Create [METHOD] [path] endpoint with [schema] validation" |
| Add tests | "Write pytest tests for [function/class] including [edge cases]" |
| Fix type errors | "Add type hints to make mypy pass in strict mode" |
| Refactor | "Extract [logic] into [service/function] following [pattern]" |
| Document | "Add Google-style docstrings with examples" |
| Optimize | "Profile and optimize for [memory/speed/queries]" |
| Migrate | "Update to Python 3.12+ patterns" |
| Debug | "Find the bug causing [error] when [condition]" |

---

*LLM Prompts for Python v1.0*
