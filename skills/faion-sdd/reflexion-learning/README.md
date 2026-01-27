# Reflexion Learning

Verbal reinforcement learning methodology for LLM agents. Based on the Reflexion paper (NeurIPS 2023) with PDCA cycle adaptation for development workflows.

## Overview

Reflexion is a paradigm for reinforcing language agents through **verbal feedback** rather than weight updates. Instead of traditional RL that requires expensive fine-tuning, Reflexion agents:

1. Attempt a task
2. Receive feedback (external or self-generated)
3. Generate verbal reflection on what went wrong
4. Store reflection in episodic memory
5. Use memory to improve subsequent attempts

This creates a **learning loop without training** - the agent improves through accumulated experience stored in context.

## The Reflexion Paper

**Title:** Reflexion: Language Agents with Verbal Reinforcement Learning
**Authors:** Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**Published:** NeurIPS 2023

### Key Contributions

| Aspect | Traditional RL | Reflexion |
|--------|---------------|-----------|
| Learning signal | Scalar reward | Verbal feedback |
| Memory | Weights | Episodic text buffer |
| Training | Expensive fine-tuning | Zero-shot in-context |
| Generalization | Task-specific | Cross-domain transfer |

### Results from Paper

| Benchmark | Baseline | Reflexion | Improvement |
|-----------|----------|-----------|-------------|
| HumanEval (code) | 80.1% | 91.0% | +10.9% |
| AlfWorld (decision) | 75% | 97% | +22% |
| HotpotQA (reasoning) | 34% | 64% | +30% |

### Core Algorithm

```
trajectory = []
memory = []

for trial in 1..max_trials:
    action = agent.act(task, memory)
    result = environment.evaluate(action)
    trajectory.append((action, result))

    if result.success:
        return action

    reflection = agent.reflect(trajectory, result)
    memory.append(reflection)
```

The reflection becomes part of the prompt for the next trial, enabling learning without weight updates.

## PDCA Cycle for LLM Development

PDCA (Plan-Do-Check-Act), also known as the Deming Cycle, maps directly to Reflexion:

```
         PLAN
      (Spec + Memory)
           |
           v
    +------+------+
    |             |
   ACT           DO
(Update Memory) (Execute Task)
    |             |
    +------+------+
           |
           v
         CHECK
    (Evaluate + Reflect)
```

### PDCA-Reflexion Mapping

| PDCA Phase | Reflexion Component | SDD Implementation |
|------------|---------------------|-------------------|
| **Plan** | Load episodic memory | Read patterns.md, mistakes.md |
| **Do** | Execute with memory context | Implement task with loaded patterns |
| **Check** | Generate verbal feedback | Evaluate against AC, identify gaps |
| **Act** | Store reflection | Update memory files |

### PDCA Implementation

```yaml
plan:
  actions:
    - Load relevant patterns from memory
    - Load mistakes to avoid
    - Review acceptance criteria
    - Plan implementation approach
  output: Enhanced task context

do:
  actions:
    - Execute task with loaded patterns
    - Apply known mistake avoidance
    - Follow established conventions
  output: Implementation result

check:
  actions:
    - Evaluate against acceptance criteria
    - Compare actual vs expected outcome
    - Identify what worked/failed
    - Generate verbal reflection
  output: Structured reflection

act:
  actions:
    - Extract new patterns (positive)
    - Document mistakes (negative)
    - Update memory files
    - Adjust confidence scores
  output: Updated memory
```

## Memory Architecture

### Pattern Memory

Stores successful approaches for reuse:

```
.aidocs/memory/patterns.md
```

**Structure:**

```markdown
## PAT-001: Error Boundary Pattern

**Context:** React async components
**Problem:** Unhandled promise rejections
**Solution:** Wrap async in try-catch with error state
**Confidence:** 0.9 (used 5 times, 100% success)
**Source:** TASK-042

---

## PAT-002: Database Migration Validation

**Context:** Schema changes on large tables
**Problem:** Migrations timeout or lock tables
**Solution:** Check row count, use batched updates, add indexes first
**Confidence:** 0.85 (used 3 times)
**Source:** TASK-055
```

### Mistake Memory

Stores failures for avoidance:

```
.aidocs/memory/mistakes.md
```

**Structure:**

```markdown
## MIS-001: Underestimating Migration Time

**Severity:** High
**Context:** Database migrations with 1M+ rows
**What happened:** Migration took 3h instead of 30min
**Root cause:** Didn't check data volume
**Prevention:** Always run COUNT(*) before estimating
**Occurrence:** 2 times
**Last seen:** 2024-01-15

---

## MIS-002: API Response Format Assumption

**Severity:** Medium
**Context:** Third-party API integration
**What happened:** Code crashed on null values
**Root cause:** Assumed fields always present
**Prevention:** Always validate response structure
**Occurrence:** 1 time
```

### Session Memory

Current context for continuity:

```
.aidocs/memory/session.md
```

**Structure:**

```markdown
# Current Session

**Task:** TASK-XXX
**Status:** in_progress
**Started:** 2024-01-15T10:00Z

## Loaded Patterns
- PAT-001: Error Boundary (confidence: 0.9)
- PAT-015: Form Validation (confidence: 0.85)

## Mistakes to Avoid
- MIS-001: Check data volume before migrations
- MIS-008: Validate API response structure

## Decisions Made
- Using TypeScript strict mode
- PostgreSQL over MySQL (see ADR-005)

## Open Questions
- Need clarification on error message wording
```

