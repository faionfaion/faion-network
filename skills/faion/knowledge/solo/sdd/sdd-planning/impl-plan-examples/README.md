# Implementation Plan Examples

## Example 1: Simple Feature (3 Tasks)

### Feature: Email Verification

**Total Context:** ~120k tokens
**Phases:** 2
**Waves:** 2

### Implementation Plan

```markdown
# Implementation Plan: Email Verification

## Overview

Add email verification to user registration flow. Users receive email with token, must verify before account activation.

**Estimated Effort:** 8 hours
**Critical Path:** 8 hours
**Waves:** 2
**Total Tasks:** 3

## Prerequisites

### Infrastructure
- [x] SMTP server configured (SendGrid)
- [x] Email templates engine exists

### Code Dependencies
- [x] User model exists
- [x] Registration flow implemented

## Dependency Graph

```
TASK-001 (Email service)
    │
    ├──[FS]──→ TASK-002 (Verification handler)
    │              │
    │              └──[FS]──→ TASK-003 (Tests)
```

## Wave Analysis

| Wave | Tasks | Parallel | Dependencies | Effort |
|------|-------|----------|--------------|--------|
| 1 | TASK-001 | No | None | 3h |
| 2 | TASK-002, TASK-003 | Yes | Wave 1 | 5h |

## Phases

| Phase | Description | Tasks | Effort |
|-------|-------------|-------|--------|
| 1 | Email Service | TASK-001 | 3h |
| 2 | Verification | TASK-002, TASK-003 | 5h |

## Phase 1: Email Service

### TASK-001: Create email verification service

**Wave:** 1
**Complexity:** normal
**Effort:** 3 hours
**Context:** ~40k tokens

**Description:**
Create service to generate verification tokens, send verification emails, and validate tokens. Use JWT for tokens with 24h expiry.

**Traces to:** AD-001 (Email verification), FR-003 (User activation)

**Depends on:** None
**Blocks:** TASK-002

**Acceptance Criteria:**
- [ ] generateToken() creates JWT with user ID and 24h expiry
- [ ] sendVerificationEmail() sends email via SendGrid
- [ ] validateToken() verifies JWT and returns user ID
- [ ] Tokens expire after 24 hours

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/services/emailVerification.ts` | Email verification logic |
| MODIFY | `src/services/email.ts` | Add verification template |

**Tests:**
- [ ] Unit: Token generation and validation
- [ ] Unit: Token expiry handling
- [ ] Integration: Email sending

## Phase 2: Verification

### TASK-002: Add verification endpoint

**Wave:** 2
**Complexity:** normal
**Effort:** 3 hours
**Context:** ~35k tokens

**Description:**
Create API endpoint to handle email verification. Accept token, validate, activate user account.

**Traces to:** AD-002 (Verification API), FR-003

**Depends on:** TASK-001 [FS]
**Blocks:** None

**Acceptance Criteria:**
- [ ] POST /api/verify-email endpoint exists
- [ ] Returns 200 on valid token
- [ ] Returns 400 on invalid/expired token
- [ ] Sets user.emailVerified = true
- [ ] Returns error if already verified

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/api/verify-email.ts` | Verification endpoint |
| MODIFY | `src/models/User.ts` | Add emailVerified field |

**Tests:**
- [ ] Integration: Successful verification
- [ ] Integration: Invalid token handling
- [ ] Integration: Expired token handling

### TASK-003: Add verification to registration

**Wave:** 2
**Complexity:** simple
**Effort:** 2 hours
**Context:** ~25k tokens

**Description:**
Modify registration flow to send verification email instead of immediately activating account. Block login for unverified users.

**Traces to:** FR-003

**Depends on:** TASK-001 [FS]
**Blocks:** None

**Acceptance Criteria:**
- [ ] Registration sends verification email
- [ ] User.emailVerified defaults to false
- [ ] Login blocked for unverified users
- [ ] Clear error message shown

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| MODIFY | `src/api/register.ts` | Send verification email |
| MODIFY | `src/api/login.ts` | Check verification status |

**Tests:**
- [ ] Integration: Registration sends email
- [ ] Integration: Unverified user cannot login
```

---

## Example 2: Medium Feature (7 Tasks)

### Feature: Payment System

**Total Context:** ~380k tokens
**Phases:** 3
**Waves:** 3

### Task List

```markdown
## Wave Analysis

| Wave | Tasks | Parallel | Dependencies | Effort |
|------|-------|----------|--------------|--------|
| 1 | TASK-001, TASK-002 | Yes | None | 5h |
| 2 | TASK-003, TASK-004 | Yes | Wave 1 | 6h |
| 3 | TASK-005, TASK-006, TASK-007 | Yes | Wave 2 | 7h |

## Phase 1: Infrastructure

### TASK-001: Payment database schema (30k tokens)
- Create payments table
- Create payment_methods table
- Add indexes and constraints

### TASK-002: Stripe integration service (45k tokens)
- Create Stripe client wrapper
- Implement payment intent creation
- Add webhook handling

## Phase 2: Core Logic

### TASK-003: Payment processing service (55k tokens)
- Create payment service
- Implement charge logic
- Add refund handling
- Error handling and retries

### TASK-004: Payment API endpoints (40k tokens)
- POST /api/payments/create
- POST /api/payments/:id/refund
- GET /api/payments/:id
- GET /api/payments (list)

## Phase 3: Testing & Integration

### TASK-005: Payment unit tests (35k tokens)
- Service tests
- API endpoint tests
- Mock Stripe responses

### TASK-006: Payment integration tests (45k tokens)
- End-to-end payment flow
- Webhook handling
- Refund flow

### TASK-007: Payment UI components (50k tokens)
- Payment form component
- Payment status display
- Payment history list
```

