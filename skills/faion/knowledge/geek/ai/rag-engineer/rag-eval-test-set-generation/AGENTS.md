---
slug: rag-eval-test-set-generation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A RAG evaluation can only be as good as its test set.
content_id: "afdc67235845f4d9"
tags: [rag, evaluation, test-set, question-generation]
---
# RAG Test Set Generation

## Summary

**One-sentence:** A RAG evaluation can only be as good as its test set.

**One-paragraph:** A RAG evaluation can only be as good as its test set. Generate test questions automatically from the document corpus using an LLM (factual, comparative, reasoning, summarization types) or curate them manually. The test set must be versioned, stratified by question type and difficulty, and include at least 20% hard or edge-case questions.

## Applies If (ALL must hold)

- Building a comprehensive evaluation framework before first deployment.
- Setting up continuous evaluation after any pipeline change (chunking, top-K, model swap).
- When no labeled data exists and the corpus is large enough for synthetic generation to be representative.
- When you need diverse question types (factual, comparative, reasoning, summarization) to measure different failure modes.

## Skip If (ANY kills it)

- Proof-of-concept phase with no budget for LLM-based generation — defer until validation stage.
- When the test set would be smaller than 20 questions — statistical noise dominates and results are not actionable.
- When ground truth answers are unavailable and the domain is too specialized for synthetic generation to be reliable.

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
