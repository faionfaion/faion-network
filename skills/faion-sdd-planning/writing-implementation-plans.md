# Writing Implementation Plans

## Methodology Reference

**Primary:** writing-implementation-plans (Writing Implementation Plans v2.0)

**Integrated:**
| Domain | Methodology | Principle Applied |
|--------|-------------|-------------------|
| PM | wbs-decomposition | WBS decomposition |
| PM | dependency-management | Dependency types (FS, SS, FF, SF) |
| PM | risk-assessment | Risk assessment |
| PM | schedule-management | Schedule management |
| BA | requirements-traceability | Requirements traceability (AD-X → TASK) |
| PdM | backlog-management | INVEST principle for tasks |
| Dev | testing-strategy | Testing strategy |
| SDD | task-parallelization | Task parallelization and waves |

---

## Problem

Developers struggle to start coding after reading design documents because:
- Design is too high-level to act on directly
- Unclear order of operations
- Dependencies between components not obvious
- No clear success criteria for each step
- AI agents fail with tasks > 100k tokens
- Parallel work opportunities missed

**The root cause:** No bridge between design and actionable tasks.

---

## Quick Reference

This methodology is split into four focused documents:

| Document | Content | Size |
|----------|---------|------|
| **[impl-plan-components.md](impl-plan-components.md)** | Document structure, prerequisites, waves, phases, risk | ~1650 tokens |
| **[impl-plan-task-format.md](impl-plan-task-format.md)** | Task definition, INVEST validation, critical path | ~1850 tokens |
| **[impl-plan-100k-rule.md](impl-plan-100k-rule.md)** | Context budget, task splitting, WBS | ~1450 tokens |
| **[impl-plan-examples.md](impl-plan-examples.md)** | Real examples, patterns, quality gates | ~1600 tokens |

**Total methodology:** 3478 tokens → 4 files < 2000 tokens each

---

## Framework

### What is an Implementation Plan?

An implementation plan breaks the design into ordered, actionable tasks with:
- Clear dependencies (graph-based)
- Effort estimates (for AI context budget)
- Success criteria (testable)
- Parallelization opportunities (waves)
- Risk mitigation strategies

### Document Hierarchy

```
SPEC (what) → DESIGN (how) → IMPL PLAN (order) → TASKS (execution)
  FR-X         AD-X          TASK-XXX outline    TASK_XXX.md files
                                   ↓
                              Wave 1: TASK-001, TASK-002 (parallel)
                              Wave 2: TASK-003, TASK-004 (depends on W1)
                              Wave 3: TASK-005 (depends on W2)
```

---

## Writing Process

### Phase 1: Load Full SDD Context

Before writing, read and understand:

```
1. .aidocs/constitution.md - project principles
2. {FEATURE_DIR}/spec.md - requirements (FR-X)
3. {FEATURE_DIR}/design.md - architecture (AD-X)
4. features/done/ - completed implementation plans for patterns
```

Extract:
- All AD-X decisions to implement
- File changes list (CREATE/MODIFY)
- Dependencies between components
- Testing requirements

### Phase 2: Prerequisites Check

See [impl-plan-components.md](impl-plan-components.md#prerequisites)

### Phase 3: Work Breakdown Structure

See [impl-plan-100k-rule.md](impl-plan-100k-rule.md#work-breakdown-structure-wbs)

### Phase 4: Build Dependency Graph

See [impl-plan-components.md](impl-plan-components.md#dependency-graph)

### Phase 5: Wave Analysis

See [impl-plan-components.md](impl-plan-components.md#wave-analysis)

### Phase 6: Define Phases

See [impl-plan-components.md](impl-plan-components.md#phase-breakdown)

### Phase 7: Task Definition

See [impl-plan-task-format.md](impl-plan-task-format.md#task-definition)

### Phase 8: Critical Path Analysis

See [impl-plan-task-format.md](impl-plan-task-format.md#critical-path)

### Phase 9: Risk Assessment

See [impl-plan-components.md](impl-plan-components.md#risk-assessment)

### Phase 10: Testing Plan

See [impl-plan-components.md](impl-plan-components.md#testing-plan)

### Phase 11: Rollout Strategy

See [impl-plan-components.md](impl-plan-components.md#rollout-strategy)

---

## Key Concepts

### 100k Token Rule

Each task must fit within 100k token context. See [impl-plan-100k-rule.md](impl-plan-100k-rule.md)

### INVEST Validation

Tasks must be Independent, Negotiable, Valuable, Estimable, Small, Testable. See [impl-plan-task-format.md](impl-plan-task-format.md#invest-validation)

### Wave-Based Creation

Create TASK files in waves, not all at once. See [impl-plan-100k-rule.md](impl-plan-100k-rule.md#wave-based-task-creation)

---

## Templates & Examples

### Full Template

See [impl-plan-components.md](impl-plan-components.md#full-template)

### Real Examples

See [impl-plan-examples.md](impl-plan-examples.md):
- Simple feature (3 tasks)
- Medium feature (7 tasks)
- Complex feature (12 tasks)
- Refactoring split example

---

## Quality Checklist

See [impl-plan-examples.md](impl-plan-examples.md#quality-checklist)

---

## Common Mistakes

See [impl-plan-examples.md](impl-plan-examples.md#common-mistakes)

---

## Sources

- [Critical Path Method](https://www.pmi.org/learning/library/critical-path-method-schedule-control-6879) - PMI CPM guide
- [Gantt Charts Best Practices](https://www.gantt.com/) - Project scheduling
- [Agile Release Planning](https://www.scaledagileframework.com/pi-planning/) - SAFe PI planning
- [Parallel Task Execution](https://www.atlassian.com/agile/project-management/estimation) - Agile estimation
- [Work Breakdown Structure](https://www.workbreakdownstructure.com/) - WBS methodology
