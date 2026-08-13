# Retrieval Drift Alerting Recipe

## Summary

**One-sentence:** Production recipe that detects RAG retrieval-distribution drift — new query types, embedding-model staleness, corpus rot — using four named metrics with thresholds, alert routes, and rollback gates.

**One-paragraph:** Generic production monitoring covers RAG quality (faithfulness, answer-relevance) but treats retrieval as healthy if recall@k holds. In practice, retrieval drifts silently in three failure modes: (a) the query distribution shifts (new product, new user segment, seasonal query), (b) the embedding model or chunking changes and old vectors become incompatible, (c) the corpus rots (documents updated but vectors not re-embedded). This recipe defines four metrics that catch each class — query-embedding KL divergence, retrieval-set Jaccard drift, top-k score histogram drift, neighbour-recency — with thresholds, alert routes (P1 page vs P3 ticket), and an automatic gate that flips the system into safer mode (return citations only, no synthesis) until drift is resolved. Mechanism: continuous sampling + nightly batch vs a frozen baseline window. Primary output: a `drift-alerts.yaml` config + Prometheus rules + Grafana dashboard.

**Ефективно для:**

- Production RAG із ≥1000 queries/day — drift приходить тихо; чотири метрики ловлять його до того як upper-funnel метрики деградують.
- Команд що часто оновлюють embedding-модель або корпус — drift-alerts фіксує silent incompatibility між старими векторами і новими запитами.
- Безпеково-критичних KB (legal, medical, finance) — auto-safer-mode gate перетворює галюцинації на "return citations only" замість синтезу.
- SLO-driven команд — кожна з 4 метрик мапиться на burn-rate з власним P1/P3 routing.

## Applies If (ALL must hold)

- production RAG system with ≥1000 queries/day OR business-critical RAG with any volume
- a baseline window of healthy retrieval has been captured (≥2 weeks of stable production)
- ability to log query embeddings, retrieved-doc IDs, and similarity scores per request
- alerting infrastructure exists (Grafana / Datadog / Sentry / PagerDuty)
- rollback path defined (feature flag, blue/green, or read-only safer mode)

## Skip If (ANY kills it)

- demo / internal RAG with no production users — over-engineered
- query volume too low (≤100/day) to compute meaningful distributional metrics — sample more before alerting
- no baseline window has been captured — capture a baseline first; alerting against undefined "normal" is alarm fatigue
- no rollback path — alerts without action are noise; build the rollback first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `query-embedding-log` | parquet (vector + timestamp + retrieved-doc-ids + scores) | production request tracer |
| `baseline_2026_XX.parquet` | parquet snapshot | 2-week stable window captured by `scripts/baseline-refresh.py` |
| `drift-metric-library` | pip dependency | one of: evidently, nannyml, scikit-multiflow, in-house |
| `alert-routing-matrix.yaml` | YAML | which on-call gets paged for each drift class |

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
| `content/01-core-rules.xml` | essential | 5 rules: baseline freshness, 4-metric coverage, P1/P3 routing, safer-mode gate, recontract trigger | 1100 |
| `content/02-output-contract.xml` | essential | drift-alerts.yaml schema, Prometheus rule format, baseline snapshot schema | 800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: silent embedding upgrade, baseline contamination, alert fatigue, corpus rot | 1100 |
| `content/04-procedure.xml` | essential | 6 steps: capture baseline → compute nightly metrics → wire alerts → install gate → drill the rollback → refresh baseline | 800 |
| `content/05-examples.xml` | essential | Worked example: corpus update without re-embed triggers Jaccard drift | 600 |
| `content/06-decision-tree.xml` | essential | Routes by metric breach class to P1 page / P3 ticket / safer-mode gate | 400 |

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
| `templates/grafana-dashboard.json` | Dashboard JSON skeleton with the four panels |
| `templates/_smoke-test.yaml` | Minimum-viable drift-alerts.yaml that validates clean |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retrieval-drift-alerting-recipe.py` | Lint drift-alerts.yaml against schema | Pre-commit + pre-deploy |

## Related

- [[rag-feature-acceptance-contract]] — recontract triggers reference these metrics
- [[router-shadow-deploy-protocol]] — pre-promotion guardrail, complementary to runtime drift
- [[embeddings-production-ops]] — re-embed protocol when drift demands it
- external: [EvidentlyAI drift docs](https://docs.evidentlyai.com/) · [NannyML](https://www.nannyml.com/)

## Decision tree

See `content/06-decision-tree.xml`. Branches on metric class (query-KL vs Jaccard vs score-histogram vs neighbour-recency), magnitude, and sustained window — routes to P1 page, P3 ticket, or auto-safer-mode gate.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/drift-alerts.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [baseline, metrics, routing, gate]
properties:
  baseline:
    type: object
    required: [path, window_days, captured_at]
    properties:
      path: { type: string }
      window_days: { type: integer, minimum: 7 }
      captured_at: { type: string, format: date }
  metrics:
    type: array
    minItems: 4
    items:
      type: object
      required: [name, kind, threshold_sigma]
      properties:
        name:
          type: string
          enum: [query-embedding-kl, retrieval-set-jaccard, score-histogram-ks, neighbour-recency]
        kind: { type: string, enum: [distribution, set, histogram, recency] }
        threshold_sigma: { type: number, minimum: 1 }
  routing:
    type: object
    required: [p1_dual_metric, p3_single_metric_sustained_min]
    properties:
      p1_dual_metric: { type: integer, minimum: 2 }
      p3_single_metric_sustained_min: { type: integer, minimum: 1 }
  gate:
    type: object
    required: [enabled, mode, flag_name]
    properties:
      enabled: { type: boolean }
      mode: { type: string, enum: [citations-only, refuse, fall-through] }
      flag_name: { type: string }
```

