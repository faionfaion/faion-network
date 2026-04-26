# RAG Evaluation

## Summary

Methodology for evaluating Retrieval-Augmented Generation pipelines by measuring retrieval (Precision@K, Recall@K, MRR, Hit Rate) and generation (Faithfulness, Answer Relevance, Hallucination Rate) components separately. Always evaluate retrieval and generation independently — a high faithfulness score with low hit rate means the model is hallucinating consistently, not retrieving well.

## Why

RAG failures have two distinct root causes — retrieval failure (wrong chunks) and generation failure (hallucination from retrieved context) — that require different fixes. Conflating them produces misleading scores and misdirected optimization effort. RAGAS provides reference-free metrics that work without ground truth, but costs $5–20 per 100 samples in LLM-as-judge calls.

## When To Use

- Before promoting a RAG pipeline to production — validate retrieval recall and generation faithfulness
- After changing chunking strategy, embedding model, or vector DB configuration — check for regression
- Comparing two embedding models for the same corpus — use Precision@K and MRR to decide
- Diagnosing user complaints about wrong or hallucinated answers
- Setting up continuous production monitoring (lightweight faithfulness + hit rate, sampled hourly)

## When NOT To Use

- No ground truth queries and the domain is too specialized for reliable synthetic generation
- Pipeline is a prototype and chunking/embedding strategy is still changing daily — evaluate after it stabilizes
- Budget is insufficient for LLM-as-judge at scale — use automated retrieval metrics only as a proxy
- Primary goal is latency optimization, not quality — use profiling tools instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-metrics.xml` | Retrieval metrics (Precision@K, Recall, MRR, NDCG, Hit Rate) and generation metrics (Faithfulness, Answer Relevance) with target thresholds |
| `content/02-evaluation-workflow.xml` | Four-step agent workflow, RAGAS runner, faithfulness judge prompt, common pitfalls |

## Templates

| File | Purpose |
|------|---------|
| `templates/ragas-runner.py` | RAGAS evaluation runner with dataset setup |
| `templates/retrieval-metrics.py` | Hit rate, MRR, Precision@K calculator (<40 lines) |
| `templates/faithfulness-judge-prompt.txt` | LLM prompt for per-claim faithfulness scoring |
