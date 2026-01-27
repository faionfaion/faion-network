# Implementation Workflow

Step-by-step workflow for planning and executing implementation with LLM assistance.

---

## Overview

The implementation workflow covers two distinct phases:
1. **Planning Phase**: Create implementation plan and tasks from design.md
2. **Execution Phase**: Execute tasks wave by wave with quality gates

```
PLANNING PHASE                           EXECUTION PHASE
==============                           ===============

LOAD-CONTEXT -> ANALYZE -> DEFINE-UNITS -> DEPENDENCIES -> WAVES -> TASKS
      |            |            |              |             |        |
   design.md   complexity    group by       map deps      parallel   TASK-XXX
                matrix        100k rule                   groups

                                              |
                                              v

                            EXECUTE-WAVE -> QUALITY-GATE -> NEXT-WAVE
                                  |              |              |
                               code           tests          repeat
                               write          lint           or done
```

---

## Part A: Planning Phase

### Prerequisites

| Requirement | Status Check |
|-------------|--------------|
| design.md exists | `.aidocs/{status}/feature-XXX/design.md` |
| design.md approved | `status: approved` in frontmatter |
| File structure defined | CREATE/MODIFY lists in design.md |
| API contracts specified | If applicable |

---

### Phase A1: Load Context

#### Purpose

Load all SDD documents needed for planning.

#### Entry State

```
INPUT: Approved design.md path
STATE: load-context
CONFIDENCE: 0%
```

#### Workflow Steps

```
1. Load design.md
   |
   +---> Extract AD-XXX decisions
   +---> Extract file structure
   +---> Extract testing strategy
   |
   v
2. Load spec.md
   |
   +---> Extract FR-XXX for traceability
   +---> Extract AC-XXX for verification
   |
   v
3. Load constitution.md
   |
   +---> Extract code standards
   +---> Extract testing requirements
   |
   v
4. Create context summary
```

#### Context Summary Template

```markdown
## Implementation Context

### Feature
- Name: [feature-XXX]
- Spec: [path]
- Design: [path]

### Requirements Summary
| FR | Description | Priority |
|----|-------------|----------|
| FR-001 | [Summary] | Must |

### Architecture Decisions
| AD | Decision | Impact |
|----|----------|--------|
| AD-001 | [Summary] | [Files affected] |

### Files to Implement
| Action | File | Complexity |
|--------|------|------------|
| CREATE | [path] | [estimate] |
| MODIFY | [path] | [estimate] |

### Testing Requirements
- Coverage: [%]
- Types: [unit, integration, e2e]
```

#### Exit Criteria

- [ ] All SDD documents loaded
- [ ] FR-XXX to AD-XXX traceability understood
- [ ] File structure extracted

#### Exit State

```
OUTPUT: Context summary
STATE: analyze
CONFIDENCE: 20%
```

---

### Phase A2: Analyze Complexity

#### Purpose

Estimate complexity and token usage for each file.

#### Entry State

```
INPUT: Context summary
STATE: analyze
CONFIDENCE: 20%
```

#### Workflow Steps

```
1. For each file in design.md:
   |
   +---> Estimate lines of code
   +---> Estimate test lines
   +---> Calculate token estimate
   +---> Assess complexity factors
   |
   v
2. Create complexity matrix
   |
   v
3. Identify high-risk items
```

#### Complexity Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Business logic | Simple CRUD | Validation rules | Complex algorithms |
| Dependencies | None | Internal modules | External services |
| Data complexity | Simple types | Nested objects | Graphs/relations |
| Integration | Isolated | Internal APIs | External APIs |
| Test difficulty | Obvious cases | Edge cases | Async/timing |

#### Complexity Matrix Template

```markdown
## Complexity Analysis

| File | Action | LOC Est. | Test LOC | Total Tokens | Complexity | Risk |
|------|--------|----------|----------|--------------|------------|------|
| models.py | CREATE | 100 | 150 | ~15k | Medium | Low |
| service.py | CREATE | 300 | 400 | ~40k | High | Medium |
| views.py | MODIFY | +50 | +100 | ~10k | Low | Low |

### High-Risk Items
- [file]: [risk reason]

### Total Estimate
- Files: [N]
- Total tokens: [~Xk]
- Complexity: [Low/Medium/High]
```

#### Exit Criteria

