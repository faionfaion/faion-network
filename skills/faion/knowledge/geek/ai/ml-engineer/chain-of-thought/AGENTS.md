# Chain-of-Thought Prompting

## Summary

Chain-of-Thought (CoT) prompting elicits intermediate reasoning steps before a final answer, improving accuracy on multi-step problems. For modern models (Claude Sonnet 4+, GPT-4+), start with zero-shot CoT ("Think step by step"). Use few-shot CoT only for strict format enforcement — not for reasoning quality. For Claude, use `<thinking>` XML tags or Extended Thinking (Opus). Do NOT add explicit CoT to o1/o3/DeepSeek-R1 reasoning models — they have it built in.

## Why

CoT makes the model's reasoning explicit and separable from its answer. This enables verification, error detection, and debugging of failures. Benchmarks: GSM8K +18% accuracy, Game of 24 +70% with Tree-of-Thoughts. However, 2025 research shows that for strong models, zero-shot CoT matches few-shot CoT — the benefit of examples is format enforcement, not reasoning improvement.

## When To Use

- Task requires multi-step reasoning: math, logic puzzles, code debugging, complex decisions
- LLM makes errors on a task it should theoretically solve — CoT surfaces where reasoning breaks
- Output needs to be auditable: visible steps allow reviewers to verify the reasoning path
- Agent must plan a sequence of actions before executing — CoT as a scratchpad before tool calls
- High-stakes single response where Self-Consistency (5 samples + majority vote) is justified

## When NOT To Use

- Simple classification, extraction, or translation — CoT adds tokens with no quality gain
- Latency is critical (&lt;1s) — CoT adds tokens and turns
- Using o1/o3/o4-mini/DeepSeek-R1 — built-in reasoning; explicit CoT interferes
- High-volume, low-complexity pipelines — 2-5x token overhead multiplies at scale

## Content

| File | What's inside |
|------|---------------|
| `content/01-techniques.xml` | CoT variants (zero-shot, few-shot, self-consistency, ToT, least-to-most); when to use each; 2025 research insights |
| `content/02-rules.xml` | Concrete rules, production gotchas, Extended Thinking guidance, cost considerations |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-zero-shot.txt` | Zero-shot CoT prompt patterns (basic + XML-structured for Claude) |
| `templates/extended-thinking.py` | Claude Extended Thinking API call pattern |
| `templates/self-consistency.py` | Self-consistency with majority voting (N parallel calls) |
