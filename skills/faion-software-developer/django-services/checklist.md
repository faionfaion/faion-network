# Checklist

## Planning Phase

- [ ] Identify services (business operations to implement)
- [ ] Map services to domain boundaries
- [ ] Identify dependencies between services
- [ ] Plan service function signatures and return types
- [ ] Identify database operations (read/write)
- [ ] Document service responsibilities

## Service Definition Phase

- [ ] Create service module/package structure
- [ ] Define service functions with clear purposes
- [ ] Use function approach (not classes) where possible
- [ ] Add comprehensive docstrings (Google style)
- [ ] Define function signatures clearly
- [ ] Document all parameters and return types
- [ ] Mark keyword-only parameters with *

## Implementation Phase

- [ ] Implement core business logic
- [ ] Call repository methods for data access
- [ ] Handle domain exceptions explicitly
- [ ] Log important operations
- [ ] Keep service functions small and focused
- [ ] Avoid circular dependencies
- [ ] Use TYPE_CHECKING for forward references

## Testing Phase

- [ ] Test service with valid inputs
- [ ] Test service error/exception cases
- [ ] Test service with mocked dependencies
- [ ] Test all code paths
- [ ] Test edge cases (None, empty, negative)
- [ ] Test integration with repositories

## Integration Phase

- [ ] Call services from views (not models)
- [ ] Inject dependencies (repositories)
- [ ] Handle service exceptions in views
- [ ] Log service calls if needed
- [ ] Test service integration end-to-end

## Documentation Phase

- [ ] Document service module purposes
- [ ] Document service function contracts
- [ ] Document expected exceptions
- [ ] Document side effects
- [ ] Create examples of service usage

## Deployment

- [ ] Monitor service performance
- [ ] Track service errors/exceptions
- [ ] Alert on service failures