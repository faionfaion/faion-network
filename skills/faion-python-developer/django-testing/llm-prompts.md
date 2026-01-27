# LLM Prompts for Django Testing

Effective prompts for LLM-assisted Django test generation.

## Table of Contents

1. [Model Test Prompts](#model-test-prompts)
2. [Service Test Prompts](#service-test-prompts)
3. [View Test Prompts](#view-test-prompts)
4. [API Test Prompts](#api-test-prompts)
5. [Factory Creation Prompts](#factory-creation-prompts)
6. [Fixture Prompts](#fixture-prompts)
7. [Refactoring Prompts](#refactoring-prompts)
8. [Debugging Prompts](#debugging-prompts)
9. [Coverage Improvement Prompts](#coverage-improvement-prompts)

---

## Model Test Prompts

### Generate Model Tests

```
Write pytest tests for this Django model:

```python
[PASTE YOUR MODEL CODE HERE]
```

Requirements:
- Use pytest-django with @pytest.mark.django_db
- Use model_bakery for fixtures
- Test __str__ method
- Test custom methods/properties
- Test model constraints (unique, validators)
- Include edge cases (None, empty values)
- Follow AAA pattern (Arrange-Act-Assert)
```

### Test Model Manager/QuerySet

```
Write tests for these custom QuerySet methods:

```python
[PASTE YOUR MANAGER/QUERYSET CODE HERE]
```

Requirements:
- Test each queryset method separately
- Create appropriate test data with model_bakery
- Test filtering logic
- Test ordering
- Test empty results
- Verify queryset returns correct objects
```

### Test Model Signals

```
Write tests for this Django signal:

```python
[PASTE YOUR SIGNAL CODE HERE]
```

Requirements:
- Use pytest-django
- Mock signal handlers where appropriate
- Test signal is called on correct event (create/update/delete)
- Test signal handler side effects
- Use factory.django.mute_signals when needed
```

---

## Service Test Prompts

### Generate Service Tests

```
Write pytest tests for this Django service:

```python
[PASTE YOUR SERVICE CODE HERE]
```

Requirements:
- Use pytest-django with @pytest.mark.django_db
- Use model_bakery or Factory Boy for test data
- Test happy path
- Test error cases (raises exceptions)
- Test edge cases (None, empty, boundary values)
- Mock external dependencies if any
- Verify database state changes
```

### Test Service with External API

```
Write tests for this service that calls an external API:

```python
[PASTE YOUR SERVICE CODE HERE]
```

Requirements:
- Use pytest with unittest.mock.patch
- Mock the external API calls
- Test successful API response
- Test API failure/timeout handling
- Test retry logic if present
- Verify correct API parameters are sent
```

### Test Transaction Handling

```
Write tests for this service with transaction management:

```python
[PASTE YOUR SERVICE CODE HERE]
```

Requirements:
- Use @pytest.mark.django_db(transaction=True)
- Test atomic operations complete fully
- Test rollback on failure
- Verify database state after both success and failure
```

---

## View Test Prompts

### Test Function-Based View

```
Write pytest tests for this Django view:

```python
[PASTE YOUR VIEW CODE HERE]
```

URL pattern: [PASTE URL PATTERN]

Requirements:
- Use Django test client fixture
- Test GET/POST methods
- Test authentication required (if applicable)
- Test permission checks
- Test form validation
- Test redirect behavior
- Test context data
- Test template used
```

### Test Class-Based View

```
Write pytest tests for this Django CBV:

```python
[PASTE YOUR VIEW CODE HERE]
```

Requirements:
- Test each HTTP method (get, post, put, delete)
- Test authentication/permission mixins
- Test queryset filtering (get_queryset)
- Test form handling (form_valid, form_invalid)
- Test context data (get_context_data)
- Test success URL
```

### Test View with File Upload

```
Write tests for this view that handles file uploads:

```python
[PASTE YOUR VIEW CODE HERE]
```

Requirements:
- Use pytest tmp_path fixture for temp files
- Create test files using SimpleUploadedFile
- Test valid file upload
- Test invalid file type
- Test file size limits
- Clean up uploaded files after test
```

---

## API Test Prompts

### Test DRF ViewSet

```
Write pytest tests for this DRF ViewSet:

```python
[PASTE YOUR VIEWSET CODE HERE]
```

Serializer:
```python
[PASTE SERIALIZER CODE]
```

Requirements:
- Use rest_framework.test.APIClient
- Test list, retrieve, create, update, destroy actions
- Test authentication (401 for unauthenticated)
- Test permissions (403 for unauthorized)
- Test serializer validation (400 for invalid data)
- Test filtering/search/ordering if present
- Test pagination
- Verify response data structure
```

### Test DRF Serializer

```
Write tests for this DRF serializer:

```python
[PASTE YOUR SERIALIZER CODE HERE]
```

Requirements:
- Test serialization (output format)
- Test deserialization (input validation)
- Test required fields
- Test field-level validation
- Test custom validate methods
- Test nested serializers if present
- Test sensitive fields are hidden
```

### Test API Authentication

```
Write tests for API authentication:

Endpoint: [PASTE ENDPOINT]
Auth method: [JWT/Token/Session]

Requirements:
- Test unauthenticated request returns 401
- Test invalid token returns 401
- Test expired token returns 401
- Test valid token returns 200
- Test token refresh if applicable
```

### Test API Permissions

```
Write tests for these API permissions:

```python
[PASTE YOUR PERMISSION CLASS HERE]
```

Requirements:
- Test permission allows owner
- Test permission denies non-owner
- Test permission allows admin
- Test object-level permissions
- Use parametrize for different user roles
```

---

## Factory Creation Prompts

### Create Factory Boy Factory

```
Create a Factory Boy factory for this Django model:

```python
[PASTE YOUR MODEL CODE HERE]
```

Requirements:
- Use DjangoModelFactory base class
- Handle ForeignKey with SubFactory
- Handle ManyToMany with post_generation
- Use Faker for realistic data
- Add Params traits for common variations
- Use Sequence for unique fields
- Handle password fields correctly
```

### Create Factory with Relationships

```
Create Factory Boy factories for these related models:

```python
[PASTE ALL RELATED MODELS HERE]
```

Requirements:
- Create factory for each model
- Use SubFactory for ForeignKey
- Use RelatedFactory for reverse relations
- Use post_generation for ManyToMany
- Ensure factories can be used independently
- Add traits for common test scenarios
```

### Convert model_bakery to Factory Boy

```
Convert these model_bakery calls to Factory Boy factories:

```python
[PASTE YOUR TESTS WITH BAKER.MAKE CALLS]
```

Requirements:
- Create explicit Factory classes
- Preserve field values and relationships
- Add appropriate Faker declarations
- Include useful traits
- Register factories with pytest-factoryboy
```

---

## Fixture Prompts

### Create conftest.py Fixtures

```
Create pytest fixtures for this test file:

```python
[PASTE YOUR TEST FILE]
```

Requirements:
- Identify repeated setup code
- Create reusable fixtures
- Use appropriate fixture scope
- Handle cleanup in fixtures
- Create fixtures for API clients
- Create fixtures for authenticated users
```

### Optimize Fixture Performance

```
Optimize these fixtures for better performance:

```python
[PASTE YOUR CONFTEST.PY]
```

Requirements:
- Use session/module scope where appropriate
- Reduce database queries
- Use batch creation
- Cache expensive operations
- Identify and fix fixture dependency issues
```

---

## Refactoring Prompts

### Refactor Duplicate Test Code

```
Refactor these tests to reduce duplication:

```python
[PASTE YOUR TEST FILE WITH DUPLICATES]
```

Requirements:
- Extract common setup to fixtures
- Use parametrize for similar tests
- Create helper methods for repeated assertions
- Maintain test readability
- Keep tests independent
```

### Convert unittest to pytest

```
Convert these unittest tests to pytest style:

```python
[PASTE YOUR UNITTEST TESTS]
```

Requirements:
- Replace TestCase with functions/classes
- Replace self.assert* with plain assert
- Replace setUp/tearDown with fixtures
- Replace setUpClass with session-scoped fixtures
- Use pytest.raises instead of assertRaises
- Use pytest.mark.parametrize instead of subTest
```

### Modernize Legacy Tests

```
Modernize these Django tests to use current best practices:

```python
[PASTE YOUR OLD TESTS]
```

Requirements:
- Use pytest-django instead of Django TestCase
- Replace fixtures files with factories
- Use model_bakery or Factory Boy
- Add proper markers (@pytest.mark.django_db)
- Improve test names to be descriptive
- Add type hints where helpful
```

---

## Debugging Prompts

### Fix Failing Test

```
This test is failing. Help me understand why and fix it:

Test code:
```python
[PASTE YOUR TEST]
```

Error message:
```
[PASTE ERROR MESSAGE]
```

Code being tested:
```python
[PASTE THE CODE BEING TESTED]
```
```

### Debug Test Isolation Issue

```
These tests pass individually but fail when run together:

Test 1:
```python
[PASTE TEST 1]
```

Test 2:
```python
[PASTE TEST 2]
```

Help me identify the isolation issue and fix it.
```

### Debug Database Access Error

```
I'm getting a database access error in my test:

Test:
```python
[PASTE TEST]
```

Error:
```
Database access not allowed
```

Help me understand why and fix the issue.
```

---

## Coverage Improvement Prompts

### Identify Missing Tests

```
Analyze this code and identify what tests are missing:

```python
[PASTE YOUR CODE]
```

Existing tests:
```python
[PASTE EXISTING TESTS]
```

Identify:
- Untested methods/functions
- Missing edge cases
- Uncovered branches
- Missing error handling tests
```

### Generate Tests for Uncovered Lines

```
Generate tests to cover these uncovered lines:

Code:
```python
[PASTE CODE WITH LINE NUMBERS]
```

Coverage report shows these lines are uncovered:
[LIST UNCOVERED LINE NUMBERS]

Generate tests to achieve 100% coverage.
```

### Improve Branch Coverage

```
Improve branch coverage for this code:

```python
[PASTE YOUR CODE]
```

Current tests:
```python
[PASTE CURRENT TESTS]
```

Coverage shows these branches are not covered:
[DESCRIBE UNCOVERED BRANCHES]

Generate additional tests to cover all branches.
```

---

## Prompt Engineering Tips

### Context to Always Include

When asking LLMs to generate Django tests, always provide:

1. **Full model/service/view code** - Not just function signatures
2. **Related models** - For relationship handling
3. **Existing test setup** - conftest.py, existing factories
4. **Project conventions** - Testing style preferences
5. **Error messages** - When debugging

### Prompt Structure

```
[TASK]: What you want (generate tests, fix issue, etc.)

[CONTEXT]:
```python
# Relevant code
```

[REQUIREMENTS]:
- Specific requirements
- Constraints
- Patterns to follow

[EXAMPLE OUTPUT] (optional):
```python
# Example of desired output format
```
```

### Common Issues to Specify

- "Use model_bakery, not Django fixtures"
- "Use pytest.mark.django_db decorator"
- "Follow AAA pattern (Arrange-Act-Assert)"
- "Include edge cases for None and empty values"
- "Mock external services, test real database"
- "Use factories for complex object creation"

### Iterative Refinement

1. Start with basic tests
2. Ask for edge cases
3. Ask for parametrized versions
4. Ask for performance improvements
5. Ask for refactoring suggestions

---

## Example Prompt Session

### Initial Prompt

```
Write pytest tests for this Django service:

```python
from decimal import Decimal
from apps.orders.models import Order, OrderItem
from apps.products.models import Product

class OrderService:
    @staticmethod
    def create_order(user, items: list[dict]) -> Order:
        if not items:
            raise ValueError("Order must have at least one item")

        order = Order.objects.create(user=user, total=Decimal('0'))

        for item_data in items:
            product = Product.objects.get(pk=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
            order.total += product.price * item_data['quantity']

        order.save()
        return order
```

Requirements:
- Use pytest-django
- Use model_bakery for fixtures
- Test happy path and error cases
```

### Follow-up for Edge Cases

```
Add tests for these edge cases:
- Product not found
- Negative quantity
- Zero quantity
- Multiple items in order
- Large quantities (1000+)
```

### Follow-up for Parametrization

```
Refactor the validation tests using @pytest.mark.parametrize
to test multiple invalid inputs efficiently.
```

---

*See also: [README.md](README.md) for overview, [examples.md](examples.md) for test examples*
