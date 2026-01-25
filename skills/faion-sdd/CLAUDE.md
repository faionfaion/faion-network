# faion-sdd Skill (Orchestrator)

**Specification-Driven Development: orchestrates planning + execution sub-skills.**

<<<<<<< HEAD
Specification-Driven Development (SDD) orchestrator. Philosophy: "Intent is the source of truth" - specification is the main artifact, code is its implementation.
=======
---

## Entry Point

Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-sdd`

---

## When to Use

- Starting a new project (constitution, specs)
- Planning a feature (spec → design → impl-plan → tasks)
- Managing task lifecycle (backlog → todo → in-progress → done)
- Quality gates and reviews
- Batch task execution

---

## Architecture

This skill orchestrates 2 sub-skills with **48 total methodologies**:

| Sub-Skill | Focus | Count |
|-----------|-------|-------|
| **[faion-sdd-planning](faion-sdd-planning/CLAUDE.md)** | Specs, design docs, impl-plans, tasks, templates | 28 |
| **[faion-sdd-execution](faion-sdd-execution/CLAUDE.md)** | Quality gates, reflexion, patterns, memory, review | 20 |

---
>>>>>>> claude

## Workflow

```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
                |        |          |          |         |        |
             PLANNING  PLANNING  PLANNING  PLANNING  EXECUTION  EXECUTION
```

---

## Quick Decision

| Need | Use | Why |
|------|-----|-----|
| Write spec/design/impl-plan | [faion-sdd-planning](faion-sdd-planning/CLAUDE.md) | Documentation phase |
| Execute/validate/learn | [faion-sdd-execution](faion-sdd-execution/CLAUDE.md) | Execution phase |

---

## Philosophy

**"Intent is the source of truth"** - specification is the main artifact, code is implementation.

**No Time Estimates** - use complexity (Low/Medium/High) + token estimates (~Xk).

---

## Key Concepts

- **100k Token Rule**: Each task fits within 100k token context
- **Quality Gates**: L1-L6 checkpoints before proceeding
- **Confidence Checks**: Pre-phase validation (90%+ to proceed)
- **Reflexion**: PDCA learning cycle with pattern/mistake memory
- **Parallelization**: Wave-based execution for 1.8-3.5x speedup

---

## Task Lifecycle

```
<<<<<<< HEAD
faion-sdd/
|-- SKILL.md              # Navigation hub with decision trees (~500 lines)
|-- CLAUDE.md             # This file
|-- templates.md          # All document templates
|-- workflows.md          # Detailed workflow instructions
|-- key-trends-summary.md # 2025-2026 SDD trends
+-- *.md                  # Methodologies and references (flat structure)
```

## Key Files

### SKILL.md (Navigation Hub)

Optimized navigation with:
- Workflow overview
- Agents table
- Section navigation table
- Decision trees (what to do when)
- Quick reference (inputs/outputs per section)
- Section summaries (1-5 lines each)
- Links to detailed content

### references/templates.md

All SDD document templates:
- Constitution template
- Specification template
- Design document template
- Implementation plan template
- Task file template
- Roadmap template
- Backlog item template
- Confidence check template
- Pattern/mistake record templates
- Token estimation guide

### references/workflows.md

Detailed step-by-step instructions for all 13 sections:
1. Writing Constitutions
2. Writing Specifications
3. Writing Design Documents
4. Writing Implementation Plans
5. Task Creation
6. Task Execution
7. Batch Execution
8. Parallelization Analysis
9. Backlog Grooming
10. Roadmapping
11. Quality Gates
12. Confidence Checks
13. Reflexion Learning

### methodologies/

16 methodology files with full content:
- Core SDD workflow
- Task management
- Learning & memory
- Best practices (2026)

## Agents

| Agent | Purpose |
|-------|---------|
| faion-task-executor-agent | Execute SDD tasks autonomously |
| faion-task-creator-agent | Create detailed TASK_*.md files |
| faion-sdd-reviewer-agent | Quality gate reviews (modes: spec, design, plan, tasks) |
| faion-hallucination-checker-agent | Validate task completion |

## SDD Project Structure

```
.aidocs/
|-- constitution.md           # Project principles
|-- contracts.md              # API contracts
|-- roadmap.md                # Milestones
+-- features/
    |-- backlog/              # Waiting for grooming
    |-- todo/                 # Ready for execution
    |-- in-progress/          # Being worked on
    +-- done/                 # Completed
        +-- {NN}-{feature}/
            |-- spec.md
            |-- design.md
            |-- implementation-plan.md
            +-- tasks/{status}/
=======
backlog/ → todo/ → in-progress/ → done/
```

---

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
>>>>>>> claude
```

---

## Memory

**Location:** Project-local `.aidocs/memory/`

```
.aidocs/memory/
├── patterns.md
├── mistakes.md
├── decisions.md
└── session.md
```

---

<<<<<<< HEAD
- **100k Token Rule**: Each task must fit within 100k token context
- **Quality Gates**: Checkpoints before proceeding (L1-L6)
- **Confidence Checks**: Pre-phase validation (90%+ to proceed)
- **Reflexion**: PDCA learning cycle with pattern/mistake memory
- **Parallelization**: Wave-based execution for 1.8-3.5x speedup
=======
## Related Skills
>>>>>>> claude

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-feature-executor](../faion-feature-executor/CLAUDE.md) | Executes SDD tasks in sequence |
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Implements code from tasks |

<<<<<<< HEAD
```
~/.sdd/memory/
|-- patterns_learned.jsonl    # Reusable patterns
|-- mistakes_learned.jsonl    # Errors and solutions
+-- session_context.md        # Current session state
```

## Quick Start

1. **New project?** Start with SKILL.md Section 1 (Constitution)
2. **New feature?** Follow decision tree in SKILL.md
3. **Need template?** See references/templates.md
4. **Need workflow details?** See references/workflows.md
5. **Need methodology?** See methodologies/ folder

---

*faion-sdd v3.0*
*Optimized: SKILL.md ~500 lines, details in references/*
=======
---

## Files

- [SKILL.md](SKILL.md) - Main orchestrator definition
- Sub-skills:
  - [faion-sdd-planning/SKILL.md](faion-sdd-planning/SKILL.md)
  - [faion-sdd-execution/SKILL.md](faion-sdd-execution/SKILL.md)

---

*faion-sdd v4.0 (Orchestrator)*
*48 methodologies across 2 sub-skills*
>>>>>>> claude
