# SDD Workflow: Design Phase

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Read and extract specification requirements | haiku | Mechanical content extraction |
| Research codebase for patterns | sonnet | Medium-complexity exploration and analysis |
| Make architecture decisions | opus | Complex decision-making with trade-offs |
| Write design document | sonnet | Medium-complexity document composition |
| Create implementation plan with tasks | sonnet | Medium-complexity task decomposition |

Detailed workflows for creating design documents and implementation plans.

---

## Table of Contents

1. [Writing Design Documents](#1-design-doc-structure)
2. [Writing Implementation Plans](#2-writing-implementation-plans)
3. [Task Creation](#3-task-creation)
4. [Parallelization Analysis](#4-parallelization-analysis)

---

## 1. Writing Design Documents

### Prerequisites

1. `spec.md` exists with status `approved`
2. `constitution.md` exists at `.aidocs/constitution.md`
3. `contracts.md` exists (for API features)

### Workflow

```
READ SPEC -> READ CONSTITUTION -> RESEARCH -> DECISIONS -> APPROACH -> TESTING -> RISKS -> REVIEW -> SAVE
```

### Phase 1: Read Specification

Extract from spec.md:
- Problem Statement
- User Stories
- Functional Requirements
- API Contract (if present)
- Data Model (if present)
- Out of Scope

### Phase 2: Read Constitution

Extract from constitution.md:
- Architecture patterns
- Code standards
- Testing requirements

### Phase 3: Read API Contracts (if API feature)

**IMPORTANT:** Do NOT redefine API endpoints in design.md. Reference contracts.md:
```markdown
## API Endpoints

This feature implements endpoints from [contracts.md](../../contracts.md):
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
```

### Phase 4: Research Codebase

Use Grep and Glob to find:
- Similar models
- Similar services
- Similar views
- Existing patterns

Determine:
- Reusable components
- Patterns in use
- Where to place new code

### Phase 5: Architecture Decisions

For each key decision:
1. Define context - what problem solving
2. List options - minimum 2 alternatives
3. Choose solution - which and why
4. Document rationale

### Phase 6: Define Technical Approach

1. **Components** - new components, interactions
2. **Data Flow** - data path, validation, error handling
3. **Files** - CREATE and MODIFY lists with scope

### Phase 7: Define Testing Strategy

Based on constitution:
1. Unit tests - isolated testing targets
2. Integration tests - flow coverage
3. Test data - required fixtures

### Phase 8: Identify Risks

For each risk:
- Description
- Impact (High/Medium/Low)
- Mitigation strategy

### Phase 9: Review with User

Present key decisions:
1. Architecture Decisions - agreement check
2. Technical Approach - better alternatives?
3. Risks - completeness check

### Phase 10: Agent Review

Call `faion-sdd-reviewer-agent (mode: design)`. Checks:
- FR coverage
- AD structure (context, options, rationale)
- Constitution compliance
- Files list completeness

### Phase 11: Save

Save to: `{feature_path}/design.md`

---

## 2. Writing Implementation Plans

### Key Principle

**Each task MUST fit 100k token context** = atomic, single-agent executable.

### Workflow

```
LOAD CONTEXT -> ANALYZE COMPLEXITY -> DEFINE WORK UNITS -> APPLY 100k RULE -> DEPENDENCIES -> DRAFT -> REVIEW -> SAVE
```

### Phase 1: Load Context

Read: `constitution.md`, `spec.md`, `design.md`

### Phase 2: Analyze Complexity

For each file in design.md:

| File | Action | Complexity | Est. Tokens |
|------|--------|------------|-------------|
| models.py | CREATE | High | 40k |
| services.py | CREATE | High | 50k |

**Factors:** LOC, dependencies, business logic, tests

### Phase 3: Define Work Units

Group related work:
```markdown
## Work Unit 1: Data Layer
- models.py (CREATE)
Est: 40k tokens
```

### Phase 4: Apply 100k Rule

```
Research: ~20k (read existing code)
Task file: ~5k
Implementation: ~50k
Buffer: ~25k
TOTAL < 100k
```

**If > 100k:** Split into smaller tasks.

### Phase 5: Map Dependencies

| Task | Depends On | Enables |
|------|------------|---------|
| TASK_001 | - | TASK_003 |
| TASK_002 | - | TASK_003 |
| TASK_003 | 001, 002 | - |

Rules: No cycles, maximize parallelization.

### Phase 6: Draft

Show section by section:
- Overview (total tasks, critical path, est. tokens)
- Tasks list (files, deps, FR/AD coverage, AC)
- Execution order (phases, parallel/sequential)

### Phase 7: Review

Call `faion-sdd-reviewer-agent (mode: plan)`. Checks: 100k compliance, deps, coverage.

### Phase 8: Save

`.aidocs/features/{feature}/implementation-plan.md`

---

## 3. Task Creation

### Workflow

```
1. Load SDD documents
   |
2. Verify: spec approved? design approved?
   |
3. Check/create implementation-plan
   |
4. For each task in plan:
   -> Call faion-task-creator-agent
   |
5. Run faion-sdd-reviewer-agent (mode: tasks) (4-pass)
   |
6. Report results
```

### Document Verification

Check these files exist and are approved:
```
.aidocs/features/{status}/{feature}/spec.md
.aidocs/features/{status}/{feature}/design.md
.aidocs/features/{status}/{feature}/implementation-plan.md
```

If implementation-plan missing: Create it first.

### Task Creation Call

```python
Task(
    subagent_type="faion-task-creator-agent",
    description=f"Create {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_INFO: {task_from_plan}
SDD_PATH: .aidocs/features/{status}/{feature}/

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

### Task Review (4-Pass)

```python
Task(
    subagent_type="faion-sdd-reviewer-agent",
    prompt=f"""
MODE: tasks
PROJECT: {project}
FEATURE: {feature}

Multi-pass review:
Pass 1: Completeness - all plan items covered?
Pass 2: Consistency - no contradictions?
Pass 3: Coverage - all requirements addressed?
Pass 4: Executability - can be implemented as written?
"""
)
```

---

## 4. Parallelization Analysis

### Workflow

```
1. Read all TASK_*.md files
   |
2. Extract dependencies from each task
   |
3. Build dependency graph
   |
4. Group into waves (independent tasks together)
   |
5. Add checkpoints between waves
   |
6. Generate execution plan
```

### Dependency Detection

**Explicit:** From task files
```markdown
## Dependencies
- TASK_001 must complete first
- Requires auth module from TASK_002
```

**Implicit:** Detect from
- File modifications (same file = sequential)
- Module imports (importing from task output)
- Database schema (migrations order)
- API contracts (consumer after producer)

### Wave Pattern

```
Wave 1: [Independent tasks - parallel]
    |
Checkpoint 1: Verify all Wave 1 complete
    |
Wave 2: [Tasks depending on Wave 1 - parallel]
    |
Checkpoint 2: Verify, merge
    |
Wave N: [Final tasks]
    |
Final Checkpoint: Integration verification
```

### Speedup Calculation

```
Sequential time = Sum of all task times
Parallel time = Sum of longest task per wave + checkpoints
Speedup = Sequential / Parallel
```

Typical speedup: 1.8x - 3.5x

### Checkpoint Types

| Type | When | Action |
|------|------|--------|
| Merge | After parallel wave | Combine outputs, resolve conflicts |
| Verify | Critical dependency | Run tests, check contracts |
| Review | Complex integration | Human review before continuing |
| Sync | State-dependent | Ensure consistent state |

---

*SDD Design Phase Workflows v1.0*
*Use with faion-sdd skill*
