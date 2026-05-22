---
slug: agentic-rag-self-correction
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A self-correcting RAG pipeline generates an answer, then runs a faithfulness verifier that checks each claim against the retrieved source chunks.
content_id: "69b136f8e2d0c44d"
tags: [rag, agentic, self-correction, faithfulness, hallucination]
---
# Agentic RAG — Self-Correction Loop

## Summary

**One-sentence:** A self-correcting RAG pipeline generates an answer, then runs a faithfulness verifier that checks each claim against the retrieved source chunks.

**One-paragraph:** A self-correcting RAG pipeline generates an answer, then runs a faithfulness verifier that checks each claim against the retrieved source chunks. If ungrounded claims are found, the verifier's feedback drives additional retrieval and re-generation, up to max_corrections attempts. When the verifier flags more than 2 ungrounded claims, the answer is escalated to human review rather than surfaced to the user.

## Applies If (ALL must hold)

- Fact-checking or compliance verification where exhaustive source coverage is required.
- Legal or regulatory content where ungrounded claims have real consequences.
- Any RAG pipeline where hallucination rate needs to drop below 10%.
- Structured data (SQL/tables) must be combined with unstructured document retrieval and cross-verified.

## Skip If (ANY kills it)

- Latency-critical queries (under 2s SLA) — correction cycles add 3–5x latency.
- Creative generation tasks where faithfulness to source is not the goal.
- High-volume low-stakes queries where the cost of correction cycles exceeds the cost of occasional hallucinations.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/rag-engineer/`
