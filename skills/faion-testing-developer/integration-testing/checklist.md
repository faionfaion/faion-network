# Integration Test Checklist

## Pre-Test Setup

### Environment

- [ ] Docker running and accessible
- [ ] Testcontainers installed (`pip install testcontainers[postgres,redis,mongodb]`)
- [ ] pytest-asyncio installed for async tests
- [ ] CI/CD has Docker socket access (`/var/run/docker.sock`)

### Configuration

- [ ] Test database configured (not production!)
- [ ] Environment variables set for test mode
- [ ] Logging configured for test output
- [ ] Timeouts set for container startup

## Test Design Checklist

### Isolation

- [ ] Each test can run independently
- [ ] Tests don't share mutable state
- [ ] Database rolled back or reset between tests
- [ ] External service mocks are per-test or properly reset
- [ ] No hardcoded ports (use dynamic port allocation)

### Data Management

- [ ] Using factories or fixtures for test data
- [ ] Unique identifiers for parallel test runs
- [ ] Minimal data setup (only what's needed)
- [ ] Cleanup happens even on test failure

### Assertions

- [ ] Testing behavior, not implementation
- [ ] Checking response status codes
- [ ] Validating response structure
- [ ] Verifying database state after operations
- [ ] Testing error cases and edge conditions

## Testcontainers Checklist

### Container Setup

- [ ] Using session scope for container fixtures
- [ ] Waiting for container readiness (health checks)
- [ ] Proper cleanup in fixture teardown
- [ ] Container images pinned to specific versions

```python
# Good: Pinned version
PostgresContainer("postgres:16-alpine")

# Bad: Floating tag
PostgresContainer("postgres:latest")
```

### Connection Management

- [ ] Connection URL retrieved from container
- [ ] Connection pool properly configured
- [ ] Connections closed after tests
- [ ] No leaked connections

## Database Testing Checklist

### Schema

- [ ] Migrations applied before tests
- [ ] Schema matches production
- [ ] Indexes exist for tested queries
- [ ] Foreign keys configured correctly

### Transactions

- [ ] Tests wrapped in transactions (where appropriate)
- [ ] Transaction rollback on test completion
- [ ] Commit-level constraints tested separately
- [ ] Deadlock scenarios considered

### Data

- [ ] Factory fixtures for consistent data
- [ ] Realistic data volumes for performance tests
- [ ] Edge cases: NULL, empty strings, unicode
- [ ] Boundary values tested

## API Testing Checklist

### Request

- [ ] All HTTP methods tested (GET, POST, PUT, DELETE)
- [ ] Request headers validated
- [ ] Request body validation tested
- [ ] Query parameters tested
- [ ] Path parameters tested

### Response

- [ ] Status codes for success cases
- [ ] Status codes for error cases (400, 401, 403, 404, 500)
- [ ] Response body structure
- [ ] Response headers (Content-Type, etc.)
- [ ] Pagination working correctly

### Authentication

- [ ] Valid token accepted
- [ ] Invalid token rejected (401)
- [ ] Expired token rejected (401)
- [ ] Missing token rejected (401)
- [ ] Insufficient permissions rejected (403)

## External Services Checklist

### Mocking

- [ ] Mock server configured (WireMock, respx)
- [ ] All expected endpoints mocked
- [ ] Error responses mocked
- [ ] Timeout scenarios tested
- [ ] Mock cleanup after tests

### Circuit Breaker

- [ ] Fallback behavior tested
- [ ] Recovery after service restoration
- [ ] Timeout handling tested

## CI/CD Integration Checklist

### Pipeline

- [ ] Docker available in CI environment
- [ ] Test containers start successfully
- [ ] Tests parallelized appropriately
- [ ] Test reports generated
- [ ] Coverage reports generated

### Performance

- [ ] Containers cached between runs (where possible)
- [ ] Parallel test execution configured
- [ ] Test timeout configured
- [ ] Resource limits set

### Artifacts

- [ ] Test results saved as artifacts
- [ ] Coverage reports uploaded
- [ ] Failed test logs captured
- [ ] Screenshots for E2E failures

## Post-Test Verification

### Cleanup

- [ ] All containers stopped
- [ ] Database connections closed
- [ ] Temporary files removed
- [ ] Mock servers reset

### Metrics

- [ ] Test execution time acceptable
- [ ] No flaky tests
- [ ] Coverage meets threshold
- [ ] All critical paths tested

## Quick Reference: Fixture Scopes

| Scope | Lifecycle | Use Case |
|-------|-----------|----------|
| `function` | Per test | DB session, mocks |
| `class` | Per test class | Shared setup |
| `module` | Per module | Container, engine |
| `session` | Per test run | Container startup |

## Quick Reference: pytest-django Markers

| Marker | Behavior |
|--------|----------|
| `@pytest.mark.django_db` | Transaction rollback |
| `@pytest.mark.django_db(transaction=True)` | Real transactions |
| `@pytest.mark.django_db(reset_sequences=True)` | Reset auto-increment |

## Quick Reference: Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Container won't start | Docker not running | Start Docker daemon |
| Port already in use | Static port binding | Use dynamic ports |
| Tests affect each other | Shared state | Transaction rollback |
| Slow tests | Container per test | Session-scoped container |
| Flaky tests | Race conditions | Proper waits/retries |
