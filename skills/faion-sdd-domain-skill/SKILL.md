---
name: faion-sdd-domain-skill
user-invocable: false
description: "SDD Domain Skill: Specification-Driven Development orchestrator. Manages full SDD workflow: specifications, design docs, implementation plans, constitutions, task management, quality gates, and reflexion learning."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# SDD Domain Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates the complete SDD (Specification-Driven Development) workflow. This domain skill consolidates all SDD-related functionality into a single orchestrator.

## Philosophy

**"Intent is the source of truth"** — specification is the main artifact, code is just its implementation.

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) ─ orchestrators
    ↓ call
Layer 2: Agents ─ executors
    ↓ use
Layer 3: Technical Skills ─ tools
```

## Workflow Overview

```
CONSTITUTION → SPEC → DESIGN → IMPL-PLAN → TASKS → EXECUTE → DONE
      ↓          ↓        ↓         ↓          ↓        ↓        ↓
   project    feature  technical  100k rule  atomic   agent    learn
   principles  intent   approach  compliance  units  execution  reflect
```

---

# Section 1: Writing Constitutions

## Philosophy

**Constitution.md** — immutable project principles for ALL features.

**Two modes:**
1. **Existing Project** → codebase analysis
2. **New Project** → Socratic dialogue

## MODE 1: Existing Project

**Workflow:** Detect → Analyze Structure → Tech Stack → Patterns → Draft → Review

**Analyze:**
- Directory layout, CLAUDE.md, README.md
- Config files (pyproject.toml, package.json)
- Architecture patterns, naming, linters, testing

**Present findings:**
```markdown
**Analysis:**
1. Tech: Python 3.11, Django 4.2, PostgreSQL
2. Architecture: Layered (views → services → models)
3. Standards: black + isort + flake8
Does this match? What to change?
```

## MODE 2: New Project

**Workflow:** Vision → Tech Choices → Architecture → Standards → Draft → Review

### Vision (Socratic)
"Tell me about the project. What problem does it solve?"

Apply Five Whys to get to real need.

### Tech Choices (Alternatives)

For each decision — present A/B/C with pros/cons:
- Backend: Django vs FastAPI vs NestJS
- Database: PostgreSQL vs MongoDB vs SQLite

### Architecture (Trade-offs)
- Monolith vs Microservices
- REST vs GraphQL
- ORM vs Raw SQL

### Standards
- Linter, formatter, type hints
- Testing coverage, CI/CD
- Git conventions

## Constitution Save

```bash
mkdir -p aidocs/sdd/{project}
# Write constitution.md
```

Create CLAUDE.md navigation hub.

## Anti-patterns

- ❌ Copying without understanding
- ❌ Over-engineering at start
- ❌ Ignoring team expertise

**Output:** `aidocs/sdd/{project}/constitution.md` → Next: Writing Specifications

---

# Section 2: Writing Specifications

## Philosophy

- **Intent is source of truth** — spec is main artifact
- **Socratic dialogue** — user formulates requirements through questions
- **Brainstorming** — iterative refinement via alternatives

## Workflow

```
BRAINSTORM → RESEARCH → CLARIFY → DRAFT → REVIEW → SAVE
```

## Phase 1: Brainstorming

Start: "Tell me about the problem. Who suffers and how?"

**Five Whys** — for each answer ask "Why?":
```
"Need export" → Why? → "Managers ask" → Why? → "No access" → Real problem: UX
```

**Alternatives** — for each idea:
```markdown
**A:** {approach 1} ✅ Pros ❌ Cons
**B:** {approach 2} ✅ Pros ❌ Cons
Which is closer?
```

**Challenge assumptions:**
- "Is this needed for v1?"
- "What if we DON'T do this?"
- "What exists in codebase?"

## Phase 2: Research Codebase

Search: `Glob **/models.py`, `Grep class.*Model`, `Glob aidocs/sdd/**/spec.md`

Share findings: "Found existing export in services.py. Does this affect approach?"

## Phase 3: Clarify Details

**User stories workshop:**
```markdown
As {role}, I want {goal}, so that {benefit}.
- How often?
- What happens if can't do this?
```

**Edge cases through questions** (not assumptions):
- "What if data invalid?"
- "What if 1000+ records?"
- "What if service unavailable?"

## Phase 4: Draft Section by Section

Each section → show → validate → next:

1. Problem Statement → "Correct?"
2. User Stories with AC → "Complete?"
3. Functional Requirements → "Anything redundant?"
4. Out of Scope → "Agree with boundaries?"

## Phase 5: Review

**Checklist:**
- [ ] Problem clear
- [ ] User Stories specific
- [ ] Requirements testable
- [ ] Out of Scope defined

Call `faion-spec-reviewer` agent before save.

## Phase 6: Save

**New feature:** `aidocs/sdd/{project}/features/backlog/{NN}-{feature}/spec.md`
**Active feature:** update existing spec.md

Create CLAUDE.md navigation hub in feature directory.

## Anti-patterns

- ❌ Assumptions instead of questions
- ❌ Solution before problem
- ❌ Large blocks without validation
- ❌ Ignoring "I don't know"

**Output:** `spec.md` → Next: Writing Design Documents

---

# Section 3: Writing Design Documents

## Purpose

Creates design.md for a feature based on:
1. Approved spec.md
2. Codebase analysis
3. Project constitution

## Prerequisites

**Required files:**
1. `spec.md` exists with status `approved`
2. Project `constitution.md` exists at `aidocs/sdd/{project}/constitution.md`
3. Project `contracts.md` exists at `aidocs/sdd/{project}/contracts.md` (for API features)

**If constitution.md doesn't exist:** Use Section 1 to create it first.
**If contracts.md doesn't exist:** Use `faion-api-designer` agent with MODE=init.

## Workflow

### Phase 1: Read Specification

Read spec.md completely and extract:
- Problem Statement
- User Stories
- Functional Requirements
- API Contract (if present)
- Data Model (if present)
- Out of Scope

### Phase 2: Read Constitution

Read project principles from constitution.md and extract:
- Architecture patterns
- Code standards
- Testing requirements

### Phase 2.5: Read API Contracts (if API feature)

Read contracts.md and extract:
- Relevant endpoint definitions
- Request/response schemas
- Auth requirements
- Error format standard

**IMPORTANT:** Do NOT redefine API endpoints in design.md. Reference contracts.md instead:
```markdown
## API Endpoints

