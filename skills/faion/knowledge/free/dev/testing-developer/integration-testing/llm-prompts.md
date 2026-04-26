# LLM Prompts for Integration Test Generation

Prompts for generating integration tests using AI assistants.

## Database Integration Tests

### PostgreSQL with Testcontainers

```
Generate pytest integration tests for a {model_name} repository using:
- Testcontainers for PostgreSQL
- SQLAlchemy ORM
- Transaction rollback for test isolation

Model definition:
{model_code}

Repository interface:
{repository_interface}

Include tests for:
1. Create operation
2. Read by ID
3. Read by unique field (e.g., email)
4. Update operation
5. Delete operation
6. List with pagination
7. Unique constraint violation
8. Not found scenario

Use session-scoped container fixture and function-scoped session with rollback.
```

### MongoDB Tests

```
Generate pytest integration tests for a {collection_name} MongoDB repository using:
- Testcontainers for MongoDB
- PyMongo client
- Collection cleanup between tests

Document schema:
{schema_definition}

Repository interface:
{repository_interface}

Include tests for:
1. Insert document
2. Find by ID
3. Find by field
4. Update document
5. Delete document
6. Aggregate query
7. Index usage validation

Clean up test data after each test.
```

### Redis Cache Tests

```
Generate pytest integration tests for a {service_name} cache service using:
- Testcontainers for Redis
- Redis-py client
- Key cleanup between tests

Cache operations:
{cache_operations}

Include tests for:
1. Set and get value
2. Set with expiration
3. Delete key
4. Hash operations (if applicable)
5. List operations (if applicable)
6. Key not found
7. Cache invalidation

Flush database after each test.
```

## API Integration Tests

### FastAPI Endpoints

```
Generate pytest integration tests for these FastAPI endpoints:
- Framework: FastAPI with Pydantic v2
- Database: SQLAlchemy with {database_type}
- Auth: JWT Bearer tokens

Endpoints:
{endpoint_definitions}

Models:
{pydantic_models}

Include tests for:
1. Successful CRUD operations (201, 200, 204)
2. Validation errors (422)
3. Not found (404)
4. Unauthorized access (401)
5. Forbidden access (403)
6. Conflict/duplicate (409)
7. Pagination and filtering

Use TestClient for sync tests, AsyncClient for async tests.
Include auth_headers and admin_headers fixtures.
```

### Django REST Framework

```
Generate pytest-django integration tests for these DRF viewsets:
- Framework: Django REST Framework
- Database: {database_type}
- Auth: Token/JWT authentication

Viewsets:
{viewset_definitions}

Serializers:
{serializer_definitions}

Include tests for:
1. List endpoint with pagination
2. Retrieve single object
3. Create with valid data
4. Create with invalid data
5. Update (PUT and PATCH)
6. Delete
7. Permission checks (authenticated, admin)
8. Filtering and ordering

Use @pytest.mark.django_db decorator.
Use APIClient with force_authenticate.
```

### Async API Tests

```
Generate async pytest integration tests for these endpoints:
- Framework: FastAPI
- Testing: httpx AsyncClient
- Async marker: pytest.mark.anyio

Endpoints:
{async_endpoint_definitions}

Include:
1. Async fixture for AsyncClient
2. Proper ASGITransport usage
3. Dependency override for database
4. Tests for all HTTP methods
5. Error handling tests

Use @pytest.mark.anyio decorator for all async tests.
```

## External Service Tests

### HTTP Service Mocking

```
Generate pytest integration tests with HTTP mocking for:
- Service: {service_name}
- HTTP client: httpx
- Mock library: respx

External API calls:
{api_calls_definition}

Include tests for:
1. Successful API response
2. 4xx error response
3. 5xx error response
4. Timeout handling
5. Connection error handling
6. Retry logic (if applicable)
7. Response parsing

Use @respx.mock decorator.
Mock all external HTTP calls.
```

### WireMock Integration

```
Generate pytest integration tests using WireMock for:
- Service: {service_name}
- Container: wiremock/wiremock:3.x

External dependencies:
{external_dependencies}

Include:
1. WireMock container fixture (session-scoped)
2. Per-test stub registration
3. Stub cleanup after tests
4. Request verification
5. Scenario testing (stateful behavior)

Use Testcontainers for WireMock.
Register stubs via /__admin/mappings API.
```

## Message Queue Tests

### RabbitMQ Integration

```
Generate pytest integration tests for message queue operations:
- Broker: RabbitMQ
- Container: rabbitmq:3-management-alpine
- Library: pika

Producer/Consumer:
{message_handlers}

Include tests for:
1. Message publishing
2. Message consumption
3. Message acknowledgment
4. Message persistence
5. Dead letter handling
6. Queue declaration
7. Routing key matching

Use Testcontainers for RabbitMQ.
Clean up queues between tests.
```

