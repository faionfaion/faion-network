# Implementation Plan: [Feature Name]

**Version:** 1.0
**Design:** `{FEATURE_DIR}/design.md`
**Status:** Draft
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X requirements |
| Design | `{FEATURE_DIR}/design.md` | AD-X decisions, file list |
| Contracts | `.aidocs/contracts.md` | API patterns |

---

## Overview

[1-2 paragraphs: implementation approach and key decisions]

**Token Estimate:** ~Xk tokens total
**Critical Path:** High/Medium/Low complexity
**Waves:** N waves
**Total Tasks:** M tasks

---

## Prerequisites

### Infrastructure
- [ ] [e.g., PostgreSQL running, Redis configured]

### Environment
- [ ] [e.g., dev environment set up, env vars configured]

### Code Dependencies
- [ ] [e.g., auth middleware exists at path/to/auth.py]

### Documentation
- [ ] spec.md status: Approved
- [ ] design.md status: Approved

---

## Dependency Graph

```
TASK-001 (DB Schema) → TASK-003 (Model)
TASK-002 (Auth Utils) → TASK-003 (Model)
TASK-003 (Model) → TASK-004 (Service) → TASK-005 (Handler) → TASK-006 (Tests)
```

---

## Wave Analysis

| Wave | Tasks | Parallel | Dependencies | Est. Tokens |
|------|-------|----------|--------------|-------------|
| 1 | TASK-001, TASK-002 | Yes | None | ~Xk |
| 2 | TASK-003 | No | Wave 1 | ~Xk |
| 3 | TASK-004, TASK-005 | Yes | Wave 2 | ~Xk |
| 4 | TASK-006 | No | Wave 3 | ~Xk |

---

## Phases

| Phase | Description | Tasks | Complexity |
|-------|-------------|-------|------------|
| 1 | Infrastructure | TASK-001, TASK-002 | Medium |
| 2 | Core Logic | TASK-003, TASK-004, TASK-005 | High |
| 3 | Testing | TASK-006 | Medium |

---

## Phase 1: Infrastructure

### TASK-001: [Task Title]

**Wave:** 1
**Complexity:** simple / normal / complex
**Est. Tokens:** ~Xk

**Description:** [2-3 sentences describing the work]

**Traces to:** AD-001, FR-001

**Depends on:** None
**Blocks:** TASK-003

**Acceptance Criteria:**
- [ ] [Verifiable condition 1]
- [ ] [Verifiable condition 2]

**Files:**
| Action | File | Description |
|--------|------|-------------|
| CREATE | `path/to/file.py` | [description] |

**Tests:**
- [ ] Unit: [what to test]

---

## Critical Path

```
TASK-001 → TASK-003 → TASK-004 → TASK-005 → TASK-006
```

**Complexity:** High
**Tasks on Critical Path:** TASK-001, TASK-003, TASK-004, TASK-005, TASK-006

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | Low/Med/High | Low/Med/High | [Concrete action] |

**Contingency Buffer:** 20% added to all token estimates

---

## Testing Plan

| Phase | Tests | Pass Criteria |
|-------|-------|---------------|
| 1 | DB migrations | Tables created, rollback works |
| 2 | Unit tests | 80%+ coverage, all pass |
| 3 | Integration | All API endpoints pass |

| Layer | Target |
|-------|--------|
| Unit | 80%+ |
| Integration | 100% endpoints |
| E2E | Critical flows |

---

## Rollout Strategy

### Pre-deployment
- [ ] All tests pass in staging
- [ ] Database backup created
- [ ] Monitoring alerts configured

### Deployment Steps
1. Apply database migrations
2. Deploy code changes
3. Verify health checks pass

### Rollback Plan
1. Disable feature flag (if applicable)
2. Revert code deployment
3. Rollback migrations if needed

### Success Criteria
- Error rate < 0.1% for 24 hours
- Response time < 500ms p95

---

## Open Questions

- [ ] [Question to resolve before execution starts]
