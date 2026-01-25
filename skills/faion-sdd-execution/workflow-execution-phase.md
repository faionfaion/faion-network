# SDD Workflow: Execution Phase

Detailed workflows for task execution, quality gates, and learning.

---

## Table of Contents

1. [Task Execution](#1-task-execution)
2. [Batch Execution](#2-batch-execution)
3. [Quality Gates](#3-quality-gates)
4. [Confidence Checks](#4-confidence-checks)
5. [Reflexion Learning](#5-reflexion-learning)

---

## 1. Task Execution

### Workflow

```
1. Parse project, feature, task_name
   |
2. Find task file in todo/ or in-progress/
   |
3. Load SDD context (constitution, spec, design, impl-plan)
   |
4. Call faion-task-executor-agent
   |
5. Report results
```

### Task Resolution

Search order:
1. `tasks/in-progress/TASK_*{name}*.md`
2. `tasks/todo/TASK_*{name}*.md`

Partial match supported: "TASK_001", "001", "models"

### Context Loading

Load these files:
```
.aidocs/constitution.md
.aidocs/features/{status}/{feature}/spec.md
.aidocs/features/{status}/{feature}/design.md
.aidocs/features/{status}/{feature}/implementation-plan.md
{task_file}
```

### Task Lifecycle

```
tasks/todo/TASK_XXX.md
       | (start execution)
tasks/in-progress/TASK_XXX.md
       | (complete successfully)
tasks/done/TASK_XXX.md
```

### Agent Invocation

```python
Task(
    subagent_type="faion-task-executor-agent",
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

---

## 2. Batch Execution

### Workflow

```
1. Parse project, feature
   |
2. Find all tasks (in-progress first, then todo, sorted)
   |
3. Load SDD context
   |
4. Clarify ambiguities BEFORE execution
   |
5. Create feature branch (optional)
   |
6. Execute each task via Task Execution workflow
   |
7. Run post-execution review
   |
8. Quality checks (tests, lint)
   |
9. Report summary
```

### Task Discovery

```bash
# Priority order
1. tasks/in-progress/TASK_*.md  # Resume first
2. tasks/todo/TASK_*.md         # Then new tasks

# Sort by task number
TASK_001, TASK_002, TASK_003...
```

### Continue vs Stop Rules

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

### Execution Loop

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

---

## 3. Quality Gates

### Code Review Mode

**Criteria:**

| Category | Check |
|----------|-------|
| Critical | Correctness, broken tests, security, breaking changes |
| Style | Convention violations, pattern deviations, naming |
| Quality | Complexity, error handling, edge cases |
| Performance | N+1 queries, missing indexes, resource leaks |

### SDD Review Mode

Run reviewers in sequence:
1. `faion-sdd-reviewer-agent (mode: spec)`
2. `faion-sdd-reviewer-agent (mode: design)`
3. `faion-sdd-reviewer-agent (mode: plan)`
4. `faion-sdd-reviewer-agent (mode: tasks)` (if tasks exist)

### Quality Gate Levels

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1 | Syntax | Linting zero errors |
| L2 | Types | Type checking zero errors |
| L3 | Tests | Unit tests 100% pass |
| L4 | Integration | Integration tests 100% pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC criteria met |

---

## 4. Confidence Checks

### Thresholds

| Score | Action |
|-------|--------|
| >=90% | Proceed confidently |
| 70-89% | Present alternatives, clarify gaps |
| <70% | Stop, ask questions first |

### Pre-Spec Check (Idea -> Spec)

| Check | Weight |
|-------|--------|
| Problem validated | 25% |
| Market gap | 25% |
| Target audience | 20% |
| Value proposition | 15% |
| Your fit | 15% |

### Pre-Design Check (Spec -> Design)

| Check | Weight |
|-------|--------|
| Requirements clear | 25% |
| AC testable | 25% |
| No contradictions | 20% |
| Scope defined | 15% |
| Dependencies known | 15% |

### Pre-Task Check (Design -> Tasks)

| Check | Weight |
|-------|--------|
| Architecture decided | 25% |
| Patterns established | 25% |
| No duplicate work | 20% |
| Dependencies mapped | 15% |
| Estimates reasonable | 15% |

### Pre-Implementation Check (Task -> Code)

| Check | Weight |
|-------|--------|
| Task requirements clear | 25% |
| Approach decided | 25% |
| No blockers | 20% |
| Tests defined | 15% |
| Rollback plan | 15% |

### Anti-Patterns to Catch

| Pattern | Risk | Action |
|---------|------|--------|
| "I think users want..." | Assumption | Require user research |
| "Should be easy..." | Underestimate | Require technical spike |
| "Similar to X..." | Missed differences | Require detailed comparison |
| "Figure it out later" | Deferred decision | Require decision now |
| "Obviously..." | Hidden assumption | Make explicit |

---

## 5. Reflexion Learning

### Memory Structure

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns
├── mistakes_learned.jsonl    # Errors and solutions
├── workflow_metrics.jsonl    # Execution metrics
└── session_context.md        # Current session state
```

### PDCA Cycle

```
Plan (hypothesis)
  |
Do (experiment)
  |
Check (self-evaluation)
  |
Act (improvement)
  |
Store (memory update)
```

### After Task Success

1. Extract what worked
2. Identify reusable patterns
3. Store in patterns_learned.jsonl
4. Update workflow_metrics.jsonl

### After Task Failure

1. Analyze root cause
2. Check if similar error exists in mistakes_learned.jsonl
3. If exists: Show previous solution
4. If new: Store error + solution
5. Update workflow_metrics.jsonl

### Before Task Start

1. Check mistakes_learned.jsonl for similar task types
2. If found: Show warnings and prevention tips
3. Check patterns_learned.jsonl for best practices
4. If found: Suggest approach

---

*SDD Execution Phase Workflows v1.0*
*Use with faion-sdd skill*
