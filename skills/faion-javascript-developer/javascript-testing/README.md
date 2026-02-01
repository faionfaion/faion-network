# JavaScript Testing

**Modern testing patterns with Vitest and Jest**

---

## Jest/Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/'],
    },
  },
});
```

---

## Unit Testing

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { calculateDiscount } from './pricing';

describe('calculateDiscount', () => {
  it('should apply percentage discount', () => {
    const result = calculateDiscount(100, { type: 'percentage', value: 10 });
    expect(result).toBe(90);
  });

  it('should apply fixed discount', () => {
    const result = calculateDiscount(100, { type: 'fixed', value: 15 });
    expect(result).toBe(85);
  });

  it('should not go below zero', () => {
    const result = calculateDiscount(10, { type: 'fixed', value: 20 });
    expect(result).toBe(0);
  });

  it('should throw for negative price', () => {
    expect(() => calculateDiscount(-10, { type: 'fixed', value: 5 }))
      .toThrow('Price must be positive');
  });
});
```

---

## Component Testing

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should render email and password inputs', () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('should call onSubmit with form data', async () => {
    const handleSubmit = vi.fn();
    const user = userEvent.setup();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('should show validation error for invalid email', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    await user.type(screen.getByLabelText(/email/i), 'invalid-email');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
  });
});
```

---

## Mocking

```typescript
import { vi, type Mock } from 'vitest';
import { fetchUsers } from './api';
import { getUsers } from './users.service';

// Mock module
vi.mock('./api', () => ({
  fetchUsers: vi.fn(),
}));

describe('getUsers', () => {
  const mockFetchUsers = fetchUsers as Mock;

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return users from API', async () => {
    const mockUsers = [{ id: '1', name: 'John' }];
    mockFetchUsers.mockResolvedValue(mockUsers);

    const result = await getUsers();

    expect(result).toEqual(mockUsers);
    expect(mockFetchUsers).toHaveBeenCalledTimes(1);
  });

  it('should handle API error', async () => {
    mockFetchUsers.mockRejectedValue(new Error('Network error'));

    await expect(getUsers()).rejects.toThrow('Network error');
  });
});
```

---

## API Testing with MSW

```typescript
// test/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json({
      users: [
        { id: '1', name: 'John' },
        { id: '2', name: 'Jane' },
      ],
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: '3', ...body },
      { status: 201 },
    );
  }),
];

// test/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Jest configuration | haiku | Test setup automation |
| Mock strategy | sonnet | Mocking pattern expertise |
| Test structure design | sonnet | Testing architecture |

## Sources

- [Vitest Documentation](https://vitest.dev/) - Fast unit test framework
- [Testing Library](https://testing-library.com/) - React component testing
- [MSW (Mock Service Worker)](https://mswjs.io/) - API mocking for testing
- [Kent C. Dodds Testing Guide](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library) - Testing best practices
- [JavaScript Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices) - Comprehensive testing guide