This feature implements endpoints from [contracts.md](../../contracts.md):
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
```

### Phase 3: Research Codebase

Use Grep and Glob tools to find related code:
- Similar models
- Similar services
- Similar views
- Existing patterns

Determine:
- Which components can be reused
- Which patterns are in use
- Where to place new code

### Phase 4: Architecture Decisions

For each key decision:
1. Define context - what problem are we solving
2. List options - minimum 2 alternatives
3. Choose solution - which and why
4. Document rationale - reasoning behind choice

### Phase 5: Define Technical Approach

Define:
1. **Components** - new components, interactions, diagrams if complex
2. **Data Flow** - data path through system, validation points, error handling
3. **Files** - CREATE and MODIFY lists with scope

### Phase 6: Define Testing Strategy

Based on constitution:
1. Unit tests - isolated testing targets
2. Integration tests - flow coverage
3. Test data - required fixtures

### Phase 7: Identify Risks

For each risk document:
- Risk description
- Impact (High/Medium/Low)
- Mitigation strategy

### Phase 8: Review with User

Present key decisions:
1. Architecture Decisions - agreement check
2. Technical Approach - better alternatives
3. Risks - completeness check

### Phase 9: Agent Review

Call `faion-design-reviewer` agent before saving.

The agent checks:
- FR coverage (all requirements addressed)
- AD structure (context, options, rationale)
- Constitution compliance
- Files list completeness
- Technical correctness

### Phase 10: Save Design

Save design.md to feature directory: `{feature_path}/design.md`

## Architecture Decision Template

```markdown
### AD-{N}: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}
- **B: {Option}**
  - Pros: {benefits}
  - Cons: {drawbacks}

**Decision:** {Chosen solution}

**Rationale:** {Why this solution, influencing factors}

**Failed Attempts:** {Optional - approaches tried and rejected}
```

## Files Section Format

```markdown
### Files

