# LLM Prompts for Django API Development

Effective prompts for LLM-assisted Django REST API development.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Models and Migrations](#2-models-and-migrations)
3. [Serializers](#3-serializers)
4. [Views and ViewSets](#4-views-and-viewsets)
5. [Authentication](#5-authentication)
6. [Permissions](#6-permissions)
7. [Filtering and Search](#7-filtering-and-search)
8. [Documentation](#8-documentation)
9. [Testing](#9-testing)
10. [Django Ninja](#10-django-ninja)
11. [Debugging and Optimization](#11-debugging-and-optimization)

---

## Prompt Structure

### Effective Prompt Template

```
Context: [Framework version, existing code structure]
Task: [What you want to accomplish]
Constraints: [Requirements, patterns to follow]
Output: [Expected format]
```

### Key Principles

1. **Provide context**: Django/DRF version, existing models, project structure
2. **Be specific**: Include field types, validation rules, response formats
3. **Reference patterns**: Mention thin views, service layer, specific serializers
4. **Request tests**: Always ask for test cases alongside implementation

---

## 1. Project Setup

### Initial DRF Configuration

```
Create REST_FRAMEWORK settings for Django 5.x with DRF 3.15:
- JWT authentication (simplejwt)
- IsAuthenticated default permission
- PageNumber pagination (20 items)
- DjangoFilterBackend, SearchFilter, OrderingFilter
- URL path versioning (v1)
- drf-spectacular for OpenAPI schema
- Custom datetime format ISO 8601

Include SIMPLE_JWT settings with:
- 15 minute access token
- 7 day refresh token
- Token rotation enabled
- Blacklisting enabled

Include SPECTACULAR_SETTINGS with project metadata.
```

### Django Ninja Setup

```
Create Django Ninja API setup for Django 5.x with Ninja 1.x:
- JWT authentication with custom bearer class
- API versioning support
- Pydantic v2 schemas
- Error handling
- CORS configuration

Include:
- Main api.py with NinjaAPI instance
- AuthBearer class for JWT validation
- Router organization pattern
- URL configuration for urls.py
```

---

## 2. Models and Migrations

### Create Model with Best Practices

```
Create a Django model for {ModelName} with these fields:
{list fields with types}

Requirements:
- UUID field for public identifier (uid)
- created_at and updated_at timestamps
- Proper indexes for query fields
- __str__ method returning meaningful representation
- related_name for all ForeignKeys
- Choices as class attributes (not inline)
- Manager for common queries (optional)

Follow patterns from django-base-model.md methodology.
```

### Example: Order Model

```
Create a Django Order model with:
- user (ForeignKey to User)
- items (ManyToMany to Product through OrderItem)
- total (DecimalField)
- status (choices: pending, processing, shipped, delivered, cancelled)
- shipping_address (ForeignKey to Address)
- notes (TextField, optional)

Include:
- UUID public identifier
- Timestamps
- Status transitions validation
- Manager method: get_active_orders(user)
- Property: is_cancellable
```

---

## 3. Serializers

### Input/Output Serializer Pair

```
Create DRF serializers for {Model}:

1. Create{Model}Serializer (input validation):
   - Fields: {list input fields}
   - Validate: {validation rules}
   - Cross-field validation: {rules if any}

2. {Model}Serializer (output):
   - Fields: {list output fields}
   - Read-only: id, uid, timestamps
   - Nested: {related serializers if any}

3. {Model}ListSerializer (minimal output for lists):
   - Fields: id, uid, {key fields only}

Follow explicit field lists (no fields = "__all__").
Include field-level and object-level validation.
```

### Nested Serializer Example

```
Create DRF serializers for Order with nested OrderItems:

Input (CreateOrderSerializer):
- items: list of {product_id: int, quantity: int}
- shipping_address_id: int
- Validate: max 100 items, all products exist, products in stock

Output (OrderDetailSerializer):
- id, uid, status, total, created_at
- items: nested OrderItemSerializer (product name, quantity, price)
- shipping_address: nested AddressSerializer

Output (OrderListSerializer):
- id, uid, status, total, items_count, created_at
```

---

## 4. Views and ViewSets

### ViewSet with Full CRUD

```
Create a ModelViewSet for {Model} with:

Configuration:
- queryset with select_related/prefetch_related for {relations}
- Filter by user's organization in get_queryset
- Different serializers for list/create/update/detail actions
- Search fields: {fields}
- Ordering fields: {fields}
- Default ordering: -created_at
- FilterSet class: {Model}Filter

Custom actions:
- {action_name} (POST on detail): {description}

Documentation:
- extend_schema_view for all standard actions
- extend_schema for custom actions
- Tag: {Tag name}

Follow thin views pattern - delegate business logic to services.
```

### Custom APIView

```
Create an APIView for {action description}:

Endpoint: POST /api/v1/{path}/
Permission: IsAuthenticated
Input: {input fields with validation}
Output: {output fields}
Errors: {error cases with status codes}

Requirements:
- Validate input with serializer
- Call service layer for business logic
- Handle service exceptions
- Return appropriate response codes
- Add @extend_schema documentation

Include the service function signature (don't implement full service).
```

---

## 5. Authentication

### JWT Setup with Custom Claims

```
Create JWT authentication setup for DRF with simplejwt:

1. CustomTokenObtainPairSerializer:
   - Add claims: email, role, organization_id
   - Add last_login update

2. CustomTokenObtainPairView:
   - Use custom serializer
   - Add rate limiting (5/minute)

3. URLs:
   - /auth/token/ - obtain pair
   - /auth/token/refresh/ - refresh
   - /auth/token/verify/ - verify

4. Settings:
   - Access: 15 min
   - Refresh: 7 days
   - Rotation: enabled
   - Blacklist: enabled

Include extend_schema documentation for all endpoints.
```

### OAuth2 / Social Auth Setup

```
Create OAuth2 authentication setup for DRF:

Providers: Google, GitHub
Package: django-allauth + dj-rest-auth

Include:
1. Settings configuration
2. URL configuration
3. Serializers for social login
4. View for token exchange
5. User creation/linking logic

Requirements:
- Create user if not exists
- Link social account to existing user by email
- Return JWT tokens after social auth
- Handle missing email edge case
```

---

## 6. Permissions

### Custom Permission Classes

```
Create custom DRF permission classes:

1. IsOrganizationMember:
   - Object must belong to user's organization
   - Check obj.organization or obj.user.organization

2. IsOwnerOrReadOnly:
   - Owner can modify, others can only read
   - Check obj.user == request.user

3. Is{Role}:
   - Only users with specific role can access
   - Check request.user.role == '{role}'

4. IsAdminOrOwner:
   - Admin users or object owner can access
   - Combine is_staff check with owner check

Include:
- Proper error messages
- has_permission and has_object_permission where appropriate
- Docstrings explaining the permission logic
```

### Dynamic Permission by Action

```
Create a ViewSet permission setup where:
- list, retrieve: IsAuthenticated
- create: IsAuthenticated + IsOrganizationMember
- update, partial_update: IsOwnerOrAdmin
- destroy: IsAdminOnly
- {custom_action}: {custom permission}

Implement get_permissions() method with action-based logic.
Include test cases for each permission scenario.
```

---

## 7. Filtering and Search

### FilterSet with Advanced Filters

```
Create a django-filter FilterSet for {Model}:

Filters:
- {field}: exact match
- {field}: choices (from model)
- {field}_min, {field}_max: range
- created_after, created_before: date range
- {boolean_field}: boolean
- {relation}__id: related object filter
- search: custom method filter (searches multiple fields)
- has_{relation}: custom boolean (exists check)

Include:
- Meta class with model and default fields
- Custom filter methods with documentation
- Integration with ViewSet (filterset_class)
```

### Full-Text Search Setup

```
Create a search endpoint for {Model} using:
- django-filter for field filters
- SearchFilter for text search
- OrderingFilter for sorting

Searchable fields: {fields}
Filterable fields: {fields}
Orderable fields: {fields}

Include:
- Search behavior configuration (icontains vs exact)
- Multiple search terms handling
- Search field prefixes (^ for startswith, @ for search)
- ViewSet configuration
- Example API calls in documentation
```

---

## 8. Documentation

### OpenAPI Schema with drf-spectacular

```
Add drf-spectacular documentation to {ViewSet/APIView}:

Requirements:
- @extend_schema for each endpoint
- summary: short description (< 10 words)
- description: detailed explanation with business rules
- request: input serializer
- responses: {status_code: serializer} mapping
- tags: [{tag_name}]
- parameters: query params with OpenApiParameter
- examples: OpenApiExample for request/response

Include error responses:
- 400: validation errors
- 401: unauthorized
- 403: forbidden
- 404: not found

Follow drf-spectacular best practices.
```

### API Examples in Documentation

```
Create OpenApiExample instances for {endpoint}:

Request examples:
- Valid request with all fields
- Valid request with minimal fields
- Invalid request (for error documentation)

Response examples:
- Success response
- Created response (for POST)
- Error response with field errors

Include realistic data, not lorem ipsum.
```

---

## 9. Testing

### ViewSet Test Suite

```
Create pytest test suite for {Model}ViewSet:

Test class structure:
- setUpTestData: create user, organization, test objects
- setUp: authenticate client

Test cases:
- test_list_{models}_authenticated: 200 + results
- test_list_{models}_unauthenticated: 401
- test_list_{models}_filtered: filter params work
- test_list_{models}_paginated: pagination metadata
- test_create_{model}_valid: 201 + object created
- test_create_{model}_invalid: 400 + field errors
- test_retrieve_{model}: 200 + correct data
- test_retrieve_{model}_not_found: 404
- test_update_{model}: 200 + updated data
- test_update_{model}_partial: PATCH works
- test_delete_{model}: 204 + object deleted
- test_permission_{scenario}: permission checks

Use:
- APITestCase or pytest-django
- reverse() for URLs
- force_authenticate for auth
- Factories or setUpTestData for test data
```

### Service Layer Tests

```
Create unit tests for {service_function}:

Test scenarios:
- Happy path: valid input returns expected result
- Validation: invalid input raises appropriate error
- Edge cases: boundary conditions
- Permissions: unauthorized access raises error
- Side effects: external calls (mock them)

Use:
- pytest with django
- Mock for external dependencies
- Factory Boy for test data
- Transactions for database isolation

Include docstrings explaining each test scenario.
```

---

## 10. Django Ninja

### Ninja CRUD Endpoints

```
Create Django Ninja CRUD endpoints for {Model}:

Schemas:
- Create{Model}Schema: input with Pydantic validation
- Update{Model}Schema: partial update (all optional)
- {Model}Schema: output from ModelSchema
- {Model}ListSchema: minimal output for lists

Routes (using Router):
- GET / -> list with filtering (query params)
- POST / -> create (auth required)
- GET /{id} -> retrieve
- PATCH /{id} -> update (auth required)
- DELETE /{id} -> delete (auth required)

Include:
- Proper response codes (201 for create, 204 for delete)
- get_object_or_404 for retrieval
- Query parameters for filtering
- Tags for OpenAPI grouping
```

### Ninja Async Endpoints

```
Create async Django Ninja endpoints for {action}:

Requirements:
- async def for view functions
- sync_to_async for ORM queries
- Async HTTP client for external APIs (httpx)
- Proper error handling

Example structure:
- Async external API call
- Async database query wrapper
- Response composition

Include performance considerations and when to use async vs sync.
```

### Ninja Pydantic Validation

```
Create Pydantic v2 schemas for Django Ninja:

{Model}Schema:
- ModelSchema from {Model}
- Custom fields: {computed fields}
- Validators: {field-level validation}

Create{Model}Schema:
- Field definitions with constraints
- field_validator decorators
- model_validator for cross-field validation
- Custom error messages

Include:
- Type hints
- Field(...) with min/max constraints
- Optional fields with default values
- Nested schemas for relations
```

---

## 11. Debugging and Optimization

### Performance Optimization

```
Optimize this DRF ViewSet for performance:

{paste ViewSet code}

Issues to check:
- N+1 queries (add select_related/prefetch_related)
- Unnecessary serialization (use different serializers for list/detail)
- Missing database indexes
- Inefficient filtering
- Pagination issues

Provide:
- Optimized get_queryset with proper prefetching
- Query analysis (which queries are executed)
- Indexing recommendations
- Caching suggestions if applicable
```

### Debug API Issue

```
Debug this DRF endpoint issue:

Endpoint: {method} {url}
Expected: {expected behavior}
Actual: {actual behavior}
Error: {error message if any}

Code:
{paste relevant code}

Request:
{paste request details}

Help identify:
- Root cause
- Fix for the issue
- Test to prevent regression
```

### Convert DRF to Ninja

```
Convert this DRF endpoint to Django Ninja:

DRF Code:
{paste DRF code}

Requirements:
- Maintain same functionality
- Use Pydantic schemas instead of serializers
- Keep same URL structure
- Preserve authentication
- Add async if beneficial

Provide:
- Ninja schema definitions
- Ninja route functions
- Router configuration
- Migration notes (breaking changes if any)
```

---

## Quick Reference

### Context to Always Include

| Item | Why |
|------|-----|
| Django version | Syntax differences (5.x vs 4.x) |
| DRF/Ninja version | Feature availability |
| Existing models | Relations, field types |
| Project structure | Where to put code |
| Auth method | JWT, Session, etc. |
| Existing patterns | Service layer, serializer style |

### Response Format Requests

```
# For code generation
Provide complete, working code with:
- All imports
- Type hints
- Docstrings
- Comments for non-obvious logic

# For debugging
Provide:
1. Root cause analysis
2. Step-by-step fix
3. Test case to verify

# For optimization
Provide:
1. Current issues identified
2. Optimized code
3. Performance comparison
```

---

## Anti-Patterns to Avoid in Prompts

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| "Create an API" | "Create a ViewSet for Order with list, create, retrieve..." |
| "Add authentication" | "Add JWT auth with simplejwt, 15min access tokens..." |
| "Make it fast" | "Optimize queries, add select_related for user, category..." |
| "Add validation" | "Validate: amount > 0, quantity 1-100, email unique..." |
| No version info | "Django 5.x, DRF 3.15, Python 3.11+" |

---

*Last updated: 2026-01-25*
