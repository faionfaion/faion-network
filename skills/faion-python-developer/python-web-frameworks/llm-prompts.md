# Python Web Frameworks - LLM Prompts

**Effective prompts for LLM-assisted framework selection and development.**

---

## Framework Selection Prompts

### 1. Framework Recommendation

```
I need to choose a Python web framework for a new project. Help me decide.

Project details:
- Type: [REST API / Full-stack web app / Microservice / Internal tool]
- Expected users: [number]
- Expected RPS: [requests per second]
- Real-time features: [yes/no - specify if yes]
- Admin panel needed: [yes/no]
- Team experience: [Django/FastAPI/Flask experience level]
- Timeline: [MVP deadline]
- Deployment: [Docker/Kubernetes/Serverless/VPS]

Compare Django, FastAPI, and Flask for this use case. Provide:
1. Recommended framework with reasoning
2. Key advantages for this project
3. Potential challenges
4. Alternative if requirements change
```

### 2. Quick Framework Decision

```
Quick framework decision needed:

Building: [one-sentence description]
Key requirement: [single most important factor]
Team knows: [framework(s) team is familiar with]

Recommend one framework and explain in 2-3 sentences.
```

### 3. Framework Comparison for Specific Feature

```
Compare how Django, FastAPI, and Flask handle [specific feature]:

Feature: [e.g., WebSocket connections, background tasks, file uploads]

For each framework, provide:
1. Native vs external library needed
2. Implementation complexity (1-10)
3. Performance considerations
4. Code snippet showing basic implementation
```

---

## Django Prompts

### 4. Django Project Setup

```
Create a Django 5.x project structure for [project description].

Requirements:
- REST API with DRF
- JWT authentication
- PostgreSQL database
- Docker deployment
- pytest for testing

Provide:
1. Complete directory structure
2. settings/base.py configuration
3. Initial models for core entities
4. Basic serializers and views
5. docker-compose.yml
```

### 5. Django Model Design

```
Design Django models for [domain description].

Entities needed: [list entities]
Relationships: [describe relationships]

For each model provide:
1. Complete model definition with fields
2. Meta class configuration
3. Custom methods if needed
4. Admin configuration
5. Factory for testing (factory_boy)
```

### 6. Django Service Layer

```
Create a Django service layer for [feature description].

Business rules:
1. [rule 1]
2. [rule 2]
3. [rule 3]

Provide:
1. Service functions with type hints
2. Error handling
3. Transaction management (@transaction.atomic)
4. Unit tests with pytest
```

### 7. Django REST API Endpoint

```
Create a Django REST Framework endpoint for [resource].

Requirements:
- HTTP methods: [GET, POST, PUT, DELETE - specify which]
- Authentication: [JWT/Session/None]
- Permissions: [specify]
- Pagination: [yes/no, if yes specify type]
- Filtering: [fields to filter by]

Provide:
1. Serializers (request and response)
2. ViewSet or APIView
3. URL configuration
4. Tests covering happy path and edge cases
```

### 8. Django Admin Customization

```
Customize Django admin for [model name].

Requirements:
- List display fields: [specify]
- Filters: [specify]
- Search fields: [specify]
- Inline models: [specify if any]
- Custom actions: [specify if any]

Provide complete admin.py with:
1. ModelAdmin class
2. Custom list_display methods if needed
3. Fieldsets organization
4. Inline admin classes if needed
```

### 9. Django Async View

```
Convert this Django view to async:

[paste existing synchronous view]

Requirements:
- Use async ORM methods where available
- Handle sync ORM calls with sync_to_async
- Maintain same functionality
- Add proper error handling
```

---

## FastAPI Prompts

### 10. FastAPI Project Setup

```
Create a FastAPI project structure for [project description].

Requirements:
- Async SQLAlchemy 2.0
- JWT authentication
- PostgreSQL with asyncpg
- Alembic migrations
- pytest-asyncio for testing

Provide:
1. Complete directory structure
2. config.py with pydantic-settings
3. Database setup (async engine, session)
4. Initial models
5. Dependencies (get_db, get_current_user)
6. docker-compose.yml
```

### 11. FastAPI Router

```
Create a FastAPI router for [resource].

Requirements:
- Endpoints: [list CRUD operations needed]
- Authentication: [required/optional]
- Pagination: [yes/no]
- Filtering: [query parameters]
- Response model: [specify fields]

Provide:
1. Pydantic schemas (request/response)
2. Router with all endpoints
3. Service functions (async)
4. Tests with httpx AsyncClient
```