app/applications/{app}/models.py           # MODIFY - add {Model}
app/applications/{app}/services.py         # MODIFY - add {Service}
app/applications/{app}/views.py            # MODIFY - add {ViewSet}
app/applications/{app}/serializers.py      # MODIFY - add {Serializer}
app/applications/{app}/tests/test_{x}.py   # CREATE - tests for {x}
```

## Checklist Before Completion

- All FR from spec.md covered
- Architecture Decisions have rationale
- Files list is complete
- Testing strategy defined
- Risks identified
- Follows constitution
- API endpoints reference contracts.md (not redefined)
- User approved

**Output:** `design.md` → Next: Writing Implementation Plans

---

# Section 4: Writing Implementation Plans

## Key Principle

**Each task MUST fit 100k token context** = atomic, single-agent executable.

## Workflow

```
LOAD CONTEXT → ANALYZE COMPLEXITY → DEFINE WORK UNITS → APPLY 100k RULE → DEPENDENCIES → DRAFT → REVIEW → SAVE
```

## Phase 1: Load Context

Read: `constitution.md`, `spec.md`, `design.md`

## Phase 2: Analyze Complexity

For each file in design.md:

| File | Action | Complexity | Est. Tokens |
|------|--------|------------|-------------|
| models.py | CREATE | High | 40k |
| services.py | CREATE | High | 50k |

**Factors:** LOC, dependencies, business logic, tests

## Phase 3: Define Work Units

Group related work:
```markdown
## Work Unit 1: Data Layer
- models.py (CREATE)
Est: 40k tokens
```

## Phase 4: Apply 100k Rule

```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

**If > 100k:** Split into smaller tasks.

## Phase 5: Dependencies

| Task | Depends On | Enables |
|------|------------|---------|
| TASK_001 | — | TASK_003 |
| TASK_002 | — | TASK_003 |
| TASK_003 | 001, 002 | — |

Rules: No cycles, maximize parallelization.

## Phase 6: Draft

Show section by section:
- Overview (total tasks, critical path, est. tokens)
- Tasks list (files, deps, FR/AD coverage, AC)
- Execution order (phases, parallel/sequential)

## Phase 7: Review

Call `faion-impl-plan-reviewer` agent. Checks: 100k compliance, deps, coverage.

## Phase 8: Save

`aidocs/sdd/{project}/features/{feature}/implementation-plan.md`

## Token Estimation Guide

| Component | Tokens |
|-----------|--------|
| Django model simple | 5-10k |
| Django model complex | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Test file | 20-40k |

**Rule:** If uncertain, estimate higher and split.

**Output:** `implementation-plan.md` → Next: Task Creation (faion-make-tasks skill)

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-spec-reviewer | Review spec before save |
| faion-design-reviewer | Review design for architecture decisions |
| faion-impl-plan-reviewer | Review impl-plan for 100k token compliance |
| faion-task-creator | Create individual tasks |
| faion-task-executor | Execute tasks autonomously |
| faion-tasks-reviewer | Review completed tasks |
| faion-hallucination-checker | Verify task completion with evidence |

---

# Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md                    # Project principles (Section 1)
├── contracts.md                       # API contracts
├── roadmap.md                         # Milestones
└── features/
    ├── backlog/                       # Features waiting for grooming
    ├── todo/                          # Features ready for execution
    ├── in-progress/                   # Features being worked on
    └── done/                          # Completed features
        └── {NN}-{feature}/
            ├── spec.md                # WHAT and WHY (Section 2)
            ├── design.md              # HOW (Section 3)
            ├── implementation-plan.md # Tasks breakdown (Section 4)
            └── tasks/
                ├── backlog/
                ├── todo/
                ├── in-progress/
                └── done/
```

---

# Section 5: Task Creation

## Purpose

Create implementation tasks from SDD documents using the `faion-task-creator` agent.

## Modes

### SDD Mode (Primary)
When project/feature specified:
1. Load spec, design, implementation-plan
2. Verify documents approved
3. Create tasks per implementation-plan
4. Review with faion-tasks-reviewer

### Free Mode (Legacy)
When description provided:
1. Clarify requirements with user
2. Research codebase
3. Plan task structure
4. Create tasks

## Workflow

```
1. Load SDD documents
   ↓
2. Verify: spec approved? design approved?
   ↓
3. Check/create implementation-plan
   ↓
4. For each task in plan:
   → Call faion-task-creator agent
   ↓
5. Run faion-tasks-reviewer (4-pass)
   ↓
