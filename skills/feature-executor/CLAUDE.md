# feature-executor

> **Entry Point:** `/faion:feature-executor` — invoked directly.

## When to Use This Skill

- Executing complete features from SDD workflow
- Sequential task execution with quality gates
- Post-task validation (tests, coverage, build)
- Iterative code review cycles
- Moving features from todo to done

## Overview

SDD feature executor with quality gates: sequential task execution, test/coverage validation after each task, code review cycles until all issues resolved.

This skill orchestrates complete feature implementation in the SDD workflow:

1. **Context Loading** - Load project constitution, feature spec, design, and implementation plan
2. **Task Discovery** - Find tasks in feature's `in-progress/` (resume) and `todo/` (new) subfolders
3. **Task Execution Loop** - Execute each task via `faion-task-executor-agent` with post-task validation (tests, coverage, build)
4. **Code Review Cycle** - Iterate with `faion-code-agent` until no issues remain
5. **Finalize** - Move all tasks to `done/` subfolder, then move feature to `done/`

**Task Lifecycle (inside feature):**
```
feature-NNN/todo/ → feature-NNN/in-progress/ → feature-NNN/done/
```

## Usage

```
/faion:feature-executor {project} {feature}
```

**Examples:**
```
/faion:feature-executor cashflow-planner 01-auth
/faion:feature-executor faion-net 02-landing-page
```

## Agents Used

| Agent | Purpose |
|-------|---------|
| `faion-task-executor-agent` | Execute individual tasks |
| `faion-code-agent` | Code review (review mode) |
| `faion-test-agent` | Test execution and coverage analysis |
| `faion-hallucination-checker-agent` | Verify task completion claims |

## Quality Gates

After each task:
- All tests pass
- Coverage meets threshold (default 80%)
- Project builds and runs

After all tasks:
- Code review passes (max 5 iterations)
- No critical/security issues
- No style violations

## Files

| File | Description |
|------|-------------|
| [SKILL.md](SKILL.md) | Skill overview, usage, decision tree, and configuration |
| [CLAUDE.md](CLAUDE.md) | This navigation file |
| [execution-workflow.md](execution-workflow.md) | Complete workflow (context, tasks, review, finalize) |
| [quality-gates.md](quality-gates.md) | Validation criteria and output formats |

## Integration

Part of SDD workflow:
```
SPEC -> DESIGN -> IMPL-PLAN -> TASKS -> [FEATURE-EXECUTOR] -> DONE
```

## Related Skills

| Skill/Knowledge | Relationship |
|-----------------|--------------|
| [faion](../faion/CLAUDE.md) | Umbrella knowledge layer (domains, methodologies) |
| [faion/knowledge/solo/sdd/sdd/](../faion/knowledge/solo/sdd/sdd/) | Provides task specs and workflow |
| [faion/knowledge/free/dev/software-developer/](../faion/knowledge/free/dev/software-developer/) | Code task patterns |
| [faion/knowledge/pro/infra/devops-engineer/](../faion/knowledge/pro/infra/devops-engineer/) | Infrastructure task patterns |

---

*v1.1.0 | 2026-01-23*
