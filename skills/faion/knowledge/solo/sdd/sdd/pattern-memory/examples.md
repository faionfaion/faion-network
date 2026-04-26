# Pattern Examples

Real-world pattern examples organized by category.

## Code Patterns

### PAT-001: Async Error Boundary

**Category:** code/error-handling
**Language:** TypeScript
**Framework:** React
**Confidence:** 0.92

**Problem:**
Async operations can fail silently, causing poor UX or app crashes with unhandled promise rejections.

**Solution:**
Wrap async operations with try-catch and manage explicit error/loading states.

```typescript
function useAsyncOperation<T>(asyncFn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await asyncFn();
      setData(result);
      return result;
    } catch (e) {
      setError(e instanceof Error ? e : new Error(String(e)));
      throw e;
    } finally {
      setLoading(false);
    }
  }, [asyncFn]);

  return { data, error, loading, execute };
}
```

**When to Use:**
- API calls in React components
- Data fetching with useEffect
- Form submissions
- Any async operation requiring user feedback

**When NOT to Use:**
- Background operations (logging, analytics)
- Operations where errors are expected and handled upstream

**Provenance:** TASK_042, verified in TASK_055, TASK_067, TASK_089

---

### PAT-002: API Response Normalization

**Category:** code/api-design
**Language:** TypeScript
**Confidence:** 0.88

**Problem:**
Inconsistent API response formats make error handling and data extraction unpredictable.

**Solution:**
Normalize all API responses to a consistent envelope format.

```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  meta?: {
    timestamp: string;
    requestId: string;
  };
}

async function fetchApi<T>(url: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url);
    const json = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: {
          code: `HTTP_${response.status}`,
          message: json.message || response.statusText,
          details: json.errors
        },
        meta: { timestamp: new Date().toISOString(), requestId: json.requestId }
      };
    }

    return {
      success: true,
      data: json.data || json,
      meta: { timestamp: new Date().toISOString(), requestId: json.requestId }
    };
  } catch (e) {
    return {
      success: false,
      error: {
        code: 'NETWORK_ERROR',
        message: e instanceof Error ? e.message : 'Unknown error'
      },
      meta: { timestamp: new Date().toISOString(), requestId: 'unknown' }
    };
  }
}
```

**When to Use:**
- API client wrappers
- SDK development
- Microservice communication

**When NOT to Use:**
- Direct passthrough proxies
- Simple scripts with single API calls

---

### PAT-003: Retry with Exponential Backoff

**Category:** code/error-handling
**Language:** TypeScript
**Confidence:** 0.85

**Problem:**
Transient failures (network issues, rate limits) cause unnecessary errors when a retry would succeed.

**Solution:**
Implement retry logic with exponential backoff and jitter.

```typescript
interface RetryOptions {
  maxAttempts: number;
  baseDelay: number;
  maxDelay: number;
  retryableErrors?: string[];
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = { maxAttempts: 3, baseDelay: 1000, maxDelay: 10000 }
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= options.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e instanceof Error ? e : new Error(String(e));

      // Check if error is retryable
      if (options.retryableErrors &&
          !options.retryableErrors.some(code => lastError.message.includes(code))) {
        throw lastError;
      }

      if (attempt === options.maxAttempts) {
        throw lastError;
      }

      // Calculate delay with jitter
      const delay = Math.min(
        options.baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000,
        options.maxDelay
      );

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}
```

**When to Use:**
- External API calls
- Database connections
- Network operations
- Rate-limited services

