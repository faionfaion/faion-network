---
slug: hallucination-detection-online
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Claim decomposition, retrieval-attribution check, self-consistency on critical fields, abstain-on-low-evidence — runtime hallucination detection beyond batch evals.
content_id: "4319a28cd4c21286"
tags: [hallucination-detection-online, ai, geek]
---

# Runtime Hallucination Detection

## Summary

**One-sentence:** Claim decomposition, retrieval-attribution check, self-consistency on critical fields, abstain-on-low-evidence — runtime hallucination detection beyond batch evals.

**One-paragraph:** faion has cheap-guardrail-tripwire and llm-judge-rubric-evidence-first (batch). Missing: runtime detection pattern. Output: detection pipeline + abstention policy + drift triggers.

## Applies If (ALL must hold)

- production LLM workflow where hallucination = real damage (finance, health, legal, code, factual support)
- RAG or tool-call available to provide grounding evidence
- engineering capacity to add a runtime check layer

## Skip If (ANY kills it)

- purely creative workflow (fiction, brainstorm)
- hallucination tolerance is high (e.g., 'wrong is funny')
- no grounding source available — detection without ground truth is guessing

## Prerequisites

- RAG corpus or tool-call output as grounding
- list of 'critical fields' that must not hallucinate
- ability to add a runtime check stage in the inference pipeline

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/cheap-guardrail-tripwire` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/llm-judge-rubric-evidence-first` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `geek/ai/cheap-guardrail-tripwire`
- peer methodology: `geek/ai/llm-judge-rubric-evidence-first`
- peer methodology: `geek/ai/rag-engineer`
- external: https://arxiv.org/abs/2305.18248 (SelfCheckGPT); https://arxiv.org/abs/2310.06770 (factuality of LLMs); https://www.anthropic.com/news/contextual-retrieval
