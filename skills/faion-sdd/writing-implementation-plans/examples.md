# Implementation Plan Examples

Real-world examples demonstrating implementation plan patterns.

---

## Example 1: User Authentication Feature

### Context
- Feature: User registration and login
- Complexity: Normal (4 waves, 7 tasks)
- Total tokens: ~175k

### Dependency Graph

```
TASK-001 (User Schema)
    |
    +--[FS]---> TASK-003 (Registration API)
    |               |
    |               +--[FS]---> TASK-005 (Registration Tests)
    |
    +--[FS]---> TASK-004 (Login API)
                    |
                    +--[FS]---> TASK-006 (Login Tests)

TASK-002 (Password Utils) --[SS]---> TASK-003
                          --[SS]---> TASK-004

                                           TASK-007 (E2E Tests)
                                               ^
                                               |
                                    [TASK-005, TASK-006]
```

### Wave Analysis

| Wave | Tasks | Token Load | Description |
|------|-------|------------|-------------|
| 1 | TASK-001, TASK-002 | ~45k | Foundation |
| 2 | TASK-003, TASK-004 | ~80k | API endpoints |
| 3 | TASK-005, TASK-006 | ~40k | Unit/Integration tests |
| 4 | TASK-007 | ~25k | E2E tests |

### Critical Path

```
TASK-001 --> TASK-003 --> TASK-005 --> TASK-007
  20k          45k          20k          25k    = ~110k tokens
```

### Task Breakdown

#### TASK-001: Create User Database Schema

**Wave:** 1
**Complexity:** simple
**Tokens:** ~20k

**Description:**
Create PostgreSQL migration for users table with email, password_hash, and timestamps. Include unique constraint on email and index for login queries.

**Traces to:**
- AD-001: PostgreSQL for data storage
- FR-001: Users can create accounts

**Depends on:** None
**Blocks:** TASK-003, TASK-004

**Acceptance Criteria:**
- [ ] Migration creates users table with all required columns
- [ ] Email column has unique constraint
- [ ] Rollback migration drops table cleanly
- [ ] Migration passes in test environment

**Files:**
| Action | File |
|--------|------|
| CREATE | `migrations/001_create_users_table.sql` |
| MODIFY | `src/db/schema.ts` | Add User type |

**Tests:**
- [ ] Migration applies successfully
- [ ] Rollback works correctly

---

#### TASK-002: Implement Password Utilities

**Wave:** 1
**Complexity:** simple
**Tokens:** ~25k

**Description:**
Create utility module for password hashing (bcrypt) and verification. Include strength validation with configurable rules.

**Traces to:**
- AD-002: bcrypt for password hashing
- FR-002: Passwords stored securely

**Depends on:** None
**Blocks:** TASK-003, TASK-004

**Acceptance Criteria:**
- [ ] hashPassword() returns bcrypt hash
- [ ] verifyPassword() correctly validates
- [ ] Password strength validation works
- [ ] Unit tests cover all functions

**Files:**
| Action | File |
|--------|------|
| CREATE | `src/utils/password.ts` |
| CREATE | `src/utils/__tests__/password.test.ts` |

---

#### TASK-003: Create Registration API Endpoint

**Wave:** 2
**Complexity:** normal
**Tokens:** ~45k

**Description:**
Implement POST /api/auth/register endpoint. Validate input, check email uniqueness, hash password, create user, return JWT token.

**Traces to:**
- AD-003: REST API with JWT auth
- FR-001: Users can create accounts

**Depends on:** TASK-001 [FS], TASK-002 [SS]
**Blocks:** TASK-005, TASK-007

**Acceptance Criteria:**
- [ ] POST /api/auth/register creates new user
- [ ] Returns 201 with JWT token on success
- [ ] Returns 400 for invalid input
- [ ] Returns 409 for duplicate email
- [ ] Password is hashed before storage

**Files:**
| Action | File |
|--------|------|
| CREATE | `src/routes/auth/register.ts` |
| CREATE | `src/validators/auth.ts` |
| MODIFY | `src/routes/index.ts` | Add register route |

---

#### TASK-004: Create Login API Endpoint

**Wave:** 2
**Complexity:** normal
**Tokens:** ~35k

**Description:**
Implement POST /api/auth/login endpoint. Validate credentials, verify password, return JWT token.

**Traces to:**
- AD-003: REST API with JWT auth
- FR-003: Users can log in

**Depends on:** TASK-001 [FS], TASK-002 [SS]
**Blocks:** TASK-006, TASK-007