---

## Example 3: Complex Feature (12 Tasks)

### Feature: Multi-tenant Architecture

**Total Context:** ~850k tokens
**Phases:** 4
**Waves:** 5

### Wave Diagram

```
Wave 1 (parallel)
┌─────────┐  ┌─────────┐
│TASK-001 │  │TASK-002 │
│ Tenant  │  │ Auth    │
│ Schema  │  │ Context │
└────┬────┘  └────┬────┘
     │            │
     └────┬───────┘
          │
     Wave 2 (parallel)
┌─────────┼─────────┐
│         │         │
│    ┌────▼────┐ ┌──▼──────┐
│    │TASK-003 │ │TASK-004 │
│    │ Tenant  │ │ User    │
│    │ Service │ │ Service │
│    └────┬────┘ └──┬──────┘
│         │         │
│    Wave 3 (parallel)
│    ┌────▼────┬────▼────┬─────────┐
│    │TASK-005 │TASK-006 │TASK-007 │
│    │ Tenant  │ Billing │ Access  │
│    │ API     │ System  │ Control │
│    └────┬────┴────┬────┴────┬────┘
│         │         │         │
│    Wave 4 (parallel)
│    ┌────▼────┬────▼────┬────▼────┐
│    │TASK-008 │TASK-009 │TASK-010 │
│    │ Tests   │ Migrat. │ Docs    │
│    └────┬────┴────┬────┴────┬────┘
│         │         │         │
│    Wave 5 (sequential)
│         │         │         │
│         └────┬────┴─────────┘
│              │
│         ┌────▼────┐
│         │TASK-011 │
│         │ E2E     │
│         │ Tests   │
│         └────┬────┘
│              │
│         ┌────▼────┐
│         │TASK-012 │
│         │ Deploy  │
│         └─────────┘
```

### Critical Path

```
TASK-001 → TASK-003 → TASK-005 → TASK-008 → TASK-011 → TASK-012
  8h         10h        8h         6h         8h         4h    = 44h
```

---

## Example 4: Refactoring Task Split

### Before Split (160k tokens)

```markdown
### TASK-001: Refactor user service to use repository pattern

**Context Estimate:** ~160k tokens

**Files to modify:**
- src/services/UserService.ts (large, 800 lines)
- src/api/users/*.ts (12 endpoints)
- src/models/User.ts
- tests/services/UserService.test.ts (300 lines)
- tests/api/users/*.test.ts (10 test files)

**Problem:** Too many files, exceeds 100k context budget
```

### After Split (3 tasks, 50-60k each)

```markdown
### TASK-001: Create user repository interface

**Context Estimate:** ~50k tokens

**Files:**
- CREATE src/repositories/UserRepository.ts
- CREATE src/repositories/interfaces/IUserRepository.ts
- CREATE tests/repositories/UserRepository.test.ts

### TASK-002: Migrate user service to use repository

**Context Estimate:** ~55k tokens

**Files:**
- MODIFY src/services/UserService.ts
- CREATE tests/services/UserService.integration.test.ts

**Depends on:** TASK-001

### TASK-003: Update user API endpoints

**Context Estimate:** ~60k tokens

**Files:**
- MODIFY src/api/users/*.ts (12 files)
- MODIFY tests/api/users/*.test.ts (10 files)

**Depends on:** TASK-002
```

---

## Quality Checklist

### Implementation Plan Quality Gate

**Completeness:**
- [ ] All AD-X from design have corresponding tasks
- [ ] All file changes from design are assigned to tasks
- [ ] Prerequisites fully documented
- [ ] Testing plan covers all phases

**Structure:**
- [ ] Tasks follow INVEST criteria
- [ ] Dependencies clearly documented (FS/SS/FF/SF)
- [ ] Effort estimates provided
- [ ] Context budget < 100k per task

**Parallelization:**
- [ ] Dependency graph documented
- [ ] Waves identified
- [ ] Critical path calculated
- [ ] Parallel opportunities maximized

**Risk:**
- [ ] Risks identified with mitigations
- [ ] Rollout strategy defined
- [ ] Rollback plan documented
- [ ] Contingency buffer added

**Traceability:**
- [ ] Each task traces to AD-X
- [ ] Each task traces to FR-X
- [ ] Skills/methodologies recommended

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tasks too large | Break down to < 4 hours, < 100k tokens |
| Missing dependencies | Every task needs explicit "Depends on" |
| No acceptance criteria | Each task needs testable criteria |
| Forgetting tests | Include test tasks in plan |
| No rollback plan | Always plan for failure |
| No wave analysis | Identify parallel opportunities |
| Tasks not traced | Every task must trace to AD-X |
| Missing context estimate | AI needs token budget |

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |

## Sources

- [Scrum Task Board Examples](https://www.atlassian.com/agile/scrum/boards) - Visual task management
- [Gantt Chart Best Practices](https://www.teamgantt.com/guide-to-gantt-charts) - Project scheduling
- [Agile Estimation Techniques](https://www.mountaingoatsoftware.com/agile/planning-poker) - Story point estimation
- [Feature Slicing Patterns](https://agileforall.com/vertical-slices-and-scale/) - Vertical slicing
- [DevOps Task Examples](https://www.atlassian.com/devops) - Real-world DevOps workflows
