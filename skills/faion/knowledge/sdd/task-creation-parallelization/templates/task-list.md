# {feature-NNN-name}: Task Overview

| Field | Value |
|-------|-------|
| **Feature** | {feature-NNN-name} |
| **Spec** | `.aidocs/{status}/{feature}/spec.md` |
| **Design** | `.aidocs/{status}/{feature}/design.md` |
| **Total tasks** | {N} |
| **Waves** | {W} |

## Dependency Graph

```
Wave 1 (parallel):  TASK_001  TASK_002  TASK_003
                        \        |        /
Wave 2 (parallel):    TASK_004  TASK_005
                             \    /
Wave 3 (sequential):       TASK_006
```

## Task Status

| Task | Title | Wave | Depends On | Status | Tokens |
|------|-------|------|-----------|--------|--------|
| TASK_001 | {title} | 1 | none | TODO | ~{X}k |
| TASK_002 | {title} | 1 | none | TODO | ~{X}k |
| TASK_003 | {title} | 1 | none | TODO | ~{X}k |
| TASK_004 | {title} | 2 | TASK_001, TASK_002 | TODO | ~{X}k |
| TASK_005 | {title} | 2 | TASK_002, TASK_003 | TODO | ~{X}k |
| TASK_006 | {title} | 3 | TASK_004, TASK_005 | TODO | ~{X}k |

**Status values:** TODO / IN-PROGRESS / DONE / BLOCKED

## Requirements Coverage

| FR | Requirement | Tasks |
|----|-------------|-------|
| FR-1 | {requirement title} | TASK_001, TASK_004 |
| FR-2 | {requirement title} | TASK_002, TASK_005 |
| FR-3 | {requirement title} | TASK_003, TASK_006 |

## Wave Execution Notes

**Wave 1:** Run in parallel. No shared file writes. Each task creates new files only.

**Wave 2:** Run after all Wave 1 tasks are DONE. May modify files created in Wave 1.

**Wave 3:** Sequential. Integrates outputs from all prior waves.

## Pattern Registry

Patterns established by Wave 1 that later waves must follow:

| Pattern | Established By | Used By |
|---------|---------------|---------|
| {pattern name} | TASK_001 | TASK_004, TASK_006 |
| {pattern name} | TASK_002 | TASK_005 |
