# Task Templates

Ready-to-use templates for task files and task lists.

---

## Task File Template v3.0

Copy and customize for each task.

```markdown
# TASK_XXX: {Title}
<!-- SUMMARY: {One sentence describing business value} -->

## Metadata

| Field | Value |
|-------|-------|
| **Complexity** | simple / normal / complex |
| **Est. Tokens** | ~Xk |
| **Priority** | P0 / P1 / P2 |
| **Created** | YYYY-MM-DD |
| **Feature** | {feature-NNN-name} |

---

## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | {relevant sections} |
| Spec | `.aidocs/{status}/{feature}/spec.md` | FR-X, FR-Y |
| Design | `.aidocs/{status}/{feature}/design.md` | AD-X, AD-Y |

## Task Dependency Tree

**This task depends on:** (read summaries before starting)

```
TASK_YYY ({title}) ────────────────────────┐
    Status: DONE                           │
    Summary: {what was accomplished}       │
    Files: {files created/modified}        │
    Patterns: {patterns to follow}         │
    Key code:                              │
    ```{lang}                              ↓
    {critical code snippet}           TASK_XXX
    ```                               (THIS TASK)
                                           ↑
TASK_ZZZ ({title}) ────────────────────────┘
    Status: DONE
    Summary: {what was accomplished}
    Files: {files created/modified}
```

**Dependency files to read:**
- `.aidocs/done/TASK_YYY_{slug}.md` -> Summary section
- `.aidocs/done/TASK_ZZZ_{slug}.md` -> Summary section

## Recommended Skills & Methodologies

**Skills:**
| Skill | Purpose |
|-------|---------|
| faion-{skill} | {when to use} |

**Methodologies:**
| ID | Name | Purpose |
|----|------|---------|
| {method-id} | {Method Name} | {how it helps} |

---

## Requirements Coverage

### FR-X: {requirement title}
{Full text of requirement from spec.md}

### NFR-X: {non-functional requirement}
{Full text if applicable}

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

### Code Dependencies
- `module.Class` - {why needed}
- `library` - {version constraint if any}

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

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk} | Low/Med/High | Low/Med/High | {Strategy} |

## Potential Blockers
- [ ] {Blocker description}

---

## Out of Scope

- {Explicit exclusion 1}
- {Explicit exclusion 2}

---

## Testing

| Type | Description | File |
|------|-------------|------|
| Unit | {What to test} | `tests/unit/test_*.py` |
| Integration | {What to test} | `tests/integration/test_*.py` |

**Test commands:**
```bash
pytest tests/unit/test_{module}.py -v
```

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

## Implementation
<!-- Filled by executor during execution -->

### Subtask 01: Research
{Findings, patterns discovered}

### Subtask 02: Implement
{Key decisions, code written}

---

## Summary
<!-- Filled after completion -->

**Completed:** YYYY-MM-DD

**What was done:**
- {Achievement 1}
- {Achievement 2}

**Key decisions:**
- {Decision and rationale}

**Files changed:**
- `path/file.py` (CREATE, X lines)
- `path/file2.py` (MODIFY, +Y lines)

**Patterns established:**
- {Pattern for future tasks to follow}

**Test results:**
- All tests pass
- Coverage: X%

---

## Lessons Learned
<!-- Optional: patterns/mistakes for memory -->

**Patterns:**
- {Reusable pattern discovered}

**Mistakes:**
- {What went wrong and fix}
```

---

## Task List Template

Overview document for feature task tracking.

```markdown
# Tasks: {Feature Name}

## Summary

| Total | TODO | In Progress | Done | Blocked |
|-------|------|-------------|------|---------|
| {n} | {n} | {n} | {n} | {n} |

**Est. Total Tokens:** ~{X}k
**Critical Path Tokens:** ~{Y}k

---

## Dependency Graph

```
TASK-001 ──[FS]──→ TASK-003 ──[FS]──→ TASK-005
    │                  │                  │
    ↓                  ↓                  ↓
TASK-002 ──[FS]──→ TASK-004 ──[FS]──→ TASK-006
```

---

## Parallel Waves

**Wave 1** (can start immediately):
| ID | Title | Tokens | Deps |
|----|-------|--------|------|
| TASK-001 | {title} | ~Xk | - |
| TASK-002 | {title} | ~Xk | - |

**Wave 2** (after Wave 1):
| ID | Title | Tokens | Deps |
|----|-------|--------|------|
| TASK-003 | {title} | ~Xk | TASK-001 |
| TASK-004 | {title} | ~Xk | TASK-002 |

**Wave 3** (after Wave 2):
| ID | Title | Tokens | Deps |
|----|-------|--------|------|
| TASK-005 | {title} | ~Xk | TASK-003 |
| TASK-006 | {title} | ~Xk | TASK-004 |

**Critical Path:** Wave 1 → Wave 2 → Wave 3 = ~{X}k tokens minimum

---

## Task Status

### TODO
| ID | Title | Tokens | Wave | Skills |
|----|-------|--------|------|--------|
| TASK-001 | {title} | ~Xk | 1 | faion-{skill} |

### IN_PROGRESS
| ID | Title | Assignee | Started |
|----|-------|----------|---------|
| - | - | - | - |

### DONE
| ID | Title | Completed |
|----|-------|-----------|
| - | - | - |

### BLOCKED
| ID | Title | Blocker |
|----|-------|---------|
| - | - | - |

---

## Requirements Coverage

| FR | Description | Tasks |
|----|-------------|-------|
| FR-1 | {requirement} | TASK-001, TASK-003 |
| FR-2 | {requirement} | TASK-002, TASK-004 |

---

## Notes

{Any additional context for task execution}
```

