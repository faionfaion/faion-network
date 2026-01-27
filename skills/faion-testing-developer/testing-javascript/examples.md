# JavaScript Testing Examples

Real-world test examples for React, Node.js, and common testing scenarios.

## React Component Testing

### Button Component

```tsx
// Button.tsx
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  loading?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  loading = false,
  variant = 'primary',
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`btn btn-${variant}`}
      aria-busy={loading}
    >
      {loading ? <Spinner /> : children}
    </button>
  )
}
```

```tsx
// Button.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { Button } from './Button'

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>)

    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()

    render(<Button onClick={handleClick}>Click me</Button>)

    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('does not call onClick when disabled', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()

    render(<Button onClick={handleClick} disabled>Click me</Button>)

    await user.click(screen.getByRole('button'))

    expect(handleClick).not.toHaveBeenCalled()
  })

  it('shows loading state', () => {
    render(<Button loading>Submit</Button>)

    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('aria-busy', 'true')
    expect(button).toBeDisabled()
  })

  it('applies variant class', () => {
    render(<Button variant="secondary">Secondary</Button>)

    expect(screen.getByRole('button')).toHaveClass('btn-secondary')
  })
})
```

### Form Component with Validation

```tsx
// LoginForm.tsx
import { useState } from 'react'

interface LoginFormProps {
  onSubmit: (data: { email: string; password: string }) => Promise<void>
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validate = () => {
    const newErrors: Record<string, string> = {}
    if (!email) newErrors.email = 'Email is required'
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = 'Email is invalid'
    if (!password) newErrors.password = 'Password is required'
    else if (password.length < 8) newErrors.password = 'Password must be at least 8 characters'
    return newErrors
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const validationErrors = validate()
    setErrors(validationErrors)

    if (Object.keys(validationErrors).length === 0) {
      setIsSubmitting(true)
      try {
        await onSubmit({ email, password })
      } catch {
        setErrors({ form: 'Login failed. Please try again.' })
      } finally {
        setIsSubmitting(false)
      }
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && <span id="email-error" role="alert">{errors.email}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && <span id="password-error" role="alert">{errors.password}</span>}
      </div>

      {errors.form && <div role="alert">{errors.form}</div>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Log in'}
      </button>
    </form>
  )
}
```

```tsx
// LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  const user = userEvent.setup()

  it('renders form fields', () => {
    render(<LoginForm onSubmit={vi.fn()} />)

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument()
  })

  it('shows validation errors for empty fields', async () => {
    render(<LoginForm onSubmit={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument()
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument()
  })

  it('shows error for invalid email', async () => {
    render(<LoginForm onSubmit={vi.fn()} />)

    await user.type(screen.getByLabelText(/email/i), 'invalid-email')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(await screen.findByText(/email is invalid/i)).toBeInTheDocument()
  })

  it('shows error for short password', async () => {
    render(<LoginForm onSubmit={vi.fn()} />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'short')
    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(await screen.findByText(/password must be at least 8 characters/i)).toBeInTheDocument()
  })

  it('submits form with valid data', async () => {
    const handleSubmit = vi.fn().mockResolvedValue(undefined)
    render(<LoginForm onSubmit={handleSubmit} />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /log in/i }))

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      })
    })
  })

  it('shows loading state during submission', async () => {
    const handleSubmit = vi.fn().mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    )
    render(<LoginForm onSubmit={handleSubmit} />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(screen.getByRole('button', { name: /logging in/i })).toBeDisabled()

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /log in/i })).toBeEnabled()
    })
  })

  it('shows error message on submission failure', async () => {
    const handleSubmit = vi.fn().mockRejectedValue(new Error('Network error'))
    render(<LoginForm onSubmit={handleSubmit} />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(await screen.findByText(/login failed/i)).toBeInTheDocument()
  })
})
```

### Component with Data Fetching

```tsx
// UserProfile.tsx
import { useEffect, useState } from 'react'

interface User {
  id: number
  name: string
  email: string
}

interface UserProfileProps {
  userId: number
}

export function UserProfile({ userId }: UserProfileProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchUser() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(`/api/users/${userId}`)
        if (!response.ok) throw new Error('Failed to fetch user')
        const data = await response.json()
        setUser(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }
    fetchUser()
  }, [userId])

  if (loading) return <div role="status" aria-label="Loading">Loading...</div>
  if (error) return <div role="alert">{error}</div>
  if (!user) return null

  return (
    <article>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </article>
  )
}
```

