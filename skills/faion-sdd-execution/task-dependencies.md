---
id: task-dependencies
name: "Task Dependencies"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Task Dependencies

## Metadata

| Field | Value |
|-------|-------|
| **ID** | task-dependencies |
| **Version** | 2.2.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #dependencies, #scheduling |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-creator-agent |

---

## Problem

Implementation plans fail when:
- Dependencies are unclear or circular
- Blocking relationships are not documented
- Dependency types are ambiguous

**The root cause:** Poor dependency analysis and documentation.

---

## Integrated Best Practices

| Domain | Methodology | Key Principle |
|--------|-------------|---------------|
| **PM** | dependency-management | Dependency types (FS, SS, FF, SF) |
| **PM** | schedule-development | Critical path method |
| **PM** | wbs-decomposition | 100% rule, dependency isolation |

---

## Dependency Types (from dependency-management)

| Type | Meaning | Example |
|------|---------|---------|
| **FS** | Finish-to-Start | User model must finish before login handler starts |
| **SS** | Start-to-Start | Frontend and API can start together |
| **FF** | Finish-to-Finish | Tests must finish when code finishes |
| **SF** | Start-to-Finish | Rare, migration starts when old code finishes |

---

## Create Task Graph

Draw tasks as nodes, dependencies as arrows:

```
TASK-001 (DB Tables)
    ↓ [FS]
TASK-003 (User Model) ────→ TASK-005 (Register Handler)
    ↓ [FS]                        ↓ [FS]
TASK-002 (Password Utils) → TASK-004 (JWT Utils) → TASK-006 (Login Handler)
```

---

## Dependency Analysis Process

### 1. List All Tasks

From implementation plan, extract all tasks with IDs.

### 2. Identify Dependencies

For each task, ask:
- What MUST exist before this task can start?
- What does this task BLOCK?
- What can run IN PARALLEL?

### 3. Document Dependency Type

Use standard notation:

```markdown
## Dependencies

**Depends on (FS = Finish-to-Start):**
- TASK-001 [FS] - Need database tables before creating models
- TASK-002 [FS] - Need password utils for user validation

**Blocks:**
- TASK-005 [FS] - Register handler depends on this model
- TASK-006 [FS] - Login handler depends on this model
```

### 4. Check for Circular Dependencies

If you find a cycle, REDESIGN:

```
BAD:
TASK-A depends on TASK-B
TASK-B depends on TASK-C
TASK-C depends on TASK-A  ← CIRCULAR!

GOOD:
Extract shared logic to TASK-D
TASK-D (no deps)
    ↓
TASK-A, TASK-B, TASK-C all depend on TASK-D
```

---

## Dependency Graph Notation

### Textual Notation

```
TASK-001 ──[FS]──→ TASK-003 ──[FS]──→ TASK-005
    │                  │                  │
    ↓ [FS]             ↓ [FS]             ↓ [FS]
TASK-002 ──[FS]──→ TASK-004 ──[FS]──→ TASK-006
```

### Table Notation

| Task ID | Title | Depends On | Blocks | Type |
|---------|-------|------------|--------|------|
| TASK-001 | DB Tables | - | TASK-003, TASK-004 | FS |
| TASK-002 | Password Utils | - | TASK-004 | FS |
| TASK-003 | User Model | TASK-001 | TASK-005 | FS |
| TASK-004 | JWT Utils | TASK-001, TASK-002 | TASK-006 | FS |
| TASK-005 | Register Handler | TASK-003 | - | FS |
| TASK-006 | Login Handler | TASK-004 | - | FS |

---

## Critical Path Calculation

### Method

1. Calculate earliest start time for each task
2. Calculate latest finish time for each task
3. Identify tasks with zero slack (critical path)

### Example

