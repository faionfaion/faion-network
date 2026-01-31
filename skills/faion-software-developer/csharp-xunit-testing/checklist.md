# Checklist

## Planning Phase

- [ ] Identify test scenarios for each controller/service
- [ ] Plan happy path and error cases
- [ ] Plan mocking strategy for dependencies
- [ ] Design test data/fixtures
- [ ] Plan test structure (Arrange-Act-Assert)
- [ ] Identify integration vs unit tests

## Unit Test Setup Phase

- [ ] Create test class for each component
- [ ] Set up Moq for mocking dependencies
- [ ] Create test fixtures and data builders
- [ ] Implement SetUp/TearDown if needed
- [ ] Create helper methods for common assertions
- [ ] Configure xUnit attributes

## Controller Test Phase

- [ ] Test GET endpoints return OK with data
- [ ] Test POST endpoints create and return 201
- [ ] Test PUT endpoints update correctly
- [ ] Test DELETE endpoints return 204
- [ ] Test invalid input returns 400
- [ ] Test authentication/authorization returns 401/403
- [ ] Test not found returns 404
- [ ] Mock service layer for isolation

## Service Test Phase

- [ ] Test service methods with valid inputs
- [ ] Test error conditions throw correct exceptions
- [ ] Test data transformation/mapping
- [ ] Test business logic constraints
- [ ] Mock repository layer
- [ ] Test all branches/conditions
- [ ] Test edge cases

## Integration Test Setup Phase

- [ ] Create WebApplicationFactory fixture
- [ ] Set up test database
- [ ] Create seeding/fixture data
- [ ] Configure test environment settings
- [ ] Handle test isolation and cleanup

## Integration Test Phase

- [ ] Test full request/response flow
- [ ] Test with real database
- [ ] Test authentication flow
- [ ] Test validation errors
- [ ] Test data persistence
- [ ] Test multiple endpoints together
- [ ] Clean up test data after each test

## Assertions Phase

- [ ] Assert response status codes
- [ ] Assert response body content
- [ ] Assert response headers
- [ ] Assert mock calls (Verify)
- [ ] Assert exact values where important
- [ ] Assert collections (Count, Contains)
- [ ] Use InlineData for parametrized tests

## Test Data Phase

- [ ] Create builders for complex objects
- [ ] Use realistic test data
- [ ] Minimize test data (only needed fields)
- [ ] Create fixtures for reusable data
- [ ] Manage test database state

## Testing Phase

- [ ] Run tests locally before commit
- [ ] Ensure all tests pass
- [ ] Verify test coverage
- [ ] Check for flaky tests
- [ ] Load test slow tests

## Deployment

- [ ] Configure CI to run tests
- [ ] Set up coverage reporting
- [ ] Create test documentation
- [ ] Monitor test execution time