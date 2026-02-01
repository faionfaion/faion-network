---
id: sdd-workflow-overview
name: "SDD Workflow Overview"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# SDD Workflow Overview

## Metadata

| Field | Value |
|-------|-------|
| **ID** | sdd-workflow-overview |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #workflow, #spec-first |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-executor-agent |

---

## What is Specification-Driven Development?

**Specification-Driven Development (SDD)** is a methodology where **intent is the source of truth**. You write documentation before code, treating specifications as the primary artifact and code as its implementation.

### Core Philosophy

```
Specification = Soul of the system
Code = Implementation details
```

SDD addresses a fundamental problem: developers (and AI agents) often start coding immediately without proper planning. This leads to scope creep, technical debt, wasted effort building the wrong thing, and difficulty explaining what you're building.

### Why SDD Matters for LLM-Assisted Development

When working with AI coding agents, specifications become even more critical:

| Without Specs | With Specs |
|---------------|------------|
| Vague prompts | Clear requirements |
| AI hallucinations | Grounded responses |
| Drift from intent | Alignment with goals |
| Random architecture | Deliberate design |
| Untestable results | Verifiable outputs |

**Research shows:** Developers who rarely encounter AI hallucinations are 2.5x more likely to be confident shipping AI-generated code.

---

## The Complete SDD Workflow

### Phase Overview

```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
      |          |        |          |          |         |
   Standards  WHAT to   HOW to    Task      Parallel   Validated
   & Stack    build     build    breakdown   waves     delivery
```

### Detailed Phase Breakdown

#### Phase 0: Constitution

**Purpose:** Establish project standards and constraints before any feature work.

**Outputs:**
- Technology stack decisions
- Coding standards
- Architecture principles
- Quality thresholds

**Key artifact:** `constitution.md`

```markdown
## Tech Stack
- Frontend: React 18, TypeScript, Tailwind
- Backend: Python 3.11, FastAPI
- Database: PostgreSQL

## Standards
- Test coverage: min 80%
- PR reviews required
- Conventional commits
```

---

#### Phase 1: Specification (WHAT to Build)

**Purpose:** Define the problem and requirements, not the solution.

**Inputs:**
- User research
- Business requirements
- Validated problem statement

**Outputs:**
- Functional requirements (FR-X)
- Non-functional requirements (NFR-X)
- User stories / acceptance criteria
- MVP/MLP scope

**Key artifact:** `spec.md`

**Characteristics of good specs:**
- Domain-oriented language (business intent, not tech specifics)
- Structured format (Given/When/Then scenarios)
- Balanced completeness (critical paths without exhaustive enumeration)
- Machine-readable sections alongside natural language

---

#### Phase 2: Design (HOW to Build)

**Purpose:** Make architecture decisions and define technical approach.

**Inputs:**
- Approved specification
- Constitution constraints
- Existing codebase patterns

**Outputs:**
- Architecture decisions (AD-X)
- File structure
- API contracts
- Data models
- Integration points

**Key artifact:** `design.md`

**Design Document Structure:**
1. Context & constraints
2. Architecture decisions with rationale
3. File structure and module boundaries
4. API contracts (OpenAPI/GraphQL schemas)
5. Data models and relationships
6. Integration points and dependencies

---

#### Phase 3: Implementation Plan (Task Breakdown)

**Purpose:** Decompose design into executable tasks with clear dependencies.

**Inputs:**
- Approved design document
- Team capacity / parallelization opportunity

**Outputs:**
- Task list with dependencies
- Execution waves
- Quality gate checkpoints
- Token estimates per task

**Key artifact:** `implementation-plan.md`

**100k Token Rule:** Each task must fit within LLM context window. If a task exceeds ~100k tokens of context, split it further.

---

#### Phase 4: Task Execution

**Purpose:** Implement code against specifications with quality gates.

**Process:**
1. Pick task from current wave
2. Load task context (spec, design, dependencies)
3. Implement following patterns
4. Run quality gates (tests, lint, type check)
5. Mark complete, proceed to next

**Parallelization:** Independent tasks in the same wave can execute concurrently (1.8-3.5x speedup).

**Key artifacts:** `TASK-XXX-*.md` files in `todo/ → in-progress/ → done/`

---

#### Phase 5: Validation & Delivery

**Purpose:** Verify implementation matches specification.

**Quality Gates:**
- L1: Syntax valid
- L2: Linting passes
- L3: Type checking passes
- L4: Unit tests pass
- L5: Integration tests pass
- L6: Acceptance criteria verified

**Self-verification pattern:** "After implementing, compare the result with the spec and confirm all requirements are met. List any spec items not addressed."

---

## Phase Transitions

### Confidence Checks

Before transitioning between phases, validate readiness:

| Transition | Confidence Threshold | Validation Method |
|------------|---------------------|-------------------|
| Idea → Spec | 70%+ | Problem validation evidence |
| Spec → Design | 90%+ | Requirements completeness |
| Design → Plan | 90%+ | Architecture clarity |
| Plan → Execute | 95%+ | Task dependencies resolved |

### Transition Gates