6. Report results
```

## Document Verification

Check these files exist and are approved:
```
aidocs/sdd/{project}/features/{status}/{feature}/spec.md
aidocs/sdd/{project}/features/{status}/{feature}/design.md
aidocs/sdd/{project}/features/{status}/{feature}/implementation-plan.md
```

If implementation-plan missing:
→ Use Section 4 to create it first

## Task File Format

```markdown
# TASK_{NNN}: {Short Name}

**Feature:** {feature}
**Status:** todo | in-progress | done
**Created:** {date}

## Objective
{Clear, single-agent executable goal}

## Dependencies
- {TASK_XXX} must complete first (if any)

## Acceptance Criteria
- [ ] AC-{NNN}.1: {Criterion 1}
- [ ] AC-{NNN}.2: {Criterion 2}

## Technical Approach
{Step-by-step implementation plan}

## Files
| File | Action | Description |
|------|--------|-------------|
| path/to/file.py | CREATE/MODIFY | What changes |

## Estimated Tokens
~{XX}k
```

## Task Creation Call

```python
Task(
    subagent_type="faion-task-creator",
    description=f"Create {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_INFO: {task_from_plan}
SDD_PATH: aidocs/sdd/{project}/features/{status}/{feature}/

Create comprehensive task file with:
- Clear objective
- Acceptance criteria (AC-XX.X)
- Technical approach
- Files to modify
- Dependencies
- Estimated complexity

Research codebase deeply before writing.
"""
)
```

## Task Review

After all tasks created:

```python
Task(
    subagent_type="faion-tasks-reviewer",
    prompt=f"""
Multi-pass review for {project}/{feature}:

Pass 1: Completeness - all plan items covered?
Pass 2: Consistency - no contradictions?
Pass 3: Coverage - all requirements addressed?
Pass 4: Executability - can be implemented as written?
"""
)
```

## Output Format

```markdown
## Tasks Created: {project}/{feature}

### Summary
- **Tasks created:** {count}
- **Review status:** Passed | Issues found

### Tasks
| Task | Description | Complexity |
|------|-------------|------------|
| TASK_001 | {desc} | Medium |
| TASK_002 | {desc} | Low |

### Review Notes
{from faion-tasks-reviewer}

### Next Steps
- Execute tasks with Section 6
- Or batch execute with Section 7
```

**Output:** Task files in `tasks/todo/` → Next: Task Execution

---

# Section 6: Task Execution

## Purpose

Execute a single SDD task using the `faion-task-executor` agent.

## Workflow

```
1. Parse project, feature, task_name
   ↓
2. Find task file in todo/ or in-progress/
   ↓
3. Load SDD context (constitution, spec, design, impl-plan)
   ↓
4. Call faion-task-executor agent
   ↓
5. Report results
```

## Task Resolution

Search order:
1. `tasks/in-progress/TASK_*{name}*.md`
2. `tasks/todo/TASK_*{name}*.md`

Partial match supported: "TASK_001", "001", "models"

## Context Loading

Load these files for agent context:
```
aidocs/sdd/{project}/constitution.md
aidocs/sdd/{project}/features/{status}/{feature}/spec.md
aidocs/sdd/{project}/features/{status}/{feature}/design.md
aidocs/sdd/{project}/features/{status}/{feature}/implementation-plan.md
{task_file}
```

## Agent Invocation

```python
Task(
    subagent_type="faion-task-executor",
    description=f"Execute {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_FILE: {task_path}

SDD CONTEXT:
- Constitution: {constitution_content}
- Spec: {spec_content}
- Design: {design_content}
- Implementation Plan: {impl_plan_content}

TASK CONTENT:
{task_content}

EXECUTION STEPS:
1. Move task to in-progress/ (if in todo/)
2. Deep research - understand codebase context
3. Plan subtasks using TodoWrite
4. Execute implementation
5. Quality checks (tests, linting)
6. Commit with message: "TASK_XXX: {description}"
7. Move task to done/
"""
)
```

## Task Lifecycle

```
tasks/todo/TASK_XXX.md
       ↓ (start execution)
tasks/in-progress/TASK_XXX.md
       ↓ (complete successfully)
tasks/done/TASK_XXX.md
```

## Output Format

```markdown
## Task Execution: {TASK_NAME}

**Status:** SUCCESS | FAILED | BLOCKED

