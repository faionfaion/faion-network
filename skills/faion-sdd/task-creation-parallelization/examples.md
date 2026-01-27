# Task Decomposition Examples

Real-world examples of breaking down features into LLM-executable tasks.

---

## Example 1: Authentication Feature

### Bad Decomposition

```
TASK-001: Build authentication system (8 hours, 200k+ tokens)
```

**Problems:**
- Too large for single context window
- No clear success criteria
- Can't parallelize anything
- Can't track progress

### Good Decomposition

```
Wave 1 (No dependencies):
├── TASK-001: Create users table migration (simple, ~20k tokens)
├── TASK-002: Create sessions table migration (simple, ~15k tokens)
├── TASK-003: Implement password hashing utilities (normal, ~35k tokens)
└── TASK-004: Implement JWT utilities (normal, ~40k tokens)

Wave 2 (Depends on Wave 1):
├── TASK-005: Create User model with validation (normal, ~45k tokens)
│   └── Depends: TASK-001, TASK-003
└── TASK-006: Create Session model (simple, ~25k tokens)
    └── Depends: TASK-002, TASK-004

Wave 3 (Depends on Wave 2):
├── TASK-007: Implement register endpoint (normal, ~50k tokens)
│   └── Depends: TASK-005
├── TASK-008: Implement login endpoint (normal, ~50k tokens)
│   └── Depends: TASK-005, TASK-006
└── TASK-009: Implement logout endpoint (simple, ~30k tokens)
    └── Depends: TASK-006

Wave 4 (Depends on Wave 3):
├── TASK-010: Implement auth middleware (normal, ~45k tokens)
│   └── Depends: TASK-007, TASK-008
├── TASK-011: Write unit tests (normal, ~50k tokens)
│   └── Depends: TASK-007, TASK-008, TASK-009
└── TASK-012: Write integration tests (normal, ~55k tokens)
    └── Depends: TASK-010
```

**Dependency Graph:**

```
TASK-001 ─────────────────────────────┐
    │                                 │
TASK-002 ──────────────────────────┐  │
    │                              │  │
TASK-003 ──→ TASK-005 ──→ TASK-007 ┼──┼──→ TASK-010 ──→ TASK-012
    │            │           │     │  │        │
TASK-004 ──→ TASK-006 ──→ TASK-008 ┘  │        │
                 │           │        │        │
                 └──→ TASK-009 ───────┴────→ TASK-011
```

**Parallelization:**
- Wave 1: 4 tasks in parallel
- Wave 2: 2 tasks in parallel
- Wave 3: 3 tasks in parallel
- Wave 4: 3 tasks in parallel

**Result:** 22k tokens of work, minimum ~150k token path (critical path through TASK-001 -> TASK-005 -> TASK-007 -> TASK-010 -> TASK-012)

---

## Example 2: TASK-005 Full Definition

Complete task file showing proper context and traceability.

```markdown
# TASK_005: Create User Model with Validation

## Metadata

| Field | Value |
|-------|-------|
| **Complexity** | normal |
| **Est. Tokens** | ~45k |
| **Priority** | P1 |
| **Created** | 2026-01-25 |
| **Feature** | feature-027-auth |

---

## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Python standards |
| Spec | `.aidocs/todo/feature-027-auth/spec.md` | FR-1, FR-2 |
| Design | `.aidocs/todo/feature-027-auth/design.md` | AD-1, AD-3 |

## Task Dependency Tree

**This task depends on:**

```
TASK-001 (Create users table migration) ───────┐
    Status: DONE                               │
    Summary: Created users table with columns: │
      - id (UUID, PK)                          │
      - email (VARCHAR, unique)                │
      - password_hash (VARCHAR)                │
      - created_at (TIMESTAMP)                 │
      - updated_at (TIMESTAMP)                 │
    Files: migrations/001_create_users.py      │
    Patterns: AlembicMigration base class      │
    Key code:                                  │
    ```python                                  │
    op.create_table(                           ↓
        'users',                          TASK-005
        sa.Column('id', UUID, primary_key=True),  (THIS TASK)
        ...                                    ↑
    )                                          │
    ```                                        │
                                               │
TASK-003 (Password hashing utilities) ─────────┘
    Status: DONE
    Summary: Created password hashing with bcrypt
    Files: utils/password.py
    Patterns:
      - hash_password(plain: str) -> str
      - verify_password(plain: str, hashed: str) -> bool
    Key code:
    ```python
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()
    ```
