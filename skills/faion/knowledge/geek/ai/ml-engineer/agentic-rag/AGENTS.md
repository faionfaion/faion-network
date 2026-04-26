# Agentic RAG (RAG 2.0)

## Summary

Agentic RAG embeds autonomous agents into the retrieval pipeline to enable multi-hop retrieval, query routing, self-correction, and iterative refinement. Unlike traditional single-shot RAG, agents plan decompositions, grade retrieved documents, rewrite failed queries, and verify answers before returning — trading latency for higher accuracy on complex queries.

## Why

Single-shot RAG fails on multi-hop questions and mixed-source corpora because one retrieval pass cannot cover heterogeneous knowledge or detect its own gaps. Agentic patterns (Corrective RAG, Adaptive RAG, multi-agent orchestration) add a feedback loop: retrieve → grade → rewrite → re-retrieve, capped at 2-3 retries before fallback to web search. Cap retries at 2; beyond that, precision drops faster than it rises.

## When To Use

- Queries require multi-hop reasoning across documents
- Single-shot retrieval consistently fails for complex or ambiguous questions
- Knowledge base spans multiple heterogeneous sources (internal docs, web, APIs)
- Self-correction is essential: domain where one retrieval miss produces costly wrong answers (legal, medical, financial)
- Complex pipelines already have observability tooling (traces, per-turn cost logging)

## When NOT To Use

- Simple factual Q&A with a single knowledge base and high recall — standard RAG is faster and cheaper
- Latency budget under 2 seconds — agentic loops add 2-10x more turns than static RAG
- The orchestration infrastructure does not exist yet — build standard RAG first, then layer agentic behavior
- Cost constraints are tight — multi-hop retrieval multiplies token usage; each agent turn = one LLM call
- No observability tooling — debugging agentic loop failures without traces is impractical

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Core patterns: Corrective RAG, Adaptive RAG, multi-agent orchestration; key components (router, grader, rewriter, verifier) |
| `content/02-rules.xml` | Concrete rules, thresholds, failure modes, and production gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/state-schemas.py` | TypedDict / dataclass state schemas for CRAG, Adaptive RAG, multi-agent RAG |
| `templates/pydantic-schemas.py` | Pydantic models: RouteQuery, GradeDocument, RewriteQuery, SufficiencyCheck, VerificationResult |
| `templates/crag-workflow.py` | LangGraph Corrective RAG workflow skeleton |
| `templates/prompt-router.txt` | Query router prompt (basic, multi-source, complexity-aware) |
| `templates/prompt-grader.txt` | Document relevance grader prompt |