### Kafka Integration

```
Generate pytest integration tests for Kafka:
- Container: confluentinc/cp-kafka:7.x
- Library: kafka-python

Topics and messages:
{kafka_definitions}

Include tests for:
1. Produce message
2. Consume message
3. Consumer group behavior
4. Partition assignment
5. Offset management
6. Serialization/deserialization

Use Testcontainers for Kafka.
Use appropriate timeouts for consumer.
```

## Authentication Tests

### JWT Authentication

```
Generate pytest integration tests for JWT authentication:
- Framework: {framework}
- JWT library: {jwt_library}

Auth endpoints:
{auth_endpoints}

Protected resources:
{protected_endpoints}

Include tests for:
1. Login with valid credentials
2. Login with invalid credentials
3. Access with valid token
4. Access with expired token
5. Access with invalid token
6. Access without token
7. Token refresh (if applicable)
8. Role-based access control

Create fixtures for auth_headers, admin_headers, expired_headers.
```

### OAuth2 Integration

```
Generate pytest integration tests for OAuth2:
- Provider: {oauth_provider}
- Flow: {oauth_flow}

Include tests for:
1. Authorization URL generation
2. Token exchange (mocked provider)
3. User info retrieval
4. Token validation
5. Scope validation
6. Error handling (invalid grant, expired token)

Mock OAuth provider responses using respx or WireMock.
```

## Test Organization

### Complete Test Suite

```
Generate a complete integration test suite for:
- Application: {app_description}
- Stack: {tech_stack}

Components to test:
{components_list}

Include:
1. conftest.py with all fixtures
2. Testcontainers for all services
3. Factory fixtures for test data
4. Auth fixtures
5. pytest.ini / pyproject.toml configuration

Organize tests by domain:
- tests/integration/
  - conftest.py
  - test_users.py
  - test_products.py
  - test_orders.py
  - test_payments.py

Follow AAA pattern (Arrange-Act-Assert).
Use descriptive test names.
```

### Fixture Generation

```
Generate pytest fixtures for integration testing:
- Database: {database_type}
- Services: {external_services}
- Auth: {auth_method}

Create:
1. Container fixtures (session-scoped)
2. Database session fixtures (function-scoped with rollback)
3. Factory fixtures for models
4. Auth header fixtures
5. Test client fixtures
6. Mock service fixtures

Include proper cleanup and teardown.
```

## Specialized Tests

### File Upload Testing

```
Generate integration tests for file upload endpoints:
- Framework: {framework}
- Storage: {storage_type}

Endpoints:
{upload_endpoints}

Include tests for:
1. Single file upload
2. Multiple file upload
3. File type validation
4. File size validation
5. Malformed file handling
6. Successful file retrieval
7. File deletion

Use io.BytesIO for test files.
Clean up uploaded files after tests.
```

### WebSocket Testing

```
Generate integration tests for WebSocket endpoints:
- Framework: FastAPI
- Testing: httpx-ws or websockets

WebSocket endpoints:
{websocket_endpoints}

Include tests for:
1. Connection establishment
2. Message sending
3. Message receiving
4. Connection closure
5. Authentication
6. Error handling

Use async test fixtures.
Properly close connections in teardown.
```

### Background Task Testing

```
Generate integration tests for background tasks:
- Task queue: {task_queue}
- Framework: {framework}

Tasks:
{task_definitions}

Include tests for:
1. Task execution
2. Task result retrieval
3. Task failure handling
4. Task retry logic
5. Task chaining (if applicable)

Use synchronous task execution for testing.
Or use Testcontainers for the message broker.
```

## Prompt Modifiers

### Add to any prompt

```
Additional requirements:
- Use Python 3.11+ syntax
- Follow PEP 8 style guide
- Include type hints
- Add docstrings to test classes and methods
- Use pytest parametrize for data-driven tests
- Target 80%+ code coverage
- Handle cleanup even on test failure
- Use meaningful assertion messages
```

### Performance considerations

```
Performance requirements:
- Session-scoped containers (start once per session)
- Transaction rollback for database isolation
- Parallel test support (unique test data)
- Reasonable timeouts for container startup
- Skip slow tests with @pytest.mark.slow
```

### CI/CD considerations

```
CI/CD requirements:
- Docker socket access assumed
- No hardcoded ports (dynamic allocation)
- Proper container cleanup
- JUnit XML report generation
- Coverage report in Cobertura format
- Exit code reflects test results
```
