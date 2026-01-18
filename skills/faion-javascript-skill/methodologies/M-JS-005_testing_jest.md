# M-JS-005: Testing with Jest and Vitest

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Intermediate
- **Tags:** #dev, #javascript, #testing, #jest, #vitest, #methodology
- **Agent:** faion-test-agent

---

## Problem

Most JavaScript projects have inadequate tests or no tests at all. Developers skip tests because they are slow, hard to write, or seem unnecessary. When bugs appear in production, you wish you had tests.

## Promise

After this methodology, you will write tests that are fast, maintainable, and catch real bugs. You will know what to test, how to test, and when to use different testing strategies.

## Overview

Modern JavaScript testing uses Jest or Vitest for unit/integration tests. Vitest is faster and has better ESM support. This methodology covers patterns that work with both.

---

## Framework

### Step 1: Setup

**Vitest (recommended for new projects):**

```bash
pnpm add -D vitest @vitest/coverage-v8
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // or 'jsdom' for browser
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules', 'tests'],
    },
    include: ['**/*.{test,spec}.{ts,tsx}'],
  },
});
```

**Jest:**

```bash
pnpm add -D jest ts-jest @types/jest
```

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/*.test.ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
};
```

### Step 2: Test Structure

**Arrange-Act-Assert Pattern:**

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid input', async () => {
      // Arrange
      const input = { email: 'test@example.com', name: 'Test User' };
      const mockRepository = { create: vi.fn().mockResolvedValue({ id: '1', ...input }) };
      const service = new UserService(mockRepository);

      // Act
      const result = await service.createUser(input);

      // Assert
      expect(result).toEqual({ id: '1', ...input });
      expect(mockRepository.create).toHaveBeenCalledWith(input);
    });

    it('should throw error for duplicate email', async () => {
      // Arrange
      const input = { email: 'existing@example.com', name: 'Test' };
      const mockRepository = {
        findByEmail: vi.fn().mockResolvedValue({ id: '1' }),
      };
      const service = new UserService(mockRepository);

      // Act & Assert
      await expect(service.createUser(input))
        .rejects
        .toThrow('User with this email already exists');
    });
  });
});
```

**Test Naming:**

```typescript
// Good - describes behavior
it('should return empty array when no users found', () => {});
it('should throw ValidationError when email is invalid', () => {});
it('should hash password before storing', () => {});

// Bad - describes implementation
it('calls findAll method', () => {});
it('uses bcrypt', () => {});
```

### Step 3: Mocking

**Function Mocks:**

```typescript
// Vitest
import { vi, describe, it, expect, beforeEach } from 'vitest';

// Create mock
const mockFetch = vi.fn();

// Mock return value
mockFetch.mockReturnValue('value');
mockFetch.mockReturnValueOnce('first call');

// Mock resolved value (async)
mockFetch.mockResolvedValue({ data: 'result' });
mockFetch.mockRejectedValue(new Error('Failed'));

// Mock implementation
mockFetch.mockImplementation((url) => {
  if (url.includes('/users')) return { users: [] };
  return null;
});

// Assertions
expect(mockFetch).toHaveBeenCalled();
expect(mockFetch).toHaveBeenCalledWith('/api/users');
expect(mockFetch).toHaveBeenCalledTimes(2);
```

**Module Mocks:**

```typescript
// Mock entire module
vi.mock('./database', () => ({
  default: {
    query: vi.fn().mockResolvedValue([]),
  },
}));

// Mock specific export
vi.mock('./utils', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    sendEmail: vi.fn(), // Only mock this function
  };
});

// Spy on existing function
const spy = vi.spyOn(console, 'log');
console.log('test');
expect(spy).toHaveBeenCalledWith('test');
spy.mockRestore();
```

**Class Mocks:**

```typescript
// Mock class
vi.mock('./UserRepository', () => ({
  UserRepository: vi.fn().mockImplementation(() => ({
    findById: vi.fn().mockResolvedValue({ id: '1', name: 'Test' }),
    create: vi.fn().mockResolvedValue({ id: '2' }),
  })),
}));

// Or use manual mock in __mocks__ folder
// __mocks__/UserRepository.ts
export const UserRepository = vi.fn().mockImplementation(() => ({
  findById: vi.fn(),
  create: vi.fn(),
}));
```

### Step 4: Testing Patterns

**Testing Async Code:**

```typescript
// Promises
it('should fetch users', async () => {
  const users = await getUsers();
  expect(users).toHaveLength(3);
});

// Rejections
it('should handle errors', async () => {
  await expect(failingOperation()).rejects.toThrow('Error message');
});

// Callbacks (if needed)
it('should call callback', (done) => {
  fetchData((error, data) => {
    expect(error).toBeNull();
    expect(data).toBeDefined();
    done();
  });
});
```

**Testing Error Cases:**

```typescript
describe('validation', () => {
  it.each([
    ['empty email', { email: '', name: 'Test' }, 'Email is required'],
    ['invalid email', { email: 'invalid', name: 'Test' }, 'Invalid email format'],
    ['empty name', { email: 'test@test.com', name: '' }, 'Name is required'],
  ])('should reject %s', async (_, input, expectedError) => {
    await expect(validateUser(input)).rejects.toThrow(expectedError);
  });
});
```

**Snapshot Testing:**

```typescript
// For complex objects or components
it('should match snapshot', () => {
  const result = generateReport({ sales: 100, revenue: 5000 });
  expect(result).toMatchSnapshot();
});

// Inline snapshot
it('should format correctly', () => {
  const output = formatDate(new Date('2024-01-15'));
  expect(output).toMatchInlineSnapshot('"January 15, 2024"');
});
```

### Step 5: Testing React Components

```typescript
// Setup with Testing Library
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('should submit form with valid data', async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();

    render(<LoginForm onSubmit={onSubmit} />);

    // Find elements
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /submit/i });

    // Fill form
    await user.type(emailInput, 'test@example.com');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);

    // Assert
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('should show validation errors', async () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  });
});
```

### Step 6: Test Organization

```
src/
├── services/
│   ├── users.service.ts
│   └── users.service.test.ts    # Unit tests next to source
├── utils/
│   ├── validators.ts
│   └── validators.test.ts
└── __tests__/                   # Integration tests
    ├── api/
    │   └── users.api.test.ts
    └── setup.ts                 # Global setup
```

**Setup and Teardown:**

```typescript
// Global setup in vitest.config.ts or setupFiles
import { beforeAll, afterAll, beforeEach, afterEach } from 'vitest';

beforeAll(async () => {
  // Run once before all tests
  await database.connect();
});

afterAll(async () => {
  // Run once after all tests
  await database.disconnect();
});

beforeEach(() => {
  // Run before each test
  vi.clearAllMocks();
});

afterEach(() => {
  // Run after each test
  vi.restoreAllMocks();
});
```

---

## Templates

### Service Test Template

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './user.service';
import type { UserRepository } from '../repositories/user.repository';

describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = {
      findById: vi.fn(),
      findAll: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    };
    service = new UserService(mockRepository);
    vi.clearAllMocks();
  });

  describe('findById', () => {
    it('should return user when found', async () => {
      const user = { id: '1', name: 'Test' };
      mockRepository.findById.mockResolvedValue(user);

      const result = await service.findById('1');

      expect(result).toEqual(user);
      expect(mockRepository.findById).toHaveBeenCalledWith('1');
    });

    it('should return null when not found', async () => {
      mockRepository.findById.mockResolvedValue(null);

      const result = await service.findById('999');

      expect(result).toBeNull();
    });
  });

  // More tests...
});
```

### API Integration Test Template

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { database } from '../config/database';

describe('Users API', () => {
  beforeAll(async () => {
    await database.connect();
    await database.seed();
  });

  afterAll(async () => {
    await database.clear();
    await database.disconnect();
  });

  describe('GET /api/users', () => {
    it('should return list of users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toBeInstanceOf(Array);
    });
  });

  describe('POST /api/users', () => {
    it('should create user with valid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'new@test.com', name: 'New User' })
        .expect(201);

      expect(response.body.data).toMatchObject({
        email: 'new@test.com',
        name: 'New User',
      });
    });

    it('should return 400 for invalid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'invalid' })
        .expect(400);

      expect(response.body.success).toBe(false);
    });
  });
});
```

---

## Examples

### Testing with MSW (API Mocking)

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'User 1' },
      { id: '2', name: 'User 2' },
    ]);
  }),
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '3', ...body }, { status: 201 });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('should fetch users', async () => {
  const users = await fetchUsers();
  expect(users).toHaveLength(2);
});
```

### Property-Based Testing

```typescript
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';

describe('sort function', () => {
  it('should sort any array of numbers', () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (arr) => {
        const sorted = sort(arr);

        // Length preserved
        expect(sorted.length).toBe(arr.length);

        // Actually sorted
        for (let i = 1; i < sorted.length; i++) {
          expect(sorted[i]).toBeGreaterThanOrEqual(sorted[i - 1]);
        }
      })
    );
  });
});
```

---

## Common Mistakes

1. **Testing implementation, not behavior** - Test what code does, not how
2. **Too many mocks** - If mocking everything, test is useless
3. **Shared state between tests** - Each test should be independent
4. **No assertions** - Empty tests pass silently
5. **Testing third-party code** - Trust your dependencies

---

## Checklist

- [ ] Vitest/Jest configured with TypeScript
- [ ] Coverage thresholds set
- [ ] Tests follow AAA pattern
- [ ] Mocks reset between tests
- [ ] Async tests properly awaited
- [ ] Edge cases covered
- [ ] Test names describe behavior
- [ ] CI runs tests on every push

---

## Next Steps

- M-JS-003: Node.js Patterns
- M-JS-008: Code Quality
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-JS-005 v1.0*
