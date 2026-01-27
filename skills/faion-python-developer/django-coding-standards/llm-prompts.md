# LLM Prompts for Django Code Generation

> Copy-paste prompts for generating Django code with LLMs (Claude, GPT-4, etc.)

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Models](#models)
3. [Services](#services)
4. [Selectors](#selectors)
5. [APIs](#apis)
6. [Serializers](#serializers)
7. [Tests](#tests)
8. [Refactoring](#refactoring)
9. [Code Review](#code-review)

---

## Project Setup

### New Django App

```
Create a new Django app structure for {app_name} following HackSoft Django Styleguide.

Requirements:
- App handles {brief description of domain}
- Main entity: {Entity} with fields: {list fields}
- Related entities: {list related models if any}

Generate the following files:
1. models.py - BaseModel inheritance, proper Meta, clean() validation
2. constants.py - TextChoices for statuses, business limits
3. services.py - CRUD operations with transactions
4. selectors.py - list, get_by_id, filtered queries
5. apis.py - REST endpoints (list/create, detail, actions)
6. serializers.py - separate input/output serializers
7. urls.py - URL patterns
8. tests/ - test files for models, services, selectors, apis

Follow these patterns:
- Services: <entity>_<action> naming
- Selectors: <entity>_<query> naming
- Type hints on all functions
- Docstrings with Args, Returns, Raises
- Cross-app imports use aliases
```

### App Initialization Checklist

```
I'm starting a new Django {app_name} app. Generate a checklist of files to create and their purpose:

Domain: {describe the business domain}
Main entities: {list entities}
Key features: {list features}

For each file, provide:
1. Purpose
2. Key components to implement
3. Dependencies on other files
4. Testing requirements
```

---

## Models

### Create Model

```
Create a Django model for {Entity} following these standards:

Fields:
- {field_name}: {type} - {description}
- {field_name}: {type} - {description}

Requirements:
1. Inherit from BaseModel (has created_at, updated_at)
2. Use TextChoices for status field
3. Add clean() method for multi-field validation
4. Add CheckConstraint for DB-level rules
5. Define proper indexes for frequently queried fields
6. Add verbose_name, verbose_name_plural
7. Implement __str__ method
8. Add computed properties where useful

Relationships:
- {related model}: {relationship type} - {description}

Example business rules to enforce:
- {rule 1}
- {rule 2}
```

### Model with Relationships

```
Create Django models for an order system:

Models needed:
1. Order - belongs to User, has status, total, shipping address
2. OrderItem - belongs to Order and Product, has quantity, unit_price

Requirements:
- Proper foreign key relationships with related_name
- on_delete behavior (CASCADE for items, PROTECT for products)
- Method to calculate order total from items
- Validation that prevents modification of completed orders
- Indexes for user + status queries

Generate both models with full implementation.
```

### Model Migration

```
I have an existing {Entity} model and need to add:
- New field: {field_name} ({type})
- Default value for existing records: {value}
- Validation rule: {rule}

Generate:
1. Updated model code
2. Migration steps (if data migration needed)
3. Any necessary clean() updates
```

---

## Services

### Create Service

```
Create a service function {entity}_{action} for Django.

Purpose: {describe what it does}

Inputs:
- {param}: {type} - {description}
- {param}: {type} - {description}

Business rules:
- {rule 1}
- {rule 2}

Side effects:
- {e.g., send email, create log, queue task}

Follow these patterns:
1. Use keyword-only arguments (*)
2. Full type hints
3. Docstring with Args, Returns, Raises
4. Call full_clean() before save()
5. Use transaction.atomic() for multi-model operations
6. Specify update_fields in save()
7. Raise domain exceptions, not HTTP exceptions
```

### Service with Transaction

```
Create a service that atomically creates {Entity} with related {RelatedEntity} items.

Function signature: {entity}_create_with_items

Inputs:
- user: User
- {entity}_data: dict with {list fields}
- items: list[dict] with {list item fields}

Requirements:
1. Wrap in transaction.atomic()
2. Validate all items before creating anything
3. Calculate totals/aggregates
4. Queue background task after commit
5. Return created entity with items

Handle these error cases:
- Invalid item data
- Referenced entity not found
- Business limit exceeded
```

### Bulk Service

```
Create a bulk operation service for {Entity}.

Function: {entity}_bulk_{action}

Purpose: {describe bulk operation}

Input: list of {Entity} instances or IDs

Requirements:
1. Use bulk_update/bulk_create where possible
2. Validate all items first, fail fast
3. Use transaction for atomicity
4. Return count of affected records
5. Handle partial failures appropriately
```

---

## Selectors

### Create Selector

```
Create a selector function {entity}_{query_type} for Django.

Purpose: {describe the query}

Filters:
- {param}: {type} - {description}
- {param}: {type} - {description}

Requirements:
1. Return QuerySet[{Entity}] for lists, {Entity} for single
2. Use select_related for foreign keys
3. Use prefetch_related for reverse relations
4. Prevent N+1 queries
5. Support optional filtering
6. Add annotations if needed (counts, sums)
7. Define default ordering
```

### Complex Query Selector

```
Create a selector for {describe complex query need}.

Requirements:
- Filter by: {list filter criteria}
- Include aggregations: {list aggregations}
- Order by: {ordering}
- Prefetch: {list related data needed}

Expected usage:
```python
results = {entity}_list_with_stats(
    user=request.user,
    status="active",
    date_range=(start, end),
)
for item in results:
    print(item.total_amount)  # Annotated field
    print(item.items.all())   # Prefetched, no N+1
```

Generate optimized selector implementation.
```

### Paginated Selector

```
Create a selector that returns paginated results for {Entity}.

Requirements:
1. Accept limit and offset parameters
2. Return total count efficiently
3. Support cursor-based pagination option
4. Optimize for large datasets
5. Include related data without N+1
```

---

## APIs

### CRUD API

```
Create Django REST Framework API views for {Entity}.

Endpoints needed:
1. GET /api/{entities}/ - List with filters and pagination
2. POST /api/{entities}/ - Create new
3. GET /api/{entities}/{id}/ - Get single
4. PATCH /api/{entities}/{id}/ - Partial update
5. DELETE /api/{entities}/{id}/ - Delete/cancel

Requirements:
1. Use APIView (not viewsets)
2. Thin views - delegate to services/selectors
3. Separate input/output serializers
4. Proper permission classes
5. Consistent error responses
6. Include pagination for list

View structure:
1. Validate input (serializer)
2. Call service/selector
3. Serialize response
4. Return with proper status code
```

### Action API

```
Create an API endpoint for {describe action} on {Entity}.

Endpoint: POST /api/{entities}/{id}/{action}/

Input: {describe input data}
Output: {describe expected response}

Business rules:
- {rule 1}
- {rule 2}

Requirements:
1. Check permissions (ownership, role)
2. Validate entity state allows action
3. Call appropriate service
4. Return updated entity or action result
5. Handle errors with proper status codes
```

### Nested Resource API

```
Create API for {ChildEntity} nested under {ParentEntity}.

Endpoints:
- GET /api/{parents}/{id}/{children}/ - List children
- POST /api/{parents}/{id}/{children}/ - Add child
- DELETE /api/{parents}/{id}/{children}/{child_id}/ - Remove

Requirements:
1. Verify parent exists and user has access
2. Scope children to parent
3. Use parent context in service calls
4. Optimize queries for nested data
```

---

## Serializers

### Input/Output Serializers

```
Create serializers for {Entity}:

Input fields (for create/update):
- {field}: {type} - {validation rules}
- {field}: {type} - {validation rules}

Output fields (for responses):
- {field}: {type} - {source if different}
- {computed_field}: {how to compute}

Requirements:
1. Separate CreateRequest, UpdateRequest, Response serializers
2. UpdateRequest: all fields optional
3. Response: include computed/derived fields
4. Use SerializerMethodField for complex computations
5. Don't expose sensitive fields (password, internal IDs)
6. Validate cross-field constraints
```

### Nested Serializer

```
Create serializers for {Entity} with nested {RelatedEntity}.

Requirements:
1. List response: minimal fields for performance
2. Detail response: include nested items
3. Create request: accept nested items data
4. Use source for renamed fields
5. Handle nested validation
```

---

## Tests

### Service Tests

```
Generate pytest tests for the {entity}_{action} service.

Service does: {describe service behavior}

Test cases needed:
1. Success case with valid data
2. Success case with minimal data
3. Failure: {describe validation error case}
4. Failure: {describe business rule violation}
5. Failure: {describe not found case}

Requirements:
1. Use Factory Boy for test data
2. Descriptive test names (test_creates_entity_with_valid_data)
3. One assertion per test (when reasonable)
4. Test both return value and side effects
5. Use pytest.raises for error cases
```

### Selector Tests

```
Generate pytest tests for the {entity}_{query} selector.

Test cases needed:
1. Returns correct entities for filter criteria
2. Excludes entities not matching criteria
3. Handles empty results
4. N+1 query check (django_assert_num_queries)
5. Correct ordering

Use Factory Boy to create test data with various states.
```

### API Tests

```
Generate pytest tests for {Entity} API endpoints.

Endpoints to test:
- GET /api/{entities}/
- POST /api/{entities}/
- GET /api/{entities}/{id}/
- PATCH /api/{entities}/{id}/
- DELETE /api/{entities}/{id}/

Test cases per endpoint:
1. Success case (correct status code, response format)
2. Authentication required (401)
3. Validation error (400)
4. Not found (404)
5. Permission denied (403) - accessing other user's data

Use APIClient with force_authenticate for authenticated tests.
```

### Test Fixtures

```
Create pytest fixtures and Factory Boy factories for {app_name}.

Models: {list models}

Requirements:
1. UserFactory with realistic data
2. {Entity}Factory with all fields
3. Fixtures: api_client, authenticated_client
4. Fixtures: {entity}_for_user (creates entity owned by client.user)
5. Use factory.Faker for realistic data
6. Use factory.SubFactory for relationships
7. Use factory.LazyAttribute for computed values
```

---

## Refactoring

### Fat View to Service

```
Refactor this fat view to use service layer:

```python
{paste the fat view code}
```

Extract:
1. Business logic into services/{entity}_{action}.py
2. Complex queries into selectors/{entity}_{query}.py
3. Keep view thin (validate, call service, respond)

Follow HackSoft Django Styleguide patterns.
```

### Add Type Hints

```
Add comprehensive type hints to this Django code:

```python
{paste code without type hints}
```

Requirements:
1. All function parameters
2. All return types
3. Use | None instead of Optional
4. Use list[T] instead of List[T]
5. Use QuerySet[Model] for queryset returns
6. Add TYPE_CHECKING imports to avoid circular imports
```

### Optimize Queries

```
Analyze and optimize these Django queries for N+1 prevention:

```python
{paste code with potential N+1 issues}
```

For each query:
1. Identify N+1 problems
2. Add select_related for FK/OneToOne
3. Add prefetch_related for reverse FK/M2M
4. Consider using Prefetch for filtered prefetch
5. Add annotations for aggregations
6. Show before/after query count
```

### Extract Constants

```
Extract magic strings and numbers into constants:

```python
{paste code with magic values}
```

Create constants.py with:
1. TextChoices for status/type enums
2. Named constants for limits
3. Named constants for configuration values
4. Descriptive names following UPPER_SNAKE_CASE
```

---

## Code Review

### Review Prompt

```
Review this Django code for issues:

```python
{paste code to review}
```

Check for:

Architecture:
- [ ] Business logic in services (not views)
- [ ] Queries in selectors (not views)
- [ ] Models are slim
- [ ] No logic in serializers

Code Quality:
- [ ] Type hints on all functions
- [ ] Docstrings on public functions
- [ ] Cross-app imports use aliases
- [ ] No circular imports

Performance:
- [ ] N+1 queries addressed
- [ ] update_fields in save()
- [ ] Proper indexes defined
- [ ] Efficient existence checks

Security:
- [ ] Permissions checked
- [ ] No SQL injection risks
- [ ] Sensitive data not exposed

Testing:
- [ ] Service has unit tests
- [ ] API has integration tests

Provide specific recommendations for each issue found.
```

### Security Review

```
Security review this Django code:

```python
{paste code}
```

Check for:
1. SQL injection (raw queries with user input)
2. XSS (template rendering of user data)
3. CSRF protection
4. Authentication on all endpoints
5. Authorization (ownership checks)
6. Sensitive data exposure in responses
7. Rate limiting on sensitive endpoints
8. Secrets in code
9. Debug settings in production

Provide severity and fix for each issue.
```

---

## Quick Prompts

### Model Field

```
Add a {field_name} field to {Entity} model.
Type: {type}
Nullable: {yes/no}
Default: {value or none}
Indexed: {yes/no}
Validation: {rules}
```

### Service Function

```
Create service: {entity}_{action}
Input: {params with types}
Logic: {describe business logic}
Returns: {return type}
Errors: {list possible errors}
```

### API Endpoint

```
Create endpoint: {METHOD} /api/{path}/
Auth: {required/optional}
Input: {request body or params}
Output: {response format}
Permissions: {who can access}
```

### Test Case

```
Test: {entity}_{action} service
Case: {describe test scenario}
Setup: {test data needed}
Action: {what to call}
Assert: {expected outcome}
```

---

## Prompt Engineering Tips

### Be Specific

```
# Too vague
Create a user service

# Better
Create a service user_update_profile that:
- Updates name, bio, avatar_url fields
- Validates bio max length 500
- Validates avatar_url is valid URL
- Returns updated User
- Raises ValidationError for invalid data
```

### Provide Context

```
# Include relevant context
Given these existing models:
```python
class User(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
```

Create a service to... (now LLM knows the model structure)
```

### Request Format

```
# Specify output format
Generate the service with:
1. Full type hints
2. Docstring with Args, Returns, Raises
3. Error handling
4. No comments explaining obvious code
```

### Iterate

```
# First prompt
Create basic {entity}_create service

# Follow-up
Add transaction.atomic() and background task queuing

# Follow-up
Add validation for duplicate names per user
```
