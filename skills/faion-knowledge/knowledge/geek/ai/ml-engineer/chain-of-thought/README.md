# Chain-of-Thought Prompting

Comprehensive guide to Chain-of-Thought (CoT) prompting techniques for enhanced LLM reasoning.

## What is Chain-of-Thought?

Chain-of-Thought prompting encourages LLMs to break down complex problems into intermediate reasoning steps before arriving at a final answer. This technique significantly improves performance on tasks requiring:

- Multi-step reasoning
- Mathematical calculations
- Logical deductions
- Complex decision-making
- Problem decomposition

## CoT Variants

| Variant | Description | Best For |
|---------|-------------|----------|
| **Zero-Shot CoT** | Add "Let's think step by step" | Quick reasoning, modern models |
| **Few-Shot CoT** | Provide examples with reasoning | Format enforcement, edge cases |
| **Self-Consistency** | Multiple reasoning paths + voting | High-stakes decisions |
| **Tree-of-Thoughts (ToT)** | Explore/evaluate multiple branches | Complex planning, search |
| **Least-to-Most** | Decompose into ordered subproblems | Sequential dependencies |
| **Plan-and-Solve** | Explicit planning before solving | Multi-step procedures |

## When to Use CoT

| Scenario | Use CoT | Why |
|----------|---------|-----|
| Math word problems | Yes | Multi-step calculation |
| Logical puzzles | Yes | Requires deduction |
| Code debugging | Yes | Step-by-step analysis |
| Complex decisions | Yes | Weighing multiple factors |
| Simple classification | No | Adds unnecessary tokens |
| Factual lookup | No | No reasoning needed |
| Translation | No | Direct transformation |

## 2025-2026 Research Insights

### Zero-Shot vs Few-Shot CoT

Recent research (2025) shows a significant shift:

| Finding | Source |
|---------|--------|
| Zero-shot CoT often matches/exceeds few-shot for strong models | [Revisiting Chain-of-Thought Prompting](https://arxiv.org/abs/2506.14641) |
| Few-shot CoT primarily enforces output format, not reasoning | Qwen2.5, DeepSeek-R1 experiments |
| DeepSeek-R1 shows performance degradation with few-shot | DeepSeek technical reports |

**Recommendation:** Start with zero-shot CoT for modern models (GPT-4+, Claude 3+). Use few-shot only for format enforcement.

### Decreasing Value of Traditional CoT

Research from Wharton (2025) indicates that as models improve, traditional CoT benefits diminish for simpler reasoning tasks. However, CoT remains essential for:

- Complex multi-step problems
- Tasks requiring verifiable reasoning
- Situations where explainability matters

### Typed Chain-of-Thought (ICLR 2026)

New technique providing external, verifiable signatures of faithful reasoning. Shows 50%+ accuracy gains for certification-critical activities.

## Key Concepts

### Reasoning Transparency

CoT makes the model's reasoning explicit, enabling:
- Verification of logic
- Detection of errors
- Understanding of approach
- Debugging of failures

### Self-Consistency

Sample multiple reasoning paths and select the most common answer:

```
Problem → [Path 1] → Answer A
        → [Path 2] → Answer A
        → [Path 3] → Answer B

Final: Answer A (majority vote)
```

### Tree-of-Thoughts Architecture

```
Problem
   ├── Thought 1 [Score: 8/10] ─→ Continue
   │       ├── Thought 1.1 ─→ Answer
   │       └── Thought 1.2 ─→ Dead end
   ├── Thought 2 [Score: 3/10] ─→ Prune
   └── Thought 3 [Score: 7/10] ─→ Continue
           └── Thought 3.1 ─→ Answer
```

## Terminology

| Term | Definition |
|------|------------|
| **CoT** | Chain-of-Thought |
| **Zero-Shot CoT** | CoT without examples ("Let's think step by step") |
| **Few-Shot CoT** | CoT with worked examples |
| **Self-Consistency** | Multiple samples + majority voting |
| **ToT** | Tree-of-Thoughts |
| **Thought** | Intermediate reasoning step |
| **Reasoning Path** | Complete sequence of thoughts to answer |
| **Verification** | Checking reasoning correctness |
| **Backtracking** | Returning to try alternative paths |

## LLM-Specific Considerations

| Model | CoT Best Practices |
|-------|-------------------|
| **Claude** | Use `<thinking>` tags, explicit step markers |
| **GPT-4** | Numbered steps, clear section breaks |
| **Gemini** | Structured outline format |
| **o1/o3** | Built-in reasoning, minimal CoT needed |
| **Local (Ollama)** | Simpler prompts, explicit format |

## Performance Benchmarks

| Task | Standard | With CoT | Improvement |
|------|----------|----------|-------------|
| GSM8K (math) | 58% | 76% | +18% |
| StrategyQA | 65% | 71% | +6% |
| Game of 24 | 4% | 74% (ToT) | +70% |

## Production Considerations

### Cost vs Quality Trade-offs

| Technique | Token Cost | Latency | Quality |
|-----------|------------|---------|---------|
| Zero-Shot CoT | Low | Low | Good |
| Few-Shot CoT | Medium | Medium | Good+ |
| Self-Consistency | High (5x) | High | Better |
| Tree-of-Thoughts | Very High | Very High | Best |

### When to Use Each

- **Zero-Shot CoT**: Default choice for reasoning tasks
- **Few-Shot CoT**: When specific format is critical
- **Self-Consistency**: Mission-critical decisions
- **ToT**: Complex planning, exploration problems

## External Resources

### Official Documentation

- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google AI Prompt Design](https://ai.google.dev/docs/prompt_best_practices)

### Research Papers

- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)
- [Self-Consistency (Wang et al., 2022)](https://arxiv.org/abs/2203.11171)
- [Tree of Thoughts (Yao et al., 2023)](https://arxiv.org/abs/2305.10601)
- [Least-to-Most Prompting (Zhou et al., 2022)](https://arxiv.org/abs/2205.10625)
- [Revisiting CoT Prompting (2025)](https://arxiv.org/abs/2506.14641)
- [Typed Chain-of-Thought (ICLR 2026)](https://arxiv.org/pdf/2510.01069)

### Guides

- [Prompt Engineering Guide - CoT](https://www.promptingguide.ai/techniques/cot)
- [Prompt Engineering Guide - Self-Consistency](https://www.promptingguide.ai/techniques/consistency)
- [Prompt Engineering Guide - ToT](https://www.promptingguide.ai/techniques/tot)

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step implementation checklists |
| [examples.md](examples.md) | Real-world examples and patterns |
| [templates.md](templates.md) | Copy-paste prompt templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM-assisted CoT work |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-llm-integration](../../faion-llm-integration/CLAUDE.md) | API implementation |
| [prompt-engineering](../prompt-engineering/README.md) | General prompting techniques |
| [faion-ai-agents](../../faion-ai-agents/CLAUDE.md) | Agent reasoning patterns |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| CoT prompting | sonnet | Prompt technique |
| Step extraction | sonnet | Analysis pattern |
| Tree of thought | opus | Advanced technique |
