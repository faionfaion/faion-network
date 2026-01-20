# faion-sdd Skill

## Overview

Specification-Driven Development (SDD) orchestrator skill. Provides a complete workflow for software development where documentation (specifications) drives implementation. The philosophy: "Intent is the source of truth" - specification is the main artifact, code is its implementation.

## Workflow

```
CONSTITUTION -> SPEC -> DESIGN -> IMPL-PLAN -> TASKS -> EXECUTE -> DONE
```

| Phase | Purpose | Output |
|-------|---------|--------|
| Constitution | Project principles | constitution.md |
| Specification | WHAT and WHY | spec.md |
| Design | HOW | design.md |
| Implementation Plan | 100k token rule | implementation-plan.md |
| Tasks | Atomic work units | TASK_*.md files |
| Execute | Agent execution | Code + commits |
| Done | Quality verified | Archived feature |

## Directory Structure

```
faion-sdd/
├── SKILL.md              # Main skill definition (13 sections)
├── CLAUDE.md             # This file
├── methodologies/        # 17 methodology files (semantic naming)
└── references/           # External research and best practices
```

## Subfolders

| Folder | Description |
|--------|-------------|
| `methodologies/` | Core SDD methodologies covering workflow, specifications, design docs, implementation plans, task creation, quality gates, reflexion, and backlog management |
| `references/` | Research compilation on SDD best practices from 2025-2026 including AI-assisted specs, docs-as-code, ADRs, API-first development, and design doc patterns |

## Key Files

### SKILL.md

Main skill file containing 13 sections:

| Section | Purpose |
|---------|---------|
| 1 | Writing Constitutions (project principles) |
| 2 | Writing Specifications (requirements) |
| 3 | Writing Design Documents (architecture) |
| 4 | Writing Implementation Plans (task breakdown) |
| 5 | Task Creation (atomic units) |
| 6 | Task Execution (single task) |
| 7 | Batch Execution (all tasks) |
| 8 | Parallelization (wave optimization) |
| 9 | Backlog Grooming (feature readiness) |
| 10 | Roadmapping (strategic planning) |
| 11 | Quality Gates (code/SDD reviews) |
| 12 | Confidence Checks (pre-phase validation) |
| 13 | Reflexion and Learning (PDCA cycle) |

## Agents

| Agent | Purpose |
|-------|---------|
| faion-task-executor-agent | Execute SDD tasks autonomously |
| faion-task-creator-agent | Create detailed TASK_*.md files from specs |
| faion-sdd-reviewer-agent | Quality gate reviews (modes: spec, design, plan, tasks) |
| faion-hallucination-checker-agent | Validate task completion with evidence |

## SDD Project Structure

```
aidocs/sdd/{project}/
├── constitution.md           # Project principles
├── contracts.md              # API contracts
├── roadmap.md                # Milestones
└── features/
    ├── backlog/              # Waiting for grooming
    ├── todo/                 # Ready for execution
    ├── in-progress/          # Being worked on
    └── done/                 # Completed
        └── {NN}-{feature}/
            ├── spec.md
            ├── design.md
            ├── implementation-plan.md
            └── tasks/{status}/
```

## Task Lifecycle

```
backlog/ -> todo/ -> in-progress/ -> done/
```

## Key Concepts

- **100k Token Rule**: Each task must fit within 100k token context
- **Quality Gates**: Checkpoints before proceeding (spec, design, plan, tasks)
- **Confidence Checks**: Pre-phase validation (90%+ to proceed)
- **Reflexion**: PDCA learning cycle with pattern/mistake memory
- **Parallelization**: Wave-based execution for 1.8-3.5x speedup

## Memory Storage

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Reusable patterns
├── mistakes_learned.jsonl    # Errors and solutions
└── session_context.md        # Current session state
```
