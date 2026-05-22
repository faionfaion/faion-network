---
slug: evaluation-benchmarks
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Runs a multi-model comparison benchmark (held-out set + LLM-as-judge) and a continuous production-sampling job to detect drift across model swaps.
content_id: "a00ab8bc492c977e"
complexity: deep
produces: report
est_tokens: 4400
tags: [benchmarking, model-comparison, production-monitoring, evaluation, quality]
---
# Evaluation Benchmarks — Multi-Model + Continuous Production

## Summary

**One-sentence:** Runs a multi-model comparison benchmark (held-out set + LLM-as-judge) and a continuous production-sampling job to detect drift across model swaps.

**One-paragraph:** Two complementary benchmarks: (1) offline multi-model comparison on a held-out task set to pick a winner; (2) continuous production sampling that re-scores 1-5% of live traffic with the same eval harness so a silent regression after a model swap is caught within hours, not weeks. Both publish a leaderboard and a drift alert.

**Ефективно для:**

- Model-swap decision (Sonnet 4.6 → 4.7 etc.) where regression risk is real.
- Vendor evaluation (OpenAI vs Anthropic vs Gemini) on a domain task.
- Continuous quality monitoring after launch.
- A/B testing prompt rewrites against a known baseline.

## Applies If (ALL must hold)

- A held-out test set (≥100 examples) exists for the task.
- Quality is measurable (LLM-as-judge or programmatic check).
- Production sampling is permitted by data-privacy policy.

## Skip If (ANY kills it)

- No held-out set — author one first.
- Single-model deployment with no swap planned — benchmark cost is wasted.
- Sampling production data violates contract — solve privacy first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Held-out test set | JSONL | BA + Eng |
| Judge rubric | markdown | evaluation-metrics methodology |
| Production log | JSONL | Observability stack |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `run_offline_bench` | haiku | Parallel API calls; deterministic. |
| `llm_as_judge` | sonnet | Quality scoring. |
| `drift_alert` | haiku | Compare to baseline; threshold check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/leaderboard.md` | Multi-model leaderboard skeleton |
| `templates/drift-alert.yaml` | Alert policy + thresholds |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-evaluation-benchmarks.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[evaluation-framework]]
- [[evaluation-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is this an offline model-swap decision? Branches route to a rule id from `content/01-core-rules.xml` (held-out-fresh, prod-sampling-1-5pct, baseline-versioned, ...) so every leaf is traceable to a testable statement.
