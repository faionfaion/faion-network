---
slug: retrieval-drift-alerting-recipe
tier: geek
group: ml-engineer
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4a151c5c5568aab5"
summary: Production recipe for detecting retrieval-distribution drift in RAG (new query types, embedding-model staleness, corpus rot) with named metrics, thresholds, alerts, and rollback gates.
tags: [rag, drift-detection, observability, embeddings, production-monitoring]
---

# Retrieval Drift Alerting Recipe

## Summary

**One-sentence:** Production recipe that detects RAG retrieval-distribution drift — new query types, embedding-model staleness, corpus rot — using four named metrics with thresholds, alert routes, and rollback gates.

**One-paragraph:** Generic production-monitoring methodology covers RAG quality metrics (faithfulness, answer-relevance) but treats retrieval as healthy if recall@k holds. In practice, retrieval drifts silently in three failure modes: (a) the query distribution shifts (new product launched, new user segment, seasonal query), (b) the embedding model is upgraded or the chunking strategy changes and old vectors become incompatible, (c) the corpus rots (documents updated but vectors not re-embedded, or stale documents indexed). This recipe defines the four metrics that catch each drift class — query-embedding KL divergence, retrieval-set Jaccard drift, top-k score histogram, neighbour-recency — with concrete thresholds, alert routes (P1 page vs P3 ticket), and an automatic gate that flips the system into safer mode (return citations only, no synthesis) until drift is resolved. Mechanism: continuous sampling + nightly batch comparison vs a frozen baseline window. Primary output: a `drift-alerts.yaml` config + a Grafana dashboard + a Prometheus rule set.

## Applies If (ALL must hold)

- production RAG system with ≥1000 queries / day OR business-critical RAG with any volume
- a baseline window of healthy retrieval has been captured (≥2 weeks of stable production)
- ability to log query embeddings, retrieved-doc IDs, and similarity scores per request
- alerting infrastructure exists (Grafana / Datadog / Sentry / PagerDuty)
- rollback path defined (feature flag, blue/green, or read-only safer mode)

## Skip If (ANY kills it)

- demo / internal RAG with no production users — over-engineered
- query volume too low (≤100/day) to compute meaningful distributional metrics — sample more before alerting
- no baseline window has been captured — first capture a baseline; alerting against an undefined "normal" is alarm fatigue
- no rollback path — alerts without action are noise; build the rollback first

## Prerequisites

- query-embedding log (vector + timestamp + retrieved-doc-ids + scores)
- baseline window saved as `baseline_2026_XX.parquet` with the four reference distributions
- chosen drift metric library (Evidently, NannyML, scikit-multiflow, or in-house)
- alert routing matrix (which on-call gets paged for which class of drift)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-feature-acceptance-contract` | Recontract triggers reference these drift metrics |
| `geek/ai/ml-engineer/rag-evaluation-frameworks` | Vocabulary for retrieval metrics |
| `geek/ai/ml-engineer/embeddings-production-ops` | Embedding model versioning + re-embed protocol |
| `pro/infra/devops-engineer/slo-burn-rate-review-protocol` | Burn-rate logic for converting drift signals into pages |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: baseline freshness, 4-metric coverage, P1/P3 routing, gate behaviour, recontract trigger | ~1100 |
| `content/02-output-contract.xml` | essential | drift-alerts.yaml schema, Prometheus rule format, baseline snapshot schema | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: silent embedding upgrade, baseline contamination, alert fatigue, corpus rot, etc. | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `nightly_drift_compute` | n/a (deterministic) | Pure stats; no LLM |
| `alert_explanation_drafting` | sonnet | Translate metric breach into operator-readable summary |
| `recontract_trigger_proposal` | opus | When drift persists, decide whether to recontract, re-embed, or accept the shift |
| `alert_routing_lint` | haiku | Verify drift-alerts.yaml matches schema |

## Templates

| File | Purpose |
|------|---------|
| `templates/drift-alerts.schema.yaml` | Schema for drift-alerts.yaml |
| `templates/prometheus-rules.yaml` | Reference Prometheus rule set for the four metrics |
| `templates/grafana-dashboard.json` | Dashboard JSON with the four panels |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-drift-metrics.py` | Nightly batch: query KL, retrieval Jaccard, score histogram, neighbour-recency | Cron 03:00 UTC |
| `scripts/baseline-refresh.py` | Promote current window to baseline after recontract | After human approval of recontract event |
| `scripts/route-alert.py` | Decide P1 page vs P3 ticket based on metric + magnitude + sustained-window | Called by Prometheus alert hook |

## Related

- parent skill: `geek/ai/ml-engineer/`
- peer methodologies: `rag-feature-acceptance-contract`, `embeddings-production-ops`, `shadow-traffic-rollout-pattern`, `router-shadow-deploy-protocol`
- external: [EvidentlyAI drift docs](https://docs.evidentlyai.com/) · [NannyML](https://www.nannyml.com/) · [Pinecone — Production RAG monitoring](https://www.pinecone.io/learn/series/wisdom/production-rag/)