- [ ] All files assessed
- [ ] Token estimates calculated
- [ ] High-risk items identified

#### Exit State

```
OUTPUT: Complexity matrix
STATE: define-units
CONFIDENCE: 35%
```

---

### Phase A3: Define Work Units

#### Purpose

Group related work respecting the 100k token rule.

#### Entry State

```
INPUT: Complexity matrix
STATE: define-units
CONFIDENCE: 35%
```

#### The 100k Token Rule

```
Each task must fit within LLM context window:

Research:        ~20k tokens (read existing code)
Task context:    ~5k tokens (spec, design, plan)
Implementation:  ~50k tokens (generated code + tests)
Buffer:          ~25k tokens (iterations, fixes)
────────────────────────────────────────────────
TOTAL:          <100k tokens
```

#### Workflow Steps

```
1. Group related files
   |
   +---> Same domain/module together
   +---> Same layer together
   +---> Logical units of work
   |
   v
2. Calculate work unit size
   |
   +---> Sum token estimates
   +---> Apply 100k rule
   |
   v
3. Split if necessary
   |
   +---> If > 60k implementation tokens: split
   +---> Identify natural split points
   |
   v
4. Create work unit definitions
```

#### Work Unit Template

```markdown
## Work Unit 1: [Name]

### Description
[What this unit accomplishes]

### Files
| File | Action | Tokens |
|------|--------|--------|
| [path] | CREATE | ~Xk |
| [path] | CREATE | ~Xk |

### Total Tokens: ~Xk

### Covers
- FR-XXX
- AD-XXX

### Dependencies
- [None | Work Unit X]
```

#### Splitting Strategies

| Scenario | Split By |
|----------|----------|
| Large model file | Split by entity/table |
| Large service file | Split by operation type |
| Large test file | Split by test category |
| Complex integration | Split by integration point |

#### Exit Criteria

- [ ] All files assigned to work units
- [ ] Each work unit < 60k implementation tokens
- [ ] Related work grouped together

#### Exit State

```
OUTPUT: Work unit definitions
STATE: dependencies
CONFIDENCE: 50%
```

---

### Phase A4: Map Dependencies

#### Purpose

Identify task dependencies and execution order.

#### Entry State

```
INPUT: Work unit definitions
STATE: dependencies
CONFIDENCE: 50%
```

#### Workflow Steps

```
1. Identify explicit dependencies
   |
   +---> File imports
   +---> API consumers
   +---> Database schema order
   |
   v
2. Identify implicit dependencies
   |
   +---> Same file modifications (sequential)
   +---> Shared module usage
   +---> Configuration dependencies
   |
   v
3. Build dependency graph
   |
   v
4. Detect cycles
   |
   +---> If cycles found: refactor work units
   |
   v
5. Calculate critical path
```

#### Dependency Types

| Type | Symbol | Meaning |
|------|--------|---------|
| Finish-to-Start (FS) | A -> B | B starts after A finishes |
| Start-to-Start (SS) | A => B | B can start when A starts |
| Finish-to-Finish (FF) | A >> B | B finishes after A finishes |

#### Dependency Matrix Template

```markdown
## Dependency Analysis

### Dependency Graph
```
TASK_001 (models) ─────┐
                       ├──> TASK_003 (service)
TASK_002 (schemas) ────┘          │
                                  v
                            TASK_004 (views)
                                  │
                                  v
                            TASK_005 (tests)
```

### Dependency Table
| Task | Depends On | Enables | Type |
|------|------------|---------|------|
| TASK_001 | - | TASK_003 | - |
| TASK_002 | - | TASK_003 | - |
| TASK_003 | 001, 002 | TASK_004 | FS |
| TASK_004 | 003 | TASK_005 | FS |

### Critical Path
TASK_001 -> TASK_003 -> TASK_004 -> TASK_005
```

#### Exit Criteria

- [ ] All dependencies mapped
- [ ] No cycles detected
- [ ] Critical path identified

#### Exit State

```
OUTPUT: Dependency graph
STATE: waves
CONFIDENCE: 65%
```

---

### Phase A5: Create Waves

#### Purpose

Group independent tasks into parallel execution waves.

#### Entry State

```
INPUT: Dependency graph
STATE: waves
CONFIDENCE: 65%
```

#### Wave Pattern

