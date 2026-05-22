---
slug: agentic-rag
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Agentic RAG pattern: query routing, multi-hop retrieval, self-correction (CRAG), iterative refinement, with LangGraph state machine + Pydantic schemas.
content_id: "49802dc931354b4d"
complexity: deep
produces: code
est_tokens: 4200
tags: [rag, retrieval, agents, langgraph, multi-hop, corrective-rag]
---
# Agentic RAG

## Summary

**One-sentence:** Agentic RAG pattern: query routing, multi-hop retrieval, self-correction (CRAG), iterative refinement, with LangGraph state machine + Pydantic schemas.

**One-paragraph:** Embeds autonomous agents into the retrieval pipeline to handle complex queries that single-shot RAG fails on. Components: query router (vectorstore vs web vs nothing), retrieval grader (relevance scoring), generation node, hallucination grader (groundedness), answer grader (question alignment). Pulls Corrective RAG (CRAG) and Self-RAG patterns into one production-ready LangGraph state machine with typed state.

**Ефективно для:** ML engineer, що бачить «single-shot RAG не тягне багатоходові запитання» і готовий перейти на CRAG-style цикл з graders + retries.

## Applies If (ALL must hold)

- queries require multi-hop retrieval (more than one source needed)
- domain has both internal docs AND public web content
- you can afford 2-5x the latency of single-shot RAG
- you have a vector store + (optional) web search tool wired
- groundedness / answer-relevance evaluation is in scope

## Skip If (ANY kills it)

- single-hop queries dominate (>80%) — vanilla RAG is enough
- latency budget < 2s — agentic RAG is too slow
- no eval suite for retrieval — build that first
- domain has no public-web fallback path

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-agentic-rag.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/crag-workflow.py` | LangGraph CRAG workflow skeleton |
| `templates/state-schemas.py` | Pydantic GraphState + intermediate schemas |
| `templates/pydantic-schemas.py` | Pydantic schemas for graders + routes |
| `templates/prompt-grader.txt` | Relevance / groundedness grader prompt template |
| `templates/prompt-router.txt` | Query router prompt template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-typed-state`, `r2-router-first`, `r3-grade-before-generate`, `r4-bounded-loop`, `r5-groundedness-gate` from `content/01-core-rules.xml`.
