# Embedding Quality Evaluation and Benchmarking

## Summary

**One-sentence:** Produces a quantitative evaluation report ranking candidate embedding models by Recall@K, MRR@10, nDCG@10 on a team-specific golden set, with A/B confidence intervals and a deployment recommendation.

**One-paragraph:** Public benchmarks (MTEB, BEIR) rank models on generic corpora; team-specific retrieval almost always disagrees with the leaderboard. This methodology ships a workflow for building a domain golden set (50-500 query-passage relevance triples), running candidate models offline, computing Recall@K / MRR@10 / nDCG@10, and (optionally) A/B testing the top two in production with click-through telemetry. Output is a Markdown report with one ranked table per metric + a chosen model + a stale-by date.

**Ефективно для:**

- Вибору embedding-моделі для нового RAG / search проекту — leaderboard sosi, твій корпус вирішує.
- Перевірки чи варто платити за proprietary (Voyage, Cohere) vs open-source (BGE, E5, Nomic) на твоєму домені.
- Аудиту production-retrieval-у, де користувачі скаржаться на якість, але метрики не міряні.
- Quarterly re-evaluation: моделі виходять / здешевшуються; рейтинг треба оновити.
- Дешевого швидкого MTEB-style sanity-check перед інвестицією в fine-tuning embedder-а.

## Applies If (ALL must hold)

- Team can produce ≥50 query-passage relevance triples from real usage logs OR via SME annotation.
- ≥2 candidate embedding models exist (e.g. text-embedding-3-small vs Voyage-3 vs BGE-M3).
- Retrieval quality is a measurable success metric (search CTR, RAG citation accuracy, classification F1).

## Skip If (ANY kills it)

- Golden set cannot be built (no usage logs, no SME availability) — eval would measure noise, not quality.
- Latency is the sole constraint and quality is sufficient on the cheapest model — measurement is overhead.
- Domain is identical to a major public benchmark (e.g. open-domain QA) and MTEB leaderboard suffices.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Golden set (queries + relevant passage ids + grades) | JSONL | Usage logs + SME annotation |
| Candidate model list (≥2) | YAML | Engineering |
| Vector store handle | client | Infra |
| Optional production telemetry | metrics dashboard | Observability |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[embeddings-model-selection]] | Defines candidate set from which this picks. |
| [[model-evaluation]] | General eval methodology this specializes for embeddings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: golden-set size ≥50, three metrics minimum, statistical-significance gate, hold-out 20%, quarterly re-eval | 900 |
| `content/02-output-contract.xml` | essential | Schema for the eval report: per-model metric table, winner, confidence interval, stale-by date | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: tiny golden set, single metric, train-on-test contamination, no significance test | 700 |
| `content/04-procedure.xml` | reference | 5-step procedure: build set → run candidates → compute metrics → significance → recommend | 600 |
| `content/05-examples.xml` | reference | One worked eval comparing 3 models on a support-bot golden set | 500 |
| `content/06-decision-tree.xml` | essential | When to escalate to live A/B vs ship offline-winner | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `annotate_golden_set` | haiku-4-5 | Cheap relevance labeling with SME-in-loop review. |
| `compute_metrics` | n/a (Python) | Deterministic computation; no LLM call needed. |
| `draft_eval_report` | sonnet-4-6 | Synthesis with confidence-interval reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/golden-set.jsonl` | Schema for golden-set rows: query_id, passage_id, grade. |
| `templates/eval-report.md` | Markdown skeleton for the eval report. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embeddings-evaluation.py` | Validate the eval report JSON against the contract. | Pre-commit; before model swap PR. |

## Related

- [[embeddings-model-selection]] — feeds candidates in.
- [[embedding-generation]] — producer of the candidate embeddings.
- [[model-evaluation]] — parent eval methodology.

## Decision tree

See `content/06-decision-tree.xml`. Branches first on whether golden_set_size ≥50 (no → block, build set first). Then asks whether offline winner is statistically separated (CI gap ≥1.5%) — yes → ship the winner; no → escalate to live A/B with click-through measurement. Final branch decides quarterly_review_due date. Leaves cite rule ids in `01-core-rules.xml`.
