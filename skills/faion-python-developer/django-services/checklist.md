# Django Services Layer Design Checklist

Step-by-step checklist for designing and implementing Django service layer architecture.

---

## Phase 1: Planning

### 1.1 Identify Business Operations

- [ ] List all CREATE operations in the app
- [ ] List all UPDATE operations in the app
- [ ] List all DELETE operations in the app
- [ ] Identify operations that span multiple models
- [ ] Identify operations with external API calls
- [ ] Identify operations requiring transaction safety

### 1.2 Identify Read Operations (Selectors)

- [ ] List complex queries (multi-join, aggregations)
- [ ] Identify permission-based filtering needs
- [ ] Identify queries that may cause N+1 issues
- [ ] List queries reused across multiple views

### 1.3 Choose File Structure

```
Simple app (< 10 services)    Complex app (10+ services)
------------------------      ------------------------
services.py                   services/
selectors.py                    __init__.py
                                user_services.py
                                order_services.py
                              selectors/
                                __init__.py
                                user_selectors.py
```

- [ ] Evaluate app complexity
- [ ] Choose single file or folder structure
- [ ] Create folder structure if needed
- [ ] Set up `__init__.py` exports

---

## Phase 2: Service Design

### 2.1 Naming Convention

Choose one pattern and document in project CLAUDE.md:

| Pattern | Example | When to Use |
|---------|---------|-------------|
| `entity_action` | `user_create()` | HackSoft style, recommended |
| `action_entity` | `create_user()` | Traditional Python style |

- [ ] Choose naming convention
- [ ] Document in project standards
- [ ] Verify consistency with existing code

### 2.2 Function Signature Design

For each service function:

- [ ] Use keyword-only arguments (`*` separator)
- [ ] Add full type hints (arguments and return type)
- [ ] Use TYPE_CHECKING for model imports
- [ ] Keep required args first, optional args after `*`
- [ ] Use `| None` for optional types
- [ ] Add trailing comma after last parameter

```python
def user_create(
    *,
    email: str,
    password: str,
    first_name: str | None = None,
    is_active: bool = True,
) -> User:
```

### 2.3 Docstring Requirements

Each service must have:

- [ ] One-line summary (what the function does)
- [ ] Business logic section (rules and side effects)
- [ ] Args section (describe each parameter)
- [ ] Returns section (what is returned)
- [ ] Raises section (custom exceptions)

---

## Phase 3: Implementation

### 3.1 Transaction Management

- [ ] Identify operations requiring atomicity
- [ ] Apply `@transaction.atomic` decorator
- [ ] Avoid catching exceptions inside atomic blocks
- [ ] Use `select_for_update()` for concurrent access
- [ ] Verify savepoint behavior in nested transactions

```python
from django.db import transaction

@transaction.atomic
def order_create(*, user: User, items: list[Item]) -> Order:
    # All operations inside are atomic
    ...
```

### 3.2 Input Validation

- [ ] Define validation at service entry point
- [ ] Use Pydantic models or dataclasses for complex inputs
- [ ] Raise `ValidationError` with clear messages
- [ ] Validate business rules (not just types)

```python
# Validate early, fail fast
def user_create(*, email: str, password: str) -> User:
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already registered")
    # ... proceed with creation
```

### 3.3 Error Handling

