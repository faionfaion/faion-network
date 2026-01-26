# SDD Skill (Orchestrator)

> **Entry point:** `/faion-net` — invoke for automatic routing.

Specification-Driven Development: "Intent is the source of truth" - specification is the main artifact, code is its implementation.

## Sub-Skills

| Sub-Skill | Focus | Methodologies |
|-----------|-------|---------------|
| [faion-sdd-planning](faion-sdd-planning/CLAUDE.md) | Specs, design docs, impl-plans, tasks, templates | 28 |
| [faion-sdd-execution](faion-sdd-execution/CLAUDE.md) | Quality gates, reflexion, patterns, memory, review | 20 |

**Total:** 48 methodologies

## Workflow

```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
                |        |          |          |         |        |
             PLANNING  PLANNING  PLANNING  PLANNING  EXECUTION  EXECUTION
```

## Quick Decision

| Need | Use |
|------|-----|
| Write spec/design/impl-plan | faion-sdd-planning |
| Execute/validate/learn | faion-sdd-execution |

## Key Concepts

- **100k Token Rule**: Each task fits within 100k token context
- **Quality Gates**: L1-L6 checkpoints before proceeding
- **Confidence Checks**: Pre-phase validation (90%+ to proceed)
- **Reflexion**: PDCA learning cycle with pattern/mistake memory
- **Parallelization**: Wave-based execution for 1.8-3.5x speedup
- **No Time Estimates**: Use complexity (Low/Medium/High) + token estimates (~Xk)

## Task Lifecycle

```
backlog/ → todo/ → in-progress/ → done/
```

## Project Structure

```
.aidocs/
├── constitution.md
├── roadmap.md
└── features/
    ├── backlog/
    ├── todo/
    ├── in-progress/
    └── done/
        └── {NN}-{feature}/
            ├── spec.md
            ├── design.md
            ├── implementation-plan.md
            └── tasks/{status}/
```

## Memory

**Location:** Project-local `.aidocs/memory/`

```
.aidocs/memory/
├── patterns.md
├── mistakes.md
├── decisions.md
└── session.md
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-feature-executor](../faion-feature-executor/CLAUDE.md) | Executes SDD tasks in sequence |
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Implements code from tasks |
