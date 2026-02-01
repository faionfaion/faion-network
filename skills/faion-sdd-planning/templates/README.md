# SDD Document Templates

All templates for SDD artifacts. Copy and customize for your project.

---

## Core Templates

### Specification Template
**File:** [template-spec.md](template-spec.md)
**Purpose:** Define WHAT and WHY - feature requirements and acceptance criteria
**Use when:** Starting a new feature

### Design Document Template
**File:** [template-design.md](template-design.md)
**Purpose:** Define HOW - technical approach and architecture decisions
**Use when:** After spec is approved

### Task File Template
**File:** [template-task.md](template-task.md)
**Purpose:** Atomic work units for agent execution (100k token rule)
**Use when:** After implementation plan is created

---

## Constitution Template

```markdown
# Constitution: {Project Name}

**Version:** 1.0
**Created:** YYYY-MM-DD
**Status:** Active

---

## Vision

{1-2 sentences: what is this project and why does it exist}

---

## Tech Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | {lang} | {ver} | {why} |
| Framework | {framework} | {ver} | {why} |
| Database | {db} | {ver} | {why} |
| Hosting | {platform} | - | {why} |

---

## Architecture Patterns

| Pattern | Description |
|---------|-------------|
| {pattern} | {brief explanation} |

---

## Code Standards

### Naming Conventions
- Files: `{convention}`
- Classes: `{convention}`
- Functions: `{convention}`
- Variables: `{convention}`

### Formatting
- Formatter: {tool}
- Linter: {tool}
- Config: {location}

### Testing
- Framework: {framework}
- Coverage target: {X}%
- Test location: {path}

---

## Git Workflow

- Branch strategy: {strategy}
- Commit format: `{format}`
- PR requirements: {requirements}

---

## Project Structure

```
{project}/
├── {folder}/     # {purpose}
├── {folder}/     # {purpose}
└── {folder}/     # {purpose}
```

---

## Quality Gates

| Gate | Criteria | When |
|------|----------|------|
| Lint | Zero errors | Pre-commit |
| Types | Zero errors | Pre-commit |
| Tests | 100% pass | Pre-push |
| Coverage | >{X}% | Pre-merge |

---

## Principles

1. {Principle 1}
2. {Principle 2}
3. {Principle 3}
```

---

## Implementation Plan Template

```markdown
# Implementation Plan: {Feature Name}

**Version:** 1.0
**Status:** Draft | Approved
**Design:** {link to design.md}
**Date:** YYYY-MM-DD

---

## Overview

- **Total tasks:** {N}
- **Complexity:** Low | Medium | High
- **Est. tokens:** ~{X}k total
- **Critical path:** TASK_001 -> TASK_003 -> TASK_005

---

## Task Summary

| Task | Name | Complexity | Est. Tokens | Depends On | Enables |
|------|------|------------|-------------|------------|---------|
| TASK_001 | {name} | Low | ~10k | - | TASK_003 |
| TASK_002 | {name} | Medium | ~25k | - | TASK_003 |
| TASK_003 | {name} | High | ~40k | 001, 002 | TASK_005 |

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

### Wave 3 (Sequential - Critical Path)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_005 | 003, 004 | {description} |

**Final Checkpoint:** All tests pass, all AC verified

---

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

### TASK_002: {Name}
...

---

## Quality Gates

| Gate | Task | Criteria |
|------|------|----------|
| Checkpoint 1 | After Wave 1 | {criteria} |
| Checkpoint 2 | After Wave 2 | {criteria} |
| Final | After Wave 3 | All tests pass |

---

## FR/AD Coverage

| FR | Task(s) | AD | Status |
|----|---------|-----|--------|
| FR-001 | TASK_001, TASK_003 | AD-1 | Planned |
| FR-002 | TASK_002 | AD-2 | Planned |

---

## Risks

| Risk | Impact | Mitigation | Contingency |
|------|--------|------------|-------------|
| {risk} | {impact} | {mitigation} | {if occurs} |
```

---

## Roadmap Template

```markdown
# Roadmap: {Project Name}

**Last Updated:** YYYY-MM-DD

---

## Vision

{1-2 sentences: where is this project going}

---

## Now (This Quarter) - 90% Confident

| Feature | Status | Target | Notes |
|---------|--------|--------|-------|
| {NN}-{feature} | In Progress | {month} | {notes} |
| {NN}-{feature} | Todo | {month} | {notes} |

---

## Next (Next Quarter) - 70% Confident

| Feature | Description | Dependencies |
|---------|-------------|--------------|
| {feature} | {one-liner} | {deps} |

---

## Later (Future) - 50% Confident

| Theme | Description |
|-------|-------------|
| {theme} | {high-level goal} |

---

## Done

| Feature | Completed | Highlights |
|---------|-----------|------------|
| {NN}-{feature} | YYYY-MM | {key outcome} |

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk} | {impact} | {mitigation} |

---

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| {metric} | {value} | {goal} |
```

---

## Backlog Item Template

```markdown
## BL-{NNN}: {Title}

**Priority:** P0 | P1 | P2 | P3
**Estimate:** {points} pts | {T-shirt size}
**Status:** grooming | ready | in-progress | done

---

### Problem

{What need does this address}

---

### Acceptance Criteria

- [ ] {criterion 1}
- [ ] {criterion 2}

---

### Dependencies

- Requires: BL-{XXX}
- Blocks: BL-{YYY}

---

### Notes

{Additional context}
```

---

## Confidence Check Template

```markdown
## Confidence Check: {Phase}

**Date:** YYYY-MM-DD
**Phase:** Pre-Spec | Pre-Design | Pre-Task | Pre-Implementation

---

### Score: {X}%

| Check | Weight | Status | Evidence |
|-------|--------|--------|----------|
| {check} | {X}% | Pass/Warn/Fail | {evidence or gap} |
| {check} | {X}% | Pass/Warn/Fail | {evidence or gap} |

---

### Verdict: Proceed | Clarify | Stop

---

### Questions to Answer First

1. {question}
2. {question}

---

### Recommended Actions

- {action}
- {action}
```

---

## Pattern Record Template

```json
{
  "id": "PAT-{NNN}",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "{project}",
  "task_type": "{type}",
  "pattern_name": "{name}",
  "description": "{what worked}",
  "context": "{when to use}",
  "code_example": "{code snippet}",
  "success_count": 1,
  "tags": ["tag1", "tag2"]
}
```

---

## Mistake Record Template

```json
{
  "id": "ERR-{NNN}",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "project": "{project}",
  "task_type": "{type}",
  "error_type": "{category}",
  "description": "{what went wrong}",
  "root_cause": "{why it happened}",
  "solution": "{how to fix}",
  "prevention": "{how to prevent}",
  "occurrence_count": 1,
  "tags": ["tag1", "tag2"]
}
```

---

## Token Estimation Guide

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

**Rule:** If uncertain, estimate higher and split.

**100k Token Budget:**
```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |
## Related Files

- [template-spec.md](template-spec.md) - Specification template (WHAT and WHY)
- [template-design.md](template-design.md) - Design document template (HOW)
- [template-task.md](template-task.md) - Task file template (100k token rule)
- [workflows.md](workflows.md) - Step-by-step workflow instructions
- [writing-specifications.md](writing-specifications.md) - How to write specs
- [design-doc-structure.md](design-doc-structure.md) - How to write design docs
- [writing-implementation-plans.md](writing-implementation-plans.md) - How to write impl plans

---

*SDD Templates v2.0*
*Use with faion-sdd skill*
