# LLM Prompts for Django Code Quality

Effective prompts for LLM-assisted Django development with focus on code quality.

## Context Setup Prompts

### Project Context Template

```
I'm working on a Django project with the following stack:
- Django 5.2 / Python 3.12
- PostgreSQL database
- Django REST Framework for APIs
- pytest for testing
- Ruff for linting, mypy for type checking

Code standards:
- Service layer pattern (Hacksoft style)
- Type hints required on all functions
- Google-style docstrings
- Specific exception handling (no bare except)
```

### Quality Requirements Template

```
Generate code following these quality standards:
1. Full type hints (parameters and return types)
2. Google-style docstrings
3. Specific exception handling
4. Query optimization (select_related/prefetch_related)
5. Input validation
6. Logging for important operations
```

## Code Generation Prompts

### Generate Service Function

```
Create a Django service function for [OPERATION] with:

Context:
- Models: [LIST RELEVANT MODELS]
- Business rules: [DESCRIBE RULES]

Requirements:
- Type hints with django-stubs types
- Transaction handling with atomic()
- Specific exception handling
- Structured logging
- Input validation
- Docstring with Args, Returns, Raises

Function signature:
def [function_name](*, [params]) -> [ReturnType]:
```

**Example:**

```
Create a Django service function for creating a user subscription with:

Context:
- Models: User, Subscription, Plan
- Business rules: User can have only one active subscription, plan must be active

Requirements:
- Type hints with django-stubs types
- Transaction handling with atomic()
- Specific exception handling
- Structured logging
- Input validation
- Docstring with Args, Returns, Raises

Function signature:
def create_subscription(*, user: User, plan_id: int, payment_method_id: int) -> Subscription:
```

### Generate Optimized QuerySet

```
Create an optimized Django QuerySet for [OPERATION]:

Models involved:
- [Model1] has ForeignKey to [Model2]
- [Model1] has ManyToMany to [Model3]
- Need to access: [fields/relations needed]

Requirements:
- Use select_related for ForeignKey/OneToOne
- Use prefetch_related for ManyToMany/reverse FK
- Use Prefetch() for filtered related objects if needed
- Use only()/defer() for large fields
- Include pagination
- Return type-annotated function
```

**Example:**

```
Create an optimized Django QuerySet for fetching orders with user, items, and products:

Models involved:
- Order has ForeignKey to User
- Order has ForeignKey to ShippingAddress
- OrderItem has ForeignKey to Order (reverse relation: items)
- OrderItem has ForeignKey to Product

Need to access: user.email, shipping_address.city, item.quantity, item.product.name

Requirements:
- Use select_related for ForeignKey/OneToOne
- Use prefetch_related for ManyToMany/reverse FK
- Use Prefetch() for filtered related objects if needed
- Include pagination
- Return type-annotated function
```

### Generate Model with Quality Standards

```
Create a Django model for [ENTITY] with:

Fields:
- [field1]: [type] - [description]
- [field2]: [type] - [description]

Requirements:
- Proper field types with validators
- Database indexes for queried fields
- CheckConstraint for data integrity
- UniqueConstraint where needed
- __str__ method
- clean() method for model validation
- Proper Meta class (ordering, verbose_name)
- Type hints
```

### Generate API Endpoint

```
Create a Django REST Framework endpoint for [OPERATION]:

Context:
- Service function: [service_name]
- Permissions: [authentication requirements]

Requirements:
- Proper HTTP method and status codes
- Input validation via serializer
- Service layer integration
- Error handling with appropriate responses
- Rate limiting consideration
- Type hints
- Docstring with description
```

### Generate Test Suite

```
Create pytest tests for [SERVICE/VIEW]:

Context:
- Function/class being tested: [name]
- Dependencies to mock: [list]

Requirements:
- Use pytest fixtures for setup
- Test happy path
- Test validation errors
- Test edge cases
- Mock external dependencies
- Use factory_boy for model instances
- Follow Arrange-Act-Assert pattern
- Type hints on test functions
```

## Code Review Prompts

### Review for Quality Issues

```
Review this Django code for quality issues:

```python
[PASTE CODE]
```

Check for:
1. Missing type hints
2. Bare except or overly broad exception handling
3. N+1 query problems
4. Missing input validation
5. Security vulnerabilities
6. Missing tests
7. Code duplication
8. Naming conventions

Provide specific improvements for each issue found.
```

### Review for Security

```
Review this Django code for security vulnerabilities:

```python
[PASTE CODE]
```

Check for:
1. SQL injection vectors
2. XSS vulnerabilities
3. CSRF issues
4. Missing permission checks
5. Sensitive data exposure
6. Insecure direct object references
7. Mass assignment vulnerabilities
8. Hardcoded secrets

Provide OWASP classification and fix for each issue.
```

### Review for Performance

```
Review this Django code for performance issues:

```python
[PASTE CODE]
```

Check for:
1. N+1 queries (missing select_related/prefetch_related)
2. Unnecessary queries in loops
3. Missing database indexes
4. Large field loading (missing only/defer)
5. Missing pagination
6. Expensive operations in request cycle
7. Missing caching opportunities

Provide optimized version with query count estimates.
```

## Refactoring Prompts

