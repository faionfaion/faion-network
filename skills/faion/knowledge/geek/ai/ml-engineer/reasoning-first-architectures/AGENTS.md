---
slug: reasoning-first-architectures
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "69084dee94f28ecc"
summary: Routes only complex tasks to reasoning models (o3 / Claude Extended Thinking / DeepSeek R1) with explicit thinking budgets, sized by task type, gated by an eval that proves the reasoning model outperforms a standard model.
complexity: deep
produces: spec
est_tokens: 4200
tags: [reasoning-models, chain-of-thought, extended-thinking, cost-optimization, agentic-workflow]
---

# Reasoning-First Architectures

## Summary

**One-sentence:** Cost-aware routing pattern that escalates only multi-step / verification-heavy tasks to reasoning models (o3, Claude Extended Thinking, DeepSeek R1) with explicit thinking budgets, while standard models handle the simple majority.

**One-paragraph:** Reasoning models scale test-time compute for breakthroughs on hard tasks (o3 hits 83.3% AIME vs 13.4% GPT-4o) but cost 10-50× more per call. Treating every task as a reasoning task burns budget without quality gain on simple retrievals. This methodology pins the contract: a cheap classifier routes incoming tasks to {standard, reasoning} based on task-type, an eval proves the reasoning route actually outperforms the standard route on a labelled set, a thinking budget is set per task-type bucket (1K–128K depending on depth), and downstream irreversible actions sit behind human review when reasoning confidence drops. Output: a versioned `reasoning-routing.yaml` consumed by the orchestrator.

**Ефективно для:**

- Multi-step math / formal proof / theorem задач — reasoning моделі дають 6× quality lift на AIME-class задачах де standard models валяться.
- Code review з обовʼязковим self-verification — Extended Thinking ловить edge cases які SFT моделі пропускають.
- Research synthesis із competing hypotheses — reasoning room for thought бачить trade-offs.
- Cost-sensitive продуктів — eval-proven routing тримає 80% калів на cheap path і дорогі тільки коли потрібно.

## Applies If (ALL must hold)

- Workload contains ≥1 task class where reasoning depth materially affects correctness (math, code-verify, planning)
- Budget for reasoning-model inference is provisioned OR a fall-through to standard is acceptable
- A 50-100 example eval set exists to calibrate routing thresholds
- Orchestrator can intercept the request and call different model providers

## Skip If (ANY kills it)

- Simple retrieval / lookup workloads only — CoT adds latency with no quality lift
- High-throughput classification (thousands of calls per minute) — reasoning latency breaks the SLO
- Creative writing as primary use case — explicit reasoning constrains output quality
- Real-time streaming UX — reasoning tokens delay first-token, break UX

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `task-sample-labelled.jsonl` | JSONL `{task, type, expected, hard?: bool}` | log analysis + SME |
| `model-rate-cards.yaml` | YAML | provider pricing as of last review |
| `latency-budget.yaml` | YAML | product SLO per task class |
| `eval-set-routing.jsonl` | JSONL | ≥50 examples mixed across task types |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/cost-optimization` | Per-model cost vocabulary |
| `geek/ai/ml-engineer/model-evaluation` | Eval discipline that gates the routing decision |
| `geek/ai/ml-engineer/llm-decision-framework` | Provider selection backdrop |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: eval-before-spend, task-type budget, classifier-first, human-gate on irreversible, fall-through-on-budget-cap | 1100 |
| `content/02-output-contract.xml` | essential | `reasoning-routing.yaml` schema with classes + budgets + fallback | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: blanket reasoning, unset budget, no eval gate, streaming broken, missing fall-through | 900 |
| `content/04-procedure.xml` | essential | 6 steps: cluster tasks → label hard set → eval routing → set budgets → wire fall-through → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: code-review router escalates only to Extended Thinking when hard | 600 |
| `content/06-decision-tree.xml` | essential | Routes by task-type to standard / Extended Thinking / o3 / DeepSeek R1 with budget per node | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `task_class_inference` | haiku | Lightweight classifier; runs per request |
| `eval_routing_decision` | sonnet | Compare reasoning vs standard outputs across labelled set |
| `budget_calibration_drafter` | opus | Picks budget per type using eval data; needs depth |
| `routing_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/extended-thinking.py` | Anthropic Extended Thinking call with budget parameter |
| `templates/prompt-reasoning.txt` | System prompt asking model to verify before answering |
| `templates/reasoning-routing.schema.yaml` | Schema for the routing spec |
| `templates/_smoke-test.yaml` | Minimum-viable routing spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reasoning-first-architectures.py` | Lint reasoning-routing.yaml against schema + rules | Pre-commit + pre-deploy |

## Related

- [[cost-optimization]] — per-model rate cards
- [[tool-use-function-calling]] — reasoning models often gate tool-call decisions
- external: [Anthropic Extended Thinking](https://docs.anthropic.com/claude/docs/extended-thinking) · [OpenAI o-series](https://openai.com/index/introducing-o3/) · [DeepSeek R1](https://github.com/deepseek-ai/DeepSeek-R1)

## Decision tree

See `content/06-decision-tree.xml`. Routes a task by inferred type and difficulty score to one of {standard, Extended Thinking, o4-mini, o3, DeepSeek R1} with a thinking-budget envelope per node.
