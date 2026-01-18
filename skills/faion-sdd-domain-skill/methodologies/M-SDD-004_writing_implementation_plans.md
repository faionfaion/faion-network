# M-SDD-004: Writing Implementation Plans

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-004 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #implementation |
| **Domain Skill** | faion-sdd-domain-skill |
| **Agents** | faion-impl-plan-reviewer |

---

## Problem

Developers struggle to start coding after reading design documents because:
- Design is too high-level to act on directly
- Unclear order of operations
- Dependencies between components not obvious
- No clear success criteria for each step

**The root cause:** No bridge between design and actionable tasks.

---

## Framework

### What is an Implementation Plan?

An implementation plan breaks the design into ordered, actionable tasks with:
- Clear dependencies
- Estimated effort
- Success criteria
- Testing requirements

### Implementation Plan Structure

```markdown
# Implementation Plan: [Feature Name]

## Overview
[Summary of implementation approach]

## Prerequisites
[What must exist before starting]

## Phase Breakdown
[Logical grouping of tasks]

## Task List
[Detailed tasks with estimates]

## Testing Plan
[What to test at each phase]

## Rollout Strategy
[How to deploy safely]
```

### Writing Process

#### Step 1: Identify Prerequisites
List everything that must exist before you start:
- Required infrastructure
- Dependencies to install
- Access/permissions needed
- Existing code to review

```markdown
## Prerequisites

- [ ] PostgreSQL database running
- [ ] Redis instance configured
- [ ] SendGrid API key obtained
- [ ] Development environment set up
```

#### Step 2: Define Phases
Group related tasks into logical phases:

```markdown
## Phases

### Phase 1: Infrastructure (Day 1)
Set up database tables, configure services

### Phase 2: Core Logic (Days 2-3)
Implement authentication handlers

### Phase 3: API Layer (Day 4)
Create REST endpoints

### Phase 4: Integration (Day 5)
Connect frontend, test E2E
```

#### Step 3: Break Down Tasks
For each phase, create specific tasks:

**Task format:**
```markdown
### TASK-XXX: [Task Title]

**Description:** [What to do]
**Depends on:** [Other tasks]
**Effort:** [Hours/Days]
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Files:**
- CREATE: `path/to/file.ts`
- MODIFY: `path/to/existing.ts`
```

#### Step 4: Define Testing Plan
Specify tests for each phase:

```markdown
## Testing Plan

### Phase 1 Tests
- [ ] Database migrations run successfully
- [ ] Tables created with correct schema

### Phase 2 Tests
- [ ] Password hashing works
- [ ] JWT generation/validation works
- [ ] Unit tests pass

### Phase 3 Tests
- [ ] API endpoints return correct responses
- [ ] Error handling works
- [ ] Integration tests pass

### Phase 4 Tests
- [ ] E2E login flow works
- [ ] E2E registration flow works
```

#### Step 5: Plan Rollout
How will you deploy safely?

```markdown
## Rollout Strategy

### Pre-deployment
- [ ] Run all tests in staging
- [ ] Database backup created

### Deployment
- [ ] Apply database migrations
- [ ] Deploy new code
- [ ] Verify health checks

### Post-deployment
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Rollback plan ready
```

---

## Templates

### Full Implementation Plan Template

```markdown
# Implementation Plan: [Feature Name]

**Design:** [link to design.md]
**Status:** Draft | In Progress | Complete
**Author:** [Name]
**Estimated Effort:** [X days]
**Start Date:** YYYY-MM-DD

---

## Overview

[1-2 paragraphs summarizing implementation approach]

---

## Prerequisites

- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]
- [ ] [Prerequisite 3]

---

## Phases

| Phase | Description | Effort | Dependencies |
|-------|-------------|--------|--------------|
| 1 | [Phase 1 name] | X days | None |
| 2 | [Phase 2 name] | X days | Phase 1 |
| 3 | [Phase 3 name] | X days | Phase 2 |

---

## Phase 1: [Phase Name]

### TASK-001: [Task Title]

**Description:**
[Detailed description of what to do]

**Depends on:** None

**Effort:** X hours

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Files:**
| Action | File | Description |
|--------|------|-------------|
| CREATE | `path/file.ts` | Description |
| MODIFY | `path/existing.ts` | What to change |

**Tests:**
- [ ] [Test 1]
- [ ] [Test 2]

---

### TASK-002: [Task Title]
...

---

## Phase 2: [Phase Name]

### TASK-003: [Task Title]
...

---

## Testing Plan

### Unit Tests
- [ ] [Test case]

### Integration Tests
- [ ] [Test case]

### E2E Tests
- [ ] [Test case]

---

## Rollout Strategy

### Pre-deployment Checklist
- [ ] All tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Database backup

### Deployment Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Rollback Plan
1. [Rollback step 1]
2. [Rollback step 2]

### Monitoring
- [ ] Error rate < X%
- [ ] Response time < Xms
- [ ] No critical errors

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Mitigation] |

---

## Open Questions

- [ ] [Question]

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial plan |
```

