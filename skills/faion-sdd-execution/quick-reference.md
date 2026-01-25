# SDD Quick Reference

## Workflow Overview

```
CONSTITUTION -> SPEC -> DESIGN -> IMPL-PLAN -> TASKS -> EXECUTE -> DONE
      |          |        |          |           |         |        |
   project    feature  technical   100k rule   atomic    agent    learn
   principles  intent   approach   compliance   units   execution reflect
```

---

## Section Input/Output Table

| Section | Input | Output | Agent |
|---------|-------|--------|-------|
| 1 | Project analysis/dialogue | constitution.md | - |
| 2 | Problem + requirements | spec.md | faion-sdd-reviewer-agent (mode: spec) |
| 3 | Approved spec | design.md | faion-sdd-reviewer-agent (mode: design) |
| 4 | Design + 100k rule | implementation-plan.md | faion-sdd-reviewer-agent (mode: plan) |
| 5 | Impl-plan + codebase | Task files in todo/ | faion-task-creator-agent |
| 6 | Single task | Task in done/ + commit | faion-task-executor-agent |
| 7 | All tasks | All tasks done/ | faion-task-executor-agent |
| 8 | Task dependencies | Optimized wave plan | - |
| 9 | Backlog features | Features ready in todo/ | - |
| 10 | Progress + priorities | roadmap.md | - |
| 11 | Code or SDD docs | Review report | faion-sdd-reviewer-agent |
| 12 | Pre-phase validation | Confidence score | - |
| 13 | Task outcomes | Lessons in memory | - |

---

## 100k Token Rule

Each task MUST fit within 100k token context:

```
Research:       ~20k (read existing code)
Task file:       ~5k
Implementation: ~50k
Buffer:         ~25k
TOTAL:         <100k
```

### Token Estimation by Component

| Component | Tokens |
|-----------|--------|
| Django model (simple) | 5-10k |
| Django model (complex) | 15-25k |
| Service class | 20-40k |
| ViewSet | 15-30k |
| Test file | 20-40k |

**Rule:** If uncertain, estimate higher and split.

---

## Confidence Thresholds

| Score | Action |
|-------|--------|
| >=90% | Proceed confidently |
| 70-89% | Present alternatives, clarify gaps |
| <70% | Stop, ask questions first |

**ROI:** 100-200 tokens checking saves 5-50K tokens of wrong-direction work.

---

## Quality Gate Levels

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1 | Syntax | Linting zero errors |
| L2 | Types | Type checking zero errors |
| L3 | Tests | Unit tests 100% pass |
| L4 | Integration | Integration tests 100% pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC criteria met |

---

## Agents Reference

| Agent | Purpose | Modes |
|-------|---------|-------|
| `faion-task-executor-agent` | Execute SDD tasks autonomously | - |
| `faion-task-creator-agent` | Create detailed TASK_*.md files | - |
| `faion-sdd-reviewer-agent` | Quality gate reviews | spec, design, plan, tasks |
| `faion-hallucination-checker-agent` | Validate task completion | - |

---

## Directory Structure

```
.aidocs/
|-- constitution.md                    # Project principles
|-- contracts.md                       # API contracts
|-- roadmap.md                         # Milestones
+-- features/
    |-- backlog/                       # Waiting for grooming
    |-- todo/                          # Ready for execution
    |-- in-progress/                   # Being worked on
    +-- done/                          # Completed
        +-- {NN}-{feature}/
            |-- spec.md                # WHAT and WHY
            |-- design.md              # HOW
            |-- implementation-plan.md # Tasks breakdown
            +-- tasks/
                |-- backlog/
                |-- todo/              # Ready tasks
                |-- in-progress/       # Executing
                +-- done/              # Completed
```

**Lifecycle:** `backlog/ -> todo/ -> in-progress/ -> done/`

---

## Memory Storage

**Location:** Project-local `.aidocs/memory/` (not global `~/.sdd/`)

```
.aidocs/memory/
|-- patterns.md               # Successful patterns (append-only)
|-- mistakes.md               # Errors and solutions (append-only)
|-- decisions.md              # Key decisions and rationale
+-- session.md                # Current session state
```

**Format:** Markdown files (not JSONL) for readability and easy CLAUDE.md updates.

**Memory → CLAUDE.md Sync:**
- After learning patterns/mistakes, update project CLAUDE.md
- Add key learnings to "Lessons Learned" section
- Keep CLAUDE.md as single source of truth for project context

**Memory Entry Format:**
```markdown
## [DATE] Pattern/Mistake Title

**Context:** Brief description of situation
**What worked/failed:** Key details
**Lesson:** Actionable takeaway
**Tags:** #tag1, #tag2
```

---

*SDD Quick Reference v1.0*
