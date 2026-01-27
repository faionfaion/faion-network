# LLM Prompts for Django Services

Effective prompts for LLM-assisted Django service layer design and implementation.

---

## Service Generation Prompts

### Generate a Complete Service

```
Create a Django service function for [OPERATION].

Context:
- Models: [list relevant models]
- Business rules: [describe rules]
- Transaction needed: [yes/no]

Requirements:
1. Use HackSoft naming: entity_action
2. Keyword-only arguments with * separator
3. Full type hints with TYPE_CHECKING pattern
4. Google-style docstring with Business logic section
5. @transaction.atomic if multiple DB operations
6. Custom exceptions for error cases

Example signature style:
def order_create(*, user: User, items: list[dict]) -> Order:
```

### Generate Service with Dependency Injection

```
Create a Django service with dependency injection for [OPERATION].

The service should:
1. Accept external dependencies as parameters
2. Define Protocol classes for dependencies
3. Be fully testable with mock objects

Dependencies needed:
- [PaymentGateway: describe interface]
- [EmailService: describe interface]

Include:
- Protocol definitions
- Service function with injected dependencies
- Example usage in views
```

### Refactor Fat Model to Service

```
Refactor this fat model method into a service function:

[PASTE MODEL CODE]

Requirements:
1. Extract business logic to services/{entity}_services.py
2. Keep model clean (only properties and simple methods)
3. Add transaction.atomic if needed
4. Create custom exceptions for error cases
5. Add comprehensive docstring
```

---

## Selector Generation Prompts

### Generate Optimized Selector

```
Create a Django selector for [QUERY DESCRIPTION].

Requirements:
1. Optimize for N+1 prevention
2. Use select_related for FK/OneToOne
3. Use prefetch_related for reverse FK/M2M
4. Document expected query count
5. Return QuerySet for chainability

Models involved:
- [Model1]: [describe relations]
- [Model2]: [describe relations]

Example output format:
def entity_list_for_user(*, user: User) -> QuerySet[Entity]:
    """
    Get entities for user.

    Query count: 3 (entities, related1, related2)
    """
```

### Generate Aggregation Selector

```
Create a Django selector with aggregations for [REPORT NAME].

Required aggregations:
- [Sum of field X]
- [Count of related Y]
- [Average of Z]

Group by: [field or time period]
Filter by: [conditions]

Use Django ORM aggregation functions.
Document the query and expected output format.
```

---

## Testing Prompts

### Generate Service Tests

```
Generate pytest tests for this Django service:

[PASTE SERVICE CODE]

Requirements:
1. Use pytest with pytest-django
2. Use Factory Boy for model instances
3. Test cases:
   - Happy path
   - Validation errors
   - Business rule violations
   - Edge cases
4. Use @pytest.mark.django_db where needed
5. Mock external dependencies
```

### Generate Factory Boy Factories

```
Create Factory Boy factories for these Django models:

[PASTE MODEL DEFINITIONS]

Requirements:
1. Use DjangoModelFactory
2. Use SubFactory for relations
3. Use LazyAttribute for computed fields
4. Use Sequence for unique fields
5. Use Faker for realistic data
6. Add traits for common variations
```

### Generate Integration Test

```
Create an integration test for this service workflow:

Workflow:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Test should:
1. Use real database (pytest-django)
2. Create all necessary test data with factories
3. Verify each step's side effects
4. Check final state is correct
5. Verify transaction rollback on failure
```

---

## Code Review Prompts

### Review Service for Best Practices

```
Review this Django service for best practices:

[PASTE SERVICE CODE]

Check for:
1. Transaction boundaries (are they correct?)
2. N+1 query issues
3. Error handling (custom exceptions?)
4. Input validation (at entry point?)
5. Type hints completeness
6. Docstring quality
7. Naming convention consistency
8. Separation of concerns

Provide specific improvements with code examples.
```

### Review Selector for Performance

```
Review this Django selector for performance:

[PASTE SELECTOR CODE]

Check for:
1. N+1 queries
2. Missing select_related/prefetch_related
3. Unnecessary fields loaded (use only/defer)
4. Missing indexes for filter fields
5. Potential for bulk operations

Provide the optimized version with query count documentation.
```

