# JavaScript Testing Checklist

Step-by-step checklist for testing JavaScript/TypeScript applications.

## Pre-Testing Setup

### Project Configuration

- [ ] Choose test framework (Vitest for Vite projects, Jest for React Native/legacy)
- [ ] Install testing dependencies
- [ ] Configure test environment (jsdom/happy-dom for React)
- [ ] Set up path aliases matching project config
- [ ] Create setup file for global mocks and cleanup
- [ ] Configure coverage thresholds
- [ ] Add test scripts to package.json

### File Structure

- [ ] Decide on test file location (co-located vs separate folder)
- [ ] Create mocks directory structure
- [ ] Set up shared test utilities
- [ ] Configure MSW handlers for API mocking

## Unit Testing Checklist

### Component Test Planning

- [ ] Identify component's public API (props, callbacks)
- [ ] List user interactions to test
- [ ] Identify conditional rendering paths
- [ ] List error states and edge cases
- [ ] Identify async behavior (loading, data fetching)

### Writing Component Tests

- [ ] Import render, screen, userEvent
- [ ] Use accessible queries (getByRole, getByLabelText)
- [ ] Test initial render state
- [ ] Test user interactions with userEvent (not fireEvent)
- [ ] Test conditional rendering
- [ ] Test error states
- [ ] Test loading states
- [ ] Verify callback invocations
- [ ] Clean up after each test (automatic with RTL)

### Hook Testing

- [ ] Use renderHook from @testing-library/react
- [ ] Test initial state
- [ ] Test state updates with act()
- [ ] Test effect cleanup
- [ ] Test with different initial values
- [ ] Test error handling

### Function Testing

- [ ] Test with valid inputs
- [ ] Test with invalid inputs
- [ ] Test edge cases (empty, null, undefined)
- [ ] Test boundary conditions
- [ ] Test error throwing

## Integration Testing Checklist

### API Integration

- [ ] Set up MSW server
- [ ] Create request handlers
- [ ] Test successful responses
- [ ] Test error responses (4xx, 5xx)
- [ ] Test network errors
- [ ] Test request parameters/body
- [ ] Test authentication headers

### Component Integration

- [ ] Test parent-child communication
- [ ] Test context provider integration
- [ ] Test form submission flow
- [ ] Test navigation/routing
- [ ] Test state management integration

### Node.js API Testing

- [ ] Set up Supertest with app instance
- [ ] Test all HTTP methods (GET, POST, PUT, DELETE)
- [ ] Test request validation
- [ ] Test authentication/authorization
- [ ] Test error responses
- [ ] Use in-memory database for isolation

## E2E Testing Checklist (Playwright)

### Setup

- [ ] Install Playwright
- [ ] Configure browsers to test
- [ ] Set up base URL
- [ ] Configure web server command
- [ ] Create Page Object files

### Test Writing

- [ ] Identify critical user flows
- [ ] Create Page Objects for reusability
- [ ] Use stable locators (data-testid, role)
- [ ] Handle authentication state
- [ ] Test happy paths
- [ ] Test error scenarios
- [ ] Add visual regression tests if needed

### CI Integration

- [ ] Configure CI workflow
- [ ] Set up artifact storage for traces/screenshots
- [ ] Configure parallel execution
- [ ] Set appropriate timeouts
- [ ] Configure retries for flaky tests

## Mocking Checklist

### When to Mock

- [ ] External API calls (use MSW)
- [ ] Third-party libraries with side effects
- [ ] Browser APIs (localStorage, geolocation)
- [ ] Time-dependent code (Date, setTimeout)
- [ ] Random values

### When NOT to Mock

- [ ] Internal implementation details
- [ ] Pure utility functions
- [ ] Simple data transformations
- [ ] Component internals

### Mock Implementation

- [ ] Use vi.fn() / jest.fn() for functions
- [ ] Use vi.mock() / jest.mock() for modules
- [ ] Use MSW for HTTP requests
- [ ] Use vi.useFakeTimers() for time
- [ ] Restore mocks in afterEach
- [ ] Use mockReturnValue for simple returns
- [ ] Use mockResolvedValue for async
- [ ] Use mockRejectedValue for errors

