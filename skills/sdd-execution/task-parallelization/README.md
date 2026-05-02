---
id: task-parallelization
name: "Task Parallelization"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Task Parallelization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | task-parallelization |
| **Version** | 2.2.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #parallelization, #optimization |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-creator-agent |

---

## Problem

Implementation plans become bottlenecks when:
- Tasks are executed sequentially when they could run in parallel
- Critical path is not identified
- Dependencies block parallelization opportunities

**The root cause:** Inadequate dependency analysis and lack of parallelization strategy.

---

## Wave-Based Task Creation

**Principle:** Create tasks in waves based on dependency graph, not all at once.

### Why Waves?

| Approach | Problem |
|----------|---------|
| All tasks at once | Later tasks lack context from completed tasks |
| Sequential creation | Slow, no parallelization |
| **Wave-based** | Balance: create parallel tasks together, incorporate learnings |

### Wave Creation Process

```
1. Analyze dependency graph
2. Identify Wave 1 tasks (no dependencies)
3. Create Wave 1 tasks with full detail
4. Execute Wave 1
5. Update context with learnings
6. Create Wave 2 tasks (depend on Wave 1)
7. Repeat until all tasks created
```

**Example:**
```
Wave 1 Creation: [TASK-001, TASK-002] - both have no dependencies
    ↓ execute
Wave 2 Creation: [TASK-003, TASK-004] - depend on Wave 1
    ↓ execute
Wave 3 Creation: [TASK-005, TASK-006] - depend on Wave 2
```

### Benefits of Wave Creation

| Benefit | Description |
|---------|-------------|
| **Incremental context** | Later tasks incorporate learnings from earlier waves |
| **Pattern discovery** | Wave 1 establishes patterns used in later waves |
| **Reduced rework** | Don't create tasks that may change after discoveries |
| **Better estimates** | Real effort data improves later estimates |

### When to Create All Tasks at Once

Sometimes all tasks should be created upfront:
- Small feature (< 6 tasks)
- Well-understood domain with clear patterns
- Need full scope estimate for planning
- Team needs parallel assignment immediately

---

## Identify Parallel Paths

Tasks without arrows between them can run in parallel:

**Can parallelize:**
- TASK-001 (DB) and TASK-002 (Password Utils) - no dependency
- TASK-003 (Model) and TASK-004 (JWT Utils) - both depend on TASK-001

**Cannot parallelize:**
- TASK-005 and TASK-003 - TASK-005 needs TASK-003

---

## Calculate Critical Path

The longest chain determines minimum time:

```
Path A: TASK-001 → TASK-003 → TASK-005 = 6 hours
Path B: TASK-001 → TASK-004 → TASK-006 = 5 hours
Path C: TASK-002 → TASK-004 → TASK-006 = 4 hours

Critical path: A (6 hours minimum)
```

---

## Task List Template

```markdown
# Tasks: {Feature Name}

## Summary

| Total | TODO | In Progress | Done | Blocked |
|-------|------|-------------|------|---------|
| 12 | 8 | 2 | 2 | 0 |

## Dependency Graph

```
TASK-001 ──[FS]──→ TASK-003 ──[FS]──→ TASK-005
    │                  │                  │
    ↓                  ↓                  ↓
TASK-002 ──[FS]──→ TASK-004 ──[FS]──→ TASK-006
```

## Parallel Waves

**Wave 1 (can start immediately):**
- TASK-001: Database setup (2h)
- TASK-002: Password utilities (2h)

**Wave 2 (after Wave 1):**
- TASK-003: User model (2h)
- TASK-004: JWT utilities (2h)

**Wave 3 (after Wave 2):**
- TASK-005: Register handler (2h)
- TASK-006: Login handler (2h)

**Critical Path:** Wave 1 → Wave 2 → Wave 3 = 6h minimum

## Task List by State

### TODO
| ID | Title | Effort | Deps | Skills |
|----|-------|--------|------|--------|
| TASK-001 | Database setup | 2h | - | faion-devops |

### IN_PROGRESS
| ID | Title | Assignee | Started |
|----|-------|----------|---------|
| TASK-003 | User model | Dev A | 2026-01-19 |

### DONE
| ID | Title | Completed |
|----|-------|-----------|
| - | - | - |
```

---

## Example: Auth Feature Parallelization

**Bad:**
```
TASK-001: Build authentication system (8 hours)
```
Problem: Too vague, can't track, can't parallelize.

**Good:**
```
TASK-001: Create users table migration (1h) - simple
TASK-002: Create sessions table migration (1h) - simple
TASK-003: Implement password hashing (2h) - normal, code-review
TASK-004: Implement JWT utilities (2h) - normal
TASK-005: Create User model with validation (2h) - normal
TASK-006: Create Session model (1h) - simple
TASK-007: Implement register handler (2h) - normal, FR-1
TASK-008: Implement login handler (2h) - normal, FR-2
TASK-009: Implement logout handler (1h) - simple, FR-3
TASK-010: Implement auth middleware (2h) - normal, AD-1
TASK-011: Write unit tests (2h) - normal, testing-strategy
TASK-012: Write integration tests (2h) - normal
```

**Parallelization waves:**
```
Wave 1 (Day 1 AM):  [TASK-001, TASK-002, TASK-003, TASK-004]
Wave 2 (Day 1 PM):  [TASK-005, TASK-006]
Wave 3 (Day 2 AM):  [TASK-007, TASK-008]
Wave 4 (Day 2 PM):  [TASK-009, TASK-010]
Wave 5 (Day 3):     [TASK-011, TASK-012]

Result: 22h of work in 2.5 days with proper parallelization
Speedup: 22h / 2.5 days (assuming 8h/day) = ~1.1x (limited by dependencies)
```

---

## Parallelization Speedup Factors

| Factor | Description | Impact |
|--------|-------------|--------|
| **Dependency chains** | Long sequential paths limit parallelization | Critical path dominates |
| **Resource availability** | Number of parallel executors (agents/humans) | Linear scaling up to bottleneck |
| **Shared resources** | Database, API rate limits | Contention reduces speedup |
| **Task granularity** | Smaller tasks = better parallelization | Overhead vs. flexibility tradeoff |

**Theoretical maximum:** 1.8-3.5x speedup (depends on dependency graph density)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Sequential by default | Analyze for parallelization |
| Hidden dependencies | List ALL dependencies explicitly |
| Circular dependencies | Redesign - split shared logic |

---

## Quality Checklist

### Parallelization Analysis
- [ ] Dependency graph drawn
- [ ] Critical path identified
- [ ] Parallel waves defined
- [ ] Resource constraints considered

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Executing design patterns | haiku | Pattern application, code generation |
| Reviewing implementation against spec | sonnet | Quality assurance, consistency check |
| Resolving design-execution conflicts | opus | Trade-off analysis, adaptive decisions |

## Related Methodologies

| ID | Name | Relationship |
|----|------|--------------|
| task-creation | Task Creation | Creates tasks to parallelize |
| task-dependencies | Task Dependencies | Maps relationships for parallelization |
| dependency-management | Schedule Development | Provides dependency types |

---

## Agents

**faion-task-creator-agent:**
- Analyzes dependency graphs
- Identifies parallel execution opportunities
- Creates wave-based task sets
- Triggers: "Analyze parallelization", "Create task waves"

---

*Methodology | SDD Foundation | Version 2.2.0*
*Integrates: PM (dependency-management, schedule-development)*
