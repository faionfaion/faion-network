# TypeScript Patterns

**Advanced TypeScript patterns and type-safe practices**

---

## Strict Mode Benefits

```typescript
// strict: true enables all of these
{
  "noImplicitAny": true,        // No implicit any
  "strictNullChecks": true,      // null/undefined handling
  "strictFunctionTypes": true,   // Function param contravariance
  "strictBindCallApply": true,   // Correct bind/call/apply types
  "strictPropertyInitialization": true,  // Class property init
  "noImplicitThis": true,        // Explicit this types
  "alwaysStrict": true           // ES5 strict mode
}

// Additional strict options (enable manually)
{
  "noUncheckedIndexedAccess": true,  // Array access returns T | undefined
  "exactOptionalPropertyTypes": true, // undefined !== optional
  "noImplicitReturns": true          // All code paths must return
}
```

---

## Utility Types

```typescript
// Built-in utility types
type UserPartial = Partial<User>;           // All props optional
type UserRequired = Required<User>;         // All props required
type UserReadonly = Readonly<User>;         // All props readonly
type UserName = Pick<User, 'name' | 'email'>;
type UserWithoutPassword = Omit<User, 'password'>;
type IdType = User['id'];                   // Indexed access
type UserKeys = keyof User;                 // Union of keys
type StringUser = Record<string, User>;     // Index signature

// Creating precise types
type Status = 'pending' | 'active' | 'inactive';
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

// Template literal types
type EventName = `on${Capitalize<string>}`;  // 'onClick', 'onSubmit', etc.
type Endpoint = `/api/${string}`;

// Conditional types
type ArrayElement<T> = T extends (infer U)[] ? U : never;
type Awaited<T> = T extends Promise<infer U> ? U : T;
```

---

## Generic Patterns

```typescript
// Generic function with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic interface
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

// Generic React component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}
```

---

## Type Guards

```typescript
// Type predicate
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

// Discriminated union
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>): T {
  if (result.success) {
    return result.data;  // TypeScript knows data exists
  }
  throw result.error;    // TypeScript knows error exists
}

// Assertion function
function assertDefined<T>(
  value: T | null | undefined,
  message = 'Value is null or undefined',
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}
```

---

## Zod Schema Validation

```typescript
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
});

// Infer TypeScript type from schema
type User = z.infer<typeof UserSchema>;

// Create partial schema for updates
const UpdateUserSchema = UserSchema.partial().omit({ id: true });
type UpdateUserData = z.infer<typeof UpdateUserSchema>;

// Validation
function validateUser(data: unknown): User {
  return UserSchema.parse(data);  // Throws ZodError if invalid
}

function safeValidateUser(data: unknown): Result<User> {
  const result = UserSchema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, error: result.error };
}
```

---

## Sources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/) - Official TypeScript docs
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/) - Comprehensive guide
- [Zod](https://zod.dev/) - TypeScript-first schema validation
- [Type Challenges](https://github.com/type-challenges/type-challenges) - TypeScript exercises
- [Total TypeScript](https://www.totaltypescript.com/) - Advanced TypeScript patterns