**Acceptance Criteria:**
- [ ] POST /api/auth/login authenticates user
- [ ] Returns 200 with JWT token on success
- [ ] Returns 400 for invalid input
- [ ] Returns 401 for wrong credentials
- [ ] Does not reveal whether email exists

**Files:**
| Action | File |
|--------|------|
| CREATE | `src/routes/auth/login.ts` |
| MODIFY | `src/routes/index.ts` | Add login route |

---

## Example 2: API Rate Limiting

### Context
- Feature: Request rate limiting per user/IP
- Complexity: Simple (3 waves, 5 tasks)
- Total tokens: ~100k

### Dependency Graph

```
TASK-001 (Redis Setup)
    |
    +--[FS]---> TASK-002 (Rate Limiter Service)
                    |
                    +--[FS]---> TASK-003 (Middleware)
                                    |
                                    +--[FS]---> TASK-004 (Tests)

TASK-005 (Config) --[SS]---> TASK-002
```

### Wave Analysis

| Wave | Tasks | Token Load |
|------|-------|------------|
| 1 | TASK-001, TASK-005 | ~30k |
| 2 | TASK-002, TASK-003 | ~50k |
| 3 | TASK-004 | ~20k |

### Task Breakdown (Compact Format)

**TASK-001: Configure Redis Connection**
- Wave: 1, Tokens: ~15k
- Depends: None, Blocks: TASK-002
- AC: Redis client connects, health check passes

**TASK-005: Add Rate Limit Configuration**
- Wave: 1, Tokens: ~15k
- Depends: None, Blocks: TASK-002
- AC: Config has limits per tier, validates on load

**TASK-002: Implement Rate Limiter Service**
- Wave: 2, Tokens: ~30k
- Depends: TASK-001 [FS], TASK-005 [SS]
- AC: Sliding window algorithm, returns remaining quota

**TASK-003: Create Rate Limit Middleware**
- Wave: 2, Tokens: ~20k
- Depends: TASK-002 [FS]
- AC: Blocks when limit exceeded, adds headers

**TASK-004: Write Rate Limiter Tests**
- Wave: 3, Tokens: ~20k
- Depends: TASK-003 [FS]
- AC: 90% coverage, tests window sliding

---

## Example 3: Complex Feature - Payment Processing

### Context
- Feature: Stripe integration for subscriptions
- Complexity: Complex (6 waves, 12 tasks)
- Total tokens: ~400k

### Dependency Graph (Simplified)

```
Wave 1: Foundation
  TASK-001 (Stripe SDK) ----+
  TASK-002 (Subscriptions table) -+---> Wave 2
  TASK-003 (Config) --------+

Wave 2: Core Services
  TASK-004 (Customer Service) ----+
  TASK-005 (Subscription Service) +---> Wave 3

Wave 3: Webhooks & API
  TASK-006 (Webhook Handler) ----+
  TASK-007 (Create Subscription API) +---> Wave 4
  TASK-008 (Cancel Subscription API) +

Wave 4: User-Facing
  TASK-009 (Checkout Flow) ----+
  TASK-010 (Billing Portal) ---+---> Wave 5

Wave 5: Testing
  TASK-011 (Integration Tests) +---> Wave 6

Wave 6: E2E
  TASK-012 (E2E Payment Flow)
```

### Wave Analysis

| Wave | Tasks | Token Load | Risk |
|------|-------|------------|------|
| 1 | 001, 002, 003 | ~60k | Low |
| 2 | 004, 005 | ~70k | Medium |
| 3 | 006, 007, 008 | ~90k | High (webhooks) |
| 4 | 009, 010 | ~70k | Medium |
| 5 | 011 | ~50k | Low |
| 6 | 012 | ~60k | Medium |

### Critical Path

```
TASK-002 --> TASK-005 --> TASK-007 --> TASK-009 --> TASK-011 --> TASK-012
  25k          35k          30k          35k          50k          60k

Total: ~235k tokens (critical path)
```

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Stripe API changes | Low | High | Pin SDK version, monitor changelog |
| Webhook delivery | Medium | High | Implement retry queue |
| Test card limits | Medium | Low | Use Stripe test clock |
| PCI compliance | Low | Critical | Use Stripe Elements only |

### Key Task Example

#### TASK-006: Implement Stripe Webhook Handler

**Wave:** 3
**Complexity:** complex
**Tokens:** ~40k

**Description:**
Create webhook endpoint for Stripe events. Handle customer.subscription.created, updated, deleted events. Verify webhook signatures, process idempotently.

**Traces to:**
- AD-008: Webhook-based event processing
- FR-010: Subscription status syncs with Stripe

