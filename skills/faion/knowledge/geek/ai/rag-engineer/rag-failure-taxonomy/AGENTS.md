---
slug: rag-failure-taxonomy
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "eba9e3039a371ddf"
summary: A shared vocabulary for clustering RAG failure cases — retrieval-fail / generation-fail / chunk-boundary / stale-doc / wrong-doc-ranked / prompt-instruction-leak — so weekly retrieval-quality reviews and customer-feedback triage produce consistent diagnoses across reviewers.
tags: [rag, failure-taxonomy, retrieval-quality, triage, weekly-review]
---

# RAG Failure Taxonomy

## Summary

**One-sentence:** A closed 7-category taxonomy of RAG failure modes — retrieval-fail, retrieval-misranked, chunk-boundary, generation-grounding-fail, stale-doc, prompt-instruction-leak, downstream-tool-fail — that lets weekly RAG reviews and customer-feedback triage produce diagnoses consistent across reviewers.

**One-paragraph:** Without a shared vocabulary, every RAG failure gets re-discovered and labelled differently. "It hallucinated", "the answer was wrong", "search was bad" describe the same incident from three angles; weekly retrieval-quality reviews drift because reviewers use different categories; customer-feedback triage cannot aggregate. This methodology pins a 7-category taxonomy with a detector clause per category (what to look at in retrieval logs, generation logs, and source documents), a recommended fix path per category (retriever, reranker, chunker, generator-prompt, knowledge-base, instruction tuning), and a per-failure record schema that captures the verdict. Mechanism: every failure (from customer feedback, internal eval, monitoring sample) is classified into exactly one category; weekly review counts categories and prioritises the fix path with the highest incident concentration. Primary output: a `rag-failures.yaml` log + a weekly category-frequency report.

## Applies If (ALL must hold)

- production RAG system with sufficient traffic to produce ≥ 5 failure reports per week
- monitoring captures retrieval-result IDs, generation prompt, and final answer per call
- engineering capacity to review and fix at least one RAG failure category per week
- customer feedback channel (support tickets, in-app thumbs-down) routes to the same triage queue

## Skip If (ANY kills it)

- pre-launch RAG with no live traffic — develop taxonomy from internal eval failures only
- pure semantic search with no LLM generation — only the retrieval categories apply
- RAG over a single tiny corpus where every doc is known — taxonomy is overhead
- system uses a black-box managed RAG (no access to retrieval logs) — adopt the provider's taxonomy

## Prerequisites

- monitoring with per-call retrieval logs (chunk IDs returned, ranks, scores)
- per-call generation log (prompt template + retrieved context + raw model output)
- access to the underlying knowledge base (source documents) for fact-checking
- a triage queue (Linear, Jira, GitHub Project) where failures land

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/rag-engineer/rag-eval-strategy` | Eval framework feeds the failure inputs |
| `geek/ai/ml-ops/rag-canary-rollout-plan` | Canary auto-rollback uses these category codes |
| `geek/ai/ml-engineer/llm-observability` | Logs and traces are the load-bearing inputs |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: closed 7-category taxonomy, one-cause-per-failure, detector evidence, fix-path-per-category, weekly aggregation | ~1000 |
| `content/02-output-contract.xml` | essential | rag-failures.yaml entry schema; weekly report schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 meta-failure modes of the taxonomy itself: multi-tag, category-creep, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage_a_failure_report` | sonnet | Per-incident judgment with retrieval + generation log inputs |
| `categorise_into_taxonomy` | sonnet | Per-incident bounded judgment using the rule book |
| `weekly_aggregation` | sonnet | Cross-incident synthesis |
| `propose_fix_path_per_top_category` | opus | Cross-system synthesis: retriever vs prompt vs KB |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-failures.yaml` | Per-failure entry skeleton |
| `templates/triage-rubric.md` | Reviewer-facing decision tree mapping evidence to category |
| `templates/weekly-report.md` | Weekly category-frequency report skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/auto-classify-prelim.py` | Heuristic pre-classifier on monitoring sample: retrieval miss, low rank, no overlap; reviewer confirms or overrides | At triage open |
| `scripts/weekly-report.py` | Aggregates last 7 days, computes category frequency, recommends top fix path | Weekly Friday |

## Related

- parent skill: `geek/ai/rag-engineer/SKILL.md`
- peer methodologies: `geek/ai/rag-engineer/rag-eval-strategy`, `geek/ai/ml-ops/rag-canary-rollout-plan`, `geek/ai/rag-engineer/reranking-pipeline-integration`
- external: [Lewis et al., Retrieval-Augmented Generation paper (NeurIPS 2020)] · [RAGAS faithfulness/answer-relevance/context-precision metrics] · [Pinecone "Common RAG Failure Modes" series] · [Anthropic Contextual Retrieval post (2024) — fix paths for several categories]