### 12. FastAPI Dependency Injection

```
Create FastAPI dependencies for [use case].

Dependencies needed:
1. [dependency 1 - e.g., database session]
2. [dependency 2 - e.g., current user]
3. [dependency 3 - e.g., pagination params]

Provide:
1. Dependency functions
2. Annotated type aliases
3. Example usage in route
4. How to override in tests
```

### 13. FastAPI WebSocket

```
Create a FastAPI WebSocket endpoint for [use case].

Requirements:
- Room/channel support: [yes/no]
- Authentication: [how to authenticate]
- Message format: [JSON structure]
- Broadcasting: [how messages are distributed]

Provide:
1. ConnectionManager class
2. WebSocket endpoint
3. Message handling logic
4. Disconnect handling
5. Client-side connection example (JavaScript)
```

### 14. FastAPI Background Tasks

```
Implement background tasks in FastAPI for [use case].

Tasks needed:
1. [task 1 - e.g., send email]
2. [task 2 - e.g., process file]

Requirements:
- Use BackgroundTasks or Celery: [specify]
- Error handling
- Logging

Provide:
1. Task functions (sync or async)
2. Route that triggers tasks
3. Error handling approach
4. If Celery: celery.py configuration
```

### 15. FastAPI Pydantic Models

```
Create Pydantic models for [domain].

Entities:
1. [entity 1 with fields]
2. [entity 2 with fields]

Requirements:
- Request and response models
- Validation (min/max, regex, etc.)
- Optional fields for updates
- Nested models if needed

Provide:
1. Base model
2. Create model
3. Update model (with all optional)
4. Response model
5. List response with pagination
```

---

## Flask Prompts

### 16. Flask Project Setup

```
Create a Flask project structure for [project description].

Requirements:
- Application factory pattern
- SQLAlchemy ORM
- Flask-Migrate
- JWT authentication (Flask-JWT-Extended)
- Blueprints organization
- pytest for testing

Provide:
1. Complete directory structure
2. app/__init__.py (factory)
3. config.py
4. extensions.py
5. Initial models
6. docker-compose.yml
```

### 17. Flask Blueprint

```
Create a Flask blueprint for [resource].

Requirements:
- Endpoints: [list CRUD operations]
- Authentication: [required/optional]
- Validation: [Marshmallow/other]

Provide:
1. Blueprint __init__.py
2. views.py with routes
3. models.py
4. schemas.py (Marshmallow)
5. services.py
6. Tests
```

### 18. Flask Extension Configuration

```
Configure Flask extensions for [project type].

Extensions needed:
- [list extensions: SQLAlchemy, Migrate, Login, etc.]

Provide:
1. extensions.py with all extension instances
2. How to initialize in app factory
3. Configuration in config.py
4. Example usage in views
```

### 19. Flask Error Handling

```
Create comprehensive error handling for Flask app.

Requirements:
- Handle HTTP exceptions
- Handle validation errors
- Handle database errors
- Log errors appropriately
- Return consistent JSON format

Provide:
1. Error handler functions
2. Custom exception classes
3. Registration in app factory
4. Example of raising custom errors
```

---

## Testing Prompts

### 20. Django Test Suite

```
Create a test suite for Django [app/feature].

Code to test:
[paste code]

Requirements:
- pytest-django
- Factory Boy for fixtures
- Test coverage: [specify percentage target]

Provide:
1. conftest.py with fixtures
2. factories.py
3. test_models.py
4. test_views.py
5. test_services.py
```

### 21. FastAPI Test Suite

```
Create async tests for FastAPI [router/feature].

Code to test:
[paste code]

Requirements:
- pytest-asyncio
- httpx AsyncClient
- Database isolation

Provide:
1. conftest.py with async fixtures
2. Test database setup
3. tests for all endpoints
4. Edge case tests
```

### 22. Flask Test Suite

```
Create tests for Flask [blueprint/feature].

Code to test:
[paste code]

Requirements:
- pytest
- Test client
- Database fixtures

Provide:
1. conftest.py with fixtures
2. test_views.py
3. test_services.py
4. Edge case tests
```

---

## Migration & Refactoring Prompts

### 23. Migrate Flask to FastAPI

```
Help me migrate this Flask code to FastAPI:

[paste Flask code]

Requirements:
- Maintain same API contract
- Use async where beneficial
- Use Pydantic for validation
- Keep same business logic

Provide:
1. Equivalent FastAPI code
2. Key differences to note
3. Testing approach changes
4. Deployment changes needed
```