---

## Minimal Task Template (Simple Tasks)

For simple tasks that don't need full template.

```markdown
# TASK_XXX: {Title}

| Field | Value |
|-------|-------|
| **Complexity** | simple |
| **Est. Tokens** | ~{X}k |
| **Depends on** | {TASK-YYY or "none"} |

## Description

{2-3 sentences describing what to do}

## Acceptance Criteria

**AC-1: {Happy path}**
- Given: {precondition}
- When: {action}
- Then: {result}

## Files to Change

| Action | File |
|--------|------|
| CREATE | `path/to/file.py` |

## Summary
<!-- Filled after completion -->
```

---

## Research Task Template

For tasks that produce documentation, not code.

```markdown
# TASK_XXX: Research - {Topic}

| Field | Value |
|-------|-------|
| **Complexity** | normal |
| **Est. Tokens** | ~{X}k |
| **Type** | Research |

## Objective

{What decision or information is needed}

## Questions to Answer

1. {Question 1}
2. {Question 2}
3. {Question 3}

## Research Scope

**Include:**
- {What to research}

**Exclude:**
- {What NOT to research}

## Deliverables

- [ ] ADR document with recommendation
- [ ] Comparison table of options
- [ ] Next tasks to create based on findings

## Acceptance Criteria

**AC-1: Decision documented**
- Given: Research completed
- When: ADR is reviewed
- Then: Clear recommendation with rationale

---

## Findings
<!-- Filled during execution -->

### Option A: {Name}
**Pros:** {list}
**Cons:** {list}

### Option B: {Name}
**Pros:** {list}
**Cons:** {list}

## Recommendation

{Chosen option and rationale}

## Next Tasks

Based on this research, create:
- TASK-XXX: {title based on decision}
- TASK-YYY: {title based on decision}
```

---

## Wave Execution Script

Bash script for tracking wave execution.

```bash
#!/bin/bash
# wave-tracker.sh - Track task wave execution

FEATURE_DIR=".aidocs/in-progress/feature-XXX-name"
TASKS_DIR="$FEATURE_DIR/tasks"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=== Wave Execution Tracker ==="
echo ""

# Wave 1
echo -e "${YELLOW}Wave 1 (No dependencies):${NC}"
for task in TASK-001 TASK-002; do
    if [ -f "$TASKS_DIR/done/${task}_*.md" ]; then
        echo -e "  ${GREEN}[DONE]${NC} $task"
    elif [ -f "$TASKS_DIR/in-progress/${task}_*.md" ]; then
        echo -e "  ${YELLOW}[IN PROGRESS]${NC} $task"
    else
        echo -e "  ${RED}[TODO]${NC} $task"
    fi
done

echo ""

# Wave 2
echo -e "${YELLOW}Wave 2 (Depends on Wave 1):${NC}"
for task in TASK-003 TASK-004; do
    if [ -f "$TASKS_DIR/done/${task}_*.md" ]; then
        echo -e "  ${GREEN}[DONE]${NC} $task"
    elif [ -f "$TASKS_DIR/in-progress/${task}_*.md" ]; then
        echo -e "  ${YELLOW}[IN PROGRESS]${NC} $task"
    else
        echo -e "  ${RED}[TODO]${NC} $task"
    fi
done

echo ""
echo "=== Summary ==="
DONE=$(find "$TASKS_DIR/done" -name "TASK-*.md" 2>/dev/null | wc -l)
IN_PROGRESS=$(find "$TASKS_DIR/in-progress" -name "TASK-*.md" 2>/dev/null | wc -l)
TODO=$(find "$TASKS_DIR/todo" -name "TASK-*.md" 2>/dev/null | wc -l)
TOTAL=$((DONE + IN_PROGRESS + TODO))

echo "Done: $DONE / $TOTAL"
echo "In Progress: $IN_PROGRESS"
echo "TODO: $TODO"
```

---

## Task Numbering Convention

```
TASK-{FEATURE_PREFIX}-{NUMBER}

Examples:
- TASK-AUTH-001 (Authentication feature, task 1)
- TASK-SEARCH-001 (Search feature, task 1)
- TASK-SK-001 (Starter Kits feature, task 1)
- TASK-KI-001 (Knowledge Infrastructure, task 1)

File naming:
TASK_{NUMBER}_{slug}.md

Examples:
- TASK_001_create_users_table.md
- TASK_002_implement_password_hashing.md
```

---

## Complexity Guidelines

| Complexity | Tokens | Files | Decisions | Example |
|------------|--------|-------|-----------|---------|
| simple | <30k | 1-2 | 0 | Add migration, create model |
| normal | 30-60k | 2-4 | 1-2 | Implement endpoint, add tests |
| complex | 60-100k | 4+ | 3+ | Design pattern, architecture |

**Upgrade triggers:**
- Multiple architecture decisions needed -> complex
- Cross-cutting concerns (auth, logging) -> complex
- Unfamiliar library/API -> complex
- Many edge cases to handle -> complex

---

*Templates v3.0.0 | Ready for copy-paste*
