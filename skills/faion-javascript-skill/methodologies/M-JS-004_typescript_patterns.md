# M-JS-004: TypeScript Advanced Patterns

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Intermediate
- **Tags:** #dev, #typescript, #patterns, #types, #methodology
- **Agent:** faion-code-agent

---

## Problem

TypeScript gives type safety, but most developers use only basic features. Without advanced patterns, you end up with `any` types, type assertions, and false confidence. You need patterns that maximize TypeScript's power.

## Promise

After this methodology, you will write TypeScript code that catches bugs at compile time, documents itself through types, and provides excellent developer experience with autocomplete.

## Overview

TypeScript 5.x offers powerful type inference, conditional types, and utility types. This methodology covers patterns that make your code safer and more maintainable.

---

## Framework

### Step 1: Strict Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,                    // Enable all strict checks
    "noUncheckedIndexedAccess": true,  // Array access returns T | undefined
    "noImplicitReturns": true,         // All code paths must return
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true, // Distinguish undefined from missing
    "noPropertyAccessFromIndexSignature": true
  }
}
```

### Step 2: Type Inference Patterns

**Let TypeScript Infer:**

```typescript
// Bad - unnecessary annotation
const users: User[] = getUsers();

// Good - let inference work
const users = getUsers(); // TypeScript knows it's User[]

// Bad - redundant annotation
function add(a: number, b: number): number {
  return a + b;
}

// Good - return type inferred
function add(a: number, b: number) {
  return a + b; // TypeScript infers number
}
```

**Explicit When Needed:**

```typescript
// Explicit for function parameters
function process(data: unknown): ProcessedData {
  // ...
}

// Explicit for complex returns
function createUser(input: CreateUserInput): User {
  // Multiple possible return paths
}

// Explicit for exported types
export type Config = {
  apiUrl: string;
  timeout: number;
};
```

### Step 3: Discriminated Unions

```typescript
// Define union with discriminant
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Usage with exhaustive handling
function handleResult<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data); // TypeScript knows data exists
  } else {
    console.error(result.error); // TypeScript knows error exists
  }
}

// More complex example: State machine
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function render<T>(state: RequestState<T>) {
  switch (state.status) {
    case 'idle':
      return 'Ready';
    case 'loading':
      return 'Loading...';
    case 'success':
      return `Data: ${state.data}`;
    case 'error':
      return `Error: ${state.error.message}`;
  }
}
```

### Step 4: Utility Types

**Built-in Utilities:**

```typescript
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

// Partial - all properties optional
type UserUpdate = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude properties
type CreateUserInput = Omit<User, 'id' | 'createdAt'>;

// Readonly - immutable
type ImmutableUser = Readonly<User>;

// Record - object type
type UserById = Record<string, User>;

// Extract/Exclude for unions
type Status = 'pending' | 'active' | 'deleted';
type ActiveStatus = Extract<Status, 'pending' | 'active'>; // 'pending' | 'active'
type InactiveStatus = Exclude<Status, 'active'>; // 'pending' | 'deleted'

// ReturnType - extract function return
type GetUserReturn = ReturnType<typeof getUser>;

// Parameters - extract function params
type GetUserParams = Parameters<typeof getUser>;

// Awaited - unwrap Promise
type User = Awaited<Promise<User>>; // User
```

**Custom Utilities:**

```typescript
// DeepPartial - nested optional
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// NonNullableProperties - remove null/undefined
type NonNullableProps<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};

// Mutable - remove readonly
type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};

// ValueOf - get union of values
type ValueOf<T> = T[keyof T];

// Prettify - expand intersections for readability
type Prettify<T> = {
  [K in keyof T]: T[K];
} & {};
```

### Step 5: Generic Patterns

**Constrained Generics:**

```typescript
// Constraint to object with id
function findById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(item => item.id === id);
}

// Constraint to keys of object
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Default generic parameter
function createArray<T = string>(length: number, value: T): T[] {
  return Array(length).fill(value);
}
```

**Generic Factory:**

```typescript
// Factory with type inference
function createStore<T>(initial: T) {
  let state = initial;

  return {
    get: () => state,
    set: (value: T) => { state = value; },
    update: (fn: (current: T) => T) => { state = fn(state); },
  };
}

const counterStore = createStore(0);
counterStore.set(5);      // OK
counterStore.set('five'); // Error: string not assignable to number
```

### Step 6: Type Guards

**User-Defined Type Guards:**

```typescript
// Type guard function
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    typeof (value as User).id === 'string' &&
    typeof (value as User).email === 'string'
  );
}

