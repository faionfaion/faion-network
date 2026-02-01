# E2E Testing (Playwright & Cypress)

End-to-end testing validates complete user workflows from start to finish, ensuring all integrated components work together correctly.

## Overview

E2E tests simulate real user interactions with your application, testing the entire stack from UI to database. They catch integration issues that unit and integration tests miss.

### When to Use E2E Tests

| Use Case | Priority |
|----------|----------|
| Critical user journeys (auth, checkout) | High |
| Cross-browser compatibility | High |
| Visual regression detection | Medium |
| API + UI integration | Medium |
| Mobile responsiveness | Medium |

### Test Pyramid Principle

```
        /\
       /E2E\        10% - Critical paths only
      /------\
     /Integr. \     20% - Service interactions
    /----------\
   /   Unit     \   70% - Business logic
  /--------------\
```

Keep E2E tests focused on the most important user journeys. A smaller set of reliable E2E tests is better than a large set of flaky tests.

---

## Playwright vs Cypress (2025-2026)

### Quick Comparison

| Feature | Playwright | Cypress |
|---------|------------|---------|
| **Browser Support** | Chromium, Firefox, WebKit (Safari) | Chrome, Firefox, Edge (no Safari) |
| **Language Support** | JS/TS, Python, Java, C#, Go | JavaScript/TypeScript only |
| **Parallelization** | Native, free, built-in | Requires Dashboard (paid) or workarounds |
| **Multi-tab/window** | Full support | No native support |
| **Mobile Emulation** | Full device emulation | Limited viewport only |
| **Debugging** | Trace Viewer, page.pause() | Time-Travel Debugger (superior) |
| **Speed** | Faster at scale | Fast for smaller suites |
| **Learning Curve** | Moderate | Easier |

### When to Choose Playwright

- Cross-browser testing required (especially Safari/WebKit)
- Multi-language team (Python, Java, C# developers)
- Large test suites (1000+ tests)
- Multi-tab/multi-window scenarios
- Mobile web testing with device emulation
- Enterprise scale with native parallelization
- API testing alongside UI testing

### When to Choose Cypress

- Frontend-focused team (JavaScript only)
- Smaller test suites (<500 tests)
- Developer experience is priority
- Quick setup and fast feedback
- Primarily Chrome-based applications
- Teams new to E2E testing

### 2025-2026 Trends

- **Playwright** has the fastest growth in community, GitHub stars, and enterprise adoption
- **Cypress** peaked in 2022-2023, now steady; strong in frontend dev community
- **Recommendation:** Playwright for new projects; Cypress migration considered for scale

---

## Core Concepts

### Page Object Model (POM)

Encapsulates page elements and interactions in reusable classes:

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  readonly emailInput = () => this.page.getByTestId('email-input');
  readonly passwordInput = () => this.page.getByTestId('password-input');
  readonly submitButton = () => this.page.getByRole('button', { name: 'Login' });

  async login(email: string, password: string) {
    await this.emailInput().fill(email);
    await this.passwordInput().fill(password);
    await this.submitButton().click();
  }
}
```

**Benefits:**
- Single source of truth for selectors
- Reusable across tests
- Easy maintenance when UI changes
- Better readability

### Test Data Management

| Strategy | Use Case |
|----------|----------|
| **Factories** | Generate realistic test data programmatically |
| **Fixtures** | Preload known data state |
| **API Seeding** | Create data via API before UI tests |
| **Database Transactions** | Rollback after each test |
| **Unique Identifiers** | UUIDs/timestamps for isolation |

### Authentication Strategies

| Strategy | Speed | Reliability | Complexity |
|----------|-------|-------------|------------|
| **storageState** | Fast | High | Low |
| **API Login** | Fast | High | Medium |
| **UI Login (per test)** | Slow | Medium | Low |
| **JWT Injection** | Fast | High | Medium |
| **OAuth Mocking** | Fast | High | High |

**Best Practice:** Login once via API, save `storageState`, reuse across tests.

### API Mocking

| Tool | Integration | Use Case |
|------|-------------|----------|
| **Playwright page.route()** | Built-in | Quick mocks, route interception |
| **MSW (Mock Service Worker)** | External | Reusable mocks across environments |
| **@msw/playwright** | MSW + Playwright | Best of both worlds |

### Visual Regression Testing

| Tool | Strength | Integration |
|------|----------|-------------|
| **Playwright (built-in)** | Basic snapshots | Native |
| **Percy** | AI-powered, cross-browser | BrowserStack |
| **Chromatic** | Storybook integration | Component-driven |
| **Argos** | Open source, CI-friendly | Framework-agnostic |

### Mobile E2E Testing

| Approach | Use Case | Limitation |
|----------|----------|------------|
| **Viewport Emulation** | Responsive testing | Not real device |
| **Device Emulation** | Touch, userAgent | No native features |
| **Real Device Cloud** | True mobile testing | Cost, complexity |
| **Appium** | Native apps | Different tooling |

**Playwright Capability:** Full device emulation including touch, geolocation, network throttling.

---

## Flaky Test Prevention

### Common Causes

1. **Timing issues** - Race conditions, slow networks
2. **Test data conflicts** - Shared state between tests
3. **Selector instability** - Fragile CSS/XPath selectors
4. **Environment issues** - Inconsistent CI environments
5. **Third-party dependencies** - External API failures

### Prevention Strategies

| Strategy | Implementation |
|----------|----------------|
| **Use auto-waiting** | Playwright auto-waits; avoid `sleep()` |
| **Stable selectors** | `data-testid`, roles, accessible names |
| **Test isolation** | Unique data per test, clean state |
| **Retry logic** | Built-in retries for transient failures |
| **Containerization** | Ephemeral environments per run |
| **Mock externals** | Isolate from third-party APIs |

### Anti-Patterns to Avoid

- Hard-coded waits (`sleep(5000)`)
- Shared test data between tests
- Testing implementation details
- Overly broad selectors (`.btn`, `#submit`)
- Ignoring flaky tests instead of fixing

