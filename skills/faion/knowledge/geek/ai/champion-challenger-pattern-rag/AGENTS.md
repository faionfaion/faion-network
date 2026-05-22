---
slug: champion-challenger-pattern-rag
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Champion Challenger Pattern Rag: codified AI-system reliability practice that turns the recurring 'p7-llm-agent-developer/RAG chunking strategy bench' decision into a repeatable, auditable artefact.
content_id: "696fa42851f0346c"
tags: [champion-challenger-pattern-rag, ai, geek]
---
# Champion Challenger Pattern Rag

## Summary

**One-sentence:** Champion Challenger Pattern Rag: codified AI-system reliability practice that turns the recurring 'p7-llm-agent-developer/RAG chunking strategy bench' decision into a repeatable, auditable artefact.

**One-paragraph:** Champion Challenger Pattern Rag addresses the gap identified by the p7-llm-agent-developer/RAG chunking strategy bench playbook: How to keep last week's winner running as the champion-challenger for next week's bench without leaking traffic. Pattern is well-known in ML, not codified for agent/RAG specifically. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p7-llm-agent-developer/RAG chunking strategy bench OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p7-llm-agent-developer/RAG chunking strategy bench task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/champion-challenger-pattern-rag.json` | JSON schema for the Champion Challenger Pattern Rag output contract |
| `templates/champion-challenger-pattern-rag.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-champion-challenger-pattern-rag.py` | Enforce Champion Challenger Pattern Rag output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `p7-llm-agent-developer/RAG chunking strategy bench`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
