# JavaScript Testing (Jest/Vitest)

Comprehensive guide to JavaScript and TypeScript testing with modern frameworks.

## Overview

JavaScript testing ecosystem in 2025-2026 has matured significantly. Vitest has emerged as the default choice for modern projects, while Jest remains essential for React Native and legacy codebases.

## Test Framework Decision Tree

```
Starting new project?
├── Using Vite/Vue/Svelte/React+Vite → Vitest
├── React Native → Jest (mandatory)
├── Legacy codebase with CommonJS → Jest
├── Next.js → Jest or Vitest (both supported)
└── Monorepo → Vitest for packages, Jest where ecosystem requires
```

## Framework Comparison (2025-2026)

| Feature | Vitest | Jest |
|---------|--------|------|
| **Performance** | 10-20x faster (watch mode) | Baseline |
| **ESM Support** | Native, zero-config | Experimental, requires config |
| **TypeScript** | Native, zero-config | Requires ts-jest |
| **Config** | Shares vite.config | Separate jest.config |
| **API Compatibility** | 95% Jest-compatible | - |
| **Watch Mode** | Instant HMR-based | Process restart |
| **Coverage** | v8 (default) or istanbul | istanbul |
| **Browser Testing** | Built-in experimental | Requires jsdom |
| **React Native** | Not supported | Required |

### When to Choose Vitest

- New Vite-based projects (React, Vue, Svelte, SolidJS)
- TypeScript-first development
- Need fast feedback loops
- Modern ESM modules
- Monorepo packages/UI libraries

### When to Choose Jest

- React Native applications (mandatory)
- Mature codebases with Jest plugins
- CommonJS-heavy projects
- Need maximum ecosystem compatibility
- Existing Jest infrastructure

## Testing Stack (2025-2026)

### Unit Testing

| Tool | Purpose |
|------|---------|
| **Vitest** | Modern test runner, Vite integration |
| **Jest** | Established runner, React Native |
| **@testing-library/jest-dom** | DOM assertions |

### Component Testing

| Tool | Purpose |
|------|---------|
| **React Testing Library** | React component testing |
| **@testing-library/user-event** | User interaction simulation |
| **@testing-library/react-hooks** | Hook testing (legacy) |

### E2E Testing

| Tool | Purpose |
|------|---------|
| **Playwright** | Cross-browser E2E, recommended |
| **Cypress** | Alternative E2E, good DX |

### API Mocking

| Tool | Purpose |
|------|---------|
| **MSW (Mock Service Worker)** | Network-level API mocking |
| **nock** | HTTP request mocking |
| **Supertest** | Express API testing |

### Coverage

| Provider | Best For |
|----------|----------|
| **v8** | Speed, default in Vitest |
| **istanbul** | Accuracy, fallback option |

Note: Since Vitest v3.2, v8 produces identical coverage to istanbul via AST-based remapping.

## Key Concepts

### Test Pyramid

```
       /\
      /  \     E2E Tests (Playwright)
     /----\    ~10% of tests
    /      \
   /--------\  Integration Tests
  /          \ ~20% of tests
 /------------\
/              \ Unit Tests
                ~70% of tests
```

### Testing Principles

1. **Test behavior, not implementation** - Focus on what users see
2. **Arrange-Act-Assert (AAA)** - Structure every test
3. **FIRST principles** - Fast, Independent, Repeatable, Self-validating, Timely
4. **Isolation** - Each test independent, no shared state
5. **One assertion per concept** - Clear failure messages

### Query Priority (React Testing Library)

```
1. getByRole         - Accessible queries (preferred)
2. getByLabelText    - Form elements
3. getByPlaceholder  - Fallback for inputs
4. getByText         - Non-interactive elements
5. getByDisplayValue - Form current values
6. getByAltText      - Images
7. getByTitle        - Tooltips
8. getByTestId       - Last resort only
```

## Installation

### Vitest Setup

```bash
# Core
npm install -D vitest @vitest/coverage-v8

# React
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom

# For happy-dom (faster alternative to jsdom)
npm install -D happy-dom
```

### Jest Setup

```bash
# Core
npm install -D jest @types/jest ts-jest

# React
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

### E2E Setup

```bash
# Playwright
npm init playwright@latest
```

### API Mocking

```bash
# MSW
npm install -D msw

# Supertest (Node.js API testing)
npm install -D supertest @types/supertest
```

## Configuration Files

### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom', // or 'happy-dom'
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.d.ts', 'src/types/**'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### jest.config.js

```javascript
/** @type {import('jest').Config} */
const config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests'],
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  testMatch: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/types/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', { useESM: true }],
  },
}

module.exports = config
```

### tests/setup.ts

```typescript
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest' // or jest