---

## CI/CD Integration

### GitHub Actions Parallelization

```yaml
strategy:
  matrix:
    shard: [1/4, 2/4, 3/4, 4/4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}
```

### Key CI/CD Practices

| Practice | Benefit |
|----------|---------|
| **Sharding** | Parallel execution across machines |
| **Browser caching** | Faster CI runs |
| **Trace on failure** | Debug CI-only failures |
| **Report merging** | Unified test reports |
| **Retry failed tests** | Handle transient failures |

---

## LLM Usage Tips

When using AI assistants for E2E testing:

### Effective Prompts

1. **Provide context:** Include page structure, existing POM classes
2. **Specify framework:** "Using Playwright with TypeScript"
3. **Include selectors strategy:** "Use data-testid attributes"
4. **Describe user flow:** Step-by-step user journey

### What LLMs Excel At

- Generating Page Object classes from HTML
- Writing test cases from acceptance criteria
- Creating data factories and fixtures
- Suggesting stable selectors
- Converting Cypress tests to Playwright

### What LLMs Struggle With

- Understanding application-specific business logic
- Debugging flaky tests without full context
- Optimizing CI/CD pipelines
- Real device testing configurations

---

## Quick Reference

### Playwright Commands

```bash
npx playwright test                    # Run all tests
npx playwright test --headed           # With browser UI
npx playwright test --debug            # Debug mode
npx playwright test --ui               # Interactive UI mode
npx playwright test --project=chromium # Single browser
npx playwright codegen URL             # Generate tests
npx playwright show-report             # View HTML report
```

### Cypress Commands

```bash
npx cypress open           # Interactive mode
npx cypress run            # Headless mode
npx cypress run --browser chrome
npx cypress run --spec "path/to/spec.cy.ts"
```

---

## External Resources

### Official Documentation

- [Playwright Docs](https://playwright.dev/docs/intro)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Page Object Model](https://playwright.dev/docs/pom)
- [Cypress Docs](https://docs.cypress.io/)
- [Testing Library Principles](https://testing-library.com/docs/guiding-principles)

### Visual Testing

- [Percy](https://percy.io/)
- [Chromatic](https://www.chromatic.com/)
- [Argos CI](https://argos-ci.com/)

### API Mocking

- [Mock Service Worker (MSW)](https://mswjs.io/)
- [@msw/playwright](https://github.com/mswjs/playwright)

### Comparison Articles (2025-2026)

- [Playwright vs Cypress 2025 - BrowserStack](https://www.browserstack.com/guide/playwright-vs-cypress)
- [E2E Testing Frameworks 2025 - QA Wolf](https://www.qawolf.com/blog/the-best-mobile-e2e-testing-frameworks-in-2025-strengths-tradeoffs-and-use-cases)
- [Playwright E2E Testing Guide 2026 - DeviQA](https://www.deviqa.com/blog/guide-to-playwright-end-to-end-testing-in-2025/)

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step E2E testing checklist |
| [examples.md](examples.md) | Real-world test examples |
| [templates.md](templates.md) | Copy-paste configurations |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI-assisted testing |
