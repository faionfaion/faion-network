# Implementation Plan Checklist

Quality gate checklist for implementation plan validation.

---

## Pre-Writing Checklist

Before writing the implementation plan, verify:

### Context Loaded

- [ ] Read constitution.md for project standards
- [ ] Read spec.md for requirements (FR-X list)
- [ ] Read design.md for architecture (AD-X list)
- [ ] Reviewed similar completed plans in done/

### Documents Approved

- [ ] Spec status: Approved
- [ ] Design status: Approved
- [ ] All AD-X decisions finalized

---

## Completeness Checklist

### Traceability (100% Rule)

- [ ] Every AD-X from design has corresponding task(s)
- [ ] Every FR-X from spec traces to task(s)
- [ ] Every file change from design is assigned to a task
- [ ] No orphan tasks (every task traces to AD-X/FR-X)

### Prerequisites

- [ ] Infrastructure prerequisites documented
- [ ] Environment prerequisites documented
- [ ] Code dependency prerequisites documented
- [ ] Documentation prerequisites documented

### Task Coverage

- [ ] All CREATE file operations have tasks
- [ ] All MODIFY file operations have tasks
- [ ] All DELETE file operations have tasks
- [ ] All integration points have tasks
- [ ] All migration tasks defined

---

## Structure Checklist

### Task Quality (INVEST)

For each task, verify:

- [ ] **Independent:** Can execute after dependencies complete
- [ ] **Negotiable:** Implementation details flexible
- [ ] **Valuable:** Clear business value
- [ ] **Estimable:** Token estimate provided
- [ ] **Small:** Under 100k tokens
- [ ] **Testable:** Acceptance criteria verifiable

### Token Budget

- [ ] Every task has token estimate
- [ ] No task exceeds 100k tokens
- [ ] Simple tasks: 15-30k tokens
- [ ] Normal tasks: 30-60k tokens
- [ ] Complex tasks: 60-100k tokens
- [ ] Tasks > 100k are split

### Complexity Assessment

- [ ] Files changed count documented
- [ ] Dependencies count documented
- [ ] Research level assessed
- [ ] Testing scope defined
- [ ] Risk level assigned
- [ ] Overall complexity calculated

---

## Dependency Checklist

### Dependency Graph

- [ ] All tasks present in graph
- [ ] All dependencies typed (FS/SS/FF/SF)
- [ ] No circular dependencies
- [ ] Graph is valid DAG
- [ ] Visualization included

### Wave Analysis

- [ ] Waves identified
- [ ] Wave dependencies documented
- [ ] Parallel opportunities maximized
- [ ] Token load per wave calculated
- [ ] Wave visualization included

### Critical Path

- [ ] Critical path identified
- [ ] Critical path token sum calculated
- [ ] Bottleneck tasks marked
- [ ] Zero-slack tasks identified
- [ ] Optimization opportunities noted

---

## Task Definition Checklist

For each task in the plan:

### Header

- [ ] Task ID (TASK-XXX format)
- [ ] Concise title (action + target)
- [ ] Phase assignment
- [ ] Wave assignment

### Context

- [ ] Description (2-3 sentences)
- [ ] Traces to AD-X
- [ ] Traces to FR-X
- [ ] Depends on (explicit list or "None")
- [ ] Blocks (what tasks depend on this)

### Estimation

- [ ] Complexity level (simple/normal/complex)
- [ ] Token estimate (~Xk)
- [ ] Files count
- [ ] Test count

### Acceptance Criteria

- [ ] At least 2 testable criteria
- [ ] Criteria use Given-When-Then or declarative format
- [ ] No vague criteria ("works correctly")
- [ ] Criteria cover happy path
- [ ] Criteria cover error cases (if applicable)

### Files

- [ ] Action specified (CREATE/MODIFY/DELETE)
- [ ] File path complete
- [ ] Purpose described
- [ ] Scope of changes noted (for MODIFY)

### Tests

- [ ] Unit tests specified
- [ ] Integration tests specified (if needed)
- [ ] E2E tests specified (if critical path)
- [ ] Test file paths included

### Technical Notes

- [ ] Patterns to follow referenced
- [ ] Gotchas/warnings documented
- [ ] Related code examples linked
- [ ] Configuration requirements noted

---

## Risk Checklist

### Risk Identification

- [ ] Technical risks listed
- [ ] Dependency risks listed
- [ ] External risks listed
- [ ] Each risk has likelihood (Low/Med/High)
- [ ] Each risk has impact (Low/Med/High)

### Mitigation

- [ ] Each risk has mitigation strategy
- [ ] Contingency plans for high-impact risks
- [ ] Fallback options documented

### Buffer

- [ ] Contingency buffer calculated (15-25%)
- [ ] Buffer applied to critical path
- [ ] Risk-adjusted estimates provided

---

## Testing Plan Checklist

### Per-Phase Testing

- [ ] Each phase has test requirements
- [ ] Pass criteria defined for each phase
- [ ] Test types specified (unit/integration/E2E)

### Coverage Targets

- [ ] Unit test coverage target set (80%+)
- [ ] Integration test coverage target set
- [ ] E2E test coverage defined (critical flows)
- [ ] Coverage tracking method specified

---

## Rollout Checklist

### Pre-deployment

- [ ] Staging test requirements
- [ ] Backup procedures
- [ ] Feature flag configuration
- [ ] Monitoring setup

### Deployment Steps

- [ ] Step-by-step deployment plan
- [ ] Verification steps after each phase
- [ ] Gradual rollout percentages

### Rollback Plan

- [ ] Rollback triggers defined
- [ ] Rollback steps documented
- [ ] Data rollback considerations
- [ ] Communication plan

### Success Criteria

- [ ] Error rate threshold
- [ ] Performance thresholds
- [ ] Business metrics
- [ ] Observation period

---

## Final Review Checklist

### Document Quality

- [ ] All sections completed
- [ ] No placeholder text remaining
- [ ] Formatting consistent
- [ ] Links valid

### Peer Review

- [ ] Architecture decision traceability verified
- [ ] Token estimates reviewed
- [ ] Dependency graph validated
- [ ] Wave analysis confirmed
- [ ] Critical path calculation checked

### Approval

- [ ] Implementation plan status: Draft → In Review → Approved
- [ ] Reviewer sign-off obtained
- [ ] Ready for task file generation

---

## Quick Validation Commands

### Count Checks

```bash
# Count tasks
grep -c "^### TASK-" implementation-plan.md

# Count AD-X references
grep -c "AD-" implementation-plan.md

# Count FR-X references
grep -c "FR-" implementation-plan.md

# Find tasks without token estimates
grep -A 5 "^### TASK-" implementation-plan.md | grep -L "tokens"
```

### Dependency Check

```bash
# Find tasks that appear in "Blocks:" but not defined
# (Manual review required)

# Verify no circular deps (requires tooling)
```

---

## Common Issues

| Issue | Detection | Fix |
|-------|-----------|-----|
| Task too large | Token estimate > 100k | Split into subtasks |
| Missing dependency | Task references undefined task | Add missing task or fix reference |
| Orphan task | No AD-X or FR-X trace | Add traceability or remove task |
| Vague AC | Contains "works correctly" | Rewrite with specific criteria |
| No tests | Test section empty | Add appropriate test requirements |
| Circular dep | A→B→A pattern | Restructure dependency chain |

---

*Checklist | SDD Foundation | Version 3.0.0*
