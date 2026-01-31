# Task File Template

Copy and customize for your SDD task files.

---

## Template

```markdown
# TASK_{NNN}: {Short Name}

**Feature:** {feature-name}
**Status:** todo | in-progress | done
**Created:** YYYY-MM-DD

---

## SDD References

| Document | Path |
|----------|------|
| Spec | .aidocs/features/{status}/{feature}/spec.md |
| Design | .aidocs/features/{status}/{feature}/design.md |
| Plan | .aidocs/features/{status}/{feature}/implementation-plan.md |

---

## Task Dependency Tree

| Dependency | Status | Key Output |
|------------|--------|------------|
| TASK_{XXX} | done | {what it provided} |

---

## Requirements Coverage

### FR-{X}: {Full requirement text}
Covered by this task.

---

## Objective

{Clear, single-agent executable goal - what exactly to implement}

---

## Dependencies

- TASK_{XXX} must complete first (provides {what})

---

## Acceptance Criteria

- [ ] AC-{NNN}.1: {Given-When-Then or criterion}
- [ ] AC-{NNN}.2: {Given-When-Then or criterion}

---

## Technical Approach

1. {Step 1}
2. {Step 2}
3. {Step 3}

---

## Files

| File | Action | Scope |
|------|--------|-------|
| {path/to/file.py} | CREATE | {what to create} |
| {path/to/file.py} | MODIFY | {what to modify} |

---

## Estimated Tokens

~{XX}k

---

## Implementation

<!-- Fill during execution -->

### Changes Made
- {file}: {change}

### Tests Added
- {test file}: {tests}

---

## Summary

<!-- Fill after completion -->

### Completed
- [x] {what was done}

### Issues Encountered
- {issue and resolution}

### Lessons Learned
- {pattern or mistake}
```

---

## Usage Notes

### When to Use
- After implementation-plan.md is created
- Breaking down features into atomic units
- Each task must fit 100k token budget

### Task Properties
- **Atomic:** Single responsibility
- **Executable:** Clear instructions for agent
- **Testable:** Has acceptance criteria
- **Independent:** Minimal dependencies
- **Sized:** ~10-40k tokens typical

### 100k Token Budget Rule
```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Tests: ~15k
Buffer: ~10k
TOTAL < 100k
```

### Token Estimation Guide

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

### Task States

```
todo → in-progress → done
```

- **todo:** Ready for execution
- **in-progress:** Being worked on
- **done:** Completed, tests pass

### Quality Gates

Before marking done:
- All acceptance criteria met
- Tests written and passing
- Code follows constitution standards
- No lint errors
- Coverage target met

---

## Related

- **Spec template:** [template-spec.md](template-spec.md)
- **Design template:** [template-design.md](template-design.md)
- **Workflow guide:** [task-creation-template-guide.md](task-creation-template-guide.md)
- **Principles:** [task-creation-principles.md](task-creation-principles.md)
- **Implementation plan:** [writing-implementation-plans.md](writing-implementation-plans.md)
- **Quality gates:** [quality-gates.md](quality-gates.md)
- **Confidence checks:** [confidence-checks.md](confidence-checks.md)

---

*SDD Task Template v2.0*
