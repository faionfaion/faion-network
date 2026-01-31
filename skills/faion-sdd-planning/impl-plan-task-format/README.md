# Implementation Plan Task Format

## Task Definition

### Task Format v2.0

```markdown
### TASK-XXX: [Concise Title]

**Phase:** [Phase number]
**Wave:** [Wave number]

**Description:**
[2-3 sentences explaining what needs to be done]

**Traces to:**
- AD-X: [Architectural decision this implements]
- FR-X: [Requirement this satisfies]

**Depends on:** TASK-YYY [FS], TASK-ZZZ [SS] (or "None")

**Blocks:** TASK-AAA, TASK-BBB

**Complexity:** simple (1-2h) | normal (2-3h) | complex (3-4h)
**Context Estimate:** ~Xk tokens

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/path/file.ts` | [What this file does] |
| MODIFY | `src/path/existing.ts` | [What to add/change] |

**Technical Notes:**
[Implementation hints, patterns to follow, gotchas]

**Tests:**
- [ ] Unit: [Test description]
- [ ] Integration: [Test description]

**Recommended Skills:**
- faion-software-developer: [specific aspect]
```

---

## INVEST Validation

| Criterion | Question | ✅ Good | ❌ Bad |
|-----------|----------|---------|--------|
| **Independent** | Can be done without other incomplete tasks? | No code dependencies on pending tasks | Needs unfinished TASK-005 |
| **Negotiable** | Implementation details flexible? | "User can register" | "Use bcrypt version 5.1.0" |
| **Valuable** | Clear business value? | Enables user registration | Technical refactoring |
| **Estimable** | Effort estimate possible? | ~50k tokens, Medium complexity | "Some time" |
| **Small** | Completable within 100k context? | ~30k-80k tokens | 200k tokens |
| **Testable** | Acceptance criteria testable? | "Returns 201 status" | "Works correctly" |

---

## Task Examples

### Example 1: Simple Task

```markdown
### TASK-001: Create Users Database Table

**Phase:** 1
**Wave:** 1

**Description:**
Create PostgreSQL table to store user account data including email, hashed password, and profile information. Table must support future OAuth providers.

**Traces to:**
- AD-001: Use PostgreSQL for relational data
- FR-001: System must support user registration

**Depends on:** None

**Blocks:** TASK-003 (Registration handler), TASK-004 (Login handler)

**Complexity:** simple
**Context Estimate:** ~15k tokens

**Acceptance Criteria:**
- [ ] Table created with fields: id, email, password_hash, created_at, updated_at
- [ ] Email field has unique constraint
- [ ] Migration script runs successfully
- [ ] Rollback migration works

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `migrations/001_create_users.sql` | Database migration |

**Technical Notes:**
- Use UUID for id field
- Add index on email for fast lookups
- Password_hash uses bcrypt (see AD-003)

**Tests:**
- [ ] Unit: Migration runs without errors
- [ ] Unit: Rollback restores previous state
- [ ] Integration: Can insert and query user records

**Recommended Skills:**
- faion-software-developer: Database schema design
```

### Example 2: Normal Task

```markdown
### TASK-003: Implement User Registration Handler

**Phase:** 2
**Wave:** 2

**Description:**
Create API endpoint for user registration that validates input, hashes passwords, stores user in database, and returns JWT token. Must handle duplicate email gracefully.

**Traces to:**
- AD-002: REST API architecture
- FR-001: User registration with email/password

**Depends on:** TASK-001 [FS], TASK-002 [SS]

**Blocks:** TASK-005 (Registration tests)

**Complexity:** normal
**Context Estimate:** ~45k tokens

**Acceptance Criteria:**
- [ ] POST /api/auth/register endpoint created
- [ ] Validates email format and password strength
- [ ] Returns 400 for invalid input
- [ ] Returns 409 for duplicate email
- [ ] Returns 201 with JWT token on success
- [ ] Password is bcrypt hashed before storage

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/handlers/auth/register.ts` | Registration logic |
| MODIFY | `src/routes/auth.ts` | Add route |
| MODIFY | `src/middleware/validation.ts` | Add validators |

**Technical Notes:**
- Use Joi for validation (see constitution.md)
- JWT secret from environment variable
- Return user_id in token payload
- Log registration attempts for monitoring

**Tests:**
- [ ] Unit: Validates email format correctly
- [ ] Unit: Rejects weak passwords
- [ ] Integration: Creates user in database
- [ ] Integration: Returns valid JWT token
- [ ] Integration: Handles duplicate email

**Recommended Skills:**
- faion-software-developer: API development, validation
```

### Example 3: Complex Task

