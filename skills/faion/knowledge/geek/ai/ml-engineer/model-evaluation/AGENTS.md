---
slug: model-evaluation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Systematic methodology for assessing LLM quality, latency, cost, safety, and reliability across offline (test dataset), online (A/B production traffic), and continuous monitoring modes.
content_id: "611b9c6ae3a1b79e"
tags: [evaluation, llm, metrics, benchmarks, llm-judge]
---
# Model Evaluation

## Summary

**One-sentence:** Systematic methodology for assessing LLM quality, latency, cost, safety, and reliability across offline (test dataset), online (A/B production traffic), and continuous monitoring modes.

**One-paragraph:** Systematic methodology for assessing LLM quality, latency, cost, safety, and reliability across offline (test dataset), online (A/B production traffic), and continuous monitoring modes. Always run at minimum two evaluation passes per output: automated metric + LLM-as-judge. Never report only BLEU/ROUGE for generation tasks.

## Applies If (ALL must hold)

- Selecting between two or more candidate models for a production use case
- Before promoting a prompt change or model upgrade to production
- After fine-tuning, to verify quality improvement over the base model
- Setting up continuous monitoring with alerts when quality drifts below threshold
- Running A/B tests to compare a new model against current production baseline

## Skip If (ANY kills it)

- Task is trivial and any capable model passes — skip formal evaluation, ship
- No baseline exists yet — gather production data first, then evaluate against it
- Purely synthetic benchmarks for a highly domain-specific task — use real query samples
- Budget does not allow LLM-as-judge at scale — use cheaper automated metrics as a proxy first

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

- parent skill: `geek/ai/ml-engineer/`