```tsx
// UserProfile.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { UserProfile } from './UserProfile'

describe('UserProfile', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
  }

  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('shows loading state initially', () => {
    vi.mocked(fetch).mockImplementation(() => new Promise(() => {}))

    render(<UserProfile userId={1} />)

    expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument()
  })

  it('displays user data after successful fetch', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockUser),
    } as Response)

    render(<UserProfile userId={1} />)

    expect(await screen.findByRole('heading', { name: mockUser.name })).toBeInTheDocument()
    expect(screen.getByText(mockUser.email)).toBeInTheDocument()
  })

  it('shows error message on fetch failure', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
    } as Response)

    render(<UserProfile userId={1} />)

    expect(await screen.findByRole('alert')).toHaveTextContent(/failed to fetch/i)
  })

  it('shows error on network error', async () => {
    vi.mocked(fetch).mockRejectedValue(new Error('Network error'))

    render(<UserProfile userId={1} />)

    expect(await screen.findByRole('alert')).toHaveTextContent(/network error/i)
  })

  it('refetches when userId changes', async () => {
    const mockFetch = vi.mocked(fetch)
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockUser),
    } as Response)

    const { rerender } = render(<UserProfile userId={1} />)
    await screen.findByText(mockUser.name)

    const newUser = { ...mockUser, id: 2, name: 'Jane Doe' }
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(newUser),
    } as Response)

    rerender(<UserProfile userId={2} />)

    expect(await screen.findByText('Jane Doe')).toBeInTheDocument()
    expect(mockFetch).toHaveBeenCalledTimes(2)
  })
})
```

## Custom Hook Testing

### useLocalStorage Hook

```typescript
// useLocalStorage.ts
import { useState, useEffect } from 'react'

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue))
    } catch {
      console.error('Failed to save to localStorage')
    }
  }, [key, storedValue])

  return [storedValue, setStoredValue] as const
}
```

```tsx
// useLocalStorage.test.ts
import { renderHook, act } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useLocalStorage } from './useLocalStorage'

describe('useLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('returns initial value when localStorage is empty', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'initial'))

    expect(result.current[0]).toBe('initial')
  })

  it('returns stored value from localStorage', () => {
    localStorage.setItem('key', JSON.stringify('stored'))

    const { result } = renderHook(() => useLocalStorage('key', 'initial'))

    expect(result.current[0]).toBe('stored')
  })

  it('updates localStorage when value changes', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'initial'))

    act(() => {
      result.current[1]('updated')
    })

    expect(result.current[0]).toBe('updated')
    expect(localStorage.getItem('key')).toBe(JSON.stringify('updated'))
  })

  it('handles objects', () => {
    const initialValue = { name: 'John', age: 30 }
    const { result } = renderHook(() => useLocalStorage('user', initialValue))

    expect(result.current[0]).toEqual(initialValue)

    act(() => {
      result.current[1]({ name: 'Jane', age: 25 })
    })

    expect(result.current[0]).toEqual({ name: 'Jane', age: 25 })
  })

  it('handles localStorage errors gracefully', () => {
    const error = new Error('Storage quota exceeded')
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw error
    })
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => useLocalStorage('key', 'initial'))

    act(() => {
      result.current[1]('updated')
    })

    expect(consoleSpy).toHaveBeenCalledWith('Failed to save to localStorage')
    consoleSpy.mockRestore()
  })
})
```

### useDebounce Hook

```typescript
// useDebounce.ts
import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}
```

```tsx
// useDebounce.test.ts
import { renderHook, act } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useDebounce } from './useDebounce'

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('initial', 500))

    expect(result.current).toBe('initial')
  })

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    )

    rerender({ value: 'updated', delay: 500 })

    // Value should not change immediately
    expect(result.current).toBe('initial')

    // Fast forward time
    act(() => {
      vi.advanceTimersByTime(500)
    })

    expect(result.current).toBe('updated')
  })

  it('cancels pending debounce on new value', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    )

    rerender({ value: 'first', delay: 500 })

    act(() => {
      vi.advanceTimersByTime(300)
    })

    rerender({ value: 'second', delay: 500 })

    act(() => {
      vi.advanceTimersByTime(300)
    })

    // Still 'initial' because second update reset the timer
    expect(result.current).toBe('initial')

    act(() => {
      vi.advanceTimersByTime(200)
    })

    expect(result.current).toBe('second')
  })
})
```

## API Mocking with MSW

### MSW Setup

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params
    return HttpResponse.json({
      id: Number(id),
      name: 'John Doe',
      email: 'john@example.com',
    })
  }),

  http.post('/api/login', async ({ request }) => {
    const body = await request.json() as { email: string; password: string }

    if (body.email === 'invalid@example.com') {
      return HttpResponse.json(
        { message: 'Invalid credentials' },
        { status: 401 }
      )
    }

    return HttpResponse.json({
      token: 'fake-jwt-token',
      user: { id: 1, email: body.email },
    })
  }),

  http.get('/api/posts', ({ request }) => {
    const url = new URL(request.url)
    const page = url.searchParams.get('page') || '1'
    const limit = url.searchParams.get('limit') || '10'

    return HttpResponse.json({
      posts: [
        { id: 1, title: 'First Post' },
        { id: 2, title: 'Second Post' },
      ],
      page: Number(page),
      limit: Number(limit),
      total: 100,
    })
  }),
]
```

```typescript
// tests/mocks/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)
```

```typescript
// tests/setup.ts
import '@testing-library/jest-dom'
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### Using MSW in Tests

