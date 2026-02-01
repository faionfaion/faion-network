# SDD Workflows

Step-by-step workflows for LLM-assisted Specification-Driven Development.

---

## Overview

SDD workflows guide the progression from idea to deployed code through structured phases. Each workflow includes decision points, state transitions, quality gates, and LLM prompts.

```
SPEC-WORKFLOW -> DESIGN-WORKFLOW -> IMPLEMENTATION-WORKFLOW -> REVIEW-WORKFLOW
      |               |                    |                       |
   WHAT to         HOW to              Execute                 Validate
   build           build                tasks                  & learn
```

---

## Workflows

| Workflow | Purpose | Input | Output |
|----------|---------|-------|--------|
| [spec-workflow.md](spec-workflow.md) | Define WHAT to build | Idea, problem | spec.md |
| [design-workflow.md](design-workflow.md) | Define HOW to build | spec.md | design.md |
| [implementation-workflow.md](implementation-workflow.md) | Execute tasks | design.md | Code + tests |
| [review-workflow.md](review-workflow.md) | Validate & learn | Completed work | Patterns, feedback |
| [llm-prompts.md](llm-prompts.md) | Prompts for each phase | - | - |

---

## Workflow Transitions

### State Machine

```
                    BRAINSTORM
                        |
                        v
    +---------> SPECIFICATION <---------+
    |                |                  |
    | reject         | approve          | clarify
    |                v                  |
    |           DESIGN ----------------+
    |                |
    |                v
    |     IMPLEMENTATION-PLAN
    |                |
    |                v
    |           TASK-CREATION
    |                |
    |                v
    |     +---> EXECUTION ---+
    |     |          |       |
    |     | blocked  v       | complete
    |     +---- REVIEW <-----+
    |                |
    +---- improve ---+
```

### Transition Gates

| From | To | Gate Criteria |
|------|----|---------------|
| Idea | Spec | Problem validated, stakeholder identified |
| Spec | Design | All FR-X defined, acceptance criteria complete |
| Design | Impl-Plan | All AD-X documented, file structure defined |
| Impl-Plan | Tasks | Dependencies mapped, waves identified |
| Tasks | Execute | Task fits 100k tokens, no blockers |
| Execute | Review | Tests pass, quality gates cleared |
| Review | Done | Patterns extracted, memory updated |

---

## Confidence Thresholds

Before transitioning between phases, validate confidence:

| Transition | Threshold | Action if Below |
|------------|-----------|-----------------|
| Idea -> Spec | 70%+ | More research, user interviews |
| Spec -> Design | 90%+ | Clarify requirements, add examples |
| Design -> Plan | 90%+ | Review architecture, check patterns |
| Plan -> Execute | 95%+ | Resolve blockers, simplify tasks |

### Confidence Calculation

| Check | Weight |
|-------|--------|
| Requirements clear and testable | 25% |
| No contradictions or gaps | 25% |
| Dependencies identified | 20% |
| Patterns established | 15% |
| Risks documented | 15% |

---

## Workflow Patterns for 2026