```
SPEC COMPLETE?
├── All FR-X defined with AC? → Yes
├── MVP scope clear? → Yes
├── Non-functional requirements? → Yes
└── Stakeholder approval? → Yes
    → Proceed to DESIGN

DESIGN COMPLETE?
├── All AD-X documented? → Yes
├── File structure defined? → Yes
├── API contracts specified? → Yes
└── Dependencies identified? → Yes
    → Proceed to IMPL-PLAN
```

---

## When to Use SDD vs Ad-Hoc Coding

### Use SDD When:

| Scenario | Reason |
|----------|--------|
| Multi-day features | Prevents scope creep |
| Team collaboration | Shared understanding |
| AI-assisted development | Reduces hallucinations |
| Complex integrations | Explicit contracts |
| Regulated domains | Audit trail |
| Production systems | Quality assurance |

### Skip SDD When:

| Scenario | Alternative |
|----------|-------------|
| < 2 hour task | Direct implementation |
| Exploratory prototype | Spike with throwaway code |
| Bug fix with clear cause | Fix + test |
| Configuration change | Direct edit |

### The 15-Minute Waterfall

For medium tasks, use "waterfall in 15 minutes":
1. 5 min: Write quick spec (problem, requirements, AC)
2. 5 min: Sketch design (key decisions, files)
3. 5 min: List tasks (max 5-7)
4. Execute with AI assistance

---

## SDD Implementation Levels

### Level 1: Spec-First

Write specification before AI-assisted development. Spec is input to coding session.

```
Human writes spec → AI generates code → Human reviews
```

### Level 2: Spec-Anchored

Keep specification after task completion for evolution and maintenance. Spec evolves with codebase.

```
Spec → Code → Spec updates → Next iteration
```

### Level 3: Spec-as-Source

Specification is the main source file. Only the spec is edited by humans; code is generated.

```
Edit spec → Generate code → Validate alignment → Deploy
```

---

## How Specs Reduce LLM Hallucinations

### The Problem

LLMs generate plausible but incorrect outputs when:
- Context is insufficient
- Requirements are ambiguous
- No validation anchor exists
- Multiple valid interpretations exist

### The Solution: Specification as Anchor

| Technique | How It Helps |
|-----------|--------------|
| Explicit requirements | Removes ambiguity |
| Structured format | Machine-readable validation |
| Examples included | Demonstrates expected patterns |
| Acceptance criteria | Verifiable checkpoints |
| Constraint documentation | Boundaries for generation |

### Practical Techniques

1. **Prepend prompts with:** "If unsure about something or context is missing, ask for clarification rather than making up an answer."

2. **Provide rules files:** Document style preferences, patterns, and constraints in CLAUDE.md or similar.

3. **Include examples:** Show desired patterns in specs.

4. **Supply test failures:** Feed linter/test outputs to guide corrections.

5. **Small chunks:** Break work into iterative pieces to prevent "going off the rails."

---

## Project Structure

```
project/
├── .aidocs/
│   ├── constitution.md        # Standards, stack, principles
│   ├── roadmap.md             # Feature timeline
│   │
│   ├── backlog/               # Features in queue
│   │   └── feature-XXX-name/
│   │       ├── spec.md
│   │       ├── design.md
│   │       └── implementation-plan.md
│   │
│   ├── todo/                  # Ready for execution
│   ├── in-progress/           # Currently executing
│   └── done/                  # Completed
│
├── src/                       # Code
└── tests/                     # Tests
```

### Task Lifecycle

```
backlog/ → todo/ → in-progress/ → done/
```

Features (folders) and tasks (files) move through this lifecycle.

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |

## Related Methodologies

| Methodology | Focus | Link |
|-------------|-------|------|
| Writing Specifications | Spec authoring | writing-specifications.md |
| Writing Design Documents | Design doc creation | writing-design-documents.md |
| Writing Implementation Plans | Task breakdown | writing-implementation-plans.md |
| Task Creation & Parallelization | Dependency management | task-creation-parallelization.md |
| Quality Gates | Validation checkpoints | quality-gates.md |
| Reflexion Learning | PDCA + memory | reflexion-learning.md |

---

## Tools & Frameworks

| Tool | Purpose |
|------|---------|
| **OpenSpec** | Source-of-truth specifications with delta specs |
| **GitHub Spec-Kit** | GitHub-integrated spec workflows |
| **Kiro** | Continuous spec-implementation validation |
| **Claude Code** | AI coding with rules files |
| **Cursor** | AI IDE with spec-aware context |

---

## Further Reading

- [Spec-Driven Development (Thoughtworks)](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [My LLM Coding Workflow (Addy Osmani)](https://addyosmani.com/blog/ai-coding-workflow/)
- [Understanding SDD Tools (Martin Fowler)](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Intent-Driven Development](https://intent-driven.dev/)
- [How to Write a Good Spec (Addy Osmani)](https://addyosmani.com/blog/good-spec/)

---

## Agent

**faion-task-executor-agent** orchestrates the SDD workflow. Invoke with:
- "Start SDD workflow for [project idea]"
- "Guide me through specification phase"
- "Create tasks from design document"

---

*Methodology | SDD Foundation | Version 2.0*
