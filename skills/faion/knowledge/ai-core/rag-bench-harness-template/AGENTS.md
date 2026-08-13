# RAG Bench Harness Template

## Summary

**One-sentence:** Spec for a reusable RAG bench harness — corpus snapshot, query set, retriever runners, eval metrics, leaderboard schema — so chunking-strategy comparisons stop being hand-wave.

**One-paragraph:** Existing RAG eval methodologies are atomic (rag-eval-metrics, rag-eval-ab-testing). A wire-it-together harness that runs a chunking experiment end-to-end is missing. This methodology produces a `rag-bench-spec.json` artefact pinning corpus snapshot, query set, retriever runners, eval metrics (Recall@k, MRR, faithfulness), and a leaderboard schema. Output is a versioned harness consumed by chunking-strategy A/Bs.

**Ефективно для:**

- Chunking strategy bench (recurring, weekly or quarterly).
- Compare retrievers (BM25 vs dense vs hybrid) on the same corpus.
- Reproducible eval — corpus snapshot pinned by sha.
- Leaderboard schema для cross-strategy comparison.
- Bridge до downstream `[[prompt-ab-power-calculator]]` для chunking A/B.

## Applies If (ALL must hold)

- Recurring RAG bench on the operating cadence.
- Corpus + query set committable to repo.
- Named accountable owner.
- Eval metrics agreed (Recall@k / MRR / faithfulness).

## Skip If (ANY kills it)

- One-shot bench without recurrence.
- No corpus snapshot can be committed (purely-live or licensed-only data).
- Fewer than 3 instances per year.
- No named owner.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Corpus snapshot | sha-pinned dataset | warehouse |
| Query set with gold labels | JSONL | eval repo |
| Retriever runner catalog (BM25, dense, hybrid) | YAML | service repo |
| Eval metric definitions | YAML | eval repo |
| Named accountable owner | string | ownership log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-ab-power-calculator]]` | Computes sample size for A/B variants. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for rag-bench-spec + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/04-procedure.xml` | essential | 5-step: snapshot → query set → runners → metrics → leaderboard | ~700 |
| `content/05-examples.xml` | essential | Worked example: chunking-bench on 50k doc corpus | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus type to retriever set | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `snapshot-corpus` | haiku | Mechanical. |
| `pick-runners` | sonnet | Per-corpus judgment. |
| `metric-validation` | opus | Cross-metric reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rag-bench-spec.json` | JSON skeleton matching 02-output-contract. |
| `templates/rag-bench-spec.md` | Narrative review draft. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-bench-harness-template.py` | Validate rag-bench-spec | Pre-commit + before bench run |

## Related

- [[prompt-ab-power-calculator]]
- [[rag-corpus-discovery-interview]]
- [[production-trace-mining-for-training-data]]

## Decision tree

See `content/06-decision-tree.xml`. The tree picks retriever set based on corpus type (free-form prose, structured docs, code) and metric set based on task (retrieval vs generation). Walk it before drafting the spec.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rag-bench-spec.json`

```json
{
  "artefact_id": "rag-bench-<task>-<period>",
  "owner": "<handle>@faion.net",
  "corpus": {
    "path": "warehouse://<table>",
    "sha": "<sha>",
    "doc_count": 50000
  },
  "query_set": {
    "path": "git://<repo>/eval/queries.jsonl",
    "gold_labels": true,
    "size": 800
  },
  "runners": [
    {
      "name": "bm25",
      "version": "rank_bm25-0.2.2",
      "config_hash": "<hash>"
    },
    {
      "name": "dense",
      "version": "<model-name>",
      "config_hash": "<hash>"
    },
    {
      "name": "hybrid",
      "version": "<v>",
      "config_hash": "<hash>"
    }
  ],
  "metrics": [
    "Recall@10",
    "MRR",
    "faithfulness"
  ],
  "leaderboard_path": "git://<repo>/leaderboards/<file>.json",
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
