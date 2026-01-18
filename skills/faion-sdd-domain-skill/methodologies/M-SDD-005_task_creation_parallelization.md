# M-SDD-005: Task Creation & Parallelization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-005 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #tasks, #parallelization |
| **Domain Skill** | faion-sdd-domain-skill |
| **Agents** | faion-task-creator |

---

## Problem

Implementation plans become bottlenecks when:
- Tasks are executed sequentially when they could run in parallel
- Task granularity is wrong (too big or too small)
- Dependencies are unclear or circular
- Progress is hard to track

**The root cause:** Poor task decomposition and dependency analysis.

---

## Framework

### Task Decomposition Principles

#### 1. Right Size
Each task should be:
- **Completable in 1-4 hours** (single work session)
- **Independently testable** (can verify completion)
- **Single responsibility** (one clear objective)

**Too big:** "Implement authentication" (multiple days)
**Too small:** "Add import statement" (minutes)
**Right size:** "Create password hashing utilities" (2-3 hours)

#### 2. Clear Boundaries
Each task must have:
- **Input:** What exists before
- **Output:** What exists after
- **Success criteria:** How to verify completion

#### 3. Explicit Dependencies
- List every task this depends on
- List every task that depends on this
- No implicit or assumed dependencies

### Dependency Analysis

#### Step 1: Create Task Graph
Draw tasks as nodes, dependencies as arrows:

```
TASK-001 (DB Tables)
    ↓
TASK-003 (User Model) ────→ TASK-005 (Register Handler)
    ↓                              ↓
TASK-002 (Password Utils) → TASK-004 (JWT Utils) → TASK-006 (Login Handler)
```

#### Step 2: Identify Parallel Paths
Tasks without arrows between them can run in parallel:

**Can parallelize:**
- TASK-001 (DB) and TASK-002 (Password Utils) - no dependency
- TASK-003 (Model) and TASK-004 (JWT Utils) - both depend on TASK-001

**Cannot parallelize:**
- TASK-005 and TASK-003 - TASK-005 needs TASK-003

#### Step 3: Calculate Critical Path
The longest chain of dependent tasks determines minimum time:

```
Path A: TASK-001 → TASK-003 → TASK-005 = 6 hours
Path B: TASK-001 → TASK-004 → TASK-006 = 5 hours
Path C: TASK-002 → TASK-004 → TASK-006 = 4 hours

Critical path: A (6 hours minimum)
```

### Task States

```
BACKLOG → TODO → IN_PROGRESS → DONE
                      ↓
                  BLOCKED
```

| State | Meaning |
|-------|---------|
| BACKLOG | Future work, not yet prioritized |
| TODO | Ready to start, dependencies met |
| IN_PROGRESS | Currently being worked on |
| BLOCKED | Cannot proceed, dependency issue |
| DONE | Completed, verified |

### Parallelization Strategy

#### For Solo Developers
Even working alone, parallelization helps:
- **Batch similar tasks:** Write all models together
- **Context switching:** If blocked, switch to independent task
- **Review breaks:** Start task B while task A is in review

#### For Teams
Assign independent tasks to different people:
- **Developer A:** Authentication handlers
- **Developer B:** Database migrations
- **Developer C:** Frontend integration

#### For AI Agents
AI can execute multiple independent tasks simultaneously:
```
# Bad: Sequential
execute(TASK-001)
execute(TASK-002)  # waits unnecessarily

# Good: Parallel
parallel_execute([TASK-001, TASK-002])  # both independent
```

---

## Templates

### Task Template

```markdown
# TASK_XXX: [Task Title]

**Status:** TODO | IN_PROGRESS | DONE | BLOCKED
**Priority:** P0 | P1 | P2
**Effort:** X hours
**Assignee:** [Name/Agent]

## Description

[Clear description of what needs to be done]

## Dependencies

**Depends on:**
- TASK_YYY - [Why]
- TASK_ZZZ - [Why]

**Blocks:**
- TASK_AAA - [Why]

## Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Files

| Action | File | Description |
|--------|------|-------------|
| CREATE | `path/to/file` | Description |
| MODIFY | `path/to/existing` | What to change |

## Technical Notes

[Any implementation hints, gotchas, or references]

## Testing

- [ ] Unit test: [Description]
- [ ] Integration test: [Description]

## Completion Checklist

- [ ] Code written
- [ ] Tests pass
- [ ] Documentation updated
- [ ] PR created
```

### Task List Template

```markdown
# Tasks: [Feature Name]

## Summary

| Total | TODO | In Progress | Done | Blocked |
|-------|------|-------------|------|---------|
| 12 | 8 | 2 | 2 | 0 |

## Dependency Graph

```
TASK-001 ──→ TASK-003 ──→ TASK-005
    │            │            │
    ↓            ↓            ↓