Based on [current best practices](https://addyosmani.com/blog/ai-coding-workflow/):

### Pattern 1: Vertical with Horizontal Brainstorming

```
Main Flow (vertical)
    |
    v
[Brainstorm Point]
    |
    +---> Branch A (explore approach 1)
    +---> Branch B (explore approach 2)
    +---> Branch C (explore approach 3)
    |
    v
Reconverge (synthesize best elements)
    |
    v
Continue Main Flow
```

**Use for:** Architecture decisions, novel problems, design trade-offs

### Pattern 2: Parallel Preparation with Checkpoints

```
Phase 1 Implementation
    |
    v
[Checkpoint Gate]
    |
    +---> Code Review (parallel)
    +---> Documentation (parallel)
    +---> Phase 2 Planning (parallel)
    |
    v
[Checkpoint Validation]
    |
    v
Phase 2 Continuation
```

**Use for:** Feature development with multiple deliverables

### Pattern 3: Spec-Driven Parallel Development

```
Specification (contract)
    |
    +---> Feature A (git branch)
    +---> Feature B (git branch)
    +---> Feature C (git branch)
    +---> Feature D (git branch)
    |
    v
Integration Merge Point
```

**Use for:** Cleanly decomposable features, sprint work

### Pattern 4: Async Parallel Spec Generation

```
Shared Spec Document
    |
    +---> Tab: Architecture section
    +---> Tab: UX flows section
    +---> Tab: Data models section
    +---> Tab: Security section
    |
    v
Periodic Consolidation
```

**Use for:** Large specifications spanning multiple domains

### Pattern 5: Multi-Perspective Planning

```
Single Objective
    |
    +---> Plan A (optimize speed)
    +---> Plan B (minimize risk)
    +---> Plan C (reduce cost)
    +---> Plan D (maximize learning)
    |
    v
Review & Synthesize
    |
    v
Final Consolidated Plan
```

**Use for:** High-stakes decisions, stress-testing approaches

---

## LLM Agent Orchestration

### Model Selection by Phase

| Phase | Recommended Model Type | Reason |
|-------|----------------------|--------|
| Brainstorming | Reasoning models (o1, Opus) | Complex problem-solving |
| Spec Writing | Balanced (Sonnet, GPT-4) | Structure + creativity |
| Design | Reasoning models | Architecture decisions |
| Implementation | Fast models (Sonnet, Claude) | Code generation speed |
| Review | Multiple models | Cross-validation |

### Context Management

```
Total Context Budget: 100k tokens

Research:      ~20k (read existing code)
Task Context:   ~5k (spec, design, plan)
Implementation: ~50k (generated code)
Buffer:        ~25k (iterations, fixes)
```

### Feedback Loops

1. **Test Feedback**: Feed test failures back to LLM
2. **Lint Feedback**: Feed linter errors for correction
3. **Type Feedback**: Feed type errors for fixing
4. **Review Feedback**: Feed code review comments
5. **User Feedback**: Feed acceptance testing results

---

## Quality Gates

### Gate Levels

| Level | Check | Pass Criteria |
|-------|-------|---------------|
| L1 | Syntax | Linting zero errors |
| L2 | Types | Type checking zero errors |
| L3 | Unit Tests | 100% pass, coverage met |
| L4 | Integration | Integration tests pass |
| L5 | Review | Code review approved |
| L6 | Acceptance | All AC criteria verified |

### Gate Actions

| Result | Action |
|--------|--------|
| Pass | Proceed to next phase |
| Fail (fixable) | Retry with feedback |
| Fail (blocking) | Escalate, document blocker |

---

## Memory and Learning

### Session Memory

Track during workflow execution:

```markdown
## Session State

### Current Phase: [phase]
### Last Action: [action]
### Blockers: [list]
### Decisions Made: [list]
```

### Pattern Memory

After successful completion:

```markdown
## Pattern Learned

### Context: [when this applies]
### Pattern: [what worked]
### Evidence: [success metrics]
```

### Mistake Memory

After failures:

```markdown
## Mistake Recorded

### Error: [what went wrong]
### Root Cause: [why it happened]
### Prevention: [how to avoid]
### Recovery: [how to fix if it happens]
```

---

## Project Structure

```
.aidocs/
├── constitution.md           # Project standards
├── roadmap.md                # Feature timeline
│
├── backlog/                  # Features in queue
│   └── feature-XXX-name/
│       ├── spec.md           # <- Spec Workflow output
│       ├── design.md         # <- Design Workflow output
│       └── implementation-plan.md  # <- Impl-Plan output
│
├── todo/                     # Ready for execution
│   └── TASK-XXX-*.md         # <- Task Creation output
│
├── in-progress/              # Currently executing
│   └── TASK-XXX-*.md         # <- Implementation Workflow
│
├── done/                     # Completed
│   └── TASK-XXX-*.md         # <- Review Workflow output
│
└── memory/                   # Learning artifacts
    ├── patterns.md           # <- Review Workflow output
    ├── mistakes.md           # <- Review Workflow output
    └── session.md            # <- Current state
```

---

## Workflow Invocation

### Starting a New Feature

```
1. /faion-net "New feature: [description]"
2. System routes to spec-workflow
3. Brainstorming phase with questions
4. Draft spec.md
5. Review and approve
6. Transition to design-workflow
```

### Resuming Work

```
1. Read .aidocs/memory/session.md
2. Identify current phase
3. Load relevant context
4. Continue from last checkpoint
```

### Handling Blockers

```
1. Document blocker in session.md
2. Create improvement suggestion
3. Either:
   a. Resolve blocker and continue
   b. Mark task as blocked
   c. Escalate to user
```

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |
## Related Documents

| Document | Purpose |
|----------|---------|
| [sdd-workflow-overview/README.md](../sdd-workflow-overview/README.md) | SDD philosophy |
| [writing-specifications/README.md](../writing-specifications/README.md) | Spec details |
| [writing-design-documents/README.md](../writing-design-documents/README.md) | Design details |
| [writing-implementation-plans/README.md](../writing-implementation-plans/README.md) | Plan details |
| [quality-gates-confidence/README.md](../quality-gates-confidence/README.md) | Quality gates |
| [reflexion-learning/README.md](../reflexion-learning/README.md) | PDCA cycle |

---

## Sources

- [My LLM Coding Workflow (Addy Osmani, 2026)](https://addyosmani.com/blog/ai-coding-workflow/)
- [Five Workflow Patterns (WeBuild-AI)](https://www.webuild-ai.com/insights/five-workflow-patterns-to-multiply-your-development-capacity-with-ai-coding-assistants)
- [5 Key Trends in Agentic Development (The New Stack)](https://thenewstack.io/5-key-trends-shaping-agentic-development-in-2026/)
- [Coding With LLMs in 2026 (Bored Hacking)](https://boredhacking.com/coding-with-llms-2026/)

---

*SDD Workflows | v1.0.0 | 2026*