```markdown
### TASK-007: End-to-End Authentication Flow Tests

**Phase:** 3
**Wave:** 4

**Description:**
Create comprehensive E2E test suite covering registration, login, token refresh, and protected resource access. Tests must run in CI/CD pipeline and verify all authentication flows work together.

**Traces to:**
- FR-001: User registration
- FR-002: User login
- FR-003: Protected resources

**Depends on:** TASK-005 [FS], TASK-006 [FS]

**Blocks:** None (final task)

**Complexity:** complex
**Context Estimate:** ~75k tokens

**Acceptance Criteria:**
- [ ] Test registers new user successfully
- [ ] Test logs in with correct credentials
- [ ] Test rejects wrong password
- [ ] Test accesses protected endpoint with valid token
- [ ] Test denies access with invalid token
- [ ] Test refreshes token before expiry
- [ ] All tests run in under 30 seconds
- [ ] Tests pass in CI/CD pipeline

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `tests/e2e/auth-flow.spec.ts` | E2E test suite |
| MODIFY | `.github/workflows/ci.yml` | Add E2E tests to CI |
| CREATE | `tests/fixtures/test-users.ts` | Test data |

**Technical Notes:**
- Use Playwright for E2E testing
- Create test database before each run
- Clean up test data after suite
- Mock external services (email, etc)
- Run tests in parallel where possible

**Tests:**
- [ ] E2E: Full registration flow
- [ ] E2E: Full login flow
- [ ] E2E: Token refresh flow
- [ ] E2E: Protected resource access
- [ ] E2E: Error handling paths

**Recommended Skills:**
- faion-software-developer: E2E testing, test automation
```

---

## Critical Path

Longest chain of dependent tasks.

### Structure

```markdown
## Critical Path

```
TASK-001 → TASK-003 → TASK-005 → TASK-007
  15k        45k        30k        75k     = ~165k tokens (split into 2 waves)
```

**Critical Path Complexity:** High

**Implications:**
- Cannot finish feature faster than critical path completion
- TASK-001, TASK-003, TASK-005, TASK-007 have no slack
- Delays on critical path delay the entire feature
- Consider parallelization where possible
```

### Critical Path Visualization

```
Critical Path (longest dependency chain):

TASK-001 (15k)  →  TASK-003 (45k)  →  TASK-005 (30k)  →  TASK-007 (75k)
Users Table        Registration        Reg Tests         E2E Tests

Parallel Paths:

TASK-002 (20k)  →  TASK-004 (40k)  →  TASK-006 (35k)  →  [joins TASK-007]
Password Utils     Login Handler       Login Tests
```

---

## Dependency Types Reference

| Type | Name | Meaning | Example |
|------|------|---------|---------|
| **FS** | Finish-to-Start | Most common. Task B starts when Task A finishes | Database migration [FS] API handler |
| **SS** | Start-to-Start | Task B can start when Task A starts | UI mockup [SS] Frontend implementation |
| **FF** | Finish-to-Finish | Task B finishes when Task A finishes | Testing [FF] Documentation |
| **SF** | Start-to-Finish | Task B finishes when Task A starts (rare) | Old system [SF] New system migration |

---

## Task Complexity Guidelines

| Complexity | Context | Characteristics | Example |
|------------|---------|----------------|---------|
| **simple** | 10k-30k tokens | Single file, clear pattern, minimal dependencies | Database migration, utility function |
| **normal** | 30k-60k tokens | Multiple files, some integration, standard patterns | API endpoint, service class |
| **complex** | 60k-100k tokens | Multiple components, integration logic, edge cases | E2E tests, complex business logic |

**Rule:** If task exceeds 100k tokens, split into multiple tasks.

---

## Acceptance Criteria Best Practices

### ✅ Good Acceptance Criteria

```markdown
**Acceptance Criteria:**
- [ ] POST /api/auth/register returns 201 on success
- [ ] Response includes valid JWT token (verified with jwt.verify)
- [ ] Password is bcrypt hashed in database (SELECT query confirms)
- [ ] Duplicate email returns 409 with error message
- [ ] Invalid email format returns 400 with validation errors
```

**Why good:**
- Specific and measurable
- Testable with code
- Clear pass/fail conditions
- Observable outcomes

### ❌ Bad Acceptance Criteria

```markdown
**Acceptance Criteria:**
- [ ] Registration works correctly
- [ ] Handles errors properly
- [ ] Follows best practices
- [ ] Code is clean
```

**Why bad:**
- Vague and subjective
- Not measurable
- No clear test procedure
- Multiple interpretations possible

---

## File Actions

| Action | When to Use | Example |
|--------|-------------|---------|
| **CREATE** | New file needed | `CREATE src/handlers/auth/register.ts` |
| **MODIFY** | Add to existing file | `MODIFY src/routes/auth.ts - Add registration route` |
| **DELETE** | Remove file | `DELETE src/deprecated/old-auth.ts` |
| **RENAME** | Change file path | `RENAME src/utils/hash.ts → src/utils/crypto.ts` |

---

## Technical Notes Guidelines

Use Technical Notes section for:

1. **Implementation patterns**: "Use Joi for validation (see constitution.md)"
2. **Gotchas**: "JWT secret must be 256-bit for HS256"
3. **References**: "Follow error handling pattern from AD-007"
4. **Performance hints**: "Use connection pooling for DB queries"
5. **Security notes**: "Never log passwords, even hashed"

**Keep notes actionable and specific.**

---

## Sources

- [INVEST Criteria](https://agileforall.com/new-to-agile-invest-in-good-user-stories/) - Bill Wake's INVEST principle
- [Acceptance Criteria Guide](https://www.visual-paradigm.com/scrum/write-acceptance-criteria-user-story/) - AC best practices
- [Given-When-Then](https://martinfowler.com/bliki/GivenWhenThen.html) - BDD format by Martin Fowler
- [Definition of Done](https://www.scrum.org/resources/blog/walking-through-definition-done) - Scrum.org guide
- [Task Breakdown Patterns](https://www.mountaingoatsoftware.com/blog/how-to-split-a-user-story) - Story splitting techniques
