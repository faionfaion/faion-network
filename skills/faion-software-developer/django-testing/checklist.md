# Checklist

## Setup Phase

- [ ] Install pytest and pytest-django
- [ ] Install model_bakery or factory_boy
- [ ] Create conftest.py with fixtures
- [ ] Configure pytest.ini or pyproject.toml
- [ ] Set DJANGO_SETTINGS_MODULE for tests
- [ ] Create test database configuration

## Test Organization Phase

- [ ] Create test files alongside app code or in tests/ folder
- [ ] Use test_*.py naming convention
- [ ] Organize tests by module/feature
- [ ] Create conftest.py for shared fixtures
- [ ] Create factories.py for test data builders

## Fixture Setup Phase

- [ ] Create @pytest.fixture for common test data
- [ ] Use model_bakery.baker.make() for models
- [ ] Create factory classes for complex objects
- [ ] Implement fixture teardown/cleanup
- [ ] Use @pytest.mark.django_db for DB access
- [ ] Create parametrized fixtures

## Model Test Phase

- [ ] Test model creation with valid data
- [ ] Test model validation (clean method)
- [ ] Test model constraints (unique, check)
- [ ] Test model relationships (FK, M2M)
- [ ] Test model methods/properties
- [ ] Test model __str__ methods
- [ ] Test model default values

## Service Test Phase

- [ ] Test service functions with valid input
- [ ] Test error scenarios raise exceptions
- [ ] Test business logic constraints
- [ ] Test all code paths
- [ ] Mock repository/external calls
- [ ] Test return values/side effects

## API View Test Phase

- [ ] Test GET request returns 200
- [ ] Test POST creates and returns 201
- [ ] Test PUT updates and returns 200
- [ ] Test DELETE returns 204
- [ ] Test invalid data returns 400
- [ ] Test authentication/permission checks
- [ ] Test not found returns 404
- [ ] Verify response schema/data

## Parametrized Test Phase

- [ ] Use @pytest.mark.parametrize for multiple cases
- [ ] Test different input variations
- [ ] Test boundary conditions
- [ ] Test edge cases (None, empty, negative)

## Test Quality Phase

- [ ] Each test has clear setup (Arrange)
- [ ] Each test has single assertion focus (Act)
- [ ] Tests verify behavior not implementation
- [ ] No test interdependencies
- [ ] Tests are deterministic/repeatable
- [ ] Use @pytest.mark.slow for slow tests

## Coverage Phase

- [ ] Run pytest --cov to check coverage
- [ ] Aim for 80%+ coverage
- [ ] Identify uncovered code
- [ ] Write tests for missing coverage
- [ ] Exclude non-critical code

## Integration Test Phase

- [ ] Test views with full request/response
- [ ] Use api_client fixture for API testing
- [ ] Test authentication flows
- [ ] Test query strings and filters
- [ ] Test multiple endpoints together

## Execution Phase

- [ ] Run all tests locally before commit
- [ ] Run coverage report
- [ ] Run slow tests separately
- [ ] Run with different database if needed

## CI/CD Phase

- [ ] Configure CI to run pytest
- [ ] Fail CI on test failures
- [ ] Set coverage thresholds
- [ ] Archive test reports
- [ ] Run tests on all commits/PRs

## Maintenance Phase

- [ ] Update tests when code changes
- [ ] Remove obsolete tests
- [ ] Refactor slow/brittle tests
- [ ] Monitor test execution time