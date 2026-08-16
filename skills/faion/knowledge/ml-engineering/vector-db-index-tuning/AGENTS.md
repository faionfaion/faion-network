# Vector Database Index and Quantization Tuning

## Summary

**One-sentence:** Tunes HNSW + quantization parameters per workload to land within (latency, recall, memory) SLAs — pinning M, ef_construct, ef_search, and quantization scheme via measured tradeoff curves on a representative dataset.

**One-paragraph:** Default vector-DB settings rarely match production workload. HNSW has three knobs: `M` (out-degree, 16-64 — bigger = more memory + better recall), `ef_construct` (build-time quality, 100-200), `ef_search` (query-time quality, 32-200). Quantization options: scalar int8 (4× compression, ≈1% recall loss), product quantization (8-32× compression, ≈3-5% loss), binary (32×, ≈5-10% loss). Read-heavy workloads tolerate higher `M` + ef_search; write-heavy needs smaller M + lower ef_construct. Output: a versioned `index-tuning.yaml` with measured (recall, p95_latency, memory_gb) per parameter set and the chosen recommendation.

**Ефективно для:**

- Production vector DBs з explicit latency SLA (p95 &lt;100ms) — tuning ловить розрив між defaults і реальними цифрами.
- Memory-constrained deployments — quantization дає 4-32× compression при дотриманні recall floor.
- Mixed workloads — read-heavy і write-heavy потребують різних M / ef налаштувань.
- Migration / re-index events — фіксована конфігурація щоб не вгадувати після зміни моделі.

## Applies If (ALL must hold)

- Vector DB live with ≥1M vectors (smaller scales — defaults usually fit)
- Defined latency / recall SLA per query mode
- Ability to run benchmark on representative query workload (1k+ queries)
- Backup of current index — tuning may require rebuild

## Skip If (ANY kills it)

- &lt;1M vectors — defaults fine
- No SLA defined — tuning has no target
- DB is managed (Pinecone) with no exposed HNSW knobs — accept managed defaults

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `corpus-snapshot` | DB collection | production or staging |
| `query-workload.jsonl` | JSONL | 1k+ representative queries |
| `sla.yaml` | YAML | (recall_floor, latency_p95_max, memory_cap_gb) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `vector-databases` | Parent DB selection |
| `vector-db-setup-prod` | Prod baseline before tuning |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bench-before-tune, quantize-with-recall-floor, workload-driven M, persist tuning record, recall regression gate | 1100 |
| `content/02-output-contract.xml` | essential | `index-tuning.yaml` schema | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: tune-without-bench, aggressive quantization, default ef_search in prod, no persist record, ignore memory cap | 900 |
| `content/04-procedure.xml` | essential | 5 steps: baseline → sweep params → quantize → re-bench → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: Qdrant 10M HNSW + scalar int8 tuning report | 500 |
| `content/06-decision-tree.xml` | essential | Routes by workload + memory + recall floor | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bench_run` | n/a (deterministic) | Pure measurement |
| `tuning_report_drafting` | sonnet | Trade-off synthesis |
| `index_tuning_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/index-tuning.schema.yaml` | Schema for index-tuning.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable spec |
| `templates/bench-template.py` | Pareto sweep skeleton for M × ef_search × quantization |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-index-tuning.py` | Lint index-tuning.yaml | Pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[vector-databases]] — parent
- [[vector-db-monitoring]] — drift signal
- external: [Qdrant indexing guide](https://qdrant.tech/documentation/concepts/indexing/) · [HNSW paper](https://arxiv.org/abs/1603.09320)

## Decision tree

See `content/06-decision-tree.xml`. Routes by (a) workload (read / write / mixed), (b) memory cap, (c) recall floor → HNSW + quantization combo.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/index-tuning.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [workload, hnsw, quantization, sla, bench, tuning_history_path]
properties:
  workload: {type: string, enum: [read-heavy, write-heavy, balanced]}
  hnsw:
    type: object
    required: [m, ef_construct, ef_search]
    properties:
      m: {type: integer, minimum: 16, maximum: 64}
      ef_construct: {type: integer, minimum: 32, maximum: 500}
      ef_search: {type: integer, minimum: 16, maximum: 500}
  quantization:
    type: object
    required: [scheme]
    properties:
      scheme: {type: string, enum: [none, scalar, product, binary]}
  sla:
    type: object
    required: [recall_floor, latency_p95_max_ms, memory_cap_gb]
    properties:
      recall_floor: {type: number, minimum: 0, maximum: 1}
      latency_p95_max_ms: {type: integer, minimum: 1}
      memory_cap_gb: {type: number, minimum: 0.1}
  bench:
    type: object
    required: [baseline, tuned]
  tuning_history_path: {type: string, minLength: 5}
```

### `templates/_smoke-test.yaml`

```yaml
workload: read-heavy
hnsw: {m: 32, ef_construct: 200, ef_search: 128}
quantization: {scheme: scalar}
sla: {recall_floor: 0.90, latency_p95_max_ms: 80, memory_cap_gb: 24}
bench:
  baseline: {recall: 0.84, latency_p95_ms: 38, memory_gb: 41}
  tuned: {recall: 0.93, latency_p95_ms: 62, memory_gb: 18}
tuning_history_path: ops/qdrant/tuning-history.yaml
```

### `templates/bench-template.py`

```python
"""Pareto sweep skeleton for HNSW M × ef_search × quantization."""
from __future__ import annotations

import time
import statistics


def bench_one(client, collection, queries, ground_truth, k: int = 10) -> dict:
    """Run queries, return recall@k + latency stats."""
    latencies = []
    hits = 0
    for q, expected in zip(queries, ground_truth):
        t0 = time.perf_counter()
        results = client.search(collection_name=collection, query_vector=q, limit=k)
        latencies.append((time.perf_counter() - t0) * 1000)
        ids = {r.id for r in results}
        hits += len(ids & set(expected)) / len(expected)
    return {
        "recall_at_k": hits / len(queries),
        "latency_p50_ms": statistics.median(latencies),
        "latency_p95_ms": sorted(latencies)[int(0.95 * len(latencies))],
    }


def sweep(client, collection, queries, ground_truth,
          m_values=(16, 32, 64),
          ef_values=(32, 64, 128, 200)) -> list[dict]:
    rows = []
    for m in m_values:
        # NOTE: in real bench, rebuild index per M; this is the skeleton
        for ef in ef_values:
            client.update_collection(collection_name=collection, hnsw_config={"ef": ef})
            r = bench_one(client, collection, queries, ground_truth)
            rows.append({"m": m, "ef_search": ef, **r})
    return rows
```
