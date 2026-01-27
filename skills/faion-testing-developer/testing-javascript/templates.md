# JavaScript Testing Templates

Copy-paste templates for Jest, Vitest, Playwright, and common testing patterns.

## Configuration Templates

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    // Test environment
    globals: true,
    environment: 'jsdom', // 'node' | 'jsdom' | 'happy-dom'

    // File patterns
    include: ['**/*.{test,spec}.{ts,tsx}'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/e2e/**'],

    // Setup files
    setupFiles: ['./tests/setup.ts'],

    // Coverage
    coverage: {
      provider: 'v8', // 'v8' | 'istanbul'
      reporter: ['text', 'html', 'lcov', 'json'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.d.ts',
        'src/**/*.test.{ts,tsx}',
        'src/**/index.ts',
        'src/types/**',
      ],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },

    // Performance
    pool: 'forks', // 'threads' | 'forks' | 'vmThreads'
    poolOptions: {
      forks: {
        singleFork: false,
      },
    },

    // Reporters
    reporters: ['default', 'html'],

    // Timeouts
    testTimeout: 10000,
    hookTimeout: 10000,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@tests': path.resolve(__dirname, './tests'),
    },
  },
})
```

### Jest Configuration

```javascript
// jest.config.js
/** @type {import('jest').Config} */
const config = {
  // Presets
  preset: 'ts-jest',
  testEnvironment: 'jsdom',

  // File patterns
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}'],
  testPathIgnorePatterns: ['/node_modules/', '/dist/', '/e2e/'],

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],

  // Module resolution
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@tests/(.*)$': '<rootDir>/tests/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/tests/__mocks__/fileMock.js',
  },

  // Coverage
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/index.ts',
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
  coverageReporters: ['text', 'html', 'lcov', 'json'],

  // Transform
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      useESM: true,
      tsconfig: 'tsconfig.json',
    }],
  },
  transformIgnorePatterns: [
    'node_modules/(?!(some-esm-package)/)',
  ],

  // Performance
  maxWorkers: '50%',

  // Timeouts
  testTimeout: 10000,

  // Clear mocks between tests
  clearMocks: true,
  restoreMocks: true,
}

module.exports = config
```

### Test Setup File

```typescript
// tests/setup.ts
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach, beforeAll, afterAll, vi } from 'vitest'
import { server } from './mocks/server'

// MSW setup
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

// Cleanup after each test
afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

// Global mocks
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
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

Object.defineProperty(window, 'scrollTo', {
  writable: true,
  value: vi.fn(),
})

class MockResizeObserver {
  observe = vi.fn()
  unobserve = vi.fn()
  disconnect = vi.fn()
}
window.ResizeObserver = MockResizeObserver as any

class MockIntersectionObserver {
  observe = vi.fn()
  unobserve = vi.fn()
  disconnect = vi.fn()
}
window.IntersectionObserver = MockIntersectionObserver as any
```

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  testMatch: '**/*.spec.ts',

  // Parallel execution
  fullyParallel: true,
  workers: process.env.CI ? 1 : undefined,

  // Retries
  retries: process.env.CI ? 2 : 0,

  // Fail fast in CI
  forbidOnly: !!process.env.CI,

  // Reporters
  reporter: [
    ['list'],
    ['html', { open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],

  // Global settings
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  // Browser projects
  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // Mobile browsers
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },

    // Authenticated tests
    {
      name: 'authenticated',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Setup project for auth
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
  ],

  // Dev server
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
})
```

## MSW Templates

### Request Handlers

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse, delay } from 'msw'

const API_URL = '/api'

// Sample data
const users = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
]

