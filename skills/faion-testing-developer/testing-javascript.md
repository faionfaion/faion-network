---
name: faion-testing-javascript
user-invocable: false
description: "Jest/Vitest testing: mocking, async, snapshots"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(jest:*, vitest:*)
---

# Jest/Vitest Testing (JavaScript/TypeScript)

## Overview

Jest is the most popular JavaScript testing framework. Vitest is a newer, faster alternative compatible with Jest API.

## Installation

```bash
# Jest
npm install --save-dev jest @types/jest ts-jest

# Vitest
npm install --save-dev vitest @vitest/coverage-v8
```

## Jest Configuration

```javascript
// jest.config.js
/** @type {import('jest').Config} */
const config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: ['src/**/*.{ts,tsx}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 },
  },
  clearMocks: true,
};

module.exports = config;
```

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.ts'],
      thresholds: { branches: 80, functions: 80, lines: 80, statements: 80 },
    },
  },
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
});
```

## Basic Test

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { UserService } from '@/services/userService';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  it('should create user with valid data', () => {
    const userData = { name: 'John', email: 'john@example.com' };

    const user = service.createUser(userData);

    expect(user).toBeDefined();
    expect(user.id).toBeDefined();
    expect(user.name).toBe('John');
  });

  it('should throw error with invalid email', () => {
    const userData = { name: 'John', email: 'invalid' };

    expect(() => service.createUser(userData)).toThrow('Invalid email');
  });
});
```

## Matchers

```typescript
// Equality
expect(2 + 2).toBe(4);                    // Strict equality
expect({ a: 1 }).toEqual({ a: 1 });       // Deep equality
expect({ a: 1, b: 2 }).toMatchObject({ a: 1 }); // Partial match

// Truthiness
expect(null).toBeNull();
expect(undefined).toBeUndefined();
expect(true).toBeTruthy();
expect(false).toBeFalsy();

// Numbers
expect(4).toBeGreaterThan(3);
expect(0.1 + 0.2).toBeCloseTo(0.3);

// Strings
expect('hello world').toContain('world');
expect('hello').toMatch(/^hel/);

// Arrays
expect([1, 2, 3]).toContain(2);
expect([1, 2, 3]).toHaveLength(3);

// Objects
expect({ name: 'John' }).toHaveProperty('name');
expect({ name: 'John' }).toHaveProperty('name', 'John');

// Exceptions
expect(() => { throw new Error('fail'); }).toThrow();
expect(() => { throw new Error('fail'); }).toThrow('fail');
```

## Mocking

### Function Mocks

```typescript
import { vi } from 'vitest';

it('should mock function', () => {
  const mockFn = vi.fn();
  mockFn('arg1', 'arg2');

  expect(mockFn).toHaveBeenCalled();
  expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
  expect(mockFn).toHaveBeenCalledTimes(1);
});

it('should mock return value', () => {
  const mockFn = vi.fn()
    .mockReturnValue('default')
    .mockReturnValueOnce('first')
    .mockReturnValueOnce('second');

  expect(mockFn()).toBe('first');
  expect(mockFn()).toBe('second');
  expect(mockFn()).toBe('default');
});
```

### Module Mocks

```typescript
// Mock entire module
vi.mock('@/services/api', () => ({
  fetchData: vi.fn().mockResolvedValue({ data: 'mocked' }),
}));

// Mock specific export
vi.mock('@/utils/helpers', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    formatDate: vi.fn().mockReturnValue('2024-01-01'),
  };
});

// Spy on module
import * as helpers from '@/utils/helpers';

it('should spy on module', () => {
  const spy = vi.spyOn(helpers, 'formatDate');
  helpers.formatDate(new Date());
  expect(spy).toHaveBeenCalled();
});
```

### HTTP Mocks

```typescript
// Mock fetch
global.fetch = vi.fn();

it('should fetch data', async () => {
  vi.mocked(fetch).mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve({ users: [] }),
  } as Response);

  const result = await fetchUsers();

  expect(fetch).toHaveBeenCalledWith('/api/users');
  expect(result).toEqual({ users: [] });
});

it('should handle error', async () => {
  vi.mocked(fetch).mockRejectedValueOnce(new Error('Network error'));

  await expect(fetchUsers()).rejects.toThrow('Network error');
});
```

## Async Testing

```typescript
// Async/await
it('should resolve async', async () => {
  const result = await asyncFetchData();
  expect(result).toBeDefined();
});

// Promises
it('should resolve promise', () => {
  return fetchData().then(result => {
    expect(result).toBeDefined();
  });
});

// Timeouts
it('should handle timers', () => {
  vi.useFakeTimers();

  const callback = vi.fn();
  setTimeout(callback, 1000);

  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalled();

  vi.useRealTimers();
});
```

## Snapshot Testing

```typescript
it('should match snapshot', () => {
  const user = { id: 1, name: 'John', email: 'john@example.com' };
  expect(user).toMatchSnapshot();
});

it('should match inline snapshot', () => {
  const result = formatUser({ name: 'John' });
  expect(result).toMatchInlineSnapshot(`"Hello, John!"`);
});
```

## Running Tests

```bash
# Jest
npx jest
npx jest --watch
npx jest --coverage
npx jest path/to/test.ts
npx jest -t "test name pattern"

# Vitest
npx vitest
npx vitest run
npx vitest --coverage
npx vitest path/to/test.ts
npx vitest -t "test name pattern"
```

## Sources

- [Jest Documentation](https://jestjs.io/docs/getting-started) - official Jest docs
- [Vitest Documentation](https://vitest.dev/) - official Vitest docs
- [Testing Library](https://testing-library.com/docs/react-testing-library/intro/) - React testing utilities
- [Jest Mock Functions](https://jestjs.io/docs/mock-functions) - mocking guide
- [Vitest API Reference](https://vitest.dev/api/) - complete API reference
