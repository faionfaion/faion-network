---
slug: evaluation-metrics
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Metrics for measuring LLM performance across different dimensions including accuracy, quality, latency, cost, safety, and reliability.
content_id: "0a35e4ac3c9ea0a9"
tags: [evaluation, metrics, llm, ml-ops, benchmarking]
---
# Evaluation Metrics

## Summary

**One-sentence:** Metrics for measuring LLM performance across different dimensions including accuracy, quality, latency, cost, safety, and reliability.

**One-paragraph:** Metrics for measuring LLM performance across different dimensions including accuracy, quality, latency, cost, safety, and reliability. Select 3-5 metrics matching the task type, run them against a fixed test dataset, compare to a pre-established baseline, and report pass/fail per metric against defined thresholds.

## Applies If (ALL must hold)

- Implementing automated quality gates in a CI/CD pipeline for LLM-powered features.
- Comparing two model versions or prompt variants before a production rollout.
- Tracking metric trends over time in a production monitoring dashboard.
- Building an evaluation harness that a subagent can run autonomously against a test dataset.
- Selecting the right metric for a specific task type (classification, QA, summarization, code generation).

## Skip If (ANY kills it)

- The task has no quantifiable success criterion — open-ended creative generation requires human preference evaluation, not automated metrics.
- Ground-truth labels are unavailable and cannot be synthesized with validation; BLEU/ROUGE without references are meaningless.
- Exact match or BLEU are the only metrics for long-form generation — they punish valid paraphrases and correlate poorly with human judgment.
- Safety metrics (toxicity, bias) are the sole gate for production decisions — automated safety metrics miss context-dependent harms and require human review.

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

- parent skill: `geek/ai/ml-ops/`