export const handlers = [
  // GET list
  http.get(`${API_URL}/users`, async () => {
    await delay(100) // Simulate network latency
    return HttpResponse.json(users)
  }),

  // GET by ID
  http.get(`${API_URL}/users/:id`, async ({ params }) => {
    const user = users.find((u) => u.id === Number(params.id))
    if (!user) {
      return HttpResponse.json(
        { message: 'User not found' },
        { status: 404 }
      )
    }
    return HttpResponse.json(user)
  }),

  // POST create
  http.post(`${API_URL}/users`, async ({ request }) => {
    const body = await request.json() as { name: string; email: string }

    if (!body.name || !body.email) {
      return HttpResponse.json(
        { message: 'Name and email are required' },
        { status: 400 }
      )
    }

    const newUser = {
      id: users.length + 1,
      ...body,
    }

    return HttpResponse.json(newUser, { status: 201 })
  }),

  // PUT update
  http.put(`${API_URL}/users/:id`, async ({ params, request }) => {
    const body = await request.json() as Partial<{ name: string; email: string }>
    const user = users.find((u) => u.id === Number(params.id))

    if (!user) {
      return HttpResponse.json(
        { message: 'User not found' },
        { status: 404 }
      )
    }

    return HttpResponse.json({ ...user, ...body })
  }),

  // DELETE
  http.delete(`${API_URL}/users/:id`, async ({ params }) => {
    const userIndex = users.findIndex((u) => u.id === Number(params.id))

    if (userIndex === -1) {
      return HttpResponse.json(
        { message: 'User not found' },
        { status: 404 }
      )
    }

    return new HttpResponse(null, { status: 204 })
  }),

  // Authentication
  http.post(`${API_URL}/auth/login`, async ({ request }) => {
    const body = await request.json() as { email: string; password: string }

    if (body.email === 'invalid@test.com') {
      return HttpResponse.json(
        { message: 'Invalid credentials' },
        { status: 401 }
      )
    }

    return HttpResponse.json({
      token: 'mock-jwt-token',
      user: { id: 1, email: body.email },
    })
  }),

  // File upload
  http.post(`${API_URL}/upload`, async ({ request }) => {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return HttpResponse.json(
        { message: 'No file provided' },
        { status: 400 }
      )
    }

    return HttpResponse.json({
      id: 'file-123',
      name: file.name,
      size: file.size,
      url: `/uploads/${file.name}`,
    })
  }),

  // With query parameters
  http.get(`${API_URL}/search`, async ({ request }) => {
    const url = new URL(request.url)
    const query = url.searchParams.get('q') || ''
    const page = Number(url.searchParams.get('page')) || 1
    const limit = Number(url.searchParams.get('limit')) || 10

    const results = users.filter((u) =>
      u.name.toLowerCase().includes(query.toLowerCase())
    )

    return HttpResponse.json({
      data: results.slice((page - 1) * limit, page * limit),
      total: results.length,
      page,
      limit,
    })
  }),
]

// Error handlers for testing
export const errorHandlers = {
  networkError: http.get(`${API_URL}/users`, () => {
    return HttpResponse.error()
  }),

  serverError: http.get(`${API_URL}/users`, () => {
    return HttpResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  }),

  timeout: http.get(`${API_URL}/users`, async () => {
    await delay('infinite')
    return HttpResponse.json([])
  }),
}
```

### MSW Server Setup

```typescript
// tests/mocks/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

### MSW Browser Setup

```typescript
// tests/mocks/browser.ts
import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

export const worker = setupWorker(...handlers)
```

## Component Test Templates

### Basic Component Test

```tsx
// Component.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { Component } from './Component'

describe('Component', () => {
  // Setup user event
  const user = userEvent.setup()

  it('renders correctly', () => {
    render(<Component />)

    expect(screen.getByRole('button')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const handleClick = vi.fn()
    render(<Component onClick={handleClick} />)

    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('shows loading state', () => {
    render(<Component loading />)

    expect(screen.getByRole('progressbar')).toBeInTheDocument()
  })

  it('shows error state', () => {
    render(<Component error="Something went wrong" />)

    expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong')
  })
})
```

### Form Component Test

