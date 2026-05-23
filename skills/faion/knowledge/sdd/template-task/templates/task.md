<!--
purpose: Canonical TASK_NNN.md skeleton; one atomic executor unit.
consumes: implementation-plan.md row, spec.md FR-X, design.md AD-X
produces: a template-task artefact validating against scripts/validate-template-task.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~5-10k once filled
-->
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

### FR-{X}: {Full requirement text from spec.md}
Covered by this task: {which part}

### AD-{X}: {Full decision text from design.md}
Applied by this task: {how}

---

## Objective

{Clear, single-agent executable goal — 2-3 sentences. One responsibility only.
If this description contains "and", split the task.}

---

## Dependencies

- TASK_{XXX} must complete first (provides {what})

---

## Acceptance Criteria

- [ ] AC-{NNN}.1: Given {precondition} / When {action} / Then {verifiable result}
- [ ] AC-{NNN}.2: Given {precondition} / When {action} / Then {verifiable result}

---

## Technical Approach

1. Read {existing file} to understand {pattern}
2. Create/modify {file} with {what}
3. Write tests for {component}
4. Verify all AC pass

---

## Files

| File | Action | Scope |
|------|--------|-------|
| {path/to/file.py} | CREATE | {what to create} |
| {path/to/file.py} | MODIFY | {what to modify} |
| {path/to/test_file.py} | CREATE | {tests for above} |

---

## Estimated Tokens

~{XX}k total
- SDD docs: ~{X}k
- Dependency tree: ~{X}k
- Research: ~{X}k
- Implementation: ~{X}k
- Tests: ~{X}k

---

## Implementation

<!-- Executor fills this section during execution -->

### Changes Made
- {file}: {change description}

### Tests Added
- {test file}: {test descriptions}

---

## Summary

<!-- Executor fills this section after completion -->

### Completed
- [x] {what was done}

### Issues Encountered
- {issue and resolution}

### Lessons Learned
- {pattern or mistake discovered}
