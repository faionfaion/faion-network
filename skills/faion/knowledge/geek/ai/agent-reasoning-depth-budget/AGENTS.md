---
slug: agent-reasoning-depth-budget
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Sets per-turn thinking budget, detects under-/over-thinking from eval data, and compresses thinking across turns.
content_id: "3caf53b25b2a9f79"
tags: [agent-reasoning-depth-budget, ai, geek]
---

# Agent Reasoning Depth Budget

## Summary

**One-sentence:** Sets per-turn thinking budget, detects under-/over-thinking from eval data, and compresses thinking across turns.

**One-paragraph:** faion has reasoning-first-architectures, plan-execute-vs-react, previous-response-id-reasoning-reuse. Missing: the operating discipline of choosing budget with eval evidence. Mechanism: start small, expand until score plateaus; under/over detectors; inter-turn compression. Output: per-task budget table + eval evidence + drift triggers.

## Applies If (ALL must hold)

- agent uses extended-thinking / chain-of-thought / reasoning-token APIs
- ≥1 eval set with ≥50 graded cases
- cost or latency is a constraint

## Skip If (ANY kills it)

- single-shot prompt with no multi-step reasoning
- research/exploration with no cost ceiling
- vendor models without exposed thinking budget — use vendor defaults

## Prerequisites

- eval set ≥50 graded cases
- ability to vary thinking tokens (max_thinking_tokens param)
- logging of thinking-token counts per call

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `reasoning-first-architectures` | peer methodology — produces inputs or consumes outputs |
| `plan-execute-vs-react` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `reasoning-first-architectures`
- peer methodology: `plan-execute-vs-react`
- peer methodology: `previous-response-id-reasoning-reuse`
- external: https://www.anthropic.com/news/visible-extended-thinking; https://platform.openai.com/docs/guides/reasoning
