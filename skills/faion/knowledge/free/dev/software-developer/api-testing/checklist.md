# Checklist

## Planning Phase

- [ ] Identify happy path for each endpoint
- [ ] Identify error scenarios (validation, auth, not found)
- [ ] Plan contract tests between services
- [ ] Identify integration points to test
- [ ] Define test data setup strategy
- [ ] Plan API mocking strategy

## Unit Test Phase

- [ ] Test request validation for each endpoint
- [ ] Test business logic in service layer
- [ ] Test database queries return expected data
- [ ] Test error handling and exceptions
- [ ] Use mocks for external dependencies
- [ ] Test with various input combinations

## Integration Test Phase

- [ ] Test complete request/response flow
- [ ] Test database changes persist correctly
- [ ] Test multiple endpoints working together
- [ ] Test authentication/authorization flow
- [ ] Test with real (test) database
- [ ] Test with external service mocks

## Contract Test Phase

- [ ] Define contracts between consumer and provider
- [ ] Create Pact tests for API contracts
- [ ] Test consumer expectations match provider responses
- [ ] Run provider tests against contracts
- [ ] Share contracts between teams
- [ ] Test in CI before deployment

## Validation Phase

- [ ] Validate responses against OpenAPI spec
- [ ] Test that responses match documented schema
- [ ] Validate error response formats
- [ ] Test HTTP status codes are correct
- [ ] Verify Content-Type headers
- [ ] Test required fields are present

## Security Test Phase

- [ ] Test authentication with invalid tokens
- [ ] Test authorization (403 on forbidden resources)
- [ ] Test rate limiting works
- [ ] Test input validation prevents injection
- [ ] Test sensitive data not leaked in responses
- [ ] Test CORS headers correct

## Performance Test Phase

- [ ] Load test endpoints with realistic traffic
- [ ] Test response times acceptable
- [ ] Test database queries optimize well
- [ ] Test pagination with large datasets
- [ ] Monitor memory usage under load

## Documentation Phase

- [ ] Create Postman collection with all endpoints
- [ ] Document test data setup procedures
- [ ] Create test execution guide
- [ ] Document known issues and workarounds

## CI/CD Integration Phase

- [ ] Configure tests to run on push
- [ ] Set up coverage reporting
- [ ] Run contract tests in CI
- [ ] Archive test reports
- [ ] Set up alerts for test failures