```

**Dependency files to read:**
- `.aidocs/done/TASK_001_create_users_table.md` -> Summary
- `.aidocs/done/TASK_003_password_hashing.md` -> Summary

## Recommended Skills & Methodologies

**Skills:**
| Skill | Purpose |
|-------|---------|
| faion-python-developer | Django/Pydantic patterns |
| faion-testing-developer | Unit test structure |

**Methodologies:**
| ID | Name | Purpose |
|----|------|---------|
| python-best-practices | Python Standards | Code style, typing |
| pydantic-validation | Pydantic Patterns | Model validation |

---

## Requirements Coverage

### FR-1: User Registration
The system shall allow users to create accounts with email and password.
- Email must be unique in the system
- Password must be at least 8 characters

### FR-2: User Authentication
The system shall verify user credentials during login.
- Compare provided password against stored hash
- Return appropriate error for invalid credentials

## Architecture Decisions

### AD-1: Pydantic for Validation
Use Pydantic models for request/response validation with automatic error messages.

### AD-3: UUID for Primary Keys
Use UUIDs instead of auto-increment integers for security and distributed systems compatibility.

---

## Description

Create the User model class that maps to the users database table.
Implement Pydantic validators for email format and password strength.
Follow patterns established in TASK-003 for password hashing integration.

**Business value:** Enables user registration and authentication (core feature).

---

## Context

### Related Files (from research)

| File | Purpose | Patterns to Follow |
|------|---------|-------------------|
| `models/base.py` | Base model class | Inherit from BaseModel |
| `utils/password.py` | Password utilities | Use hash_password() |
| `migrations/001_*.py` | Table structure | Match column names |

### Code Dependencies
- `pydantic` v2.x - Model validation
- `sqlalchemy` v2.x - ORM mapping
- `utils.password.hash_password` - Password hashing

---

## Goals

1. Create User model class with all database fields
2. Implement email validation (format + uniqueness check)
3. Implement password validation (min 8 chars, complexity)
4. Add password hashing on create/update
5. Add timestamps (created_at, updated_at) auto-management

---

## Acceptance Criteria

**AC-1: Valid user creation**
- Given: Valid email "test@example.com" and password "SecurePass123"
- When: User.create(email, password) is called
- Then: User record created with hashed password, UUID id, timestamps

**AC-2: Invalid email rejection**
- Given: Invalid email "not-an-email" and valid password
- When: User.create(email, password) is called
- Then: ValidationError with message "Invalid email format"

**AC-3: Weak password rejection**
- Given: Valid email and weak password "123"
- When: User.create(email, password) is called
- Then: ValidationError with message "Password must be at least 8 characters"

**AC-4: Duplicate email rejection**
- Given: Existing user with email "existing@example.com"
- When: User.create("existing@example.com", password) is called
- Then: ValidationError with message "Email already exists"

**AC-5: Password never stored in plain text**
- Given: Any user creation or update
- When: Database is queried
- Then: password_hash field contains bcrypt hash, not plain password

---

## Dependencies

**Depends on (FS):**
- TASK-001 [FS] - Users table must exist
- TASK-003 [FS] - Password utilities needed

**Blocks:**
- TASK-007 - Register endpoint needs User model
- TASK-008 - Login endpoint needs User model

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | `models/user.py` | User model class |
| MODIFY | `models/__init__.py` | Export User |
| CREATE | `tests/unit/test_user_model.py` | Unit tests |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Email validation edge cases | Medium | Low | Use email-validator library |
| Hash timing attacks | Low | Medium | Use constant-time comparison |

## Potential Blockers
- [ ] None identified

---

## Out of Scope

- User profile fields (name, avatar) - separate task
- Email verification flow - separate feature
- Password reset - separate feature
- OAuth/social login - separate feature

---

## Testing

| Type | Description | File |
|------|-------------|------|
| Unit | Model creation, validation, hashing | `tests/unit/test_user_model.py` |

**Test commands:**
```bash
pytest tests/unit/test_user_model.py -v
```

---

## Estimated Context

| Phase | Tokens | Notes |
|-------|--------|-------|
| SDD Docs | ~5k | constitution, spec, design |
| Dependency Tree | ~5k | TASK-001, TASK-003 summaries |
| Research | ~10k | existing models, patterns |
| Implementation | ~20k | model + validators |
| Testing | ~5k | unit tests |
| **Total** | ~45k | Within budget |

---

## Subtasks

- [ ] 01. Research: Review existing models/base.py patterns
- [ ] 02. Implement: Create User model class
- [ ] 03. Implement: Add Pydantic validators
- [ ] 04. Implement: Integrate password hashing
- [ ] 05. Test: Write unit tests
- [ ] 06. Verify: Run all AC scenarios

---

## Implementation
<!-- Filled by executor during execution -->

---

## Summary
<!-- Filled after completion -->
```

---

## Example 3: API Feature with Frontend

### Feature: Product Search

**Context:** E-commerce app needs product search with filters, pagination, and real-time suggestions.

### Decomposition

```
Wave 1 - Backend Foundation:
├── TASK-001: Create products table migration
├── TASK-002: Create product_categories table migration
└── TASK-003: Seed sample product data

Wave 2 - Backend Models:
├── TASK-004: Create Product model
│   └── Depends: TASK-001, TASK-002
└── TASK-005: Create Category model
    └── Depends: TASK-002

Wave 3 - Backend API:
├── TASK-006: Implement search endpoint with filters
│   └── Depends: TASK-004, TASK-005
├── TASK-007: Implement suggestions endpoint
│   └── Depends: TASK-004
└── TASK-008: Add pagination utilities
    └── Depends: TASK-006

Wave 4 - Frontend Foundation:
├── TASK-009: Create SearchInput component
├── TASK-010: Create ProductCard component
└── TASK-011: Create FilterSidebar component

Wave 5 - Frontend Integration:
├── TASK-012: Implement search results page
│   └── Depends: TASK-006, TASK-009, TASK-010, TASK-011
├── TASK-013: Implement real-time suggestions
│   └── Depends: TASK-007, TASK-009
└── TASK-014: Implement pagination UI
    └── Depends: TASK-008, TASK-012

Wave 6 - Testing & Polish:
├── TASK-015: E2E tests for search flow
│   └── Depends: TASK-012, TASK-013, TASK-014
└── TASK-016: Performance optimization
    └── Depends: TASK-015
```