```
TASK-001: ES=0, EF=1, LS=0, LF=1, Slack=0 ✅ CRITICAL
TASK-002: ES=0, EF=1, LS=1, LF=2, Slack=1
TASK-003: ES=1, EF=3, LS=1, LF=3, Slack=0 ✅ CRITICAL
TASK-004: ES=1, EF=3, LS=2, LF=4, Slack=1
TASK-005: ES=3, EF=5, LS=3, LF=5, Slack=0 ✅ CRITICAL
TASK-006: ES=3, EF=5, LS=4, LF=6, Slack=1

Critical Path: TASK-001 → TASK-003 → TASK-005 = 5 hours
```

**Focus on critical path tasks** - delays here impact overall timeline.

---

## Dependency Best Practices

### 1. Explicit Over Implicit

**Bad:** "Task A needs some stuff from Task B"
**Good:** "TASK-A [FS] depends on TASK-B (needs User model class definition)"

### 2. Minimize Dependencies

Each dependency:
- Reduces parallelization
- Increases coordination overhead
- Creates blocking risk

**Ask:** Can this dependency be eliminated by:
- Refactoring shared logic?
- Using interfaces/contracts?
- Mocking/stubbing?

### 3. Document WHY

Not just "depends on TASK-X", but **why**:

```markdown
**Depends on:**
- TASK-003 [FS] - Register handler needs User model for database operations
- TASK-004 [FS] - Register handler needs JWT utils to generate auth tokens
```

### 4. Track Blocking

Document what this task blocks to understand impact:

```markdown
**Blocks:**
- TASK-010 [FS] - Integration tests need working register endpoint
- TASK-011 [FS] - Frontend signup form needs API endpoint
```

---

## Common Dependency Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| **Assumed knowledge** | "Obviously A needs B" | Document ALL dependencies explicitly |
| **Circular dependencies** | A→B→C→A | Extract shared logic, redesign |
| **Transitive assumptions** | "A needs B, B needs C, so A waits for C" | Document direct deps only, resolve transitively |
| **Over-dependency** | "Everything depends on Task 1" | Break Task 1 into smaller, independent pieces |
| **Hidden dependencies** | "Need API keys but not documented" | Include ALL prerequisites (code, data, access) |

---

## Dependency Template

```markdown
## Dependencies

**Depends on (must finish before this starts):**
- TASK-XXX [FS] - {Specific reason why needed}
- TASK-YYY [FS] - {Specific reason why needed}

**Start-to-Start (can start when these start):**
- TASK-ZZZ [SS] - {Reason for parallel start}

**Blocks (these wait for this to finish):**
- TASK-AAA - {What they need from this task}
- TASK-BBB - {What they need from this task}

**Prerequisites (not other tasks):**
- [ ] Database access configured
- [ ] API keys available in .env
- [ ] Design mockups approved (see #123)
```

---

## Quality Checklist

### Dependencies
- [ ] All dependencies explicit (FS/SS/FF)
- [ ] No circular dependencies
- [ ] Blocking tasks identified
- [ ] WHY documented for each dependency
- [ ] Prerequisites (non-task) listed

### Dependency Graph
- [ ] Graph drawn (text or diagram)
- [ ] Critical path identified
- [ ] Parallel opportunities noted

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hidden dependencies | List ALL dependencies explicitly |
| Circular dependencies | Redesign - split shared logic |

---

## Related Methodologies

| ID | Name | Relationship |
|----|------|--------------|
| task-creation | Task Creation | Creates tasks with dependencies |
| task-parallelization | Task Parallelization | Uses dependency graph for waves |
| dependency-management | Schedule Development | Source of dependency types |
| wbs-decomposition | Work Breakdown Structure | Dependency isolation principles |

---

## Agents

**faion-task-creator-agent:**
- Analyzes task dependencies
- Identifies circular dependencies
- Documents dependency relationships
- Triggers: "Analyze dependencies", "Check for circular deps"

---

*Methodology | SDD Foundation | Version 2.2.0*
*Integrates: PM (dependency-management, schedule-development, wbs-decomposition)*