```
Wave 1: [All tasks with no dependencies]
    |
    v
Checkpoint 1: Verify Wave 1 complete, merge, test
    |
    v
Wave 2: [Tasks depending on Wave 1]
    |
    v
Checkpoint 2: Verify Wave 2 complete, merge, test
    |
    v
...
    |
    v
Wave N: [Final tasks]
    |
    v
Final Checkpoint: Integration verification
```

#### Workflow Steps

```
1. Identify Wave 1
   |
   +---> All tasks with no dependencies
   |
   v
2. For each subsequent wave:
   |
   +---> Find tasks whose dependencies are all in previous waves
   +---> Group as Wave N
   |
   v
3. Define checkpoints
   |
   +---> After each wave
   +---> Integration points
   |
   v
4. Calculate speedup
   |
   +---> Sequential time vs parallel time
```

#### Wave Definition Template

```markdown
## Execution Waves

### Wave 1 (Parallel)
| Task | Focus | Tokens | Can Parallelize |
|------|-------|--------|-----------------|
| TASK_001 | Models | ~30k | Yes |
| TASK_002 | Schemas | ~20k | Yes |

**Checkpoint 1:**
- [ ] All models created
- [ ] Schema validation passes
- [ ] No migration conflicts

### Wave 2 (Parallel)
| Task | Focus | Depends On | Tokens |
|------|-------|------------|--------|
| TASK_003 | Service | 001, 002 | ~40k |

**Checkpoint 2:**
- [ ] Service tests pass
- [ ] Integration with models works

### Wave 3 (Sequential)
| Task | Focus | Depends On | Tokens |
|------|-------|------------|--------|
| TASK_004 | Views | 003 | ~25k |
| TASK_005 | E2E | 004 | ~15k |

**Final Checkpoint:**
- [ ] All tests pass
- [ ] API contracts verified
- [ ] AC criteria met

### Speedup Analysis
- Sequential: 5 tasks x avg 30min = 150min
- Parallel (2 agents): Wave1(30min) + Wave2(30min) + Wave3(40min) = 100min
- **Speedup: 1.5x**
```

#### Checkpoint Types

| Type | When | Action |
|------|------|--------|
| Merge | After parallel wave | Combine outputs, resolve conflicts |
| Verify | Critical dependency | Run tests, check contracts |
| Review | Complex integration | Human review before continuing |
| Sync | State-dependent | Ensure consistent state |

#### Exit Criteria

- [ ] All tasks assigned to waves
- [ ] Checkpoints defined
- [ ] Parallelization opportunities identified

#### Exit State

```
OUTPUT: Wave plan
STATE: tasks
CONFIDENCE: 75%
```

---

### Phase A6: Create Tasks

#### Purpose

Generate TASK-XXX.md files for each work unit.

#### Entry State

```
INPUT: Wave plan
STATE: tasks
CONFIDENCE: 75%
```

#### Workflow Steps

```
1. For each work unit:
   |
   +---> Generate TASK-XXX.md
   +---> Include SDD references
   +---> Include file list
   +---> Include acceptance criteria
   |
   v
2. Review task set
   |
   +---> Completeness check
   +---> 100k compliance
   +---> Dependency accuracy
   |
   v
3. Save tasks to todo/
```

#### Task File Template

```markdown
---
id: TASK-{XXX}
feature: feature-{NNN}
wave: {N}
status: todo
depends_on: [TASK-XXX, TASK-YYY]
tokens_estimate: ~Xk
complexity: Low | Medium | High
---

# TASK-{XXX}: [Title]

## SDD References

| Document | Path |
|----------|------|
| Spec | .aidocs/{status}/feature-{NNN}/spec.md |
| Design | .aidocs/{status}/feature-{NNN}/design.md |
| Impl-Plan | .aidocs/{status}/feature-{NNN}/implementation-plan.md |

## Objective

[Clear statement of what this task accomplishes]

## Requirements Coverage

### FR-{XXX}: [Requirement Title]
[Full requirement text from spec]

### AD-{XXX}: [Decision Title]
[Decision summary from design]

## Acceptance Criteria

### AC-{XXX}.1: [Scenario Name]
**Given:** [Context]
**When:** [Action]
**Then:** [Expected result]

## Files to Change

| Action | File | Scope |
|--------|------|-------|
| CREATE | [path] | [description] |
| MODIFY | [path] | [description] |

## Technical Approach

### Step 1: [First step]
[Details]

### Step 2: [Second step]
[Details]

## Testing Requirements

- [ ] Unit tests for [X]
- [ ] Integration test for [Y]

## Dependencies

### Completed Before This Task
- TASK-{XXX}: [What it provides]

### Needed By Other Tasks
- TASK-{YYY}: [What this provides]

## Implementation Notes

[Any special considerations, patterns to follow, gotchas]
```