// Usage
function processData(data: unknown) {
  if (isUser(data)) {
    console.log(data.email); // TypeScript knows it's User
  }
}

// Array filter with type guard
const items: (User | null)[] = [user1, null, user2];
const users = items.filter((item): item is User => item !== null);
// users is User[], not (User | null)[]
```

**Assertion Functions:**

```typescript
function assertIsUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new Error('Value is not a User');
  }
}

// After assertion, type is narrowed
function handleData(data: unknown) {
  assertIsUser(data);
  console.log(data.email); // data is now User
}
```

### Step 7: Branded Types

```typescript
// Create branded type for type safety
type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

function createOrderId(id: string): OrderId {
  return id as OrderId;
}

// Now these can't be confused
function getUser(id: UserId): User { /* ... */ }
function getOrder(id: OrderId): Order { /* ... */ }

const userId = createUserId('user-123');
const orderId = createOrderId('order-456');

getUser(userId);  // OK
getUser(orderId); // Error: OrderId not assignable to UserId
```

---

## Templates

### API Response Types

```typescript
// Base response structure
type ApiResponse<T> = {
  success: true;
  data: T;
  meta?: {
    page: number;
    total: number;
  };
} | {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

// Type-safe API client
async function fetchApi<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return response.json();
}

// Usage
const result = await fetchApi<User[]>('/api/users');
if (result.success) {
  result.data.forEach(user => console.log(user.email));
} else {
  console.error(result.error.message);
}
```

### Event Handler Types

```typescript
// Define event map
interface EventMap {
  'user:created': { user: User };
  'user:updated': { user: User; changes: Partial<User> };
  'user:deleted': { userId: string };
}

// Type-safe event emitter
class TypedEventEmitter {
  private listeners = new Map<string, Set<Function>>();

  on<K extends keyof EventMap>(
    event: K,
    callback: (data: EventMap[K]) => void
  ): void {
    const set = this.listeners.get(event) ?? new Set();
    set.add(callback);
    this.listeners.set(event, set);
  }

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    this.listeners.get(event)?.forEach(cb => cb(data));
  }
}

// Usage
const emitter = new TypedEventEmitter();
emitter.on('user:created', ({ user }) => {
  console.log(user.email); // Fully typed
});
```

---

## Examples

### Zod Schema Integration

```typescript
import { z } from 'zod';

// Define schema
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  role: z.enum(['user', 'admin']),
});

// Infer type from schema
type User = z.infer<typeof userSchema>;

// Now schema and type are in sync
function createUser(input: unknown): User {
  return userSchema.parse(input);
}
```

### Builder Pattern with Types

```typescript
class QueryBuilder<T, Selected extends keyof T = never> {
  private fields: string[] = [];
  private conditions: string[] = [];

  select<K extends Exclude<keyof T, Selected>>(
    ...fields: K[]
  ): QueryBuilder<T, Selected | K> {
    this.fields.push(...(fields as string[]));
    return this as unknown as QueryBuilder<T, Selected | K>;
  }

  where(condition: Partial<T>): this {
    // Add conditions
    return this;
  }

  build(): { fields: (Selected)[]; sql: string } {
    return {
      fields: this.fields as Selected[],
      sql: `SELECT ${this.fields.join(', ')}`,
    };
  }
}

// Usage
const query = new QueryBuilder<User>()
  .select('id', 'email')
  .select('name')
  .where({ role: 'admin' })
  .build();
// query.fields is ('id' | 'email' | 'name')[]
```

---

## Common Mistakes

1. **Using `any` instead of `unknown`** - Use unknown for truly unknown types
2. **Type assertions without guards** - Validate before asserting
3. **Ignoring strict mode** - Enable all strict flags
4. **Over-engineering types** - Keep types simple when possible
5. **Not using const assertions** - Use `as const` for literal types

---

## Checklist

- [ ] Strict mode enabled in tsconfig.json
- [ ] No unnecessary type annotations
- [ ] Discriminated unions for state
- [ ] Type guards for unknown data
- [ ] Utility types used appropriately
- [ ] Generic constraints are specific
- [ ] No `any` types (use `unknown`)

---

## Next Steps

- M-JS-005: Testing with Jest/Vitest
- M-JS-002: React Patterns
- M-JS-008: Code Quality

---

*Methodology M-JS-004 v1.0*
