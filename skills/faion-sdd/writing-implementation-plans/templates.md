# Implementation Plan Templates

Reusable templates for implementation plans and tasks.

---

## Full Implementation Plan Template

```markdown
# Implementation Plan: [Feature Name]

**Version:** 1.0
**Design:** `{FEATURE_DIR}/design.md`
**Status:** Draft | In Review | Approved
**Author:** [Name/Agent]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Key Sections |
|----------|------|--------------|
| Constitution | `.aidocs/constitution.md` | Tech stack, standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X requirements |
| Design | `{FEATURE_DIR}/design.md` | AD-X decisions |
| Contracts | `.aidocs/contracts.md` | API patterns |

---

## Overview

[1-2 paragraphs summarizing implementation approach and key decisions]

| Metric | Value |
|--------|-------|
| Total Tasks | [N] |
| Waves | [N] |
| Critical Path | ~[X]k tokens |
| Complexity | Low / Medium / High |

---

## Prerequisites

### Infrastructure
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

### Environment
- [ ] [Environment variable or config]

### Code Dependencies
- [ ] [Required module/class exists]

### Documentation
- [ ] Spec approved (status: Approved)
- [ ] Design approved (status: Approved)

---

## Dependency Graph

```
TASK-001 (Description)
    |
    +--[FS]---> TASK-003 (Description)
    |               |
    |               +--[FS]---> TASK-005 (Description)
    |
    +--[FS]---> TASK-004 (Description)

TASK-002 (Description) --[SS]---> TASK-003
```

---

## Wave Analysis

| Wave | Tasks | Parallel | Dependencies | Token Load |
|------|-------|----------|--------------|------------|
| 1 | TASK-001, TASK-002 | Yes | None | ~45k |
| 2 | TASK-003, TASK-004 | Yes | Wave 1 | ~80k |
| 3 | TASK-005 | No | Wave 2 | ~50k |

**Wave Visualization:**

```
Wave 1          Wave 2          Wave 3
+---------+     +---------+     +---------+
| TASK-01 |---->| TASK-03 |---->| TASK-05 |
+---------+  |  +---------+     +---------+
             |
+---------+  |  +---------+
| TASK-02 |--+->| TASK-04 |
+---------+     +---------+
```

---

## Phases

| Phase | Name | Tasks | Focus |
|-------|------|-------|-------|
| 1 | Infrastructure | TASK-001, TASK-002 | Database, utils |
| 2 | Core Logic | TASK-003, TASK-004 | Business logic |
| 3 | Testing | TASK-005 | Validation |

---

## Phase 1: [Phase Name]

### TASK-001: [Concise Title]

**Wave:** 1
**Complexity:** simple | normal | complex
**Tokens:** ~[X]k

**Description:**
[2-3 sentences explaining what needs to be done]

**Traces to:**
- AD-001: [Decision this implements]
- FR-001: [Requirement this satisfies]

**Depends on:** None
**Blocks:** TASK-003, TASK-004

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `src/path/file.ts` | [Description] |
| MODIFY | `src/path/existing.ts` | [What to add/change] |

**Tests:**
- [ ] Unit: `src/path/__tests__/file.test.ts`
- [ ] Integration: [If applicable]

**Technical Notes:**
- Follow pattern in `src/examples/similar.ts`
- [Gotcha or warning]

**Recommended Skills:**
- faion-software-developer: [specific aspect]

---

### TASK-002: [Concise Title]

[Same format as TASK-001]

---

## Phase 2: [Phase Name]

### TASK-003: [Concise Title]

[Same format]

---

## Critical Path

```
TASK-001 --> TASK-003 --> TASK-005
  25k          45k          50k     = ~120k tokens
```

**Critical Path Tasks:** TASK-001, TASK-003, TASK-005
**Total Tokens:** ~120k
**Bottleneck:** TASK-003 (largest on critical path)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |
| [Risk 2] | Low/Med/High | Low/Med/High | [Strategy] |

**Contingency Buffer:** 20% added to estimates

---

## Testing Plan

### Per-Phase Testing

| Phase | Tests | Pass Criteria |
|-------|-------|---------------|
| 1 | Unit tests for utils | All pass, 80% coverage |
| 2 | Integration tests | API endpoints respond correctly |
| 3 | E2E tests | Critical flow completes |

### Coverage Targets

| Layer | Target |
|-------|--------|
| Unit | 80%+ |
| Integration | All endpoints |
| E2E | Critical flows |

---

## Rollout Strategy

### Pre-deployment
- [ ] All tests pass in staging
- [ ] Database backup created
- [ ] Feature flag configured (off)
- [ ] Monitoring alerts configured

### Deployment Steps
1. Apply database migrations
2. Deploy code changes
3. Verify health checks
4. Enable feature flag (10%)
5. Monitor for 30 minutes
6. Gradual rollout (25% --> 50% --> 100%)

### Rollback Plan
1. Disable feature flag (immediate)
2. Revert code if needed
3. Rollback migrations if needed

### Success Criteria
- Error rate < 0.1%
- Response time < 500ms p95
- No critical bugs in 24 hours

---

## Recommended Skills & Methodologies

| Skill | Tasks | Purpose |
|-------|-------|---------|
| faion-software-developer | All | Core implementation |
| faion-testing-developer | TASK-005 | Test coverage |

| Methodology | Tasks |
|-------------|-------|
| python | TASK-001, TASK-003 |
| testing | TASK-005 |

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial plan |
```

