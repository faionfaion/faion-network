# RAG Canary Rollout Plan

## Summary

**One-sentence:** Produces a RAG-feature canary rollout plan — fixed 1/5/25/100 curve, golden-eval gate per step, sampled online quality scoring, 60s kill switch.

**One-paragraph:** RAG quality regresses in ways that latency and error-rate canaries do not see. This methodology fixes the canary curve at 1% (24h hold) → 5% (24h) → 25% (48h) → 100%, gates each step with a golden-eval pass and online rubric-based quality scoring (5-10% sampled, ≥200 samples/hour during the 5% step), and enforces a ≤60-second kill switch by atomic in-memory routing flip (no deploy). Output: a versioned rollout-plan + per-step gate result + online-quality event + rollback receipt — all typed against the schema so step promotion can be automated.

**Ефективно для:** ML-engineer / SRE, що випускає новий retriever / prompt / model у RAG-пайплайн і хоче ловити quality drop без чекання на user complaints.

## Applies If (ALL must hold)

- RAG feature with measurable answer-quality rubric (groundedness, relevance, completeness, no-hallucination).
- Gateway can atomically flip versions in ≤60 seconds (in-memory routing table).
- Golden eval suite exists and is updated within the last 90 days.
- LLM-as-judge or human review queue available for online sampling.

## Skip If (ANY kills it)

- No measurable quality rubric — return to rubric design first.
- Gateway requires a deploy or cache warm-up to flip versions (rebuild gateway first).
- Internal-only tool with no SLO and no users (no canary needed).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Versioned retriever + prompt + reranker config | git sha | repo |
| Golden eval suite (≥200 items) | JSONL | eval repo |
| Online rubric definition with weights | YAML | rubric repo |
| Atomic-flip gateway | service | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/ml-engineer/rag-pipeline-design` | Defines the pipeline shape that is being rolled out. |
| `geek/ai/ml-engineer/rag-evaluation` | Provides the eval that gates each step. |
| `geek/ai/ml-engineer/llm-observability-stack` | Source of the online-quality sink. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: fixed curve, golden eval per step, sampled online quality, 60s kill switch, atomic flip. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for rollout plan + per-step gate result + online quality event + rollback receipt. | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: slow kill switch, sampling too thin, stale eval, skipped steps, no kill-switch rehearsal, judge drift. | ~900 |
| `content/04-procedure.xml` | medium | Steps: plan → golden eval pass at 1% → 24h hold → online sample → promote/rollback → repeat at 5/25/100. | ~800 |
| `content/06-decision-tree.xml` | essential | Routes by gate-state and quality-band at each step. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft-rollout-plan` | sonnet | Schema fill from prior templates. |
| `score-sampled-traffic` | haiku | LLM-as-judge for cheap online scoring. |
| `decide-rollback` | opus | Cross-signal synthesis on borderline cases. |

## Templates

| File | Purpose |
|---|---|
| `templates/rollout-plan.json` | JSON schema for the rollout plan. |
| `templates/rollout-plan.md` | Markdown skeleton for the human-readable plan. |
| `templates/step-gate-result.json` | Per-step gate result schema. |
| `templates/rollback-receipt.json` | Rollback receipt schema (records the 60s contract). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-rag-canary-rollout-plan.py` | Validate the plan: 4 steps, sample_rate ≥0.05 during 5%, kill_switch criteria ≥4, atomic flip = true. | Pre-commit + per-step gate. |

## Related

- [[rag-pipeline-design]]
- [[rag-evaluation]]
- [[retrieval-drift-alerting-recipe]]
- [[router-shadow-deploy-protocol]]

## Decision tree

The tree at `content/06-decision-tree.xml` enumerates the per-step gate path: golden eval pass + online quality within band + latency p95 within +20% → promote; else → rollback within 60s. Walk it before promoting any step; never skip the hold.