### `templates/prometheus-rules.yaml`

```yaml
groups:
  - name: rag-retrieval-drift
    interval: 5m
    rules:
      - alert: RetrievalDriftP1Dual
        expr: count by (env) (drift_metric_sigma > 1) >= 2
        for: 10m
        labels:
          severity: page
        annotations:
          summary: "RAG retrieval drift: 2+ metrics breach"
          runbook: "https://runbooks.example.com/rag-drift-p1"

      - alert: RetrievalDriftP1SingleSevere
        expr: drift_metric_sigma >= 3
        for: 10m
        labels:
          severity: page
        annotations:
          summary: "RAG retrieval drift: single metric 3σ"

      - alert: RetrievalDriftP3Sustained
        expr: drift_metric_sigma >= 1 and drift_metric_sigma < 3
        for: 60m
        labels:
          severity: ticket
        annotations:
          summary: "RAG retrieval drift: sustained low-intensity (recontract candidate)"
```

### `templates/grafana-dashboard.json`

```json
{
  "_header": [
    "purpose: Grafana dashboard skeleton with 4 panels (one per drift metric)",
    "consumes: drift_metric_sigma{name=...} Prometheus series",
    "produces: config (Grafana dashboard JSON import payload)",
    "depends-on: grafana >= 10.0",
    "token-budget-impact: 0 at runtime"
  ],
  "title": "RAG Retrieval Drift",
  "uid": "rag-retrieval-drift",
  "schemaVersion": 39,
  "version": 1,
  "panels": [
    {
      "id": 1,
      "title": "Query-embedding KL divergence",
      "type": "timeseries",
      "targets": [
        {
          "expr": "drift_metric_sigma{name=\"query-embedding-kl\"}"
        }
      ],
      "thresholds": {
        "steps": [
          {
            "value": 1,
            "color": "yellow"
          },
          {
            "value": 3,
            "color": "red"
          }
        ]
      }
    },
    {
      "id": 2,
      "title": "Retrieval-set Jaccard drift",
      "type": "timeseries",
      "targets": [
        {
          "expr": "drift_metric_sigma{name=\"retrieval-set-jaccard\"}"
        }
      ],
      "thresholds": {
        "steps": [
          {
            "value": 1,
            "color": "yellow"
          },
          {
            "value": 3,
            "color": "red"
          }
        ]
      }
    },
    {
      "id": 3,
      "title": "Score-histogram KS",
      "type": "timeseries",
      "targets": [
        {
          "expr": "drift_metric_sigma{name=\"score-histogram-ks\"}"
        }
      ],
      "thresholds": {
        "steps": [
          {
            "value": 1,
            "color": "yellow"
          },
          {
            "value": 3,
            "color": "red"
          }
        ]
      }
    },
    {
      "id": 4,
      "title": "Neighbour recency",
      "type": "timeseries",
      "targets": [
        {
          "expr": "drift_metric_sigma{name=\"neighbour-recency\"}"
        }
      ],
      "thresholds": {
        "steps": [
          {
            "value": 1,
            "color": "yellow"
          },
          {
            "value": 3,
            "color": "red"
          }
        ]
      }
    }
  ]
}
```

### `templates/_smoke-test.yaml`

```yaml
baseline:
  path: "s3://rag-baselines/2026-05-01.parquet"
  window_days: 14
  captured_at: "2026-05-01"

metrics:
  - name: query-embedding-kl
    kind: distribution
    threshold_sigma: 1.0
  - name: retrieval-set-jaccard
    kind: set
    threshold_sigma: 1.0
  - name: score-histogram-ks
    kind: histogram
    threshold_sigma: 1.0
  - name: neighbour-recency
    kind: recency
    threshold_sigma: 1.0

routing:
  p1_dual_metric: 2
  p3_single_metric_sustained_min: 60

gate:
  enabled: true
  mode: citations-only
  flag_name: rag.safer_mode
```
