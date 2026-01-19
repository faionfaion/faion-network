# Methodologies Folder

## Overview

Contains 8 core SDD (Specification-Driven Development) methodologies covering the complete workflow from project setup to backlog management. Each methodology follows a standard format with metadata, problem statement, framework, templates, examples, and common mistakes.

## File Summary

| File | ID | Description |
|------|-----|-------------|
| M-SDD-001_sdd_workflow_overview.md | M-SDD-001 | Foundation overview of the SDD workflow phases (Idea -> Validation -> Spec -> Design -> Implementation -> Launch) |
| M-SDD-002_writing_specifications.md | M-SDD-002 | How to write spec.md files with user stories, functional requirements, and acceptance criteria |
| M-SDD-003_writing_design_documents.md | M-SDD-003 | How to write design.md files with architecture decisions, file structure, data models, and API contracts |
| M-SDD-004_writing_implementation_plans.md | M-SDD-004 | How to break design into phased tasks with estimates, dependencies, and rollout strategy |
| M-SDD-005_task_creation_parallelization.md | M-SDD-005 | Task decomposition principles, dependency analysis, and parallelization strategies |
| M-SDD-006_quality_gates_confidence.md | M-SDD-006 | Quality checkpoints (spec review, design review, code review) and confidence assessment |
| M-SDD-007_reflexion_learning.md | M-SDD-007 | Post-task reflection process, learning storage, and PDCA cycle implementation |
| M-SDD-008_backlog_grooming_roadmapping.md | M-SDD-008 | Backlog management, RICE/MoSCoW prioritization, and roadmap planning |

## Methodology Structure

Each methodology file contains:

1. **Metadata** - ID, category, difficulty, tags, domain skill, agents
2. **Problem** - What issue this methodology addresses
3. **Framework** - Step-by-step process and principles
4. **Templates** - Ready-to-use markdown templates
5. **Examples** - Practical application examples
6. **Common Mistakes** - Pitfalls and fixes
7. **Related Methodologies** - Cross-references
8. **Agent** - Which agent implements this methodology

## Detailed File Descriptions

### M-SDD-001: SDD Workflow Overview

- **Category:** SDD Foundation
- **Difficulty:** Beginner
- **Agent:** faion-task-executor-agent

Introduces the six-phase SDD workflow. Covers time allocation for solo vs team projects. Includes project structure template and phase checklist.

### M-SDD-002: Writing Specifications

- **Category:** SDD Foundation
- **Difficulty:** Beginner
- **Agent:** faion-spec-reviewer-agent

Defines spec.md structure: overview, user stories, functional requirements (FR-X), non-functional requirements (NFR-X), acceptance criteria (Given-When-Then), and out of scope. Includes full spec template.

### M-SDD-003: Writing Design Documents

- **Category:** SDD Foundation
- **Difficulty:** Intermediate
- **Agent:** faion-design-reviewer-agent

Bridges spec (what) to implementation (code). Covers architecture decisions (AD-X format), file changes (CREATE/MODIFY), data models, API contracts, dependencies, and testing strategy.

### M-SDD-004: Writing Implementation Plans

- **Category:** SDD Foundation
- **Difficulty:** Intermediate
- **Agent:** faion-impl-plan-reviewer-agent

Breaks design into actionable tasks. Covers prerequisites, phases, task format (TASK-XXX), testing plan, rollout strategy, and risk assessment.

### M-SDD-005: Task Creation and Parallelization

- **Category:** SDD Foundation
- **Difficulty:** Intermediate
- **Agent:** faion-task-creator-agent

Task decomposition principles (right size, clear boundaries, explicit dependencies). Dependency graph analysis, parallel path identification, critical path calculation, and wave-based execution.

### M-SDD-006: Quality Gates and Confidence Checks

- **Category:** SDD Foundation
- **Difficulty:** Intermediate
- **Agent:** faion-hallucination-checker-agent

Quality gate types (spec review, design review, code review, test gate, deploy gate). Confidence levels (high/medium/low). Includes checklists for each gate type and AI code confidence assessment.

### M-SDD-007: Reflexion and Learning

- **Category:** SDD Foundation
- **Difficulty:** Intermediate
- **Agent:** faion-task-executor-agent

PDCA learning loop (Do -> Reflect -> Learn -> Apply). Covers task reflexion, feature retrospectives, learning entry format (JSONL), and session context. Storage in ~/.sdd/memory/.

### M-SDD-008: Backlog Grooming and Roadmapping

- **Category:** SDD Foundation
- **Difficulty:** Beginner
- **Agent:** faion-task-executor-agent

Backlog structure (ideas -> validated -> specified -> designed -> ready). Weekly grooming process. Prioritization frameworks (RICE, MoSCoW, Value vs Effort). Roadmap templates (time-based, theme-based).