```tsx
// UserService.test.ts
import { http, HttpResponse } from 'msw'
import { server } from '../mocks/server'
import { describe, it, expect } from 'vitest'

async function fetchUser(id: number) {
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) throw new Error('Failed to fetch')
  return response.json()
}

describe('fetchUser', () => {
  it('fetches user successfully', async () => {
    const user = await fetchUser(1)

    expect(user).toEqual({
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
    })
  })

  it('handles server error', async () => {
    server.use(
      http.get('/api/users/:id', () => {
        return HttpResponse.json(
          { message: 'Server error' },
          { status: 500 }
        )
      })
    )

    await expect(fetchUser(1)).rejects.toThrow('Failed to fetch')
  })

  it('handles network error', async () => {
    server.use(
      http.get('/api/users/:id', () => {
        return HttpResponse.error()
      })
    )

    await expect(fetchUser(1)).rejects.toThrow()
  })
})
```

## Node.js API Testing with Supertest

### Express App Testing

```typescript
// app.ts
import express from 'express'

const app = express()
app.use(express.json())

interface User {
  id: number
  name: string
  email: string
}

const users: User[] = [
  { id: 1, name: 'John', email: 'john@example.com' },
]

app.get('/api/users', (req, res) => {
  res.json(users)
})

app.get('/api/users/:id', (req, res) => {
  const user = users.find((u) => u.id === parseInt(req.params.id))
  if (!user) {
    return res.status(404).json({ message: 'User not found' })
  }
  res.json(user)
})

app.post('/api/users', (req, res) => {
  const { name, email } = req.body

  if (!name || !email) {
    return res.status(400).json({ message: 'Name and email are required' })
  }

  const newUser: User = {
    id: users.length + 1,
    name,
    email,
  }
  users.push(newUser)
  res.status(201).json(newUser)
})

export default app
```

```typescript
// app.test.ts
import request from 'supertest'
import { describe, it, expect, beforeEach } from 'vitest'
import app from './app'

describe('Users API', () => {
  describe('GET /api/users', () => {
    it('returns all users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect('Content-Type', /json/)
        .expect(200)

      expect(response.body).toBeInstanceOf(Array)
      expect(response.body.length).toBeGreaterThan(0)
    })
  })

  describe('GET /api/users/:id', () => {
    it('returns user by id', async () => {
      const response = await request(app)
        .get('/api/users/1')
        .expect(200)

      expect(response.body).toEqual({
        id: 1,
        name: 'John',
        email: 'john@example.com',
      })
    })

    it('returns 404 for non-existent user', async () => {
      const response = await request(app)
        .get('/api/users/999')
        .expect(404)

      expect(response.body.message).toBe('User not found')
    })
  })

  describe('POST /api/users', () => {
    it('creates new user', async () => {
      const newUser = {
        name: 'Jane',
        email: 'jane@example.com',
      }

      const response = await request(app)
        .post('/api/users')
        .send(newUser)
        .expect('Content-Type', /json/)
        .expect(201)

      expect(response.body).toMatchObject(newUser)
      expect(response.body.id).toBeDefined()
    })

    it('returns 400 for missing fields', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'Jane' })
        .expect(400)

      expect(response.body.message).toBe('Name and email are required')
    })
  })
})
```

## E2E Testing with Playwright

### Page Object Pattern

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Log in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }
}
```

```typescript
// e2e/pages/DashboardPage.ts
import { Page, Locator } from '@playwright/test'

export class DashboardPage {
  readonly page: Page
  readonly welcomeMessage: Locator
  readonly logoutButton: Locator

  constructor(page: Page) {
    this.page = page
    this.welcomeMessage = page.getByRole('heading', { level: 1 })
    this.logoutButton = page.getByRole('button', { name: 'Log out' })
  }

  async isVisible() {
    await this.welcomeMessage.waitFor()
    return true
  }
}
```

### E2E Test

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

test.describe('Authentication', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page)
    const dashboardPage = new DashboardPage(page)

    await loginPage.goto()
    await loginPage.login('user@example.com', 'password123')

    await expect(page).toHaveURL('/dashboard')
    expect(await dashboardPage.isVisible()).toBe(true)
  })

  test('invalid credentials shows error', async ({ page }) => {
    const loginPage = new LoginPage(page)

    await loginPage.goto()
    await loginPage.login('invalid@example.com', 'wrong')

    await expect(loginPage.errorMessage).toBeVisible()
    await expect(loginPage.errorMessage).toHaveText(/invalid credentials/i)
    await expect(page).toHaveURL('/login')
  })

  test('empty form shows validation errors', async ({ page }) => {
    const loginPage = new LoginPage(page)

    await loginPage.goto()
    await loginPage.submitButton.click()

    await expect(page.getByText(/email is required/i)).toBeVisible()
    await expect(page.getByText(/password is required/i)).toBeVisible()
  })
})
```