**Depends on:** TASK-004 [FS], TASK-005 [FS]
**Blocks:** TASK-011, TASK-012

**Acceptance Criteria:**
- [ ] POST /webhooks/stripe receives events
- [ ] Signature verification rejects invalid requests
- [ ] Processes subscription events correctly
- [ ] Idempotent (handles duplicates)
- [ ] Returns 200 within 5 seconds
- [ ] Logs all events for debugging

**Files:**
| Action | File |
|--------|------|
| CREATE | `src/webhooks/stripe/handler.ts` |
| CREATE | `src/webhooks/stripe/events/subscription.ts` |
| CREATE | `src/webhooks/stripe/verify.ts` |
| MODIFY | `src/routes/index.ts` | Add webhook route |

**Technical Notes:**
- Use raw body for signature verification
- Queue processing for slow operations
- Add Stripe-Signature header validation
- Implement event deduplication with Redis

---

## Example 4: Token Estimation Breakdown

### Detailed Token Calculation

**Task: Create REST API Endpoint**

| Component | Tokens | Notes |
|-----------|--------|-------|
| Task file reading | ~2k | Task definition, AC, deps |
| Design doc reading | ~5k | Relevant AD-X sections |
| Related code reading | ~10k | Similar endpoints, patterns |
| Type definitions | ~3k | Request/response types |
| Validation logic | ~3k | Input validation |
| Handler implementation | ~5k | Core business logic |
| Error handling | ~2k | Error responses |
| Tests writing | ~8k | Unit + integration tests |
| Documentation | ~2k | JSDoc, API docs |
| **Total** | **~40k** | Normal complexity |

### Estimation Heuristics

| Task Type | Base Tokens | Per-File Modifier | Test Modifier |
|-----------|-------------|-------------------|---------------|
| Create file | 15k | +5k per additional | +8k if tests |
| Modify file | 20k | +3k per additional | +5k if tests |
| API endpoint | 35k | +5k per endpoint | +10k with integration |
| Database migration | 15k | +3k per table | +5k for rollback |
| Complex refactor | 50k | +10k per system | +15k regression tests |

---

## Example 5: Wave-Based Task Creation

### Progressive Task Creation Pattern

**Principle:** Create detailed TASK files in waves, not all at once.

**Wave 1 - Created Initially:**

```markdown
# TASK_001: Create Users Table

[Full task definition with all details]
---

# TASK_002: Implement Password Utils

[Full task definition with all details]
```

**After Wave 1 Execution - Learnings Applied to Wave 2:**

```markdown
# TASK_003: Create Registration API

[Updated based on patterns discovered in Wave 1]

**Technical Notes:**
- Use User type from src/db/schema.ts (created in TASK-001)
- Follow password hashing pattern from TASK-002
- See src/utils/password.ts for validation approach
```

**Benefits of Progressive Creation:**
1. Later tasks incorporate learnings from earlier waves
2. Patterns discovered early are documented and reused
3. Better context from completed dependency tasks
4. Reduced rework from early discoveries
5. More accurate token estimates based on actual execution

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Monolithic Task

```markdown
# TASK-001: Implement Authentication System

**Complexity:** complex
**Tokens:** ~350k  # TOO LARGE!

**Description:**
Create user registration, login, password reset, JWT handling,
refresh tokens, and session management.

**Files:**
| Action | File |
|--------|------|
| CREATE | 15+ files |  # TOO MANY FILES
```

**Fix:** Split into 7-10 smaller tasks with clear dependencies.

---

### Anti-Pattern 2: Missing Dependencies

```markdown
# TASK-003: Create API Handler

**Depends on:** None  # WRONG - needs schema!

# TASK-001: Create Database Schema

**Blocks:** [not listed]  # WRONG - should list TASK-003
```

**Fix:** Explicitly map all dependencies in both directions.

---

### Anti-Pattern 3: Vague Acceptance Criteria

```markdown
**Acceptance Criteria:**
- [ ] Works correctly  # TOO VAGUE
- [ ] Handles errors properly  # NOT TESTABLE
- [ ] Is fast enough  # NO THRESHOLD
```

**Fix:**
```markdown
**Acceptance Criteria:**
- [ ] Returns 201 with user object on success
- [ ] Returns 400 with validation errors for invalid email
- [ ] Response time < 200ms for registration request
```

---

### Anti-Pattern 4: No Token Estimates

```markdown
# TASK-001: Big Feature

**Complexity:** complex
**Tokens:** TBD  # MISSING!
```

**Fix:** Always estimate tokens based on files, complexity, and testing requirements.

---

*Examples | SDD Foundation | Version 3.0.0*