### Summary
{what was done}

### Files Changed
- {file1}: {change description}
- {file2}: {change description}

### Commit
{commit_hash}: {commit_message}

### Notes
{any issues or blockers}
```

## Error Handling

| Error | Action |
|-------|--------|
| Task not found | List available tasks, ask user |
| Context missing | Warn, continue with available context |
| Execution failed | Report error, keep task in in-progress |
| Tests failed | Document failures, don't move to done |

**Output:** Executed task in `done/` → Next: Batch Execution or Parallelization

---

# Section 7: Batch Execution

## Purpose

Execute all tasks for a feature in sequence, with intelligent failure handling.

## Workflow

```
1. Parse project, feature
   ↓
2. Find all tasks (in-progress first, then todo, sorted)
   ↓
3. Load SDD context
   ↓
4. Clarify ambiguities BEFORE execution
   ↓
5. Create feature branch (optional)
   ↓
6. Execute each task via Section 6
   ↓
7. Run post-execution review
   ↓
8. Quality checks (tests, lint)
   ↓
9. Report summary
```

## Task Discovery

```bash
# Priority order
1. tasks/in-progress/TASK_*.md  # Resume first
2. tasks/todo/TASK_*.md         # Then new tasks

# Sort by task number
TASK_001, TASK_002, TASK_003...
```

## Pre-Execution Clarification

Before starting, review all tasks for:
- Ambiguous requirements
- Missing dependencies
- Unclear acceptance criteria

Use AskUserQuestion if clarification needed.

## Execution Loop

```python
for task in sorted_tasks:
    result = execute_task(project, feature, task.name)

    if result.status == "BLOCKED":
        if is_critical(result.error):
            STOP  # Git conflict, build broken, security
        else:
            CONTINUE  # Test failures, minor issues

    log_result(result)
```

## Continue vs Stop Rules

**Continue if:**
- Single task fails (document and continue)
- Test failures (log for later fix)
- Minor code style issues
- Non-blocking warnings

**Stop if:**
- Git merge conflict
- Build completely broken
- Security vulnerability detected
- User requests stop

## Post-Execution Review

```python
Task(
    subagent_type="faion-tasks-reviewer",
    prompt=f"Review completed tasks for {project}/{feature}"
)
```

## Output Format

```markdown
## Feature Execution: {project}/{feature}

### Summary
- **Tasks:** {completed}/{total}
- **Status:** Complete | Partial | Failed
- **Duration:** {time}

### Task Results
| Task | Status | Commit | Notes |
|------|--------|--------|-------|
| TASK_001 | Done | abc123 | |
| TASK_002 | Done | def456 | |
| TASK_003 | Blocked | - | Tests failing |

### Quality Report
- Tests: {pass}/{total}
- Lint: {status}

### Next Steps
{recommendations}
```

**Output:** All tasks in `done/` (or partial) → Next: Feature complete or Parallelization

---

# Section 8: Parallelization Logic

## Purpose

Analyze task dependencies and group into parallel execution waves. Achieve up to 3.5x speedup through optimized execution order.

## Workflow

```
1. Read all TASK_*.md files
   ↓
2. Extract dependencies from each task
   ↓
3. Build dependency graph
   ↓
4. Group into waves (independent tasks together)
   ↓
5. Add checkpoints between waves
   ↓
6. Generate execution plan
```

## Dependency Detection

### Explicit Dependencies
From task files:
```markdown
## Dependencies
- TASK_001 must complete first
- Requires auth module from TASK_002
```

### Implicit Dependencies
Detect from:
- File modifications (same file = sequential)
- Module imports (importing from task output)
- Database schema (migrations order)
- API contracts (consumer after producer)

## Wave Pattern

```
Wave 1: [Independent tasks - run in parallel]
    ↓
Checkpoint 1: Verify all Wave 1 complete, merge results
    ↓
Wave 2: [Tasks depending on Wave 1 - run in parallel]
    ↓
Checkpoint 2: Verify, merge
    ↓
Wave N: [Final tasks]
    ↓
Final Checkpoint: Integration verification
```

## Dependency Graph Example

```
TASK_001 ──┬──→ TASK_004 ──┐
           │               │
TASK_002 ──┼──→ TASK_005 ──┼──→ TASK_006
           │               │
