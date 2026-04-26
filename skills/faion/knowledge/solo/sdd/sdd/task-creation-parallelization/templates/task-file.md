# TASK_XXX: {Title}
<!-- SUMMARY: {One sentence describing business value} -->

## Metadata

| Field | Value |
|-------|-------|
| **Complexity** | simple / normal / complex |
| **Est. Tokens** | ~Xk |
| **Priority** | P0 / P1 / P2 |
| **Feature** | {feature-NNN-name} |

## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | {relevant sections} |
| Spec | `.aidocs/{status}/{feature}/spec.md` | FR-X, FR-Y |
| Design | `.aidocs/{status}/{feature}/design.md` | AD-X, AD-Y |

## Task Dependency Tree

**This task depends on:** (read summaries before starting)

```
TASK_YYY ({title})
    Status: DONE
    Summary: {what was accomplished}
    Files: {files created/modified}
    Patterns: {patterns to follow}
    Key code:
    ```{lang}
    {critical code snippet, max 10 lines}
    ```
```

## Recommended Skills & Methodologies

**Skills:**
| Skill | Purpose |
|-------|---------|
| faion-{skill} | {when to use} |

---

## Requirements Coverage

### FR-X: {requirement title}
{Full text of requirement from spec.md}

## Architecture Decisions

### AD-X: {decision title}
{Full text of decision from design.md}

---

## Description

{Clear description of what needs to be done, 2-4 sentences}

**Business value:** {From spec.md problem statement}

---

## Context

### Related Files (from research)

| File | Purpose | Patterns to Follow |
|------|---------|-------------------|
| `path/to/similar.py` | Similar implementation | Pattern X, Y |

---

## Goals

1. {Specific, measurable goal}
2. {Specific, measurable goal}
3. {Specific, measurable goal}

---

## Acceptance Criteria

**AC-1: {Scenario name}**
- Given: {precondition}
- When: {action}
- Then: {expected result}

**AC-2: {Error scenario}**
- Given: {precondition}
- When: {action}
- Then: {error handling}

---

## Dependencies

**Depends on (FS):**
- TASK_YYY [FS] - {reason}

**Blocks:**
- TASK_ZZZ - {reason}

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | `path/to/new_file.py` | {description} |
| MODIFY | `path/to/existing.py` | {what changes} |

---

## Estimated Context

| Phase | Tokens | Notes |
|-------|--------|-------|
| SDD Docs | ~Xk | constitution, spec, design |
| Dependency Tree | ~Xk | dependency summaries |
| Research | ~Xk | existing patterns |
| Implementation | ~Xk | coding |
| Testing | ~Xk | verification |
| **Total** | ~Xk | Must be <100k |

---

## Subtasks

- [ ] 01. Research: {description}
- [ ] 02. Implement: {description}
- [ ] 03. Test: {description}
- [ ] 04. Verify: {description}

---

## Summary
<!-- Filled after completion -->

**What was done:**
- {Achievement 1}

**Patterns established:**
- {Pattern for future tasks}

**Files changed:**
- `path/file.py` (CREATE, X lines)
