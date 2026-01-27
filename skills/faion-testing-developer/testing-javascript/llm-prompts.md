# LLM Prompts for JavaScript Testing

Effective prompts for AI-assisted test generation, debugging, and improvement.

## General Guidelines

### Prompt Structure

```
CONTEXT: [Framework, versions, project type]
CODE: [Full component/function code]
DEPENDENCIES: [External APIs, context, stores]
REQUEST: [Specific test scenarios]
CONSTRAINTS: [Style preferences, patterns to follow]
```

### Best Practices

1. **Provide full code** - Include the entire component, not snippets
2. **Specify framework** - Vitest vs Jest matters for syntax
3. **Include types** - TypeScript interfaces improve accuracy
4. **List edge cases** - Explicitly mention scenarios to cover
5. **Show patterns** - Include an example of your test style

## Component Testing Prompts

### Basic Component Test

```
Generate Vitest tests for this React component using React Testing Library.

```tsx
// Button.tsx
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
  loading?: boolean
}

export function Button({ children, onClick, disabled, variant = 'primary', loading }: ButtonProps) {
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

Test requirements:
1. Renders children correctly
2. Calls onClick when clicked
3. Does not call onClick when disabled
4. Shows loading state (spinner, aria-busy)
5. Applies correct variant class

Use userEvent for interactions, not fireEvent.
```

### Form Component Test

```
Generate comprehensive tests for this login form component.

```tsx
[Paste full component code here]
```

Framework: Vitest + React Testing Library
Test scenarios:
1. Initial render with all fields
2. Form validation (empty fields, invalid email, short password)
3. Successful form submission
4. Loading state during submission
5. Error handling on API failure
6. Accessibility (labels, error announcements)

Patterns to follow:
- Use async/await with userEvent.setup()
- Use findBy for async elements
- Use role-based queries (getByRole, getByLabelText)
- Mock onSubmit as vi.fn()
```

### Component with Data Fetching

```
Generate tests for a component that fetches data on mount.

```tsx
[Paste component code]
```

Test setup:
- Framework: Vitest
- API mocking: Mock global fetch (not MSW)

Test cases:
1. Shows loading state initially
2. Displays data after successful fetch
3. Shows error message on API failure
4. Refetches when userId prop changes

Include beforeEach/afterEach for mock cleanup.
```

## Hook Testing Prompts

### Custom Hook Test

```
Generate tests for this custom React hook.

```typescript
// useLocalStorage.ts
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
    window.localStorage.setItem(key, JSON.stringify(storedValue))
  }, [key, storedValue])

  return [storedValue, setStoredValue] as const
}
```

Framework: Vitest with @testing-library/react
Test scenarios:
1. Returns initial value when localStorage is empty
2. Returns stored value from localStorage
3. Updates localStorage when value changes
4. Handles objects and arrays
5. Handles localStorage errors gracefully (quota exceeded)

Use renderHook and act() from @testing-library/react.
```

### Async Hook Test

```
Generate tests for a hook that performs async operations.

```typescript
[Paste hook code]
```

Test requirements:
1. Initial loading state
2. Successful data fetch
3. Error handling
4. Refetch on dependency change
5. Abort on unmount

Use fake timers if needed for timeouts.
Mock external API calls.
```

## API Mocking Prompts

### MSW Handlers

```
Generate MSW request handlers for these API endpoints.

Endpoints:
- GET /api/users - List all users (paginated)
- GET /api/users/:id - Get user by ID
- POST /api/users - Create new user (validate name, email)
- PUT /api/users/:id - Update user
- DELETE /api/users/:id - Delete user
- POST /api/auth/login - Login (return JWT token)

Requirements:
- Use MSW v2 syntax (http.get, HttpResponse)
- Include realistic error responses (400, 401, 404, 500)
- Add artificial delay for loading state testing
- Include query parameter handling for pagination/search
```

### Mock Override for Error Testing

```
Show how to override MSW handlers in tests to simulate different error scenarios.

Base handler returns users list successfully.
Need to test:
1. 500 server error
2. 401 unauthorized
3. Network error (no connection)
4. Slow response (timeout testing)

Use server.use() for per-test overrides.
```

## E2E Testing Prompts

### Page Object Generation

```
Generate a Playwright Page Object class for this login page.

Page structure:
- Email input (label: "Email")
- Password input (label: "Password")
- "Log in" submit button
- "Forgot password?" link
- Error message alert
- "Remember me" checkbox

Include methods:
1. goto() - Navigate to login page
2. login(email, password) - Fill and submit
3. expectError(message) - Assert error is shown
4. expectLoggedIn() - Assert redirect to dashboard
```

### E2E Test Suite

```
Generate Playwright E2E tests for authentication flow.

Scenarios:
1. Successful login redirects to dashboard
2. Invalid credentials shows error
3. Empty form shows validation errors
4. Logout returns to login page
5. Protected route redirects to login when not authenticated

Use Page Object pattern.
Include proper waits and assertions.
Handle authentication state with storageState.
```

### Visual Regression Test

```
Generate Playwright visual regression tests for a component library.

Components to test:
- Button (primary, secondary, disabled, loading)
- Card (with/without image)
- Modal (open state)
- Form (empty, filled, error state)

Requirements:
- Screenshot each variant
- Use toMatchSnapshot for comparison
- Handle animations (disable or wait)
- Test dark/light themes
```

## Debugging Prompts

### Flaky Test Investigation

```
This test is flaky in CI but passes locally. Help me debug.

Test code:
```tsx
[Paste test code]
```

Component code:
```tsx
[Paste component code]
```

Symptoms:
- Passes 80% of the time
- "Unable to find element" error
- Works with longer timeout

Questions:
1. What could cause inconsistent behavior?
2. Should I use findBy instead of getBy?
3. Are there race conditions?
4. How to make this test deterministic?
```

### Async Test Failure

```
My async test is failing with timeout. Help diagnose.

Test:
```tsx
it('loads data', async () => {
  render(<UserList />)
  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument()
  })
})
```

Error: "Unable to find an element with the text: John"

Component makes fetch call on mount.
I'm mocking fetch with vi.fn().

Questions:
1. Is the mock set up correctly?
2. Am I waiting properly?
3. Is the component actually making the request?
```

### Mock Not Working

```
My mock isn't being called. Help debug.

Test setup:
```tsx
vi.mock('@/services/api', () => ({
  fetchUsers: vi.fn().mockResolvedValue([])
}))
```

Component imports: `import { fetchUsers } from '@/services/api'`

The real API is being called instead of the mock.

Questions:
1. Is the path correct?
2. Should I use vi.mock at module level?
3. Do I need to reset between tests?
```

## Refactoring Prompts

### Improve Test Quality

```
Review and improve these tests for better quality.

Current tests:
```tsx
[Paste tests]
```

Problems I see:
- Tests are brittle
- Too much implementation detail testing
- Repeated setup code

Improve:
1. Focus on user behavior
2. Extract common setup
3. Use better assertions
4. Add missing edge cases
```

### Convert Jest to Vitest

```
Convert this Jest test file to Vitest.

```tsx
[Paste Jest test code]
```

Changes needed:
1. Replace jest.fn() with vi.fn()
2. Replace jest.mock() with vi.mock()
3. Update imports
4. Update any Jest-specific matchers
5. Update fake timers syntax
```

### Add TypeScript to Tests

```
Add proper TypeScript types to these tests.

```tsx
[Paste untyped test code]
```

Requirements:
1. Type all mocks properly
2. Type custom render functions
3. Type test data factories
4. Avoid 'any' where possible
```

## Coverage Improvement Prompts

### Identify Missing Coverage

```
Analyze this component and suggest tests to improve coverage.

```tsx
[Paste component code]
```

Current coverage: 60% branches, 75% lines

Identify:
1. Uncovered branches (conditionals)
2. Error paths not tested
3. Edge cases missing
4. Async scenarios

Generate specific test cases for each gap.
```

### Critical Path Testing

```
What are the most critical tests to write for this feature?

Feature: User checkout flow
Components involved:
- CartSummary
- PaymentForm
- ShippingForm
- OrderConfirmation

I have limited time. Prioritize:
1. Happy path tests
2. Most likely failure points
3. Business-critical validations

For each, provide the test case name and brief description.
```

## Specific Scenario Prompts

### Testing Drag and Drop

```
Generate tests for a drag-and-drop sortable list component.

```tsx
[Paste component code]
```

Test scenarios:
1. Renders items in correct order
2. Reorders items on drag
3. Fires onReorder callback with new order
4. Handles keyboard reordering (a11y)
5. Cancels drag on Escape

Use userEvent or Playwright as appropriate.
```

### Testing File Upload

```
Generate tests for a file upload component.

```tsx
[Paste component code]
```

Test scenarios:
1. Accepts valid file types
2. Rejects invalid file types
3. Shows upload progress
4. Handles upload success
5. Handles upload failure
6. Supports drag and drop

Mock the upload API call.
Use userEvent.upload() for file selection.
```

### Testing Infinite Scroll

```
Generate tests for an infinite scroll list.

```tsx
[Paste component code]
```

Test scenarios:
1. Loads initial page
2. Loads next page when scrolling
3. Shows loading indicator
4. Handles end of list
5. Handles API error on subsequent pages

Mock IntersectionObserver for scroll detection.
```

### Testing WebSocket

```
Generate tests for a component using WebSocket for real-time updates.

```tsx
[Paste component code]
```

Test scenarios:
1. Connects on mount
2. Displays received messages
3. Handles connection error
4. Reconnects on disconnect
5. Cleans up on unmount

Provide WebSocket mock implementation.
```

## Template Generation Prompts

### Generate Test Template

```
Generate a test template for a new [type] component.

Component type: [Form/List/Modal/etc.]
Framework: Vitest + RTL
Features: [list features]

Include:
1. Import statements
2. describe block structure
3. Common setup (beforeEach)
4. Test case skeletons
5. Comments for what each test should verify
```

### Generate Test Data Factory

```
Generate test data factories for these TypeScript interfaces.

```typescript
interface User {
  id: number
  name: string
  email: string
  avatar?: string
  role: 'admin' | 'user' | 'guest'
  createdAt: Date
  preferences: {
    theme: 'light' | 'dark'
    notifications: boolean
  }
}

interface Post {
  id: number
  title: string
  content: string
  authorId: number
  tags: string[]
  status: 'draft' | 'published'
}
```

Use @faker-js/faker for realistic data.
Support overrides parameter.
Include createMany helper.
```

## Anti-Pattern Detection

### Review for Testing Anti-Patterns

```
Review these tests for anti-patterns and suggest improvements.

```tsx
[Paste tests]
```

Check for:
1. Testing implementation details
2. Overly specific assertions
3. Tests that could break from refactoring
4. Missing error handling tests
5. Unclear test names
6. Shared mutable state
7. Over-mocking
8. Testing library code instead of our code

For each issue found:
- Explain why it's problematic
- Show the improved version
```