```tsx
// Form.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { ContactForm } from './ContactForm'

describe('ContactForm', () => {
  const user = userEvent.setup()
  const mockSubmit = vi.fn()

  beforeEach(() => {
    mockSubmit.mockClear()
  })

  it('submits form with valid data', async () => {
    render(<ContactForm onSubmit={mockSubmit} />)

    await user.type(screen.getByLabelText(/name/i), 'John Doe')
    await user.type(screen.getByLabelText(/email/i), 'john@example.com')
    await user.type(screen.getByLabelText(/message/i), 'Hello!')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com',
        message: 'Hello!',
      })
    })
  })

  it('shows validation errors', async () => {
    render(<ContactForm onSubmit={mockSubmit} />)

    await user.click(screen.getByRole('button', { name: /submit/i }))

    expect(await screen.findByText(/name is required/i)).toBeInTheDocument()
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument()
    expect(mockSubmit).not.toHaveBeenCalled()
  })

  it('disables submit during loading', async () => {
    mockSubmit.mockImplementation(() => new Promise(() => {}))
    render(<ContactForm onSubmit={mockSubmit} />)

    await user.type(screen.getByLabelText(/name/i), 'John')
    await user.type(screen.getByLabelText(/email/i), 'john@test.com')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    expect(screen.getByRole('button', { name: /submitting/i })).toBeDisabled()
  })
})
```

### Component with API Call

```tsx
// UserList.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { server } from '../tests/mocks/server'
import { describe, it, expect } from 'vitest'
import { UserList } from './UserList'

describe('UserList', () => {
  it('displays loading state initially', () => {
    render(<UserList />)

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('displays users after loading', async () => {
    render(<UserList />)

    expect(await screen.findByText('John Doe')).toBeInTheDocument()
    expect(screen.getByText('Jane Smith')).toBeInTheDocument()
  })

  it('displays error on API failure', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { message: 'Server error' },
          { status: 500 }
        )
      })
    )

    render(<UserList />)

    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('displays empty state when no users', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json([])
      })
    )

    render(<UserList />)

    expect(await screen.findByText(/no users found/i)).toBeInTheDocument()
  })
})
```

## Hook Test Templates

### Custom Hook Test

```tsx
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter())

    expect(result.current.count).toBe(0)
  })

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10))

    expect(result.current.count).toBe(10)
  })

  it('increments count', () => {
    const { result } = renderHook(() => useCounter())

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(4)
  })

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.increment()
      result.current.increment()
      result.current.reset()
    })

    expect(result.current.count).toBe(5)
  })
})
```

### Async Hook Test

```tsx
// useAsync.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { useAsync } from './useAsync'

describe('useAsync', () => {
  it('handles successful async operation', async () => {
    const asyncFn = vi.fn().mockResolvedValue('data')
    const { result } = renderHook(() => useAsync(asyncFn))

    expect(result.current.loading).toBe(true)

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.data).toBe('data')
    expect(result.current.error).toBeNull()
  })

  it('handles async error', async () => {
    const error = new Error('Failed')
    const asyncFn = vi.fn().mockRejectedValue(error)
    const { result } = renderHook(() => useAsync(asyncFn))

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.data).toBeNull()
    expect(result.current.error).toBe(error)
  })

  it('refetches on dependency change', async () => {
    const asyncFn = vi.fn().mockResolvedValue('data')
    const { result, rerender } = renderHook(
      ({ id }) => useAsync(() => asyncFn(id), [id]),
      { initialProps: { id: 1 } }
    )

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    rerender({ id: 2 })

    await waitFor(() => {
      expect(asyncFn).toHaveBeenCalledTimes(2)
    })
  })
})
```

## Playwright E2E Templates

### Page Object