// Cleanup after each test
afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock IntersectionObserver
class MockIntersectionObserver {
  observe = vi.fn()
  unobserve = vi.fn()
  disconnect = vi.fn()
}
window.IntersectionObserver = MockIntersectionObserver as any
```

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## LLM Usage Tips

### Effective Patterns for AI-Assisted Testing

1. **Provide component code** - Always include the full component when asking for tests
2. **Specify framework** - Mention Vitest vs Jest explicitly
3. **Request specific test types** - Unit, integration, or E2E
4. **Include types** - TypeScript interfaces improve test accuracy
5. **Describe edge cases** - List scenarios you want covered

### What LLMs Do Well

- Generating boilerplate test structure
- Creating mock implementations
- Writing assertion variations
- Suggesting edge cases
- Converting between Jest/Vitest syntax

### What LLMs Struggle With

- Complex async timing issues
- Framework-specific quirks
- Integration with specific project setup
- Performance optimization
- Flaky test debugging

### Prompt Structure for Best Results

```
Context: [Framework, React version, testing library versions]
Component: [Full code]
Dependencies: [API calls, context, stores]
Request: Generate tests for:
1. Happy path
2. Error states
3. Loading states
4. Edge cases: [specific scenarios]
```

## Common Patterns

### Testing Async Code

```typescript
// Async/await (preferred)
it('fetches user data', async () => {
  const data = await fetchUser(1)
  expect(data.name).toBe('John')
})

// Promises
it('fetches user data', () => {
  return fetchUser(1).then((data) => {
    expect(data.name).toBe('John')
  })
})

// Fake timers
it('debounces input', async () => {
  vi.useFakeTimers()
  const callback = vi.fn()

  debouncedSearch('query', callback)

  vi.advanceTimersByTime(300)
  expect(callback).toHaveBeenCalledWith('query')

  vi.useRealTimers()
})
```

### Testing React Context

```typescript
const customRender = (ui: ReactElement, options?: RenderOptions) => {
  const AllProviders = ({ children }: { children: ReactNode }) => (
    <ThemeProvider theme="dark">
      <AuthProvider>
        {children}
      </AuthProvider>
    </ThemeProvider>
  )

  return render(ui, { wrapper: AllProviders, ...options })
}

export { customRender as render }
```

### Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react'

it('updates counter', () => {
  const { result } = renderHook(() => useCounter())

  act(() => {
    result.current.increment()
  })

  expect(result.current.count).toBe(1)
})
```

## File Organization

```
project/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx      # Co-located unit tests
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   └── useAuth.test.ts
│   └── services/
│       ├── api.ts
│       └── api.test.ts
├── tests/
│   ├── setup.ts                 # Global test setup
│   ├── utils.tsx                # Custom render, helpers
│   ├── mocks/
│   │   ├── handlers.ts          # MSW handlers
│   │   └── server.ts            # MSW server
│   └── integration/             # Integration tests
│       └── checkout.test.tsx
├── e2e/
│   ├── auth.spec.ts             # Playwright E2E
│   ├── checkout.spec.ts
│   └── pages/                   # Page Objects
│       └── LoginPage.ts
├── vitest.config.ts
└── playwright.config.ts
```

## Running Tests

### Vitest Commands

```bash
# Run all tests
npx vitest

# Run in watch mode (default)
npx vitest

# Run once
npx vitest run

# Run specific file
npx vitest Button.test.tsx

# Run with coverage
npx vitest run --coverage

# Run specific test by name
npx vitest -t "should render button"

# UI mode
npx vitest --ui
```

### Jest Commands

```bash
# Run all tests
npx jest

# Watch mode
npx jest --watch

# Coverage
npx jest --coverage

# Specific file
npx jest Button.test.tsx

# Specific test name
npx jest -t "should render button"

# Update snapshots
npx jest -u
```

### Playwright Commands

```bash
# Run all E2E tests
npx playwright test

# Run headed
npx playwright test --headed

# Run specific browser
npx playwright test --project=chromium

# Debug mode
npx playwright test --debug

# Generate tests
npx playwright codegen localhost:3000

# Show report
npx playwright show-report
```

## External Resources

### Official Documentation

- [Vitest Documentation](https://vitest.dev/)
- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Playwright Documentation](https://playwright.dev/)
- [MSW Documentation](https://mswjs.io/)

### Best Practices Guides

- [Kent C. Dodds - Common Mistakes with RTL](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Node.js Testing Best Practices](https://github.com/goldbergyoni/nodejs-testing-best-practices)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

### Comparison Articles

- [Vitest vs Jest - Better Stack](https://betterstack.com/community/guides/scaling-nodejs/vitest-vs-jest/)
- [Jest vs Vitest 2025](https://medium.com/@ruverd/jest-vs-vitest-which-test-runner-should-you-use-in-2025-5c85e4f2bda9)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Methodologies

- [testing-patterns/](../testing-patterns/) - AAA, Given-When-Then, Test Pyramid
- [unit-testing/](../unit-testing/) - FIRST principles, isolation
- [integration-testing/](../integration-testing/) - Testcontainers, API testing
- [e2e-testing/](../e2e-testing/) - Playwright guide
- [mocking-strategies/](../mocking-strategies/) - Test doubles, MSW
