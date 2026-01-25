# faion-sdd-execution Sub-Skill

**SDD Execution Phase: Quality Gates, Reflexion Learning, Pattern Memory, Code Review.**

---

## Entry Point

Invoked via [faion-sdd](../faion-sdd/SKILL.md) orchestrator or [faion-net](../faion-net/CLAUDE.md).

---

## Overview

Execution and learning phase of Specification-Driven Development:
- Task execution workflows
- Quality gates (L1-L6)
- Code review cycles
- Reflexion learning (PDCA)
- Pattern/mistake memory
- Context management

---

## Quick Start

| Need | File |
|------|------|
| Run quality gates | [quality-gates.md](quality-gates.md) |
| Code review | [code-review-cycle.md](code-review-cycle.md) |
| Learn patterns | [pattern-memory.md](pattern-memory.md) |
| Track mistakes | [mistake-tracking.md](mistake-tracking.md) |
| Reflexion cycle | [reflexion-learning.md](reflexion-learning.md) |

---

## Workflow

```
EXECUTE → VALIDATE → REVIEW → LEARN
    |         |         |        |
  tasks    quality    code    pattern
          gates L1-6  review   memory
```

---

## Key Files

| Category | Files |
|----------|-------|
| **Quality** | quality-gates, confidence-checks, code-review-cycle |
| **Learning** | reflexion-learning, pattern-memory, mistake-tracking, mistake-prevention |
| **Execution** | sdd-workflow-overview, workflow-execution-phase |
| **Context** | context-basics, context-strategies |
| **Optimization** | task-parallelization, task-dependencies |

---

## Quality Gates

| Level | Phase | Validation |
|-------|-------|------------|
| L1 | Spec | Requirements complete |
| L2 | Design | Architecture sound |
| L3 | Impl-Plan | 100k compliant |
| L4 | Task | Pre-execution ready |
| L5 | Completion | Tests pass |
| L6 | Integration | System validated |

---

## Reflexion Cycle

```
PLAN → DO → CHECK → ACT
  ↓      ↓      ↓      ↓
spec  execute gates  learn
             review  memory
```

---

## Related

- **Parent:** [faion-sdd](../faion-sdd/SKILL.md)
- **Sibling:** [faion-sdd-planning](../faion-sdd-planning/CLAUDE.md)
- **Full list:** See [SKILL.md](SKILL.md)

---

*faion-sdd-execution v1.0*
*20 methodologies for execution, quality, and learning*