```typescript
// e2e/pages/BasePage.ts
import { Page, Locator } from '@playwright/test'

export abstract class BasePage {
  readonly page: Page

  constructor(page: Page) {
    this.page = page
  }

  async goto(path: string) {
    await this.page.goto(path)
  }

  async waitForNavigation() {
    await this.page.waitForLoadState('networkidle')
  }

  getByTestId(testId: string): Locator {
    return this.page.getByTestId(testId)
  }
}
```

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class LoginPage extends BasePage {
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorAlert: Locator
  readonly forgotPasswordLink: Locator

  constructor(page: Page) {
    super(page)
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Log in' })
    this.errorAlert = page.getByRole('alert')
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot password?' })
  }

  async goto() {
    await super.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectError(message: string | RegExp) {
    await expect(this.errorAlert).toBeVisible()
    await expect(this.errorAlert).toContainText(message)
  }

  async expectLoggedIn() {
    await expect(this.page).toHaveURL('/dashboard')
  }
}
```

### E2E Test with Fixtures

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

type Fixtures = {
  loginPage: LoginPage
  dashboardPage: DashboardPage
}

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page))
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page))
  },
})

export { expect } from '@playwright/test'
```

```typescript
// e2e/auth.spec.ts
import { test, expect } from './fixtures'

test.describe('Authentication', () => {
  test('successful login', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.login('user@example.com', 'password123')
    await loginPage.expectLoggedIn()
  })

  test('invalid credentials', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.login('invalid@example.com', 'wrong')
    await loginPage.expectError(/invalid credentials/i)
  })

  test('empty form validation', async ({ loginPage }) => {
    await loginPage.goto()
    await loginPage.submitButton.click()
    await expect(loginPage.page.getByText(/email is required/i)).toBeVisible()
  })
})
```

### Authentication Setup

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test'
import path from 'path'

const authFile = path.join(__dirname, '../playwright/.auth/user.json')

setup('authenticate', async ({ page }) => {
  // Navigate to login
  await page.goto('/login')

  // Fill credentials
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!)
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!)
  await page.getByRole('button', { name: 'Log in' }).click()

  // Wait for successful login
  await expect(page).toHaveURL('/dashboard')

  // Save authentication state
  await page.context().storageState({ path: authFile })
})
```

## Test Utility Templates

### Custom Render

```tsx
// tests/utils.tsx
import { ReactElement, ReactNode } from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { MemoryRouter } from 'react-router-dom'
import { ThemeProvider } from '@/contexts/ThemeContext'
import { AuthProvider } from '@/contexts/AuthContext'

interface WrapperProps {
  children: ReactNode
}

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  initialRoute?: string
  queryClient?: QueryClient
}

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
        staleTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
  })
}

export function createWrapper(options: CustomRenderOptions = {}) {
  const {
    initialRoute = '/',
    queryClient = createTestQueryClient(),
  } = options

  return function Wrapper({ children }: WrapperProps) {
    return (
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[initialRoute]}>
          <ThemeProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </ThemeProvider>
        </MemoryRouter>
      </QueryClientProvider>
    )
  }
}

export function customRender(
  ui: ReactElement,
  options: CustomRenderOptions = {}
) {
  return render(ui, { wrapper: createWrapper(options), ...options })
}

// Re-export everything
export * from '@testing-library/react'
export { customRender as render }
export { default as userEvent } from '@testing-library/user-event'
```

### Test Data Factories

```typescript
// tests/factories.ts
import { faker } from '@faker-js/faker'

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.number.int(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar(),
    createdAt: faker.date.past().toISOString(),
    ...overrides,
  }
}

export function createPost(overrides: Partial<Post> = {}): Post {
  return {
    id: faker.number.int(),
    title: faker.lorem.sentence(),
    content: faker.lorem.paragraphs(3),
    author: createUser(),
    publishedAt: faker.date.recent().toISOString(),
    tags: faker.helpers.arrayElements(['react', 'typescript', 'testing'], 2),
    ...overrides,
  }
}

export function createUsers(count: number, overrides: Partial<User> = {}): User[] {
  return Array.from({ length: count }, () => createUser(overrides))
}
```

## CI/CD Templates

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true

  e2e-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Build app
        run: npm run build

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload Playwright report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:unit": "vitest run --exclude e2e/**",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "test:watch": "vitest --watch",
    "e2e": "playwright test",
    "e2e:ui": "playwright test --ui",
    "e2e:debug": "playwright test --debug",
    "e2e:codegen": "playwright codegen localhost:3000"
  }
}
```
