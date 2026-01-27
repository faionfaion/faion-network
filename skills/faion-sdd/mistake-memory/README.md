# Mistake Memory

## Overview

Mistake Memory is the SDD system for capturing, analyzing, and preventing recurring errors in LLM-assisted development. It transforms failures into learning opportunities by documenting what went wrong, why, and how to prevent similar issues.

**Key Principle:** Blameless culture - focus on systems and processes, not individuals.

## Why Mistake Memory Matters for LLM Agents

LLM coding agents are ["over-confident and prone to mistakes"](https://addyosmani.com/blog/ai-coding-workflow/) - they write code with complete conviction, including bugs or nonsense, without self-awareness of errors. Unlike human developers who accumulate experience, LLMs start fresh each session without persistent memory of past mistakes.

Mistake Memory bridges this gap by:
- Documenting errors in persistent storage
- Injecting relevant warnings into agent context before similar tasks
- Creating automated prevention rules
- Building organizational knowledge from individual failures

## LLM-Specific Error Categories

### 1. Hallucination Errors

| Type | Description | Prevention |
|------|-------------|------------|
| **Factuality Hallucination** | Generated content conflicts with verifiable facts | RAG grounding, citation requirements |
| **Faithfulness Hallucination** | Output diverges from user instructions | Instruction echoing, verification steps |
| **API Hallucination** | Inventing non-existent APIs/methods | API documentation in context, type checking |
| **Confident Fabrication** | Presenting plausible but wrong information | Multi-model review, fact-checking gates |

### 2. Context Errors

| Type | Description | Prevention |
|------|-------------|------------|
| **Context Window Loss** | Earlier information fades in long conversations | Chunked processing, context summarization |
| **Instruction Drift** | Forgetting original requirements mid-task | Periodic instruction refresh |
| **Cross-Task Contamination** | Mixing context from different tasks | Clear task boundaries, session isolation |

### 3. Implementation Errors

| Type | Description | Prevention |
|------|-------------|------------|
| **Edge Cases Missed** | Not handling boundary conditions | Test-driven development, fuzzing |
| **Error Handling Gaps** | Missing try/catch, no error recovery | Error handling checklist |
| **Race Conditions** | Concurrent access issues | Concurrency review checklist |
| **Resource Leaks** | Unclosed connections, memory leaks | Resource cleanup patterns |

### 4. Process Errors

| Type | Description | Prevention |
|------|-------------|------------|
| **Skipped Validation** | Proceeding without verification | Quality gates, mandatory checks |
| **Premature Optimization** | Optimizing before correctness | "Make it work, then make it fast" |
| **Scope Creep** | Adding unrequested features | Strict requirement adherence |

## Mistake Capture Workflow

```
Error Occurs → Document → Analyze → Extract Prevention → Update Rules → Verify
      |            |          |             |                |            |
  Detection   Incident    Root Cause    Checklist        Prevention   Effectiveness
              Report      Analysis      Items            Automation   Tracking
```

### Capture Triggers

**Automatic:**
- CI/CD pipeline failure
- Production error alert
- Test failure pattern detected
- Estimation miss > 50%

**Manual:**
- Developer reports issue
- Code review finding
- Retrospective action item
- Customer-reported bug

**AI-Detected:**
- Agent encounters known anti-pattern
- Similar mistake pattern recognized
- Repeated debugging cycles (>3 attempts)

## Root Cause Analysis for LLM Errors

### Five Whys Framework

```markdown
## Example: API Hallucination

1. Why did the code fail?
   → Called non-existent method `response.getData()`

2. Why was non-existent method called?
   → LLM generated it without verification

3. Why wasn't it verified?
   → No API documentation in context

4. Why no documentation in context?
   → Context was too large, docs were truncated

5. Why were docs truncated?
   → No prioritization of essential context

**Root Cause:** Missing context prioritization strategy
**Prevention:** Always include API reference for libraries being used
```

### Analysis Questions

1. **Was the error in LLM output or human review?**
   - LLM-generated errors need better prompts/context
   - Human-missed errors need better review processes

2. **Was sufficient context provided?**
   - Missing documentation
   - Truncated examples
   - Unclear requirements

3. **Was the task appropriately scoped?**
   - Too large for single prompt
   - Too many concurrent concerns
   - Unclear boundaries

4. **Were verification steps skipped?**
   - No test execution
   - No type checking
   - No code review

## Prevention Layers

### Layer 1: Pre-Task Warnings

Before starting a task, check for relevant past mistakes:

```python
# Pseudocode for warning injection
relevant_mistakes = find_mistakes_by_keywords(task.description)
for mistake in relevant_mistakes:
    inject_warning(f"Warning: {mistake.title}. See {mistake.id}")
```

### Layer 2: Quality Gates

Checkpoints that must pass before proceeding:
- L1: Requirements understood
- L2: Design reviewed
- L3: Implementation complete
- L4: Tests passing
- L5: Code reviewed
- L6: Deployed and verified

### Layer 3: Automated Rules

Pattern-based detection in CI/CD:
- Detect destructive migrations without backup
- Flag hardcoded secrets
- Require tests for new functions
- Check for common anti-patterns

### Layer 4: Multi-Model Review

Use second model/session to review first model's output:
- Cross-validate generated code
- Check for logical inconsistencies
- Verify against requirements

## Integration with SDD

### Task Files

Include mistake warnings in task context:

```markdown
## Relevant Mistakes
- MIS_2024_001: Database migration without backup
- MIS_2024_015: Missing error handling in API calls
```

### Memory Storage

```
.aidocs/memory/
├── mistakes.md           # Human-readable mistake log
├── mistakes.jsonl        # Structured mistake records
└── prevention_rules.json # Automated check rules
```

### Reflexion Learning

Mistake Memory feeds into the PDCA reflexion cycle:
1. **Plan:** Review relevant mistakes before task
2. **Do:** Execute with prevention rules active
3. **Check:** Verify against known failure patterns
4. **Act:** Update mistake database if new error found

## Best Practices

### Documentation Quality

1. **Be specific** - Vague descriptions don't help
2. **Include context** - What led to the situation
3. **Actionable prevention** - Concrete steps to avoid
4. **Keep updated** - Prevention evolves

### Blameless Culture

1. **Focus on systems** - Not individuals
2. **Assume good intent** - Everyone wants to succeed
3. **Share openly** - Transparency aids learning
4. **Celebrate finding** - Better to catch than hide

### Prevention Focus

1. **Automate where possible** - Reduce human error
2. **Multiple layers** - Defense in depth
3. **Regular review** - Are preventions working?
4. **Low friction** - Easy to follow

## Related Methodologies

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Mistake capture checklist |
| [examples.md](examples.md) | Mistake examples with fixes |
| [templates.md](templates.md) | Mistake file templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for mistake analysis |

## External References

### Post-Mortem Practices

- [Blameless Post-Mortems (Google SRE)](https://sre.google/sre-book/postmortem-culture/)
- [The Five Whys](https://en.wikipedia.org/wiki/Five_whys)
- [Learning from Incidents](https://www.learningfromincidents.io/)

### LLM Error Prevention Research

- [LLM Hallucinations Survey](https://arxiv.org/html/2510.06265v2)
- [LLM Hallucinations in Code Generation](https://arxiv.org/pdf/2409.20550)
- [LLM Code Generation Mistakes Analysis](https://arxiv.org/html/2411.01414v1)

### Workflow References

- [AI Coding Workflow 2026 (Addy Osmani)](https://addyosmani.com/blog/ai-coding-workflow/)
- [AI Coding Agents Comparison](https://www.prismlabs.uk/blog/ai-coding-agents-comparison-2026)