---

## Architecture Prompts

### Design Service Layer Structure

```
Design a service layer structure for this Django app:

App purpose: [describe app]

Models:
- [Model1]: [describe]
- [Model2]: [describe]

Operations needed:
- [List operations]

Questions to answer:
1. Single services.py or services/ folder?
2. What services do we need?
3. What selectors do we need?
4. What exceptions do we need?
5. File organization recommendation
```

### Convert Business Logic from Views

```
I have business logic scattered across views. Help me extract to services:

[PASTE VIEW CODE]

For each piece of business logic:
1. Identify what should be a service
2. Identify what should be a selector
3. Identify what should stay in view (HTTP only)
4. Propose the refactored structure
5. Show the resulting thin view
```

### Design Exception Hierarchy

```
Design a custom exception hierarchy for this Django app:

App: [name]
Domain: [describe domain]

Error cases to handle:
- [Error 1]
- [Error 2]
- [Error 3]

Create:
1. Base exception class
2. Category exceptions (Validation, NotFound, Permission, Business, External)
3. Specific domain exceptions
4. Appropriate HTTP status code mapping
```

---

## Migration Prompts

### Migrate from Fat Models

```
Help me migrate from fat models to service layer pattern.

Current model:
[PASTE FAT MODEL]

Create migration plan:
1. Identify business logic methods
2. Group by domain/entity
3. Create service functions for each
4. Update all callers
5. Remove methods from model
6. Keep only data-related methods on model

Provide step-by-step refactoring with code.
```

### Add Services to Existing App

```
I have an existing Django app without services. Help me add service layer:

Current structure:
- models.py: [describe]
- views.py: [describe where logic is]
- serializers.py: [describe where logic is]

Create:
1. services.py with extracted logic
2. selectors.py for complex queries
3. exceptions.py for custom errors
4. Updated views using services
5. Updated serializers using services
```

---

## Prompt Templates with Context

### Full Context Template

```
# Django Service Request

## Project Context
- Django version: [5.x]
- Python version: [3.11+]
- Project style: HackSoft styleguide
- Testing framework: pytest + Factory Boy

## Models
```python
[PASTE RELEVANT MODELS]
```

## Existing Services (for consistency)
```python
[PASTE EXAMPLE SERVICE]
```

## Request
[DESCRIBE WHAT YOU NEED]

## Requirements
- Keyword-only arguments
- Full type hints
- Transaction safety
- Custom exceptions
- Tests included
```

### Quick Request Template

```
Django service: [entity_action]
Models: [Model1, Model2]
Logic: [describe in 1-2 sentences]
Transaction: [yes/no]
External calls: [none / list them]
```

---

## Common Corrections

### Fix Missing Transaction

```
This service has multiple DB operations without @transaction.atomic:

[PASTE CODE]

Fix by:
1. Add @transaction.atomic decorator
2. Identify operations that should be atomic
3. Handle exceptions properly (no try/catch inside atomic)
```

### Fix N+1 Query

```
This selector causes N+1 queries:

[PASTE CODE]

Fix by:
1. Add select_related for [relations]
2. Add prefetch_related for [relations]
3. Use only() to limit fields if needed
4. Document final query count
```

### Fix Business Logic in Serializer

```
This serializer has business logic in create():

[PASTE CODE]

Refactor to:
1. Move logic to service function
2. Call service from serializer.create()
3. Or call service from view and use serializer for validation only
```

---

## Response Format Requests

### Request Specific Format

```
Generate Django service with this exact format:

1. File: services/{entity}_services.py
2. Imports: TYPE_CHECKING pattern
3. Function: def entity_action(*, ...) -> Type:
4. Docstring: Google style with Business logic section
5. Implementation with inline comments
6. Related test file: tests/services/test_{entity}_services.py
```

### Request Documentation

```
For this service, generate:

1. Docstring (Google style)
2. ADR explaining design decisions
3. Usage examples in views
4. Test examples
5. Update to CLAUDE.md section
```

---

*Part of the faion-python-developer skill. Last updated: 2026-01.*
