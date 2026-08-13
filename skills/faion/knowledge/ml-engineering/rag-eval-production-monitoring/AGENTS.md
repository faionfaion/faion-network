# RAG Production Monitoring

## Summary

**One-sentence:** Logs latency / source count / user feedback per query and exposes calibrated anomaly thresholds for production RAG.

**One-paragraph:** Production RAG monitoring logs latency, source count, and user feedback for every query, aggregates rolling summaries (24h default window), and detects anomalies against calibrated thresholds. Lightweight metrics (latency, hit rate, user signals) run on every query; expensive LLM-based evaluation runs on sampled batches. Anomaly thresholds must be calibrated against actual production baselines — hardcoded defaults are placeholders only.

**Ефективно для:** команд із production RAG, які потребують безперервного нагляду без надмірних LLM-judge витрат.

## Applies If (ALL must hold)

- Any RAG system in production with real user traffic.
- User feedback signals (thumbs up/down) are available in the UI.
- Latency spikes (embedding timeout, vector DB overload) must be detected.
- Corpus is updated regularly and drift is expected.

## Skip If (ANY kills it)

- High-frequency LLM-judge on every query — too slow/expensive.
- User feedback is too sparse (<10 signals/day) — rely on scheduled batch eval.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Log sink | structured JSON | infra |
| Anomaly thresholds | JSON | calibration step |
| User-feedback hook | UI event | product |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-pipeline` | Provides batch eval that anchors anomaly thresholds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Stream-aggregate signals | haiku | Mechanical rollup. |
| Detect anomalies | haiku | Threshold comparisons. |
| Calibrate thresholds | sonnet | Per-domain judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/monitor-config.yaml` | Monitor config with window, signals, thresholds. |
| `templates/query-log-schema.json` | JSON schema for per-query log lines. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-production-monitoring.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-pipeline]]
- [[rag-eval-strategy]]
- [[rag-failure-taxonomy]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides per-query monitoring scope based on traffic and feedback availability. Each leaf references a rule id from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/monitor-config.yaml`

```yaml
window: 24h
signals:
  - latency_ms
  - source_count
  - thumbs_up
  - thumbs_down
thresholds:
  latency_p95_ms: 2000
  hit_rate_min: 0.88
  thumbs_down_ratio_max: 0.1
sampled_llm_judge:
  fraction: 0.05
  judge_model: gpt-4o
  seed: 42
```

### `templates/query-log-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "rag-query-log-line",
  "type": "object",
  "required": [
    "ts",
    "query_id",
    "latency_ms",
    "source_count",
    "top1_chunk_id"
  ],
  "properties": {
    "ts": {
      "type": "string"
    },
    "query_id": {
      "type": "string"
    },
    "latency_ms": {
      "type": "number"
    },
    "source_count": {
      "type": "integer"
    },
    "top1_chunk_id": {
      "type": "string"
    },
    "thumb": {
      "type": [
        "string",
        "null"
      ],
      "enum": [
        "up",
        "down",
        null
      ]
    }
  }
}
```