## Async Testing Checklist

- [ ] Use async/await in test functions
- [ ] Use findBy queries for async elements
- [ ] Use waitFor for complex conditions
- [ ] Handle loading states
- [ ] Test timeout scenarios
- [ ] Use fake timers for debounce/throttle
- [ ] Clean up timers after tests

## Snapshot Testing Checklist

### When to Use

- [ ] UI components with stable output
- [ ] Serializable data structures
- [ ] Error message formats
- [ ] Configuration objects

### Best Practices

- [ ] Keep snapshots small and focused
- [ ] Review snapshot changes in PRs
- [ ] Use inline snapshots for small outputs
- [ ] Avoid dynamic data (dates, IDs)
- [ ] Use snapshot serializers for styled-components

## Coverage Checklist

### Configuration

- [ ] Set coverage provider (v8 or istanbul)
- [ ] Configure include/exclude patterns
- [ ] Set minimum thresholds (80% recommended)
- [ ] Configure reporters (text, html, lcov)

### Analysis

- [ ] Review uncovered lines
- [ ] Check branch coverage
- [ ] Identify dead code
- [ ] Don't chase 100% blindly
- [ ] Focus on critical paths

## Test Quality Checklist

### Test Structure

- [ ] One concept per test
- [ ] Descriptive test names
- [ ] AAA pattern (Arrange-Act-Assert)
- [ ] DRY setup with beforeEach
- [ ] Independent tests (no shared state)

### Assertions

- [ ] Use specific matchers (toBe, toHaveBeenCalledWith)
- [ ] Use jest-dom matchers (toBeDisabled, toBeVisible)
- [ ] Avoid toBeTruthy for specific checks
- [ ] Test error messages, not just throwing

### Maintainability

- [ ] Avoid testing implementation details
- [ ] Use test utilities for common setup
- [ ] Keep tests close to source files
- [ ] Update tests when refactoring
- [ ] Remove obsolete tests

## CI/CD Checklist

### Pipeline Configuration

- [ ] Run tests on every PR
- [ ] Run tests on main branch
- [ ] Cache node_modules
- [ ] Run unit tests first (fast feedback)
- [ ] Run E2E tests after unit tests pass
- [ ] Fail build on test failure
- [ ] Upload coverage reports

### Performance

- [ ] Parallelize test execution
- [ ] Use sharding for large suites
- [ ] Set appropriate timeouts
- [ ] Use CI-specific configurations
- [ ] Cache Playwright browsers

## React-Specific Checklist

### Testing Library Best Practices

- [ ] Use screen.getByRole over getByTestId
- [ ] Use userEvent over fireEvent
- [ ] Avoid waitForElementToBeRemoved when possible
- [ ] Don't use act() manually (RTL handles it)
- [ ] Use findBy for async elements

### Context Testing

- [ ] Create custom render with providers
- [ ] Export from test utilities
- [ ] Test context consumers
- [ ] Test context updates

### Hook Testing

- [ ] Test hooks via components when possible
- [ ] Use renderHook for reusable hooks
- [ ] Wrap state updates in act()
- [ ] Test cleanup effects

## Node.js-Specific Checklist

### Express API Testing

- [ ] Use Supertest for HTTP assertions
- [ ] Don't start actual server (use app directly)
- [ ] Test middleware separately
- [ ] Mock external services
- [ ] Use database transactions/cleanup

### Database Testing

- [ ] Use test database
- [ ] Clean up data between tests
- [ ] Consider mongodb-memory-server
- [ ] Test migrations
- [ ] Test edge cases (duplicates, constraints)

## Pre-Commit Checklist

- [ ] All tests pass locally
- [ ] Coverage meets thresholds
- [ ] No skipped tests (unless documented)
- [ ] No console.log in tests
- [ ] Snapshots updated intentionally
- [ ] New code has corresponding tests
- [ ] Tests follow project conventions
