# SDD Section Summaries

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Guide through workflow sections | sonnet | Medium-complexity workflow explanation |
| Create specification documents | sonnet | Medium-complexity document authoring |
| Generate implementation plans | sonnet | Medium-complexity task decomposition |
| Execute task workflow | haiku | Mechanical task execution orchestration |
| Analyze parallelization opportunities | opus | Complex dependency analysis and optimization |

Quick overview of all 13 workflow sections.

---

## Section 1: Constitutions

**Purpose:** Define immutable project principles.

**Modes:**
1. **Existing Project** - Analyze codebase, present findings, draft
2. **New Project** - Socratic dialogue: Vision -> Tech -> Architecture -> Standards

**Output:** `.aidocs/constitution.md`

**Details:** [workflows.md#1](workflows.md#1-writing-constitutions) | [templates.md](templates.md#constitution-template)

---

## Section 2: Specifications

**Purpose:** Define WHAT and WHY.

**Workflow:** Brainstorm -> Research -> Clarify -> Draft -> Review -> Save

**Key Techniques:**
- Five Whys for root cause
- Alternatives (A/B/C) with pros/cons
- User stories (As/I want/So that)
- Given-When-Then acceptance criteria

**Review:** Call `faion-sdd-reviewer-agent (mode: spec)` before save.

**Output:** `features/{status}/{feature}/spec.md`

**Details:** [workflows.md#2](workflows.md#2-writing-specifications) | [templates.md](templates.md#specification-template)

---

## Section 3: Design Documents

**Purpose:** Define HOW.

**Prerequisites:** Approved spec.md, constitution.md

**Workflow:** Read Spec -> Read Constitution -> Research -> Decisions -> Approach -> Testing -> Risks -> Review -> Save

**Key Elements:**
- Architecture Decisions (AD-X) with context, options, rationale
- File mappings (CREATE/MODIFY)
- API endpoints (reference contracts.md)
- Testing strategy

**Review:** Call `faion-sdd-reviewer-agent (mode: design)` before save.

**Output:** `features/{status}/{feature}/design.md`

**Details:** [workflows.md#3](workflows.md#3-design-doc-structure) | [templates.md](templates.md#design-document-template)

---

## Section 4: Implementation Plans

**Purpose:** Break design into 100k-compliant tasks.

**Workflow:** Load Context -> Analyze Complexity -> Work Units -> Apply 100k Rule -> Dependencies -> Review -> Save

**Key Elements:**
- Token estimates per task
- Dependency graph
- Execution waves (parallel/sequential)
- Critical path

**Review:** Call `faion-sdd-reviewer-agent (mode: plan)` before save.

**Output:** `features/{status}/{feature}/implementation-plan.md`

**Details:** [workflows.md#4](workflows.md#4-writing-implementation-plans) | [templates.md](templates.md#implementation-plan-template)

---

## Section 5: Task Creation

**Purpose:** Create TASK_*.md files from implementation plan.

**Agent:** `faion-task-creator-agent`

**Workflow:** Load SDD -> Verify documents -> For each task: Call agent -> Review all tasks

**Review:** Call `faion-sdd-reviewer-agent (mode: tasks)` (4-pass review).

**Output:** Task files in `tasks/todo/`

**Details:** [workflows.md#5](workflows.md#5-task-creation) | [templates.md](templates.md#task-file-template)

---

## Section 6: Task Execution

**Purpose:** Execute single task.

**Agent:** `faion-task-executor-agent`

**Workflow:** Find task -> Load context -> Execute -> Quality checks -> Commit -> Move to done

**Task Lifecycle:**
```
tasks/todo/ -> tasks/in-progress/ -> tasks/done/
```

**Output:** Executed task + commit

**Details:** [workflows.md#6](workflows.md#6-task-execution)

---

## Section 7: Batch Execution

**Purpose:** Execute all tasks for a feature.

**Workflow:** Find all tasks -> Load context -> Clarify -> Execute each -> Review -> Report

**Continue/Stop Rules:**
- **Continue:** Single task fails, test failures, minor issues
- **Stop:** Git conflict, build broken, security issue

**Output:** All tasks in done/ (or partial)

**Details:** [workflows.md#7](workflows.md#7-batch-execution)

---

## Section 8: Parallelization

**Purpose:** Optimize execution with wave pattern.

**Workflow:** Read tasks -> Extract dependencies -> Build graph -> Group waves -> Add checkpoints

**Wave Pattern:**
```
Wave 1: [Independent] -> Checkpoint -> Wave 2: [Dependent] -> ... -> Final
```

**Speedup:** 1.8x - 3.5x typical

**Output:** Parallelized execution plan

**Details:** [workflows.md#8](workflows.md#8-parallelization-analysis)

---

## Section 9: Backlog Grooming

**Purpose:** Prepare features for execution.

**Workflow:** Load backlog -> Display status -> Select feature -> Refine spec -> Create design -> Generate tasks -> Move to todo

**Definition of Ready:**
- Problem clear, AC defined, dependencies known
- Spec approved, design approved, tasks created

**Output:** Feature with complete artifacts in todo/

**Details:** [workflows.md#9](workflows.md#9-backlog-grooming)

---

## Section 10: Roadmapping

**Purpose:** Strategic planning and progress tracking.

**Structure:**
- **Now (90%):** Detailed, committed
- **Next (70%):** Planned, flexible
- **Later (50%):** Thematic, vision

**Output:** `roadmap.md`

**Details:** [workflows.md#10](workflows.md#10-roadmapping) | [templates.md](templates.md#roadmap-template)

---

## Section 11: Quality Gates

**Purpose:** Code and SDD document reviews.

**Code Review Criteria:**
- Critical: Correctness, tests, security
- Style: Conventions, patterns, naming
- Quality: Complexity, error handling
- Performance: N+1, indexes, leaks

**SDD Review:** Sequential reviewers (spec -> design -> plan -> tasks)

**Output:** Review report with verdict

**Details:** [workflows.md#11](workflows.md#11-quality-gates)

---

## Section 12: Confidence Checks

**Purpose:** Pre-phase validation to prevent wasted work.

**Phases:**
- Pre-Spec: Problem validated? Market gap? Target audience?
- Pre-Design: Requirements clear? AC testable? Scope defined?
- Pre-Task: Architecture decided? Patterns established?
- Pre-Implementation: Task clear? Approach decided? No blockers?

**Output:** Confidence score + recommendation

**Details:** [workflows.md#12](workflows.md#12-confidence-checks) | [templates.md](templates.md#confidence-check-template)

---

## Section 13: Reflexion Learning

**Purpose:** PDCA cycle - learn from outcomes.

**Cycle:** Plan -> Do -> Check -> Act -> Store

**Triggers:**
- After task success: Extract patterns
- After task failure: Analyze root cause, store solution
- Before task start: Check memory for warnings/recommendations

**Output:** Lessons in `.aidocs/memory/` + CLAUDE.md update

**Details:** [workflows.md#13](workflows.md#13-reflexion-learning) | [templates.md](templates.md#pattern-record-template)

---

*SDD Section Summaries v1.0*