**When NOT to Use:**
- User input validation (won't help)
- Deterministic errors (fix the code)
- Time-sensitive operations (user waiting)

---

## Architecture Patterns

### PAT-010: Repository Pattern

**Category:** architecture/structural
**Language:** TypeScript
**Confidence:** 0.90

**Problem:**
Direct database access in business logic creates tight coupling and makes testing difficult.

**Solution:**
Abstract data access behind a repository interface.

```typescript
// Interface
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<void>;
}

// Implementation
class PostgresUserRepository implements UserRepository {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.db.query('SELECT * FROM users WHERE id = $1', [id]);
    return row ? this.mapToUser(row) : null;
  }

  // ... other methods
}

// Test implementation
class InMemoryUserRepository implements UserRepository {
  private users: Map<string, User> = new Map();

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }

  // ... other methods
}
```

**When to Use:**
- Any application with database access
- When you need to test business logic in isolation
- When you might switch databases

**When NOT to Use:**
- Simple scripts
- One-off data migrations
- Prototypes (add later when stabilized)

---

### PAT-011: Event-Driven State Updates

**Category:** architecture/behavioral
**Language:** TypeScript
**Framework:** React
**Confidence:** 0.82

**Problem:**
Complex state updates across components lead to prop drilling or tangled dependencies.

**Solution:**
Use an event bus for cross-component communication.

```typescript
type EventHandler<T = unknown> = (payload: T) => void;

class EventBus {
  private handlers: Map<string, Set<EventHandler>> = new Map();

  on<T>(event: string, handler: EventHandler<T>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler as EventHandler);

    // Return unsubscribe function
    return () => this.handlers.get(event)?.delete(handler as EventHandler);
  }

  emit<T>(event: string, payload: T): void {
    this.handlers.get(event)?.forEach(handler => handler(payload));
  }
}

// Usage in React
const eventBus = new EventBus();

function useEvent<T>(event: string, handler: EventHandler<T>) {
  useEffect(() => {
    return eventBus.on(event, handler);
  }, [event, handler]);
}
```

**When to Use:**
- Cross-component notifications
- Decoupled feature modules
- Real-time updates

**When NOT to Use:**
- Simple parent-child communication
- Synchronous state updates
- When you need state persistence

---

## Workflow Patterns

### PAT-020: Wave-Based Task Execution

**Category:** workflow/execution
**Confidence:** 0.88

**Problem:**
Sequential task execution is slow when tasks don't have dependencies on each other.

**Solution:**
Group tasks into waves based on dependencies, execute each wave in parallel.

```markdown
## Wave Analysis

### Wave 1 (Parallel)
- TASK_001: Setup database schema
- TASK_002: Create API types
- TASK_003: Setup test framework

### Wave 2 (Parallel, depends on Wave 1)
- TASK_004: User repository (needs schema)
- TASK_005: Auth types (needs API types)

### Wave 3 (Parallel, depends on Wave 2)
- TASK_006: Auth endpoints (needs repo + types)
- TASK_007: User endpoints (needs repo + types)

### Wave 4 (Sequential, depends on Wave 3)
- TASK_008: Integration tests (needs all endpoints)
```

**Speedup:** 1.8-3.5x depending on parallelization depth

**When to Use:**
- Multi-task features
- Team projects with multiple developers
- CI/CD pipelines

**When NOT to Use:**
- Single sequential tasks
- Highly interdependent work
- Learning/exploration phases

---

### PAT-021: Progressive Confidence Validation

**Category:** workflow/planning
**Confidence:** 0.85

**Problem:**
Starting implementation without validating understanding leads to costly rework.

**Solution:**
Check confidence at each phase, don't proceed below threshold.

```markdown
## Confidence Checkpoints

### Before Spec
- [ ] Understand user need (>80%?)
- [ ] Know success criteria (>80%?)
- [ ] Aware of constraints (>70%?)

### Before Design
- [ ] Spec is complete (>90%?)
- [ ] Know implementation approach (>80%?)
- [ ] Identified risks (>70%?)

### Before Implementation
- [ ] Design is validated (>90%?)
- [ ] Know file changes needed (>85%?)
- [ ] Test approach clear (>80%?)

### Before Merge
- [ ] All tests pass (100%)
- [ ] Code reviewed (>90%?)
- [ ] Docs updated (>80%?)
```

**Threshold:** 90% overall confidence to proceed

**When to Use:**
- Any SDD workflow
- Complex features
- High-risk changes

**When NOT to Use:**
- Trivial fixes
- Exploratory prototyping
- Emergency hotfixes (but document debt)

---

## Anti-Patterns (from mistakes.md)

### ANTI-001: Premature Abstraction

**Problem:** Creating abstractions before understanding the variation points.

**Symptoms:**
- Abstract base class with only one implementation
- Interfaces that exactly match the single implementation
- Generic utilities used in only one place

**Solution:**
Wait for the "Rule of Three" - abstract after seeing the pattern three times.

---

### ANTI-002: Silent Error Swallowing

**Problem:** Catching exceptions without proper handling or logging.

```typescript
// BAD
try {
  await riskyOperation();
} catch (e) {
  // Silent failure
}

// GOOD
try {
  await riskyOperation();
} catch (e) {
  logger.error('Operation failed', { error: e, context });
  throw new OperationError('Failed to complete operation', { cause: e });
}
```

---

### ANTI-003: Over-Engineering Initial Implementation

**Problem:** Building for scale before validating the approach.

**Symptoms:**
- Microservices for a prototype
- Complex caching before measuring performance
- Extensive configuration for single use case

**Solution:**
Start simple, measure, then optimize. "Make it work, make it right, make it fast."