### E2E with Authentication State

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test'
import path from 'path'

const authFile = path.join(__dirname, '../playwright/.auth/user.json')

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('user@example.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: 'Log in' }).click()

  await expect(page).toHaveURL('/dashboard')

  await page.context().storageState({ path: authFile })
})
```

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test'

test.use({ storageState: 'playwright/.auth/user.json' })

test('dashboard shows user data', async ({ page }) => {
  await page.goto('/dashboard')

  await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible()
  await expect(page.getByText(/user@example.com/i)).toBeVisible()
})
```

## Snapshot Testing

### Component Snapshot

```tsx
// Card.test.tsx
import { render } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { Card } from './Card'

describe('Card', () => {
  it('matches snapshot', () => {
    const { container } = render(
      <Card title="Test Card" description="Test description">
        <p>Card content</p>
      </Card>
    )

    expect(container).toMatchSnapshot()
  })

  it('matches inline snapshot', () => {
    const { container } = render(<Card title="Simple" />)

    expect(container.innerHTML).toMatchInlineSnapshot(`
      "<div class=\"card\"><h2>Simple</h2></div>"
    `)
  })
})
```

### API Response Snapshot

```typescript
// api.test.ts
import { describe, it, expect } from 'vitest'
import { formatUserResponse } from './utils'

describe('formatUserResponse', () => {
  it('formats user data consistently', () => {
    const user = {
      id: 1,
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@example.com',
      createdAt: new Date('2024-01-01'),
    }

    const result = formatUserResponse(user)

    // Use snapshot for complex object structures
    expect(result).toMatchSnapshot()
  })
})
```

## Testing Async Code

### Timers and Debounce

```typescript
// search.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { debouncedSearch } from './search'

describe('debouncedSearch', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('debounces multiple calls', async () => {
    const searchFn = vi.fn()
    const debounced = debouncedSearch(searchFn, 300)

    debounced('a')
    debounced('ab')
    debounced('abc')

    expect(searchFn).not.toHaveBeenCalled()

    vi.advanceTimersByTime(300)

    expect(searchFn).toHaveBeenCalledTimes(1)
    expect(searchFn).toHaveBeenCalledWith('abc')
  })
})
```

### Retries and Polling

```typescript
// polling.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { pollUntilReady } from './polling'

describe('pollUntilReady', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('resolves when condition is met', async () => {
    let attempts = 0
    const checkStatus = vi.fn().mockImplementation(() => {
      attempts++
      return attempts >= 3
    })

    const promise = pollUntilReady(checkStatus, { interval: 100, maxAttempts: 5 })

    // Advance through polling attempts
    await vi.advanceTimersByTimeAsync(100)
    await vi.advanceTimersByTimeAsync(100)
    await vi.advanceTimersByTimeAsync(100)

    await expect(promise).resolves.toBe(true)
    expect(checkStatus).toHaveBeenCalledTimes(3)
  })

  it('rejects after max attempts', async () => {
    const checkStatus = vi.fn().mockReturnValue(false)

    const promise = pollUntilReady(checkStatus, { interval: 100, maxAttempts: 3 })

    await vi.advanceTimersByTimeAsync(300)

    await expect(promise).rejects.toThrow('Max attempts reached')
  })
})
```

## Testing React Context

### Custom Render with Providers

```tsx
// tests/utils.tsx
import { ReactElement, ReactNode } from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { ThemeProvider } from '../contexts/ThemeContext'
import { AuthProvider } from '../contexts/AuthContext'

interface AllProvidersProps {
  children: ReactNode
}

function AllProviders({ children }: AllProvidersProps) {
  return (
    <ThemeProvider defaultTheme="light">
      <AuthProvider>
        {children}
      </AuthProvider>
    </ThemeProvider>
  )
}

function customRender(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options })
}

export * from '@testing-library/react'
export { customRender as render }
```

```tsx
// ThemeToggle.test.tsx
import { render, screen } from '../tests/utils'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import { ThemeToggle } from './ThemeToggle'

describe('ThemeToggle', () => {
  it('toggles theme', async () => {
    const user = userEvent.setup()
    render(<ThemeToggle />)

    const button = screen.getByRole('button', { name: /toggle theme/i })

    // Initial state
    expect(button).toHaveAttribute('aria-pressed', 'false')

    await user.click(button)

    expect(button).toHaveAttribute('aria-pressed', 'true')
  })
})
```
