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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-index-tuning.py` | Lint index-tuning.yaml | Pre-commit |

## Related

- [[vector-databases]] — parent
- [[vector-db-monitoring]] — drift signal
- external: [Qdrant indexing guide](https://qdrant.tech/documentation/concepts/indexing/) · [HNSW paper](https://arxiv.org/abs/1603.09320)

## Decision tree

See `content/06-decision-tree.xml`. Routes by (a) workload (read / write / mixed), (b) memory cap, (c) recall floor → HNSW + quantization combo.