---

## Task Template (for TASK_XXX.md files)

```markdown
# TASK_XXX: [Title]

## SDD References

| Document | Path |
|----------|------|
| Spec | `.aidocs/{status}/feature-XXX/spec.md` |
| Design | `.aidocs/{status}/feature-XXX/design.md` |
| Implementation Plan | `.aidocs/{status}/feature-XXX/implementation-plan.md` |

---

## Task Metadata

| Field | Value |
|-------|-------|
| **Phase** | [N] |
| **Wave** | [N] |
| **Complexity** | simple / normal / complex |
| **Tokens** | ~[X]k |
| **Status** | todo / in-progress / done |

---

## Task Dependency Tree

### Dependencies (must complete first)
| Task | Status | Description |
|------|--------|-------------|
| TASK-YYY | done | [Brief description] |

### Blocks (waiting on this)
| Task | Description |
|------|-------------|
| TASK-ZZZ | [Brief description] |

---

## Requirements Coverage

### AD-XXX: [Architectural Decision Title]

[Full text of the architectural decision this task implements]

### FR-XXX: [Functional Requirement Title]

[Full text of the functional requirement this task satisfies]

---

## Description

[2-3 sentences explaining what needs to be done and why]

---

## Acceptance Criteria

### AC-1: [Criterion Name]
**Given** [precondition]
**When** [action]
**Then** [expected result]

### AC-2: [Criterion Name]
- [ ] [Declarative criterion]
- [ ] [Another criterion]

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | `src/path/new-file.ts` | [Full file] |
| MODIFY | `src/path/existing.ts` | [What to add/change] |
| DELETE | `src/path/old-file.ts` | [Entire file] |

---

## Subtasks

- [ ] 01. [First subtask]
- [ ] 02. [Second subtask]
- [ ] 03. [Third subtask]
- [ ] 04. Write unit tests
- [ ] 05. Verify acceptance criteria

---

## Technical Notes

### Patterns to Follow
- See `src/examples/similar-implementation.ts` for pattern
- Use existing types from `src/types/index.ts`

### Gotchas
- [Warning or non-obvious requirement]

### Configuration
- [Any config changes needed]

---

## Tests

### Unit Tests
- [ ] `src/__tests__/new-file.test.ts`: [Test description]

### Integration Tests
- [ ] `tests/integration/feature.test.ts`: [Test description]

---

## Implementation

<!-- Fill during execution -->

### Progress
- [ ] Subtask 1
- [ ] Subtask 2
- [ ] ...

### Decisions Made
[Document any decisions made during implementation]

### Issues Encountered
[Document any issues and how they were resolved]

---

## Summary

<!-- Fill after completion -->

### Completed
- [x] [What was done]

### Files Changed
| Action | File |
|--------|------|
| CREATE | `path/file.ts` |

### Tests Added
- `path/test.ts`: X tests passing

### Verification
- [ ] All AC verified
- [ ] All tests passing
- [ ] Code reviewed

---

## Lessons Learned

<!-- Optional: Fill if anything notable -->

### Patterns Discovered
[New patterns to add to memory]

### Mistakes to Avoid
[Issues that could help future tasks]
```

---

## Mini Task Template (for simple tasks)

```markdown
# TASK_XXX: [Title]

**Traces to:** AD-XXX, FR-XXX
**Depends on:** TASK-YYY (or None)
**Complexity:** simple
**Tokens:** ~20k

## Description
[1-2 sentences]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Files
| Action | File |
|--------|------|
| CREATE | `path/file.ts` |

## Implementation
[Notes during execution]

## Summary
[Completion notes]
```

---

## Wave Summary Template

```markdown
## Wave [N] Summary

**Tasks:** TASK-XXX, TASK-YYY, TASK-ZZZ
**Token Load:** ~[X]k total
**Parallel:** Yes/No

### Execution Order
1. TASK-XXX - [Brief description]
2. TASK-YYY - [Brief description] (parallel with 1)
3. TASK-ZZZ - [Brief description] (parallel with 1, 2)

### Dependencies Satisfied
- Wave [N-1] complete
- [Specific prerequisite met]

### Exit Criteria
- [ ] All tasks in wave complete
- [ ] All tests passing
- [ ] No blockers for Wave [N+1]
```

---

## Dependency Graph Template

```markdown
## Dependency Graph

### Legend
- `[FS]` = Finish-to-Start (sequential)
- `[SS]` = Start-to-Start (parallel start)
- `[FF]` = Finish-to-Finish (parallel finish)
- `--->` = Dependency direction

### Graph

```
[Entry Point]
     |
     v
TASK-001 -----[FS]-----> TASK-003 -----[FS]-----> TASK-005
     |                        |                       |
     |                        v                       v
     |                   TASK-004               [Exit Point]
     |
     +----[SS]-----> TASK-002
```

### Dependency Table

| Task | Depends On | Blocks | Type |
|------|------------|--------|------|
| TASK-001 | None | TASK-002, TASK-003 | Foundation |
| TASK-002 | TASK-001 [SS] | TASK-004 | Parallel |
| TASK-003 | TASK-001 [FS] | TASK-004, TASK-005 | Sequential |
| TASK-004 | TASK-002, TASK-003 | TASK-005 | Merge |
| TASK-005 | TASK-003, TASK-004 | None | Final |
```

---

*Templates | SDD Foundation | Version 3.0.0*