- [ ] Create service-specific exception hierarchy
- [ ] Use descriptive exception messages
- [ ] Include relevant context in exceptions
- [ ] Let exceptions bubble up (don't swallow)

```python
# exceptions.py
class ServiceError(Exception):
    """Base service exception."""

class UserNotFoundError(ServiceError):
    def __init__(self, user_id: int):
        super().__init__(f"User {user_id} not found")
        self.user_id = user_id
```

### 3.4 External Dependencies

- [ ] Inject external services via parameters
- [ ] Abstract external APIs behind interfaces
- [ ] Handle external service failures gracefully
- [ ] Add timeouts for external calls
- [ ] Log external service interactions

```python
def payment_process(
    *,
    order: Order,
    payment_gateway: PaymentGateway,  # Injected dependency
) -> PaymentResult:
    ...
```

---

## Phase 4: Selectors Design

### 4.1 Selector Function Criteria

Use selector when:

- [ ] Query spans multiple relations
- [ ] Query includes permission checks
- [ ] Query involves aggregations
- [ ] Property would cause N+1 when serialized
- [ ] Query logic is reused across views

### 4.2 Selector Implementation

- [ ] Return QuerySet (for further chaining) or list/object
- [ ] Use `select_related()` and `prefetch_related()` appropriately
- [ ] Document expected query count
- [ ] Add `only()` / `defer()` for optimization

```python
# selectors.py
def order_list_for_user(*, user: User) -> QuerySet[Order]:
    return (
        Order.objects
        .filter(user=user, is_visible=True)
        .select_related('user', 'payment')
        .prefetch_related('items')
        .order_by('-created_at')
    )
```

---

## Phase 5: Testing

### 5.1 Test Structure

- [ ] Create `tests/test_services.py` or `tests/services/` folder
- [ ] Create `tests/test_selectors.py` or `tests/selectors/` folder
- [ ] Set up Factory Boy factories for all models
- [ ] Set up fixtures in `conftest.py`

### 5.2 Test Coverage Requirements

For each service:

- [ ] Happy path test
- [ ] Validation error test
- [ ] Business rule violation test
- [ ] Edge cases (empty input, boundary values)
- [ ] Transaction rollback test (if applicable)
- [ ] External service failure test (if applicable)

```python
class TestUserCreate:
    def test_creates_user_with_valid_data(self, db):
        user = user_create(email="test@example.com", password="secure123")
        assert user.email == "test@example.com"
        assert user.check_password("secure123")

    def test_raises_error_for_duplicate_email(self, db, user_factory):
        existing = user_factory(email="taken@example.com")
        with pytest.raises(ValidationError, match="already registered"):
            user_create(email="taken@example.com", password="secure123")
```

### 5.3 Mocking Strategy

| Test Type | Database Access | External Services |
|-----------|-----------------|-------------------|
| Unit test | No (use `build()`) | Mock |
| Integration test | Yes (use `create()`) | Mock or use |
| E2E test | Yes | Real (staging) |

- [ ] Use `build()` for unit tests (no DB)
- [ ] Use `create()` for integration tests (with DB)
- [ ] Mock external services with `pytest-mock`
- [ ] Use `freezegun` for time-dependent tests

---

## Phase 6: Integration with Views/Serializers

### 6.1 View Integration

- [ ] Keep views thin (HTTP handling only)
- [ ] Call services from views
- [ ] Handle service exceptions in views
- [ ] Return appropriate HTTP status codes

```python
class UserCreateView(APIView):
    def post(self, request):
        try:
            user = user_create(
                email=request.data['email'],
                password=request.data['password'],
            )
            return Response(UserSerializer(user).data, status=201)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
```

### 6.2 Serializer Integration

- [ ] Use serializers for input validation (basic)
- [ ] Call services from serializer `.create()` / `.save()`
- [ ] Or call services from view and bypass serializer write

```python
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return user_create(**validated_data)
```

---

## Phase 7: Documentation

### 7.1 Code Documentation

- [ ] Docstrings on all public services
- [ ] Type hints on all functions
- [ ] Comments for non-obvious business logic
- [ ] Update CLAUDE.md with service patterns

### 7.2 Architecture Documentation

- [ ] Document service layer decisions in ADR
- [ ] Update API documentation
- [ ] Add examples to developer guide

---

## Quick Reference Card

### Service Function Template

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import transaction

if TYPE_CHECKING:
    from apps.users.models import User

@transaction.atomic
def entity_action(
    *,
    required_arg: str,
    optional_arg: str | None = None,
) -> ReturnType:
    """
    One-line description.

    Business logic:
    - Rule 1
    - Rule 2

    Args:
        required_arg: Description.
        optional_arg: Description.

    Returns:
        Description of return value.

    Raises:
        ValidationError: When validation fails.
    """
    # Implementation
    ...
```

### Red Flags Checklist

- [ ] Business logic in views
- [ ] Business logic in serializers
- [ ] Business logic in model `save()` override
- [ ] Missing transaction boundaries
- [ ] Swallowed exceptions
- [ ] God service (too many responsibilities)
- [ ] Circular imports between services

---

*Part of the faion-python-developer skill. Last updated: 2026-01.*