## Confidence Calibration

### Confidence Levels

| Level | Score | Criteria |
|-------|-------|----------|
| High | 0.9+ | 5+ uses, validated across contexts, no recent failures |
| Medium | 0.7-0.89 | 2-4 uses, context-specific, minor issues |
| Low | 0.5-0.69 | 1-2 uses, limited validation |
| Experimental | 0.3-0.49 | Newly identified, not yet validated |

### Update Rules

```python
def update_confidence(pattern, outcome):
    if outcome == "success":
        pattern.confidence = min(0.95, pattern.confidence + 0.05)
        pattern.usage_count += 1
    elif outcome == "partial":
        pattern.confidence *= 0.95
    elif outcome == "failure":
        pattern.confidence = max(0.3, pattern.confidence - 0.15)

    # Decay unused patterns (90 days)
    if days_since_use(pattern) > 90:
        pattern.confidence *= 0.9
```

## Self-Correction Research

### Key Finding: External Feedback Required

Research shows LLMs struggle with intrinsic self-correction (correcting without external signals). The "Self-Correction Blind Spot" study found 64.5% blind spot rate across models.

**What works:**

| Approach | Effectiveness |
|----------|--------------|
| External test feedback | High - clear signal |
| Compiler/linter errors | High - deterministic |
| User feedback | High - explicit correction |
| Self-evaluation alone | Low - often degrades quality |
| Multi-agent verification | Medium - second opinion helps |

### SCoRe Approach (ICLR 2025)

SCoRe (Self-Correction via Reinforcement Learning) achieved significant gains:
- +15.6% on MATH problems
- +9.1% on HumanEval

Key insight: Multi-turn RL on self-generated data works better than SFT.

### Practical Implications

For SDD workflow:

1. **Use external feedback** - tests, linters, type checkers
2. **Store feedback verbally** - in memory files
3. **Load relevant memory** - before each task
4. **Multi-agent review** - when possible

## Kaizen Integration

Kaizen ("change for better") principles enhance Reflexion:

| Kaizen Principle | Reflexion Application |
|------------------|----------------------|
| Small improvements | Incremental pattern updates |
| Everyone participates | Both human and agent contribute |
| Gemba (go see) | Examine actual errors, not assumptions |
| Standardize | Document patterns for reuse |
| 5 Whys | Root cause in reflections |

### 5 Whys in Reflections

```markdown
## Reflection: TASK-042 Failure

**Problem:** API integration failed in production

**Why 1:** Response parsing threw null error
**Why 2:** Field expected but not present
**Why 3:** API docs were outdated
**Why 4:** Didn't test against live API
**Why 5:** No sandbox environment configured

**Root Cause:** Missing integration test infrastructure
**Prevention:** Add sandbox API to CI pipeline
```

## Integration with SDD

### Pre-Task Phase

```yaml
pre_task:
  - Load session.md (if continuing)
  - Query patterns.md for task-relevant patterns
  - Query mistakes.md for domain-specific warnings
  - Add loaded context to task prompt
```

### Post-Task Phase

```yaml
post_task:
  - Evaluate outcome against AC
  - Generate structured reflection
  - Extract patterns (if success)
  - Document mistakes (if failure)
  - Update confidence scores
  - Clear session.md or update for next task
```

### Quality Gates

Reflexion integrates with SDD quality gates:

| Gate | Reflexion Action |
|------|------------------|
| L1 (Spec) | Load domain patterns |
| L2 (Design) | Load architecture patterns |
| L3 (Impl Plan) | Load estimation patterns |
| L4 (Pre-Code) | Load coding patterns, mistakes |
| L5 (Post-Code) | Generate reflection |
| L6 (Complete) | Update memory, close session |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Reflexion cycle checklist |
| [examples.md](examples.md) | Real-world learning examples |
| [templates.md](templates.md) | Memory file templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for reflexion |

## References

### Papers

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) - Original paper (NeurIPS 2023)
- [When Can LLMs Actually Correct Their Own Mistakes?](https://arxiv.org/abs/2406.01297) - Critical survey (TACL 2024)
- [Training Language Models to Self-Correct via RL](https://arxiv.org/abs/2409.12917) - SCoRe approach (ICLR 2025)

### Implementations

- [noahshinn/reflexion](https://github.com/noahshinn/reflexion) - Official implementation
- [A Plan-Do-Check-Act Framework for AI Code Generation](https://www.infoq.com/articles/PDCA-AI-code-generation/) - PDCA for AI coding

### Concepts

- [PDCA Cycle (Deming Wheel)](https://en.wikipedia.org/wiki/PDCA)
- [Kaizen](https://en.wikipedia.org/wiki/Kaizen)
- [5 Whys Root Cause Analysis](https://en.wikipedia.org/wiki/Five_whys)

## Related Methodologies

- [Pattern Memory](../pattern-memory/) - Pattern storage and retrieval
- [Mistake Memory](../mistake-memory/) - Error tracking and prevention
- [Quality Gates](../quality-gates/) - Validation checkpoints
- [Task Execution](../task-execution/) - SDD task lifecycle
