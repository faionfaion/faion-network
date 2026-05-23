<!-- purpose: rag-bench-spec narrative skeleton -->
<!-- consumes: rag-bench-spec.json -->
<!-- produces: review draft -->
<!-- depends-on: content/02-output-contract.xml schema -->
<!-- token-budget-impact: ~200 tokens -->

# RAG Bench Spec — `<artefact_id>`

- **Owner:** `<handle>`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-22`

## Corpus

- Path: `warehouse://<table>`
- Sha: `<sha>`
- Docs: `50000`

## Query set

- Path: `git://<repo>/eval/queries.jsonl`
- Gold labels: `true`
- Size: `800`

## Runners

| name | version | config_hash |
|------|---------|-------------|
| bm25 | rank_bm25-0.2.2 | <hash> |
| dense | <model> | <hash> |
| hybrid | <v> | <hash> |

## Metrics

- Recall@10
- MRR
- faithfulness