### Extract Service Layer

```
Refactor this Django view to use service layer pattern:

```python
[PASTE VIEW CODE]
```

Requirements:
- Extract business logic to services.py
- Keep view thin (only HTTP handling)
- Add proper type hints
- Add error handling in view
- Make service testable in isolation
```

### Add Type Hints

```
Add comprehensive type hints to this Django code:

```python
[PASTE CODE]
```

Requirements:
- Use django-stubs types (HttpRequest, HttpResponse, QuerySet[Model])
- Use Optional, Union, list, dict appropriately
- Add return type hints
- Handle None cases explicitly
- No unnecessary casts
```

### Optimize Queries

```
Optimize the database queries in this code:

```python
[PASTE CODE]
```

Show:
1. Current query analysis (estimated query count)
2. Optimized version with select_related/prefetch_related
3. New query count
4. Any additional recommendations (indexes, caching)
```

## Configuration Prompts

### Generate Settings Module

```
Generate Django settings configuration for [ENVIRONMENT]:

Stack:
- Django [version]
- Database: [PostgreSQL/MySQL/SQLite]
- Cache: [Redis/Memcached]
- Task queue: [Celery/None]

Requirements:
- Environment variable management (django-environ)
- Security settings for production
- Logging configuration (structured)
- Connection pooling if PostgreSQL
- [Additional requirements]
```

### Generate Pre-commit Config

```
Generate pre-commit configuration for Django project:

Tools to include:
- Ruff (linting + formatting)
- mypy with django-stubs
- Django system checks
- Security scanning (bandit)
- pytest on push

Python version: [3.11/3.12]
Django version: [5.x/6.x]
```

## Debugging Prompts

### Debug N+1 Queries

```
I'm seeing slow performance in this Django code. Help identify N+1 queries:

```python
[PASTE CODE]
```

Models:
[DESCRIBE MODEL RELATIONSHIPS]

Provide:
1. List of N+1 query locations
2. Query count before optimization
3. Optimized code with select_related/prefetch_related
4. Query count after optimization
```

### Debug Type Errors

```
I'm getting mypy errors in this Django code:

```python
[PASTE CODE]
```

Error:
[PASTE MYPY ERROR]

Provide:
1. Explanation of the type error
2. Correct type annotation
3. Whether django-stubs types should be used
```

## Migration Prompts

### Generate Migration Strategy

```
I need to add/change [DESCRIBE CHANGE] to the [MODEL] model.

Current model:
```python
[PASTE MODEL]
```

Requirements:
- Zero-downtime migration
- Data preservation
- Backwards compatibility (if needed)

Provide:
1. Migration steps
2. Any data migration needed
3. Potential issues and solutions
```

## Documentation Prompts

### Generate API Documentation

```
Generate API documentation for this Django REST Framework viewset:

```python
[PASTE VIEWSET CODE]
```

Include:
- Endpoint URLs
- HTTP methods
- Request/response formats
- Authentication requirements
- Error responses
- Example requests with curl
```

### Generate Docstrings

```
Add comprehensive Google-style docstrings to this Django code:

```python
[PASTE CODE]
```

Requirements:
- Module docstring
- Class docstrings with Attributes section
- Function docstrings with Args, Returns, Raises
- Include types in docstrings
- Add usage examples for complex functions
```

## Quick Reference Prompts

### Quick Query Optimization

```
Optimize this Django QuerySet for accessing [RELATIONS]:
[ONE LINE QUERYSET]

Show optimized version with select_related/prefetch_related.
```

### Quick Exception Handling

```
Replace bare except with specific handling:
[CODE WITH BARE EXCEPT]

Context: This code [DESCRIBE WHAT IT DOES]
```

### Quick Type Hint

```
What's the correct type hint for:
- Django model instance: Answer with Model name
- QuerySet of models: QuerySet[Model]
- Request object: HttpRequest
- Response: HttpResponse or Response (DRF)
- Manager: Manager[Model]
- ForeignKey field access: Related model type
```

## Prompt Chaining Examples

### Complete Feature Development

**Step 1: Design**
```
Design a Django service for [FEATURE].
Include: function signatures, error types, data flow
```

**Step 2: Implementation**
```
Implement the service functions from the design:
[PASTE DESIGN]
```

**Step 3: Tests**
```
Generate pytest tests for the implemented service:
[PASTE SERVICE CODE]
```

**Step 4: API**
```
Create DRF endpoint that uses the service:
[PASTE SERVICE SIGNATURE]
```

**Step 5: Review**
```
Review the complete implementation for:
- Type safety
- Error handling
- Query optimization
- Security
```

## Anti-Patterns to Avoid in Prompts

### DO NOT ask for:

```
# BAD: Vague request
"Write some Django code"

# BAD: No quality requirements
"Create a view for user registration"

# BAD: No context
"Optimize this query"
```

### DO ask for:

```
# GOOD: Specific with quality requirements
"Create a Django service function for user registration with:
- Type hints
- Validation
- Specific exception handling
- Transaction management
- Logging"

# GOOD: Context provided
"Optimize this query. Models: Order -> User (FK), Order -> OrderItem (reverse FK).
Need to access user.email and all order items."
```