TASK_003 ──┴───────────────┘
```

Wave 1: TASK_001, TASK_002, TASK_003 (parallel)
Wave 2: TASK_004, TASK_005 (parallel)
Wave 3: TASK_006 (sequential)

## Speedup Calculation

```
Sequential time = Sum of all task times
Parallel time = Sum of longest task per wave + checkpoints

Speedup = Sequential / Parallel
```

Example:
- 6 tasks, 30 min each = 180 min sequential
- 3 waves (3+2+1 tasks) + 2 checkpoints (5 min each)
- Parallel = 30 + 5 + 30 + 5 + 30 = 100 min
- Speedup = 180/100 = 1.8x

With more parallelizable tasks: up to 3.5x

## Checkpoint Types

| Type | When | Action |
|------|------|--------|
| Merge | After parallel wave | Combine outputs, resolve conflicts |
| Verify | Critical dependency | Run tests, check contracts |
| Review | Complex integration | Human review before continuing |
| Sync | State-dependent | Ensure consistent state |

## Output Format

```markdown
## Parallel Execution Plan

### Summary
- Total tasks: {N}
- Waves: {M}
- Estimated speedup: {X}x
- Critical path: TASK_A → TASK_D → TASK_G

### Wave 1 (Parallel)
| Task | Description | Est. Tokens |
|------|-------------|-------------|
| TASK_001 | Setup models | 3000 |
| TASK_002 | Setup serializers | 2500 |
| TASK_003 | Setup permissions | 2000 |

**Checkpoint 1:** Verify models, serializers, permissions created

### Wave 2 (Parallel)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_004 | TASK_001 | Create views |
| TASK_005 | TASK_001, TASK_002 | Create API endpoints |

**Checkpoint 2:** Verify API endpoints functional

### Wave 3 (Sequential - Critical Path)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_006 | TASK_004, TASK_005 | Integration tests |

**Final Checkpoint:** All tests pass
```

## Integration

- After Section 5 (Task Creation) → Auto-analyze parallelization
- Add wave structure to implementation-plan.md
- Execute in wave order with Section 7

**Output:** Parallelized execution plan → Execute with optimized order

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-spec-reviewer | Review spec before save |
| faion-design-reviewer | Review design for architecture decisions |
| faion-impl-plan-reviewer | Review impl-plan for 100k token compliance |
| faion-task-creator | Create individual tasks with deep research |
| faion-task-executor | Execute tasks autonomously |
| faion-tasks-reviewer | Review completed tasks (4-pass) |
| faion-hallucination-checker | Verify task completion with evidence |

---

# Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md                    # Project principles (Section 1)
├── contracts.md                       # API contracts
├── roadmap.md                         # Milestones
└── features/
    ├── backlog/                       # Features waiting for grooming
    ├── todo/                          # Features ready for execution
    ├── in-progress/                   # Features being worked on
    └── done/                          # Completed features
        └── {NN}-{feature}/
            ├── spec.md                # WHAT and WHY (Section 2)
            ├── design.md              # HOW (Section 3)
            ├── implementation-plan.md # Tasks breakdown (Section 4)
            └── tasks/
                ├── backlog/
                ├── todo/              # Tasks ready (Section 5 output)
                ├── in-progress/       # Currently executing (Section 6)
                └── done/              # Completed (Section 6/7 output)
```

---

# Quick Reference

| Section | Purpose | Input | Output |
|---------|---------|-------|--------|
| 1 | Constitutions | Project analysis/dialogue | constitution.md |
| 2 | Specifications | Problem + requirements | spec.md |
| 3 | Design Documents | Approved spec | design.md |
| 4 | Implementation Plans | Design + 100k rule | implementation-plan.md |
| 5 | Task Creation | Impl-plan + codebase | Task files in todo/ |
| 6 | Task Execution | Single task | Task in done/ + commit |
| 7 | Batch Execution | All tasks | All tasks done/ |
| 8 | Parallelization | Task dependencies | Optimized wave plan |

---

*SDD Domain Skill v1.1 - Part 1+2 of 3*
*Sections 1-4: Constitutions, Specifications, Design, Implementation Plans*
*Sections 5-8: Task Creation, Execution, Batch Execution, Parallelization*
*Next: Part 3 (Quality Gates, Reflexion, Workflows)*
