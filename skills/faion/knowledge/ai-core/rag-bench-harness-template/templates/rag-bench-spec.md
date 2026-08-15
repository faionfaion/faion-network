<!--
purpose: rag-bench-spec narrative skeleton
consumes: rag-bench-spec.json
produces: review draft
depends-on: content/02-output-contract.xml schema
token-budget-impact: ~200 tokens
variables:
  - name: slug
    type: string
    required: true
    description: Kebab-case id for this benchmark run, naming the corpus and the date - "support-kb-2026-08". Every number below is only comparable to runs sharing this id's corpus.
  - name: owner
    type: string
    required: true
    description: Handle of the engineer who owns the harness. When a number moves, this is the person who has to say whether the retriever changed or the corpus did.
  - name: corpus_table
    type: string
    required: true
    description: The warehouse table the corpus is read from, as schema.table. Pin a table, never a view - a view can change under the benchmark and the scores quietly stop comparing.
  - name: corpus_sha
    type: string
    required: true
    description: Content hash of the exact corpus snapshot this run indexed. Without it a re-run that scores differently tells you nothing about the change you were testing.
  - name: query_repo
    type: string
    required: true
    description: The git repo holding eval/queries.jsonl and its gold labels. Queries belong in git so a reviewer can see the commit where the benchmark got easier.
  - name: dense_model
    type: string
    required: true
    description: Embedding model and version behind the dense runner. Changing it invalidates every stored vector, so record which one produced these numbers before anyone tries to reproduce them.
-->

# RAG Bench Spec — `{{slug}}`

- **Owner:** `{{owner}}`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-22`

## Corpus

- Path: `warehouse://{{corpus_table}}`
- Sha: `{{corpus_sha}}`
- Docs: `50000`

## Query set

- Path: `git://{{query_repo}}/eval/queries.jsonl`
- Gold labels: `true`
- Size: `800`

## Runners

| name | version | config_hash |
|------|---------|-------------|
| bm25 | rank_bm25-0.2.2 | [hash] |
| dense | {{dense_model}} | [hash] |
| hybrid | [version] | [hash] |

## Metrics

- Recall@10
- MRR
- faithfulness
