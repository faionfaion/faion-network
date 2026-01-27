# E2E Testing Checklist

Step-by-step checklist for implementing comprehensive E2E testing.

---

## 1. Project Setup

### Initial Configuration

- [ ] Choose framework (Playwright recommended for new projects)
- [ ] Install dependencies
  - Playwright: `npm install --save-dev @playwright/test && npx playwright install`
  - Cypress: `npm install --save-dev cypress`
- [ ] Create configuration file (`playwright.config.ts` or `cypress.config.ts`)
- [ ] Set up directory structure:
  ```
  e2e/
  ├── fixtures/           # Test data
  ├── pages/              # Page objects
  ├── tests/              # Test specs
  ├── support/            # Helpers, custom commands
  └── playwright.config.ts
  ```
- [ ] Configure base URL and environment variables
- [ ] Set up TypeScript (recommended for type safety)
- [ ] Add scripts to `package.json`

### Browser Configuration

- [ ] Enable required browsers (Chrome, Firefox, Safari/WebKit)
- [ ] Configure mobile device emulation if needed
- [ ] Set viewport sizes for responsive testing
- [ ] Configure browser launch options (headless for CI)

---

## 2. Test Organization

### Directory Structure

- [ ] Group tests by feature/domain
- [ ] Create Page Object classes for each page/component
- [ ] Set up shared fixtures and helpers
- [ ] Organize test data (factories, fixtures)
- [ ] Configure test tagging (@smoke, @regression, @critical)

### Naming Conventions

- [ ] Use descriptive test file names: `auth.spec.ts`, `checkout.spec.ts`
- [ ] Use clear test descriptions: `should display error for invalid credentials`
- [ ] Page objects follow pattern: `LoginPage.ts`, `DashboardPage.ts`
- [ ] Fixtures clearly named: `testUsers.ts`, `productData.ts`

---

## 3. Page Object Model Implementation

### Page Class Design

- [ ] Create base page class with common methods
- [ ] Define locators using stable selectors
- [ ] Implement page-specific actions as methods
- [ ] Add wait conditions within methods
- [ ] Include page navigation helpers

### Selector Strategy

- [ ] Prefer `data-testid` attributes
- [ ] Use accessible names and roles (`getByRole`, `getByLabel`)
- [ ] Avoid CSS classes and implementation details
- [ ] Document selector strategy in team guidelines
- [ ] Add `data-testid` to components during development

### Checklist for Each Page Object

- [ ] Constructor accepts Page/Locator
- [ ] All selectors defined as properties
- [ ] Action methods return appropriate type (void or next page)
- [ ] No assertions in page objects (only in tests)
- [ ] Comments for complex interactions

---

## 4. Test Data Management

### Data Strategy

- [ ] Identify test data requirements per test
- [ ] Create data factories for dynamic data
- [ ] Set up fixtures for static data
- [ ] Implement API seeding for complex scenarios
- [ ] Plan cleanup/teardown strategy

### Data Isolation

- [ ] Each test creates its own data
- [ ] Use unique identifiers (UUIDs, timestamps)
- [ ] Clean up data after tests (or use transactions)
- [ ] Avoid shared state between tests
- [ ] Tests can run in any order

### Environment Handling

- [ ] Configure environment-specific URLs
- [ ] Manage credentials securely (env vars)
- [ ] Handle feature flags per environment
- [ ] Document data dependencies

---

## 5. Authentication Setup

### Authentication Strategy Selection

- [ ] Evaluate options: storageState, API login, UI login
- [ ] Implement chosen strategy
- [ ] Create authenticated fixtures
- [ ] Handle token refresh/expiration
- [ ] Support multiple user roles

### Implementation Checklist

- [ ] Create auth helper/fixture
- [ ] Save `storageState` to file
- [ ] Reuse state across tests
- [ ] Handle auth for parallel tests
- [ ] Test logout functionality

### Multi-Role Testing

- [ ] Define user roles (admin, user, guest)
- [ ] Create separate auth state per role
- [ ] Configure project-level auth dependencies
- [ ] Test role-specific access

---

## 6. API Mocking

### Mock Strategy

- [ ] Identify APIs to mock (external, slow, flaky)
- [ ] Choose approach: route interception vs MSW
- [ ] Create mock data matching real API shape
- [ ] Document mocked vs real API tests

### Implementation

- [ ] Set up route handlers
- [ ] Create mock response factories
- [ ] Handle error scenarios
- [ ] Verify request payloads when needed
- [ ] Clean up mocks after tests

