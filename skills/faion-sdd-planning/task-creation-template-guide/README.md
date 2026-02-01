# Task Creation Template Guide

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Build task dependency trees | sonnet | Medium-complexity task relationship analysis |
| Create task templates | haiku | Template-based mechanical generation |
| Estimate task complexity | sonnet | Medium-complexity analysis and judgment |
| Identify risks and blockers | sonnet | Medium-complexity risk assessment |
| Generate task files from plan | haiku | Mechanical template instantiation |

## Context Management (for AI Execution)

### Context Budget

| Phase | Budget | Purpose |
|-------|--------|---------|
| **SDD Docs** | 15% | constitution, spec, design |
| **Task Tree** | 10% | completed dependency tasks |
| **Research** | 25% | existing code patterns |
| **Implementation** | 40% | actual coding |
| **Testing** | 10% | verification |

**Total:** <100k tokens per task

### Reference Documents with Task Dependency Tree

**CRITICAL:** Each task MUST include the full dependency tree of completed tasks.

```markdown
## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Code standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, FR-Y |
| Design | `{FEATURE_DIR}/design.md` | AD-X, AD-Y |
| Contracts | `.aidocs/contracts.md` | (if API) |

## Task Dependency Tree

**This task depends on:**

```
TASK-001 (DB Tables) ─────────────────────┐
    Summary: Created users, sessions tables│
    Files: migrations/001_*.py            │
    Patterns: AlterField for nullable     │
                                          ↓
TASK-003 (User Model) ──────────→ TASK-005 (THIS TASK)
    Summary: User model with validation
    Files: models/user.py
    Patterns: BaseModel, email validator
    Key code:
    ```python
    class User(BaseModel):
        email = models.EmailField(unique=True)
    ```
```

**Read these task summaries before starting:**
- `{TASKS_DIR}/done/TASK_001_db_tables.md` → Summary section
- `{TASKS_DIR}/done/TASK_003_user_model.md` → Summary section

## Recommended Skills

| Skill | When to Use |
|-------|-------------|
| faion-software-developer | Code implementation |
| faion-devops-engineer | CI/CD, Docker, infra |
| faion-ml-engineer | AI/LLM integration |

## Recommended Methodologies

| ID | Name | Purpose |
|----|------|---------|
| code-review | Python Best Practices | Code standards |
| shadcn-ui-components | shadcn/ui Components | UI implementation |
| docker-patterns | Docker Patterns | Containerization |
```

### Task Tree Content Requirements

For each completed dependency task, include:

| Field | Purpose | Example |
|-------|---------|---------|
| **Summary** | What was done | "Created User model with email validation" |
| **Files** | What was created/modified | `models/user.py`, `migrations/002_*.py` |
| **Patterns** | Reusable patterns discovered | "BaseModel inheritance", "email validator" |
| **Key code** | Critical code snippets | Class definition, key functions |
| **Decisions** | Implementation decisions made | "Used UUID for PK instead of auto-increment" |

### Why Task Tree is Critical

| Without Task Tree | With Task Tree |
|-------------------|----------------|
| Agent re-discovers patterns | Agent reuses established patterns |
| Inconsistent implementations | Consistent code style |
| Duplicate research effort | Builds on prior work |
| Context wasted on discovery | Context used for implementation |
| May contradict earlier tasks | Aligned with earlier decisions |

---

## Risk & Blocker Pre-identification

```markdown
## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API rate limits | Medium | High | Implement retry with backoff |
| Schema migration fails | Low | High | Test on staging first |

## Potential Blockers
- [ ] External API access required (need credentials)
- [ ] Design decision AD-3 unclear (ask PO)
```

---

## Enhanced Task Template v2.0

```markdown
# TASK_XXX: {Title}
<!-- SUMMARY: {One sentence business value} -->

## Metadata
| Field | Value |
|-------|-------|
| **Complexity** | simple / normal / complex |
| **Effort** | X hours |
| **Priority** | P0 / P1 / P2 |
| **Created** | YYYY-MM-DD |
| **Project** | {project} |
| **Feature** | {feature} |

---

## SDD References

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Code standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X, FR-Y |
| Design | `{FEATURE_DIR}/design.md` | AD-X, AD-Y |
| Contracts | `.aidocs/contracts.md` | (if API) |

## Task Dependency Tree

**This task depends on:** (read summaries before starting)

```
TASK_YYY ({title}) ────────────────────────┐
    Status: DONE                           │
    Summary: {what was done}               │
    Files: {files created/modified}        │
    Patterns: {patterns to follow}         │
    Key decisions: {decisions made}        ↓
                                     TASK_XXX (THIS TASK)
TASK_ZZZ ({title}) ────────────────────────┘
    Status: DONE
    Summary: {what was done}
    Files: {files created/modified}
    Key code:
    ```{lang}
    {critical code snippet}
    ```
```

**Dependency task files:**
- `{TASKS_DIR}/done/TASK_YYY_{slug}.md` → Read Summary section
- `{TASKS_DIR}/done/TASK_ZZZ_{slug}.md` → Read Summary section

## Recommended Skills & Methodologies

**Skills:**
| Skill | Purpose |
|-------|---------|
| faion-{skill} | {When to use} |

**Methodologies:**
| ID | Name | Purpose |
|----|------|---------|
| M-XXX-YYY | {Name} | {How it helps} |

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

**AC-2: {Scenario name}**
- Given: {precondition}
- When: {action}
- Then: {expected result}

---

## Dependencies

**Depends on (FS = Finish-to-Start):**
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
| {Risk description} | Low/Med/High | Low/Med/High | {Mitigation strategy} |

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

---

## Estimated Context

| Phase | Tokens | Notes |
|-------|--------|-------|
| SDD Docs | ~Xk | constitution, spec, design |
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

**Test results:**
- All tests pass
- Coverage: X%

---

## Lessons Learned
<!-- Optional: patterns/mistakes for .aidocs/memory/ -->

**Patterns:**
- {Reusable pattern discovered}

**Mistakes:**
- {What went wrong and fix}
```

---

## Sources

- [Context Window Management](https://platform.openai.com/docs/guides/prompt-engineering) - OpenAI prompt engineering guide
- [Token Counting Tools](https://platform.openai.com/tokenizer) - Token estimation
- [Task Decomposition Patterns](https://www.extremeprogramming.org/rules/userstories.html) - XP user story breakdown
- [Risk Management in Agile](https://www.scrumalliance.org/community/articles/2020/august/managing-risk-in-agile-projects) - Risk identification
- [Technical Debt Documentation](https://martinfowler.com/bliki/TechnicalDebt.html) - Documenting decisions
