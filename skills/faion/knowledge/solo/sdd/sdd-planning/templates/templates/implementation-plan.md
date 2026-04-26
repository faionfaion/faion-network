# Implementation Plan: {Feature Name}

**Version:** 1.0
**Status:** Draft | Approved
**Design:** {link to design.md}
**Date:** YYYY-MM-DD

## Overview

- **Total tasks:** {N}
- **Complexity:** Low | Medium | High
- **Est. tokens:** ~{X}k total
- **Critical path:** TASK_001 -> TASK_003 -> TASK_005

## Task Summary

| Task | Name | Complexity | Est. Tokens | Depends On | Enables |
|------|------|------------|-------------|------------|---------|
| TASK_001 | {name} | Low | ~10k | - | TASK_003 |
| TASK_002 | {name} | Medium | ~25k | - | TASK_003 |
| TASK_003 | {name} | High | ~40k | 001, 002 | TASK_005 |

## Dependency Graph

```
TASK_001 -> TASK_003 -> TASK_005
TASK_002 -> TASK_003
TASK_004 -> TASK_005
```

## Execution Waves

### Wave 1 (Parallel)

| Task | Description | Est. Tokens |
|------|-------------|-------------|
| TASK_001 | {description} | ~10k |
| TASK_002 | {description} | ~25k |

**Checkpoint 1:** Verify {criteria}

### Wave 2 (Parallel)

| Task | Depends On | Description |
|------|------------|-------------|
| TASK_003 | 001, 002 | {description} |
| TASK_004 | - | {description} |

**Checkpoint 2:** Verify {criteria}

### Wave 3 (Sequential)

| Task | Depends On | Description |
|------|------------|-------------|
| TASK_005 | 003, 004 | {description} |

**Final Checkpoint:** All tests pass, all AC verified

## Tasks Detail

### TASK_001: {Name}

**Objective:** {Clear, single-agent executable goal}

**Dependencies:** None

**Files:**
| File | Action | Description |
|------|--------|-------------|
| {path} | CREATE | {what} |

**Acceptance Criteria:**
- [ ] AC-001.1: {criterion}
- [ ] AC-001.2: {criterion}

**Est. tokens:** ~10k

## Quality Gates

| Gate | Task | Criteria |
|------|------|----------|
| Checkpoint 1 | After Wave 1 | {criteria} |
| Final | After Wave 3 | All tests pass |

## FR/AD Coverage

| FR | Task(s) | AD | Status |
|----|---------|-----|--------|
| FR-001 | TASK_001, TASK_003 | AD-1 | Planned |

## Risks

| Risk | Impact | Mitigation | Contingency |
|------|--------|------------|-------------|
| {risk} | {impact} | {mitigation} | {if occurs} |