### Task Template

```markdown
### TASK-XXX: [Concise Title]

**Description:**
[2-3 sentences explaining what needs to be done]

**Depends on:** TASK-YYY, TASK-ZZZ (or "None")

**Effort:** [X hours/days]

**Acceptance Criteria:**
- [ ] [Specific, measurable criterion]
- [ ] [Another criterion]

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/path/file.ts` | [What this file does] |
| MODIFY | `src/path/existing.ts` | [What to add/change] |

**Technical Notes:**
[Any implementation hints or gotchas]

**Tests:**
- [ ] Unit: [Test description]
- [ ] Integration: [Test description]
```

---

## Examples

### Example: Authentication Implementation Plan

```markdown
# Implementation Plan: User Authentication

**Design:** features/04-auth-system/design.md
**Effort:** 5 days
**Start Date:** 2026-01-20

---

## Overview

Implement JWT-based authentication in 4 phases:
1. Database setup (0.5 days)
2. Core auth logic (1.5 days)
3. API endpoints (1.5 days)
4. Integration & testing (1.5 days)

---

## Prerequisites

- [ ] PostgreSQL database configured
- [ ] Redis for token blacklist
- [ ] SendGrid API key for emails
- [ ] JWT_SECRET in environment

---

## Phase 1: Database Setup (0.5 days)

### TASK-001: Create Users Table

**Description:**
Create PostgreSQL migration for users table with email,
password_hash, and timestamps.

**Depends on:** None

**Effort:** 2 hours

**Acceptance Criteria:**
- [ ] Migration runs without errors
- [ ] Users table exists with correct columns
- [ ] Unique constraint on email
- [ ] Indexes created

**Files:**
| Action | File |
|--------|------|
| CREATE | `migrations/001_create_users.sql` |
| CREATE | `src/models/user.ts` |

**Tests:**
- [ ] Migration up/down works
- [ ] Can insert/query users

---

### TASK-002: Create Sessions Table

**Description:**
Create sessions table for refresh token tracking.

**Depends on:** TASK-001

**Effort:** 1 hour

**Acceptance Criteria:**
- [ ] Sessions table with user_id foreign key
- [ ] Expiration timestamp column

**Files:**
| Action | File |
|--------|------|
| CREATE | `migrations/002_create_sessions.sql` |
| CREATE | `src/models/session.ts` |

---

## Phase 2: Core Auth Logic (1.5 days)

### TASK-003: Password Hashing Utilities

**Description:**
Create bcrypt wrapper for hashing and comparing passwords.

**Depends on:** None (parallel with TASK-001)

**Effort:** 2 hours

**Acceptance Criteria:**
- [ ] hashPassword() returns bcrypt hash
- [ ] comparePassword() correctly validates
- [ ] Cost factor is configurable

**Files:**
| Action | File |
|--------|------|
| CREATE | `src/auth/utils/password.ts` |
| CREATE | `tests/auth/password.test.ts` |

---

### TASK-004: JWT Utilities

**Description:**
Create JWT sign/verify utilities with access and refresh tokens.

**Depends on:** None

**Effort:** 3 hours

**Acceptance Criteria:**
- [ ] signAccessToken() creates 15min token
- [ ] signRefreshToken() creates 7-day token
- [ ] verifyToken() validates and returns payload
- [ ] Handles expired tokens gracefully

**Files:**
| Action | File |
|--------|------|
| CREATE | `src/auth/utils/jwt.ts` |
| CREATE | `tests/auth/jwt.test.ts` |
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tasks too large | Break down to < 4 hours each |
| Missing dependencies | Every task needs explicit "Depends on" |
| No acceptance criteria | Each task needs testable criteria |
| Forgetting tests | Include test tasks in plan |
| No rollback plan | Always plan for failure |

---

## Related Methodologies

- **M-SDD-003:** Writing Design Documents
- **M-SDD-005:** Task Creation & Parallelization
- **M-PRD-001:** MVP Scoping
- **M-PMBOK-008:** Schedule Management

---

## Agent

**faion-impl-plan-reviewer** reviews implementation plans. Invoke with:
- "Review this implementation plan"
- "Break down this design into tasks"
- "Estimate effort for these tasks"

---

*Methodology M-SDD-004 | SDD Foundation | Version 1.0*
