# Implementation Plan Template

Task breakdown with dependencies and execution order. Copy after design approval.

---

```markdown
---
version: "1.0"
status: draft | approved
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: {name}
feature: {feature-NNN-slug}
design: design.md
---

# Implementation Plan: {Feature Name}

## Reference Documents

| Document | Path |
|----------|------|
| Specification | `spec.md` |
| Design | `design.md` |
| Constitution | `.aidocs/constitution.md` |

---

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | {N} |
| Complexity | Low / Medium / High |
| Est. Tokens | ~{X}k total |
| Critical Path | TASK_001 -> TASK_003 -> TASK_005 |
| Parallel Potential | {X} waves |

---

## Task Summary

| Task | Name | Complexity | Est. Tokens | Depends On | Enables |
|------|------|------------|-------------|------------|---------|
| TASK_001 | {name} | Low | ~10k | - | TASK_003 |
| TASK_002 | {name} | Medium | ~25k | - | TASK_003 |
| TASK_003 | {name} | High | ~40k | 001, 002 | TASK_005 |
| TASK_004 | {name} | Low | ~15k | - | TASK_005 |
| TASK_005 | {name} | Medium | ~20k | 003, 004 | - |

---

## Dependency Graph

```
TASK_001 ──┬──> TASK_003 ──┐
           │               │
TASK_002 ──┘               ├──> TASK_005
                           │