#### Exit Criteria

- [ ] All work units have TASK-XXX.md
- [ ] Each task fits 100k context
- [ ] Dependencies accurately reflected
- [ ] Acceptance criteria from spec

#### Exit State

```
OUTPUT: TASK-XXX.md files in todo/
STATE: complete (planning)
NEXT: execution phase
CONFIDENCE: 85%
```

---

## Part B: Execution Phase

### Prerequisites

| Requirement | Status Check |
|-------------|--------------|
| Implementation plan exists | `.aidocs/{status}/feature-XXX/implementation-plan.md` |
| Tasks created | TASK-XXX.md files in todo/ |
| Wave plan defined | Waves and checkpoints documented |

---

### Phase B1: Execute Wave

#### Purpose

Execute all tasks in current wave (sequentially or in parallel).

#### Entry State

```
INPUT: Wave with tasks
STATE: execute-wave
WAVE: N
```

#### Workflow Steps

```
1. Load wave tasks
   |
   +---> Read all TASK-XXX in wave
   +---> Verify dependencies complete
   |
   v
2. For each task (parallel if multiple agents):
   |
   +---> Move TASK-XXX.md to in-progress/
   +---> Load task context
   +---> Execute implementation
   +---> Run local quality checks
   +---> Commit changes
   +---> Move to done/ on success
   |
   v
3. Aggregate wave results
```

#### Task Execution Flow

```
1. CONTEXT LOADING
   |
   +---> Read TASK-XXX.md
   +---> Read referenced spec sections
   +---> Read referenced design sections
   +---> Read existing code patterns
   |
   v
2. IMPLEMENTATION
   |
   +---> Create files (if CREATE action)
   +---> Modify files (if MODIFY action)
   +---> Follow patterns from design
   +---> Add inline documentation
   |
   v
3. TESTING
   |
   +---> Write unit tests
   +---> Write integration tests (if applicable)
   +---> Run tests locally
   |
   v
4. QUALITY CHECKS
   |
   +---> Run linter
   +---> Run type checker
   +---> Run formatter
   +---> Fix issues from feedback
   |
   v
5. COMMIT
   |
   +---> Stage changes
   +---> Commit: "TASK-XXX: [description]"
   +---> Update task status
```

#### Parallel Execution Pattern

```
Wave N: Independent Tasks
        |
        +---> Agent 1: TASK_001 (git worktree A)
        +---> Agent 2: TASK_002 (git worktree B)
        +---> Agent 3: TASK_003 (git worktree C)
        |
        v
Merge Point: Combine all branches
        |
        v
Checkpoint: Run integration tests
```

#### Continue vs Stop Rules

| Scenario | Action |
|----------|--------|
| Single task fails (fixable) | Log, continue other tasks |
| Test failures (fixable) | Log, continue with warning |
| Minor code style issues | Auto-fix, continue |
| Git merge conflict | **STOP**, resolve manually |
| Build completely broken | **STOP**, investigate |
| Security vulnerability | **STOP**, report immediately |

#### Exit Criteria

- [ ] All tasks in wave attempted
- [ ] Successful tasks in done/
- [ ] Failed tasks documented
- [ ] Code committed

#### Exit State

```
OUTPUT: Wave completion status
STATE: quality-gate
WAVE: N
```

---

### Phase B2: Quality Gate

#### Purpose

Validate wave completion before proceeding.

#### Entry State

```
INPUT: Wave execution results
STATE: quality-gate
WAVE: N
```

#### Workflow Steps

```
1. Run quality checks
   |
   +---> L1: Syntax (lint)
   +---> L2: Types (type check)
   +---> L3: Unit tests
   +---> L4: Integration tests (if wave checkpoint)
   |
   v
2. Evaluate results
   |
   +---> All pass: Proceed
   +---> Failures: Attempt fix (max 3 retries)
   |
   v
3. Checkpoint verification
   |
   +---> Merge parallel work
   +---> Run combined tests
   +---> Verify contracts
```