### 24. Add Async to Django

```
Convert these Django views/services to async:

[paste synchronous code]

Constraints:
- Must work with Django [version]
- Uses Django ORM
- Has external API calls

Provide:
1. Async version of code
2. sync_to_async usage for ORM
3. httpx for async HTTP calls
4. Potential performance improvements
```

### 25. Refactor Monolith to Microservices

```
Help me break this [Django/Flask/FastAPI] monolith into microservices:

Current structure:
[describe or paste structure]

Requirements:
- [list services to extract]
- Communication: [REST/gRPC/message queue]
- Database: [shared/per-service]

Provide:
1. Service boundaries
2. API contracts between services
3. Shared libraries approach
4. Deployment recommendations
```

---

## Performance Prompts

### 26. Optimize Endpoint Performance

```
Optimize this slow [Django/FastAPI/Flask] endpoint:

[paste code]

Current performance:
- Response time: [ms]
- RPS: [requests per second]

Target:
- Response time: [target ms]
- RPS: [target RPS]

Analyze and provide:
1. Identified bottlenecks
2. Optimization recommendations
3. Optimized code
4. Caching strategy if applicable
5. Database query optimizations
```

### 27. Handle High Concurrency

```
This [Django/FastAPI/Flask] endpoint needs to handle high concurrency:

[paste code]

Requirements:
- Expected concurrent users: [number]
- Expected RPS: [number]
- Database: [PostgreSQL/MySQL/etc.]

Provide:
1. Async/await optimizations
2. Connection pooling config
3. Caching layer recommendations
4. Rate limiting implementation
5. Horizontal scaling strategy
```

---

## Architecture Prompts

### 28. Design API Architecture

```
Design API architecture for [project description].

Requirements:
- Framework: [Django/FastAPI/Flask]
- Authentication: [JWT/OAuth/API keys]
- Authorization: [RBAC/ABAC]
- Versioning: [URL/header]
- Rate limiting: [specify limits]

Provide:
1. Project structure
2. Authentication flow
3. Authorization implementation
4. API versioning approach
5. Error handling standards
6. Documentation approach
```

### 29. Implement Repository Pattern

```
Implement repository pattern for [Django/FastAPI/Flask] project.

Entities:
[list entities]

Provide:
1. Base repository interface
2. Concrete implementations
3. Dependency injection setup
4. Usage in services
5. Testing approach with mocks
```

---

## Prompt Tips for Better Results

### Specify Context

Always include:
- Framework name AND version (Django 5.1, not just Django)
- Python version (3.11+)
- Database (PostgreSQL, SQLite, etc.)
- Deployment target (Docker, K8s, serverless)

### Be Specific About Requirements

Good:
```
Create a FastAPI endpoint that:
- Lists users with pagination (20 per page)
- Filters by status (active/inactive)
- Returns UserResponse schema
- Requires JWT authentication
```

Bad:
```
Create a FastAPI endpoint for users
```

### Request Modern Patterns

Add to prompts:
- "Use 2025 best practices"
- "Use modern Python 3.11+ syntax"
- "Use type hints throughout"
- "Follow clean architecture"

### Ask for Tests

Always include:
```
Include tests covering:
1. Happy path
2. Edge cases (empty results, invalid input)
3. Authentication/authorization failures
4. Database errors
```

### Request Error Handling

```
Include proper error handling:
- Validation errors (400)
- Not found (404)
- Unauthorized (401)
- Forbidden (403)
- Internal errors (500)
```

---

## Template: Complete Feature Request

```
Create a complete [feature name] feature for [framework].

## Context
- Framework: [Django 5.x / FastAPI 0.109+ / Flask 3.x]
- Python: 3.11+
- Database: [specify]
- Authentication: [JWT/Session/None]

## Requirements
[list requirements]

## Acceptance Criteria
1. [criterion 1]
2. [criterion 2]
3. [criterion 3]

## Deliverables
1. Models/Schemas
2. Service layer
3. API endpoints/Views
4. Tests (unit + integration)
5. Documentation (OpenAPI/docstrings)

## Constraints
- [any constraints]

Use 2025 best practices, type hints, and follow [Clean Architecture / DDD / etc.].
```

---

*Python Web Frameworks LLM Prompts v1.0*
*Effective prompts for Django, FastAPI, and Flask development*
