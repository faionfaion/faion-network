# Implementation Plan: [Feature Name]

<!-- Requires: spec.md (Approved) + design.md (Approved) before writing -->

## Metadata

- **feature:** FEAT-NNN
- **status:** draft
- **spec:** approved
- **design:** approved
- **created:** YYYY-MM-DD

## Prerequisites

| Type | Item | Status |
|------|------|--------|
| Infrastructure | ... | Ready / Pending |
| Environment | ... | Ready / Pending |
| Code dep | ... | Ready / Pending |

## Wave Summary

| Wave | Tasks | Parallel | Token Load |
|------|-------|----------|------------|
| 1 | TASK-001, TASK-002 | Yes | ~Xk + ~Xk |
| 2 | TASK-003 | No | ~Xk |

**Critical path:** TASK-001 → TASK-003 = ~Xk tokens

## Tasks

---

### TASK-001: [Action Verb + Target]

- **Complexity:** Simple / Normal / Complex
- **Tokens:** ~Xk
- **AD-X:** AD-001
- **FR-X:** FR-001
- **Depends on:** None
- **Blocks:** TASK-002

**Files:**
- CREATE `path/to/file.py` — purpose

**Acceptance Criteria:**
1. Given [...], when [...], then [...].
2. Given [...], when [...], then [...].

**Technical Notes:**
- Pattern reference or gotcha

---

### TASK-002: [Action Verb + Target]

- **Complexity:** Normal
- **Tokens:** ~Xk
- **AD-X:** AD-002
- **FR-X:** FR-002
- **Depends on:** TASK-001
- **Blocks:** None

**Files:**
- MODIFY `path/to/file.py` — what changes

**Acceptance Criteria:**
1. ...
2. ...

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | Low/Med/High | Low/Med/High | ... |

## Rollback Plan

1. Step 1 — verification
2. Step 2 — rollback trigger: _condition_