---

## 7. Visual Regression Testing

### Setup

- [ ] Choose tool (Playwright built-in, Percy, Chromatic, Argos)
- [ ] Configure screenshot directory
- [ ] Set up baseline approval workflow
- [ ] Handle cross-platform differences

### Best Practices

- [ ] Screenshot stable states only
- [ ] Mask dynamic content (timestamps, avatars)
- [ ] Set consistent viewport sizes
- [ ] Document visual test coverage
- [ ] Review baselines in PR process

---

## 8. Mobile Testing

### Configuration

- [ ] Define target devices (iPhone, Android)
- [ ] Configure device emulation in config
- [ ] Set touch event handling
- [ ] Configure geolocation if needed

### Test Coverage

- [ ] Responsive layout tests
- [ ] Touch interactions (swipe, pinch)
- [ ] Mobile-specific navigation
- [ ] Soft keyboard handling
- [ ] Network throttling tests

---

## 9. Flaky Test Prevention

### During Test Writing

- [ ] Use auto-waiting (avoid explicit waits)
- [ ] Use stable selectors (data-testid, roles)
- [ ] Ensure test isolation
- [ ] Handle async operations properly
- [ ] Mock external dependencies

### Monitoring

- [ ] Track test stability metrics
- [ ] Quarantine flaky tests immediately
- [ ] Root cause analysis for failures
- [ ] Regular test suite maintenance
- [ ] Delete obsolete tests

### Anti-Patterns to Avoid

- [ ] No `sleep()` or `waitForTimeout()`
- [ ] No shared test data
- [ ] No order-dependent tests
- [ ] No testing implementation details
- [ ] No ignoring failures

---

## 10. CI/CD Integration

### Pipeline Setup

- [ ] Install browsers in CI
- [ ] Configure caching (browser binaries)
- [ ] Set up parallel execution (sharding)
- [ ] Configure retries for transient failures
- [ ] Set appropriate timeouts

### Reporting

- [ ] Generate HTML/JSON reports
- [ ] Upload artifacts (screenshots, traces)
- [ ] Configure Slack/email notifications
- [ ] Track test metrics over time
- [ ] Merge reports from parallel runs

### GitHub Actions Specific

- [ ] Use matrix strategy for sharding
- [ ] Cache `~/.cache/ms-playwright`
- [ ] Upload trace on first retry
- [ ] Merge reports job after all shards
- [ ] Fail PR on test failures

---

## 11. Test Coverage

### Critical Paths (Must Have)

- [ ] User registration/login
- [ ] Core business workflows
- [ ] Payment/checkout flows
- [ ] Error handling (validation, 404, 500)
- [ ] Access control (permissions)

### Secondary Paths

- [ ] Settings/profile management
- [ ] Search functionality
- [ ] Navigation and routing
- [ ] Email/notifications
- [ ] Data export/import

### Cross-Browser

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari/WebKit
- [ ] Edge (if required)
- [ ] Mobile browsers

---

## 12. Documentation

### Team Documentation

- [ ] E2E testing guidelines
- [ ] Selector strategy guide
- [ ] Page object conventions
- [ ] How to run tests locally
- [ ] How to debug failures

### Test Documentation

- [ ] Clear test descriptions
- [ ] Comments for complex logic
- [ ] README in e2e directory
- [ ] Data setup requirements
- [ ] Known issues/limitations

---

## 13. Maintenance

### Regular Tasks

- [ ] Review and update flaky tests
- [ ] Remove obsolete tests
- [ ] Update selectors after UI changes
- [ ] Refresh test data
- [ ] Update dependencies

### Metrics to Track

- [ ] Test pass rate
- [ ] Execution time
- [ ] Flaky test count
- [ ] Coverage of critical paths
- [ ] CI build times

---

## Quick Reference

### Pre-Commit Checklist

- [ ] Tests pass locally
- [ ] No hardcoded data (use factories/fixtures)
- [ ] Selectors use data-testid or accessible names
- [ ] No explicit waits
- [ ] Tests are independent

### PR Review Checklist

- [ ] Tests cover the feature
- [ ] Page objects updated if UI changed
- [ ] No duplicate test coverage
- [ ] Clear test descriptions
- [ ] No sensitive data exposed

### Debugging Checklist

- [ ] Run test in headed mode
- [ ] Check trace viewer
- [ ] Verify selectors in DevTools
- [ ] Check for timing issues
- [ ] Review test data state