TASK_004 ─────────────────┘
```

---

## Execution Waves

### Wave 1: Foundation (Parallel)

| Task | Description | Est. Tokens | Files |
|------|-------------|-------------|-------|
| TASK_001 | {description} | ~10k | {files} |
| TASK_002 | {description} | ~25k | {files} |
| TASK_004 | {description} | ~15k | {files} |

**Wave 1 Total:** ~50k tokens
**Parallelization:** 3 agents

**Checkpoint 1:**
- [ ] All files from Wave 1 exist
- [ ] Unit tests pass
- [ ] No lint errors

### Wave 2: Integration (Parallel)

| Task | Depends On | Description | Est. Tokens |
|------|------------|-------------|-------------|
| TASK_003 | 001, 002 | {description} | ~40k |

**Wave 2 Total:** ~40k tokens
**Parallelization:** 1 agent

**Checkpoint 2:**
- [ ] Integration tests pass
- [ ] Components connect correctly

### Wave 3: Finalization (Sequential)

| Task | Depends On | Description | Est. Tokens |
|------|------------|-------------|-------------|
| TASK_005 | 003, 004 | {description} | ~20k |

**Wave 3 Total:** ~20k tokens
**Parallelization:** 1 agent (critical path)

**Final Checkpoint:**
- [ ] All acceptance criteria verified
- [ ] All tests pass
- [ ] Coverage targets met
- [ ] Documentation updated

---

## Tasks Detail

### TASK_001: {Name}

**Objective:**
{Clear, single-agent executable goal - what exactly to implement}

**Complexity:** Low
**Est. Tokens:** ~10k
**Dependencies:** None
**Enables:** TASK_003

**Requirements Covered:**
- FR-001: {requirement text}

**Files:**

| File | Action | Description |
|------|--------|-------------|
| `{path/to/file.py}` | CREATE | {what to create} |
| `{path/to/test.py}` | CREATE | {test coverage} |

**Acceptance Criteria:**
- [ ] AC-001.1: {Given-When-Then or criterion}
- [ ] AC-001.2: {Given-When-Then or criterion}

**Technical Notes:**
- {Implementation hint 1}
- {Implementation hint 2}

---

### TASK_002: {Name}

**Objective:**
{Clear, single-agent executable goal}

**Complexity:** Medium
**Est. Tokens:** ~25k
**Dependencies:** None
**Enables:** TASK_003

**Requirements Covered:**
- FR-002: {requirement text}
- FR-003: {requirement text}

**Files:**

| File | Action | Description |
|------|--------|-------------|
| `{path/to/file.py}` | CREATE | {what} |
| `{path/to/existing.py}` | MODIFY | {what to modify} |

**Acceptance Criteria:**
- [ ] AC-002.1: {criterion}
- [ ] AC-002.2: {criterion}

---

### TASK_003: {Name}

**Objective:**
{Clear, single-agent executable goal}

**Complexity:** High
**Est. Tokens:** ~40k
**Dependencies:** TASK_001, TASK_002
**Enables:** TASK_005

**Dependency Summary:**
- TASK_001 provides: {what it outputs}
- TASK_002 provides: {what it outputs}

**Requirements Covered:**
- FR-004: {requirement text}

**Files:**

| File | Action | Description |
|------|--------|-------------|
| `{path}` | MODIFY | {what} |
| `{path}` | CREATE | {what} |

**Acceptance Criteria:**
- [ ] AC-003.1: {criterion}
- [ ] AC-003.2: {criterion}

---

### TASK_004: {Name}

{Continue pattern for each task}

---

### TASK_005: {Name}

**Objective:**
{Clear, single-agent executable goal}

**Complexity:** Medium
**Est. Tokens:** ~20k
**Dependencies:** TASK_003, TASK_004
**Enables:** None (Final task)

**Dependency Summary:**
- TASK_003 provides: {what}
- TASK_004 provides: {what}

**Requirements Covered:**
- FR-005: {requirement text}

**Files:**

| File | Action | Description |
|------|--------|-------------|
| `{path}` | MODIFY | {what} |

**Acceptance Criteria:**
- [ ] AC-005.1: {criterion}
- [ ] AC-005.2: {criterion}

---

## Quality Gates

| Gate | After | Criteria | Blocks |
|------|-------|----------|--------|
| Checkpoint 1 | Wave 1 | Unit tests pass, lint clean | Wave 2 |
| Checkpoint 2 | Wave 2 | Integration tests pass | Wave 3 |
| Final | Wave 3 | All AC verified, coverage met | Release |

---

## FR/AD Coverage

| FR | AD | Task(s) | Status |
|----|-----|---------|--------|
| FR-001 | AD-1 | TASK_001 | Planned |
| FR-002 | AD-1 | TASK_002 | Planned |
| FR-003 | AD-2 | TASK_002 | Planned |
| FR-004 | AD-2 | TASK_003 | Planned |
| FR-005 | AD-3 | TASK_005 | Planned |

---

## Risks

| Risk | Impact | Mitigation | Contingency |
|------|--------|------------|-------------|
| {risk} | {impact} | {mitigation} | {if it occurs} |

---

## Rollback Strategy

If implementation fails:
1. {Step 1}
2. {Step 2}
3. {Step 3}

---

*Implementation Plan v1.0*
*Feature: {feature-NNN-slug}*
```

---

## Usage Notes

### 100k Token Rule

Each task must complete within 100k token context:
- Research: ~20k (reading existing code)
- Task file: ~5k
- Implementation: ~50k
- Buffer: ~25k

If a task exceeds this, split it.

### Dependency Types

| Type | Symbol | Description |
|------|--------|-------------|
| Finish-to-Start | -> | B starts after A finishes |
| Parallel | // | Can run simultaneously |
| Critical Path | ** | Longest dependency chain |

### Wave Strategy

Group tasks into waves for parallel execution:
- **Wave 1**: Foundation tasks (no dependencies)
- **Wave 2**: Tasks depending on Wave 1
- **Wave N**: Final integration

Speedup: 1.8-3.5x depending on parallelization potential

### Token Estimation Guide

| Component | Typical Tokens |
|-----------|----------------|
| Django model (simple) | 5-10k |
| Django model (complex) | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Serializer | 5-15k |
| Test file | 20-40k |
| React component (simple) | 5-10k |
| React component (complex) | 15-30k |
| API endpoint | 10-20k |

**Rule:** When uncertain, estimate higher and split.
