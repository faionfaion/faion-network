# Reasoning-First Architectures

## Summary

Patterns for using reasoning models (o3/o4-mini, Claude Extended Thinking, DeepSeek R1) and chain-of-thought techniques to solve tasks requiring multi-step logic, self-verification, and planning. Route by task complexity: use cheap classifiers to decide when a reasoning model is warranted, set thinking budgets explicitly, and always gate irreversible downstream actions behind human review.

## Why

Reasoning models scale test-time compute to achieve breakthrough accuracy on hard tasks: o3 scores 83.3% on AIME 2024 vs 13.4% for GPT-4o. The cost is 10-50x per call. The key insight is that not all tasks need deep reasoning — routing only complex tasks to reasoning models while using cheap models for simple ones keeps cost under control while unlocking qualitatively better outputs for the tasks that matter.

## When To Use

- Multi-step math, logic, or formal proofs where intermediate steps matter
- Code generation requiring self-verification before returning
- Research synthesis where competing hypotheses must be explored before concluding
- Planning tasks with dependencies where ordering must be validated
- Any workflow where the cost of a wrong answer outweighs the cost of extra tokens

## When NOT To Use

- Simple retrieval or lookup tasks — CoT adds latency with no quality gain
- High-throughput classification or routing (thousands of calls per minute)
- Creative writing where deliberate reasoning constrains output quality
- Cost-sensitive pipelines where standard models already meet the bar (verified by eval)
- Real-time streaming where users see partial output — reasoning tokens break UX

## Content

| File | What's inside |
|------|---------------|
| `content/01-models.xml` | Reasoning model comparison (o3, o4-mini, Claude ET, DeepSeek R1, Gemini DeepThink), pricing, benchmarks |
| `content/02-patterns.xml` | Think-before-act patterns (ReAct, Reflexion, Tree-of-Thought, Critique+Revise), budget selection rules |
| `content/03-production.xml` | Cost guards, routing strategy, gotchas (non-determinism, PII in think blocks, tool call latency) |

## Templates

| File | Purpose |
|------|---------|
| `templates/extended-thinking.py` | Claude Extended Thinking minimal invocation with budget selector function |
| `templates/prompt-reasoning.txt` | System prompt pattern for careful reasoning agents with verification steps |
