<!--
purpose: Fully worked TASK_XXX skeleton (metadata, dependency tree, requirements coverage, out of scope, goals, acceptance criteria, risks, testing, implementation log, lessons learned) demonstrating the fill order this guide teaches.
consumes: templates/TASK_skeleton.md, spec.md, design.md per Prerequisites
produces: artefact conforming to content/02-output-contract.xml (task_id, fill_steps_completed, sections_present)
depends-on: content/01-core-rules.xml
token-budget-impact: ~1300-2000 tokens when loaded as context
-->

# TASK_XXX: <title>
<!-- SUMMARY: {One sentence business value delivered by this task} -->

## Metadata
| Field | Value |
|-------|-------|
| **Complexity** | simple / normal / complex |
| **Priority** | P0 / P1 / P2 |
| **Created** | YYYY-MM-DD |
| **Project** | <project> |
| **Feature** | <feature> |

---

## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Code standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, FR-Y |
| Design | `{FEATURE_DIR}/design.md` | AD-X, AD-Y |
| Contracts | `.aidocs/contracts.md` | (if API task) |

## Task Dependency Tree

**This task depends on:** (read summaries before starting)

```
TASK_YYY ({title}) ────────────────────┐
    Status: DONE                       │
    Summary: {what was done}           │
    Files: {files created/modified}    │
    Patterns: {patterns to follow}     ↓
                                TASK_XXX (THIS TASK)
TASK_ZZZ ({title}) ────────────────────┘
    Status: DONE
    Summary: {what was done}
    Key code:
    ```{lang}
    <critical_code_snippet>
    ```
```

**Read these before starting:**
- `{TASKS_DIR}/done/TASK_YYY.md` → Summary section
- `{TASKS_DIR}/done/TASK_ZZZ.md` → Summary section

## Recommended Skills

| Skill | Purpose |
|-------|---------|
| faion-<skill> | {When to use} |

---

## Requirements Coverage

### FR-X: <requirement_title>
{Full text of requirement from spec.md}

### AD-X: <decision_title>
{Full text of decision from design.md}

---

## Out of Scope

- {Explicit exclusion 1 — write BEFORE Goals}
- <explicit_exclusion_2>

---

## Description

{Clear description of what needs to be done, 2-4 sentences}

**Business value:** {From spec.md problem statement}

---

## Goals

1. {Specific, measurable goal}
2. {Specific, measurable goal}
3. {Specific, measurable goal}

---

## Acceptance Criteria

**AC-1: <scenario_name>** (covers FR-X)
- Given: <precondition>
- When: <action>
- Then: <expected_result>

**AC-2: <scenario_name>** (covers FR-Y)
- Given: <precondition>
- When: <action>
- Then: <expected_result>

---

## Dependencies

**Depends on (FS = Finish-to-Start):**
- TASK_YYY <fs> — <reason>

**Blocks:**
- TASK_ZZZ — <reason>

---

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | `path/to/new_file.py` | <description> |
| MODIFY | `path/to/existing.py` | <what_changes> |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| <risk> | Low/Med/High | Low/Med/High | <concrete_action> |

## Potential Blockers
- [ ] {Blocker — treat as exit condition, not checkbox}

---

## Testing

| Type | Description | File |
|------|-------------|------|
| Unit | {What to test} | `tests/unit/test_{slug}.py` |
| Integration | {What to test} | `tests/integration/test_{slug}.py` |

---

## Estimated Context

| Phase | Tokens | Notes |
|-------|--------|-------|
| SDD Docs | ~Xk | constitution, spec FR-X, design AD-X |
| Dependency Tree | ~Xk | prior task summaries + snippets |
| Research | ~Xk | existing code patterns |
| Implementation | ~Xk | coding |
| Testing | ~Xk | verification |
| **Total** | ~Xk | **Must be &lt; 100k** |

---

## Subtasks

- [ ] 01. Research: <description>
- [ ] 02. Implement: <description>
- [ ] 03. Test: <description>
- [ ] 04. Verify: <description>

---

## Implementation
<!-- Filled by executor during execution -->

### Subtask 01: Research
{Findings, patterns discovered}

### Subtask 02: Implement
{Key decisions, code written}

---

## Summary
<!-- Filled after completion — used by downstream tasks' dependency trees -->

**Completed:** YYYY-MM-DD

**What was done:**
- <achievement_1>
- <achievement_2>

**Key decisions:**
- {Decision and rationale}

**Files changed:**
- `path/file.py` (CREATE, X lines)
- `path/file2.py` (MODIFY, +Y lines)

**Test results:**
- All tests pass
- Coverage: X%

---

## Lessons Learned
<!-- Optional: patterns/mistakes for .aidocs/memory/ -->

**Patterns:**
- <reusable_pattern_discovered>

**Mistakes:**
- {What went wrong and fix}
