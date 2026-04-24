# Task Template

Single executable unit of work. Copy and customize for each task.

---

```markdown
---
version: "1.0"
status: todo | in-progress | done | blocked
created: YYYY-MM-DD
updated: YYYY-MM-DD
feature: {feature-NNN-slug}
task_id: TASK_{NNN}
complexity: low | medium | high
est_tokens: ~{X}k
---

# TASK_{NNN}: {Short Name}

## SDD References

| Document | Path |
|----------|------|
| Spec | `.aidocs/{status}/{feature}/spec.md` |
| Design | `.aidocs/{status}/{feature}/design.md` |
| Plan | `.aidocs/{status}/{feature}/implementation-plan.md` |
| Constitution | `.aidocs/constitution.md` |

---

## Task Dependency Tree

| Dependency | Status | Key Output |
|------------|--------|------------|
| TASK_{XXX} | done | {what it provided} |
| TASK_{YYY} | done | {what it provided} |

---

## Requirements Coverage

### FR-{X}: {Full requirement text}

This task implements/contributes to this requirement.

### FR-{Y}: {Full requirement text}

{If multiple FRs}

---

## Objective

{Clear, single-agent executable goal. What exactly to implement. 2-3 sentences max.}

---

## Acceptance Criteria

- [ ] **AC-{NNN}.1:** {criterion using Given-When-Then or simple statement}
- [ ] **AC-{NNN}.2:** {criterion}
- [ ] **AC-{NNN}.3:** {criterion}

---

## Technical Approach

1. {Step 1 - what to do first}
2. {Step 2 - next step}
3. {Step 3 - next step}
4. Run tests and verify AC

---

## Files

| File | Action | Scope |
|------|--------|-------|
| `{path/to/file.py}` | CREATE | {what to create} |
| `{path/to/file.py}` | MODIFY | {what to modify} |
| `{path/to/test.py}` | CREATE | {test coverage} |

---

## Context Required

{List any files the agent should read before implementing}

| File | Why |
|------|-----|
| `{path}` | {understand pattern/interface} |
| `{path}` | {see related implementation} |

---

## Constraints

- {Constraint 1 - what NOT to do}
- {Constraint 2 - limitation to respect}

---

## Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| {edge case} | {how to handle} |

---

## Est. Tokens

~{X}k

---

## Implementation

<!-- Fill during execution -->

### Changes Made

| File | Change |
|------|--------|
| `{path}` | {what was done} |

### Commands Run

```bash
{command 1}
{command 2}
```

### Tests Added

| Test File | Tests |
|-----------|-------|
| `{path}` | {test names/descriptions} |

### Issues Encountered

| Issue | Resolution |
|-------|------------|
| {problem} | {how solved} |

---

## Summary

<!-- Fill after completion -->

### Completed

- [x] {what was done 1}
- [x] {what was done 2}
- [x] {what was done 3}

### Acceptance Criteria Status

- [x] AC-{NNN}.1: Verified
- [x] AC-{NNN}.2: Verified
- [x] AC-{NNN}.3: Verified

### Lessons Learned

| Type | Description |
|------|-------------|
| Pattern | {reusable approach discovered} |
| Mistake | {error made and how to avoid} |

---

*Task completed: YYYY-MM-DD*
```

---

## Task Lifecycle

### Status Flow

```
todo  -->  in-progress  -->  done
                |
                v
            blocked
```

### File Location

```
.aidocs/
├── todo/          # Ready for execution
│   └── TASK_{NNN}-{slug}.md
├── in-progress/   # Currently executing
│   └── TASK_{NNN}-{slug}.md
└── done/          # Completed
    └── TASK_{NNN}-{slug}.md
```

### Moving Tasks

When status changes, move the file:
```bash
mv .aidocs/todo/TASK_001-models.md .aidocs/in-progress/
mv .aidocs/in-progress/TASK_001-models.md .aidocs/done/
```

---

## Usage Notes

### Good Objectives

- **Specific**: "Create User model with email, password_hash, created_at fields"
- **Actionable**: "Implement JWT authentication for /api/v1/auth/login endpoint"
- **Measurable**: "Add unit tests for UserService with >90% coverage"

### Bad Objectives

- **Vague**: "Work on authentication"
- **Too broad**: "Implement entire auth system"
- **Unmeasurable**: "Improve code quality"

### Filling During Execution

Update these sections as you work:
1. **Changes Made** - Log each file change
2. **Commands Run** - Record test/build commands
3. **Issues Encountered** - Document problems and solutions

### Filling After Completion

Before marking done:
1. **Completed** - List all accomplishments
2. **AC Status** - Verify each criterion
3. **Lessons Learned** - Capture patterns/mistakes for memory

### Blocked Tasks

When blocked:
1. Update status to `blocked`
2. Add to Issues Encountered section
3. Document what's needed to unblock
4. Create dependency task if needed
