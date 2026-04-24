# SDD Workflow Instructions

Navigation hub for SDD workflow documentation. All detailed workflows are split by phase for better organization and token efficiency.

---

## Overview

SDD workflow follows three main phases:

```
SPEC PHASE → DESIGN PHASE → EXECUTION PHASE
```

Each phase has dedicated documentation with step-by-step instructions.

---

## Workflow Files by Phase

### [Specification Phase](workflow-spec-phase.md)

**Focus:** Requirements gathering, problem definition, roadmap planning

| Section | Purpose |
|---------|---------|
| 1. Writing Constitutions | Define project principles (existing or new project) |
| 2. Writing Specifications | Brainstorm, research, clarify, draft spec documents |
| 3. Backlog Grooming | Refine backlog features, move to todo |
| 4. Roadmapping | Strategic planning, prioritization |

**When to use:** Starting a new project, defining new features, planning work

---

### [Design Phase](workflow-design-phase.md)

**Focus:** Technical design, task breakdown, parallelization

| Section | Purpose |
|---------|---------|
| 1. Writing Design Documents | Architecture decisions, technical approach, testing strategy |
| 2. Writing Implementation Plans | Break down work into 100k-token tasks |
| 3. Task Creation | Generate TASK_*.md files from implementation plan |
| 4. Parallelization Analysis | Dependency graphs, wave-based execution |

**When to use:** After spec approved, before implementation starts

---

### [Execution Phase](workflow-execution-phase.md)

**Focus:** Task execution, quality control, continuous learning

| Section | Purpose |
|---------|---------|
| 1. Task Execution | Execute single task via agent |
| 2. Batch Execution | Execute all tasks in feature (with resilience) |
| 3. Quality Gates | Code review, SDD review, L1-L6 gates |
| 4. Confidence Checks | Pre-phase validation (90%+ threshold) |
| 5. Reflexion Learning | PDCA cycle, pattern/mistake memory |

**When to use:** During implementation, quality checks, learning from results

---

## Quick Reference

### Complete Workflow Path

```
1. Constitution (spec-phase) → Define principles
2. Specification (spec-phase) → What and why
3. Design (design-phase) → How to build
4. Implementation Plan (design-phase) → Task breakdown
5. Task Creation (design-phase) → Generate task files
6. Task Execution (execution-phase) → Build features
7. Quality Gates (execution-phase) → Verify quality
8. Reflexion (execution-phase) → Learn and improve
```

### Common Workflows

| Goal | Files to Use |
|------|--------------|
| Start new project | spec-phase (Constitution) |
| Plan new feature | spec-phase (Specification, Grooming) |
| Design feature | design-phase (Design, Impl Plan) |
| Create tasks | design-phase (Task Creation) |
| Execute single task | execution-phase (Task Execution) |
| Execute all tasks | execution-phase (Batch Execution) |
| Review quality | execution-phase (Quality Gates) |
| Update roadmap | spec-phase (Roadmapping) |

---

## Workflow Inputs/Outputs

### Specification Phase

| Workflow | Input | Output |
|----------|-------|--------|
| Constitution | Project vision or codebase | constitution.md |
| Specification | Problem description | spec.md |
| Backlog Grooming | Backlog features | Refined specs, designs |
| Roadmapping | Completed features, new ideas | roadmap.md |

### Design Phase

| Workflow | Input | Output |
|----------|-------|--------|
| Design | spec.md, constitution.md | design.md |
| Implementation Plan | design.md | implementation-plan.md |
| Task Creation | implementation-plan.md | TASK_*.md files |
| Parallelization | All TASK_*.md | Execution plan with waves |

### Execution Phase

| Workflow | Input | Output |
|----------|-------|--------|
| Task Execution | TASK_*.md, SDD context | Code, tests, commits |
| Batch Execution | All tasks in feature | Completed feature |
| Quality Gates | Code, SDD documents | Pass/fail with feedback |
| Confidence Checks | Phase context | Confidence score, recommendations |
| Reflexion Learning | Task results | Updated patterns/mistakes |

---

## Key Principles

### 100k Token Rule (Design Phase)

Each task must fit within 100k token context:
```
Research: ~20k
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

### Quality Gate Levels (Execution Phase)

| Level | Gate | Criteria |
|-------|------|----------|
| L1 | Syntax | Zero linting errors |
| L2 | Types | Zero type errors |
| L3 | Tests | 100% unit tests pass |
| L4 | Integration | 100% integration tests pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC met |

### Confidence Thresholds (Execution Phase)

| Score | Action |
|-------|--------|
| >=90% | Proceed confidently |
| 70-89% | Clarify gaps, present alternatives |
| <70% | Stop, ask questions first |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |
## Related Files

- [SKILL.md](SKILL.md) - Main skill navigation
- [templates.md](templates.md) - All SDD document templates
- [CLAUDE.md](CLAUDE.md) - Quick reference
- [meth-CLAUDE.md](meth-CLAUDE.md) - Methodologies index

---

*SDD Workflows Navigation Hub v3.0*
*Use with faion-sdd skill*
