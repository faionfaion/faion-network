# Task Decomposition Checklist

Step-by-step checklist for breaking down implementation plans into LLM-executable tasks.

---

## Phase 1: Pre-Decomposition

### 1.1 Gather Inputs

- [ ] Implementation plan reviewed and understood
- [ ] Spec.md FR-X requirements identified
- [ ] Design.md AD-X decisions understood
- [ ] Constitution.md standards loaded
- [ ] Existing codebase patterns researched

### 1.2 Understand Scope

- [ ] Total feature complexity assessed
- [ ] Approximate number of tasks estimated (n)
- [ ] Critical path dependencies identified
- [ ] Parallelization opportunities spotted

---

## Phase 2: Task Identification

### 2.1 Extract Tasks from Implementation Plan

For each component in the plan:

- [ ] Identify discrete deliverables
- [ ] Check: Can this be done independently?
- [ ] Check: Does this fit in 100k tokens?
- [ ] Check: Is there clear success criteria?

### 2.2 Apply Right-Size Rule

For each candidate task:

| Check | Question | Action if NO |
|-------|----------|--------------|
| Too big? | >100k tokens or >4 subtasks? | Split into smaller tasks |
| Too small? | <10k tokens, trivial? | Merge with related task |
| Clear boundary? | Input/output well-defined? | Add context or split |

### 2.3 INVEST Validation

For each task:

- [ ] **Independent** - No circular dependencies
- [ ] **Negotiable** - Implementation details flexible
- [ ] **Valuable** - Links to FR-X business value
- [ ] **Estimable** - Token budget assignable
- [ ] **Small** - Fits single context window
- [ ] **Testable** - Has Given-When-Then AC

---

## Phase 3: Dependency Mapping

### 3.1 Create Dependency Graph

- [ ] List all tasks as nodes
- [ ] Draw arrows for dependencies
- [ ] Label dependency types (FS/SS/FF/SF)
- [ ] Verify no circular dependencies

### 3.2 Identify Waves

```
Wave 1: Tasks with no dependencies
Wave 2: Tasks depending only on Wave 1
Wave 3: Tasks depending on Wave 1-2
...continue...
```

- [ ] Wave 1 identified (entry points)
- [ ] All tasks assigned to waves
- [ ] Critical path calculated

### 3.3 Validate Parallelization

For each wave:

- [ ] Tasks within wave are truly independent
- [ ] No hidden shared state
- [ ] No file conflicts

---

## Phase 4: Task Definition

### 4.1 Core Content

For each task:

- [ ] Title: Clear, action-oriented (verb + object)
- [ ] Description: 2-4 sentences, business context
- [ ] Goals: 3-5 specific, measurable items
- [ ] Out of Scope: Explicit exclusions

### 4.2 Traceability

- [ ] FR-X links added (from spec.md)
- [ ] AD-X links added (from design.md)
- [ ] NFR-X links added (if applicable)

### 4.3 Acceptance Criteria

For each task:

- [ ] AC-1: Happy path (Given-When-Then)
- [ ] AC-2+: Alternative paths
- [ ] Error cases covered
- [ ] Boundary conditions covered
- [ ] Test commands specified

### 4.4 Files to Change

| Column | Content |
|--------|---------|
| Action | CREATE / MODIFY / DELETE |
| File | Exact path from project root |
| Scope | What specifically changes |

### 4.5 Context Section

- [ ] Related files identified (patterns to follow)
- [ ] Code dependencies listed
- [ ] Recommended skills added
- [ ] Recommended methodologies added

### 4.6 Task Dependency Tree

For tasks with dependencies:

```markdown
## Task Dependency Tree

TASK-YYY ({title})
    Status: DONE
    Summary: {what was done}
    Files: {files created}
    Patterns: {patterns to follow}
    Key code:
    ```{lang}
    {critical snippet}
    ```
```

- [ ] All dependency summaries included
- [ ] Key patterns documented
- [ ] Critical code snippets added

### 4.7 Risk Assessment

- [ ] Technical risks identified
- [ ] Mitigation strategies documented
- [ ] Potential blockers listed

### 4.8 Token Budget

| Phase | Estimate |
|-------|----------|
| SDD Docs | ~Xk |
| Dependency Tree | ~Xk |
| Research | ~Xk |
| Implementation | ~Xk |
| Testing | ~Xk |
| **Total** | <100k |

---

## Phase 5: Quality Review

### 5.1 Individual Task Review

For each task:

- [ ] Title is action-oriented
- [ ] No ambiguous language ("implement auth")
- [ ] Success criteria are testable
- [ ] Token budget is realistic
- [ ] Dependencies are complete

### 5.2 Task Set Review

- [ ] All FR-X requirements covered
- [ ] All AD-X decisions reflected
- [ ] No gaps between tasks
- [ ] No overlapping scope
- [ ] Waves are balanced (similar effort)

### 5.3 Execution Readiness

- [ ] Wave 1 tasks can start immediately
- [ ] Each task has all context needed
- [ ] Testing strategy is clear
- [ ] Rollback strategy exists (git commits)

---

## Phase 6: Documentation

### 6.1 Task Files Created

- [ ] TASK_XXX files in `todo/` folder
- [ ] Naming convention: `TASK_XXX_{slug}.md`
- [ ] Sequential numbering

### 6.2 Task List Summary

```markdown
# Tasks: {Feature Name}

## Dependency Graph
[ASCII diagram]

## Waves
- Wave 1: [TASK-001, TASK-002]
- Wave 2: [TASK-003, TASK-004]

## Critical Path
Wave 1 -> Wave 2 -> Wave 3 = Xk tokens minimum
```

### 6.3 Update Feature Folder

- [ ] implementation-plan.md references tasks
- [ ] README.md updated with task overview

---

## Quick Reference: Common Mistakes

| Mistake | Detection | Fix |
|---------|-----------|-----|
| Task too large | >100k tokens, >4 subtasks | Split by concern |
| Vague AC | No Given-When-Then | Rewrite with BDD |
| Missing deps | Task fails on missing code | Add to dependency tree |
| No patterns | Inconsistent implementations | Document patterns |
| Hidden state | Parallel tasks conflict | Serialize or split state |
| No tests | Verification impossible | Add test commands to AC |

---

## Checklist Export

Copy this abbreviated checklist for quick use:

```
PRE-DECOMPOSITION
[ ] Inputs gathered (impl-plan, spec, design)
[ ] Scope understood

TASK IDENTIFICATION
[ ] Tasks extracted
[ ] Right-sized (30-100k tokens)
[ ] INVEST validated

DEPENDENCIES
[ ] Graph created
[ ] Waves identified
[ ] No circular deps

TASK DEFINITION (per task)
[ ] Title/Description
[ ] FR-X/AD-X traceability
[ ] Given-When-Then AC
[ ] Files to change
[ ] Dependency tree
[ ] Token budget <100k

QUALITY REVIEW
[ ] All FRs covered
[ ] No gaps/overlaps
[ ] Wave 1 ready to start
```

---

*Checklist v3.0.0 | For LLM coding agents*