#### Quality Gate Levels

| Level | Check | Pass Criteria | On Fail |
|-------|-------|---------------|---------|
| L1 | Linting | 0 errors | Auto-fix, retry |
| L2 | Types | 0 errors | Feed errors to LLM, retry |
| L3 | Unit Tests | 100% pass | Feed failures to LLM, retry |
| L4 | Integration | 100% pass | Review, may need rollback |
| L5 | Review | Approved | Address comments |
| L6 | Acceptance | All AC pass | Review requirements |

#### Feedback Loop Pattern

```
Test/Lint Failed
      |
      v
Extract error message
      |
      v
Feed to LLM: "Fix this error: [error]"
      |
      v
LLM generates fix
      |
      v
Apply fix
      |
      v
Re-run check
      |
      +---> Pass: Continue
      +---> Fail: Retry (max 3)
             |
             +---> Max retries: Escalate
```

#### Exit Criteria

- [ ] All quality gates passed
- [ ] Checkpoint criteria met
- [ ] Ready for next wave

#### Exit State

```
OUTPUT: Quality gate status
STATE: next-wave | complete
```

---

### Phase B3: Next Wave

#### Purpose

Proceed to next wave or complete execution.

#### Entry State

```
INPUT: Quality gate passed
STATE: next-wave
WAVE: N
```

#### Workflow Steps

```
1. Check remaining waves
   |
   +---> More waves: Go to Phase B1 with Wave N+1
   +---> No more waves: Go to Completion
   |
   v
2. Prepare next wave
   |
   +---> Verify all dependencies met
   +---> Load next wave tasks
```

#### Completion Flow

```
All Waves Complete
      |
      v
Final Integration
      |
      +---> Run all tests
      +---> Verify all AC
      +---> Check coverage
      |
      v
Generate Summary
      |
      +---> Tasks completed: [list]
      +---> Files changed: [list]
      +---> Tests added: [count]
      +---> Coverage: [%]
      |
      v
Move feature to done/
```

#### Exit State

```
OUTPUT: Feature implementation complete
STATE: complete
NEXT: review-workflow
```

---

## Decision Points

### Task Execution Decision Tree

```
START TASK
    |
    v
Dependencies complete?
    |
    +--NO--> Wait or execute dependency first
    |
    YES
    |
    v
Context fits 100k?
    |
    +--NO--> Split task further
    |
    YES
    |
    v
Patterns exist in codebase?
    |
    +--NO--> Check similar features, create pattern
    |
    YES
    |
    v
EXECUTE
    |
    v
Tests pass?
    |
    +--NO--> Feed failures, retry (max 3)
    |         |
    |         +--Still fails--> Escalate/mark blocked
    |
    YES
    |
    v
Lint/Type checks pass?
    |
    +--NO--> Auto-fix or feed errors
    |
    YES
    |
    v
COMMIT AND CONTINUE
```

### Blocker Handling

| Blocker Type | Action |
|--------------|--------|
| Missing dependency | Wait or prioritize dependency |
| Unclear requirement | Document assumption, proceed |
| External service down | Mock, continue, note for integration |
| Merge conflict | Stop, resolve, continue |
| Security issue | Stop, report, await decision |

---

## Parallel Execution Strategies

### Strategy 1: Git Worktrees

```bash
# Create worktree for each parallel task
git worktree add ../feature-task-001 feature-branch
git worktree add ../feature-task-002 feature-branch

# Execute in parallel
# Agent 1 works in ../feature-task-001
# Agent 2 works in ../feature-task-002

# Merge back
git checkout feature-branch
git merge feature-task-001
git merge feature-task-002
```

### Strategy 2: Feature Branches

```bash
# Each task gets a branch
git checkout -b task-001
# Execute task
git push origin task-001

# Repeat for other tasks

# Merge via PRs or direct merge
```

### Strategy 3: Single Branch Sequential

```bash
# One agent, one branch, tasks in order
git checkout feature-branch
# Execute TASK_001, commit
# Execute TASK_002, commit
# Execute TASK_003, commit
```

---

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| [design-workflow.md](design-workflow.md) | Input to planning phase |
| [review-workflow.md](review-workflow.md) | After execution complete |
| [llm-prompts.md](llm-prompts.md) | Prompts for execution |

---

*Implementation Workflow | SDD Workflows | v1.0.0*
