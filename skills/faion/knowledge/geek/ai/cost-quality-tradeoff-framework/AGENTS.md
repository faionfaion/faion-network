---
slug: cost-quality-tradeoff-framework
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Decision-table for the cost vs quality vs latency Pareto-front: when to escalate weak→strong, when to add a second pass, when to add a critic, when reranking pays for itself.
content_id: "b51291b85b8e314d"
tags: [cost-quality-tradeoff-framework, ai, geek]
---

# LLM Cost-Quality-Latency Tradeoff Framework

## Summary

**One-sentence:** Decision-table for the cost vs quality vs latency Pareto-front: when to escalate weak→strong, when to add a second pass, when to add a critic, when reranking pays for itself.

**One-paragraph:** cost-reduction-strategies + llm-cost-basics cover cost reduction. They do not give a decision framework for the cost vs quality vs latency Pareto. Mechanism: per-task eval + decision-table + drift triggers. Output: tradeoff table + per-task pick with evidence + drift alarm.

## Applies If (ALL must hold)

- ≥1 production LLM workflow with eval set
- team has authority to swap models or add post-processing
- cost OR latency OR quality complaint actively constraining the workflow

## Skip If (ANY kills it)

- no eval — sizing is guesswork; build eval first
- experimental research with no cost ceiling
- single-shot demo / hackathon — over-engineering

## Prerequisites

- eval set ≥50 cases with graded outputs
- ability to measure cost per call + p95 latency
- model-router or routing layer (LangChain/LlamaIndex/custom)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/llm-cost-basics` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/cost-reduction-strategies` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer methodology: `geek/ai/llm-cost-basics`
- peer methodology: `geek/ai/cost-reduction-strategies`
- peer methodology: `geek/ai/llm-cascade-routing`
- external: https://arxiv.org/abs/2305.05176 (FrugalGPT); https://www.anthropic.com/news/prompt-caching