TASK-002 ──→ TASK-004 ──→ TASK-006
```

## Parallel Groups

**Group 1 (can start immediately):**
- TASK-001: Database setup
- TASK-002: Password utilities

**Group 2 (after Group 1):**
- TASK-003: User model
- TASK-004: JWT utilities

**Group 3 (after Group 2):**
- TASK-005: Register handler
- TASK-006: Login handler

## Task List

### TODO

| ID | Title | Effort | Depends On |
|----|-------|--------|------------|
| TASK-001 | Database setup | 2h | - |
| TASK-002 | Password utilities | 2h | - |

### IN_PROGRESS

| ID | Title | Assignee | Started |
|----|-------|----------|---------|
| TASK-003 | User model | Dev A | 2026-01-17 |

### DONE

| ID | Title | Completed |
|----|-------|-----------|
| - | - | - |
```

### Parallelization Checklist

```markdown
## Parallelization Review

### Pre-flight Checks
- [ ] All tasks have explicit dependencies
- [ ] No circular dependencies
- [ ] Critical path identified
- [ ] Tasks right-sized (1-4 hours)

### Parallel Groups Identified
- [ ] Group 1: [Tasks that can start now]
- [ ] Group 2: [Tasks after Group 1]
- [ ] Group 3: [Tasks after Group 2]

### Resource Allocation
- [ ] Tasks assigned to available resources
- [ ] No resource conflicts
- [ ] Blockers identified and addressed

### Monitoring Plan
- [ ] Progress tracking method defined
- [ ] Blocker escalation path clear
- [ ] Daily sync scheduled (if team)
```

---

## Examples

### Example: Task Decomposition for Auth Feature

**Implementation Plan says:** "Implement user authentication"

**Bad decomposition:**
```
TASK-001: Build authentication system (8 hours)
```
Problem: Too vague, can't track progress, can't parallelize.

**Good decomposition:**
```
TASK-001: Create users table migration (1h)
TASK-002: Create sessions table migration (1h)
TASK-003: Implement password hashing (2h)
TASK-004: Implement JWT utilities (2h)
TASK-005: Create User model (2h)
TASK-006: Create Session model (1h)
TASK-007: Implement register handler (2h)
TASK-008: Implement login handler (2h)
TASK-009: Implement logout handler (1h)
TASK-010: Implement auth middleware (2h)
TASK-011: Write unit tests (2h)
TASK-012: Write integration tests (2h)
```

**Dependency analysis:**
```
TASK-001 ─┬→ TASK-005 ─┬→ TASK-007
          │            │      ↓
TASK-002 ─┼→ TASK-006 ─┼→ TASK-008 ──→ TASK-010
          │            │      ↓           ↓
TASK-003 ─┤            │  TASK-009   TASK-011
          │            │               ↓
TASK-004 ─┴────────────┴──────────→ TASK-012
```

**Parallel groups:**
```
Day 1 Morning:  [TASK-001, TASK-002, TASK-003, TASK-004] - all parallel
Day 1 Afternoon: [TASK-005, TASK-006] - parallel after DB tasks
Day 2 Morning:  [TASK-007, TASK-008] - parallel after models
Day 2 Afternoon: [TASK-009, TASK-010] - parallel
Day 3:          [TASK-011, TASK-012] - testing
```

**Result:** 8 hours of work done in ~2.5 days with proper parallelization.

### Example: AI Agent Parallelization

```python
# Task executor configuration
tasks = [
    Task("TASK-001", depends_on=[]),
    Task("TASK-002", depends_on=[]),
    Task("TASK-003", depends_on=["TASK-001"]),
    Task("TASK-004", depends_on=["TASK-001", "TASK-002"]),
]

# Execution plan
round_1 = ["TASK-001", "TASK-002"]  # No dependencies
round_2 = ["TASK-003"]              # Depends on TASK-001
round_3 = ["TASK-004"]              # Depends on both

# Execute in parallel rounds
for round in [round_1, round_2, round_3]:
    parallel_execute(round)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tasks too large | Break down until < 4 hours |
| Hidden dependencies | List ALL dependencies explicitly |
| Circular dependencies | Redesign - split shared logic |
| No acceptance criteria | Add testable criteria to every task |
| Sequential by default | Always analyze for parallelization |
| Forgetting tests | Include testing tasks in plan |

---

## Related Methodologies

- **M-SDD-004:** Writing Implementation Plans
- **M-SDD-006:** Quality Gates & Confidence Checks
- **M-PMBOK-008:** Schedule Management
- **M-PMBOK-009:** Resource Management

---

## Agent

**faion-task-creator** creates and organizes tasks. Invoke with:
- "Create tasks from implementation plan"
- "Analyze task dependencies"
- "Find parallelization opportunities"

---

*Methodology M-SDD-005 | SDD Foundation | Version 1.0*
