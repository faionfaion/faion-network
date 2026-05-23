# RAG Architecture

## Summary

**One-sentence:** Produces an architecture decision record covering chunking, embeddings, vector DB, retrieval, context, and quality metrics for a RAG system.

**One-paragraph:** Retrieval Augmented Generation (RAG) combines information retrieval with LLM generation to produce accurate, grounded responses. This methodology produces a written architecture decision record covering: indexing pipeline, query pipeline, chunking strategy, retrieval strategy, context budget, vector DB choice, and quality metrics. Each decision is justified and linked to a downstream implementation methodology.

**Ефективно для:** архітекторів, які роблять верхньорівневі вибори до того, як писати pipeline-код.

## Applies If (ALL must hold)

- Team is starting a new RAG project or planning a major redesign.
- The team has degrees of freedom on chunking, embeddings, vector DB, and reranker choice.
- A written decision record is required for compliance, onboarding, or stakeholder review.
- The corpus characteristics (size, type, freshness) are known.

## Skip If (ANY kills it)

- Data fits a single LLM context window — long-context prompting is simpler.
- Real-time data — use live tool-calling, not RAG.
- Fine-tuning already meets accuracy on a stable corpus.
- No infrastructure for a vector DB — consider pgvector first (record that decision).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Corpus characteristics | doc (size, type, change rate) | discovery |
| Quality targets | metric thresholds | product |
| Cost budget | $/month and $/query | finance |
| Latency budget | ms | SLA |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/vector-database-setup` | Vector DB comparison drives the DB section. |
| `geek/ai/rag-engineer/chunking-basics` | Chunking strategy section. |
| `geek/ai/rag-engineer/embedding-models` | Embedding choice. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 2-phase pipeline, chunk by doc type, hybrid default, rerank for production, eval before launch | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the architecture decision record | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: no record, static top-k, no eval gate | ~700 |
| `content/04-procedure.xml` | medium | 6-step decision procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Tree for RAG vs long-context vs fine-tune | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Evaluate constraints | sonnet | Multi-criteria analysis. |
| Draft decision record | sonnet | Structured writing. |
| Pick novel pattern (graph/agentic) | opus | Cross-domain judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-architecture.md.tmpl` | Decision record skeleton with all 7 architecture sections. |
| `templates/_smoke-test.md` | Filled example for a docs Q&amp;A RAG. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-architecture.py` | Validates a decision record JSON against schema. | Pre-commit; CI. |

## Related

- [[rag]]
- [[rag-implementation]]
- [[vector-database-setup]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether RAG is the right approach at all: root question — "Does the corpus exceed a single LLM context window AND is it private/freshly updated?". Branches lead to long-context prompting (no), fine-tuning (closed corpus, stable), or RAG architecture (default). Each leaf references the rule that owns it.