**Key Insight:** Waves 1-3 (backend) and Waves 4 (frontend foundation) can run in parallel since frontend components don't depend on backend initially.

**Parallel Execution Plan:**

```
Stream A (Backend):     TASK-001 → TASK-004 → TASK-006 → TASK-008
Stream B (Backend):     TASK-002 → TASK-005 → TASK-007
Stream C (Frontend):    TASK-009 → TASK-012 → TASK-015
Stream D (Frontend):    TASK-010 → (merge into TASK-012)
Stream E (Frontend):    TASK-011 → (merge into TASK-012)
```

---

## Example 4: Refactoring Task

### Feature: Migrate from REST to GraphQL

**Challenge:** Can't do big-bang migration; need incremental approach.

### Decomposition Strategy: Strangler Pattern

```
Wave 1 - Setup:
├── TASK-001: Add GraphQL dependencies and config
├── TASK-002: Create base schema structure
└── TASK-003: Set up GraphQL playground

Wave 2 - Read Operations:
├── TASK-004: Migrate GET /users to users query
├── TASK-005: Migrate GET /products to products query
└── TASK-006: Migrate GET /orders to orders query

Wave 3 - Write Operations:
├── TASK-007: Migrate POST /users to createUser mutation
├── TASK-008: Migrate POST /orders to createOrder mutation
└── TASK-009: Add subscription for order updates

Wave 4 - Frontend Migration:
├── TASK-010: Update user list to use GraphQL
├── TASK-011: Update product catalog to use GraphQL
└── TASK-012: Update order creation to use GraphQL

Wave 5 - Cleanup:
├── TASK-013: Add deprecation warnings to REST endpoints
├── TASK-014: Update API documentation
└── TASK-015: Remove old REST endpoints (after monitoring)
```

**Key Pattern:** Each wave is independently deployable and testable. Old REST endpoints remain until new GraphQL equivalents are proven.

---

## Example 5: Complex Wave with Decision Point

### Feature: Payment Integration

Some tasks need research before decomposition is possible.

### Initial Decomposition (Waves 1-2):

```
Wave 1 - Research (MUST complete before Wave 2 planning):
├── TASK-001: Research Stripe vs PayPal integration
│   Deliverable: ADR document with recommendation
└── TASK-002: Research PCI compliance requirements
    Deliverable: Compliance checklist

Wave 2 - Foundation (created AFTER Wave 1):
├── TASK-003: Set up payment provider SDK
├── TASK-004: Create payment_methods table
└── TASK-005: Create transactions table
```

**Decision Point:** Wave 2 tasks depend on Wave 1 decisions. Don't pre-create Wave 2+ tasks until Wave 1 research completes.

**Task-001 triggers task creation:**
```markdown
## Summary (filled after completion)

**Decision:** Use Stripe
**Rationale:** Better API documentation, lower fees, built-in fraud detection

**Next tasks to create:**
- TASK-003: Set up Stripe SDK (not generic "payment provider")
- TASK-004: Create stripe_customers table (Stripe-specific schema)
- TASK-005: Create stripe_transactions table
```

---

## Anti-Patterns to Avoid

### 1. The Monolith Task

```
BAD:
TASK-001: Build the entire feature

GOOD:
TASK-001: Create database schema
TASK-002: Create data models
TASK-003: Create API endpoints
TASK-004: Create frontend components
TASK-005: Write tests
```

### 2. The Micro-Task

```
BAD:
TASK-001: Add import statement
TASK-002: Define function signature
TASK-003: Implement function body
TASK-004: Add return statement

GOOD:
TASK-001: Implement utility function with tests
```

### 3. The Circular Dependency

```
BAD:
TASK-001: Create User model (depends on TASK-002)
TASK-002: Create UserService (depends on TASK-001)

GOOD:
TASK-001: Create User model
TASK-002: Create UserService (depends on TASK-001)
```

### 4. The Missing Context

```
BAD:
TASK-005: Create register endpoint

GOOD:
TASK-005: Create register endpoint
  - Dependency Tree: TASK-003 (User model), TASK-004 (Password utils)
  - Patterns: Follow existing health endpoint structure
  - Key code snippets from dependencies
```

### 5. The Vague Acceptance Criteria

```
BAD:
AC-1: Registration should work

GOOD:
AC-1: Successful registration
- Given: Valid email "test@example.com" and password "SecurePass123"
- When: POST /api/register is called with these credentials
- Then: 201 response with user ID, email verified = false
```

---

*Examples v3.0.0 | Real-world decomposition patterns*
