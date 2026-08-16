<!--
purpose: instrumentation recipe — where to put the token counter for the four common retrieval shapes.
consumes: an existing retriever and either a provider usage field or a local tokenizer.
produces: the four per-row columns of retrieval-cost-ledger.yaml.
depends-on: content/01-core-rules.xml (r1-lookup-is-the-unit)
token-budget-impact: one replay of ten queries; no permanent runtime overhead if the counter is sampled.
-->

# Measuring one lookup

The unit is the whole lookup, not the retrieval call (r1). Wrap the counter around the
outermost boundary — query in, answer body out — and attribute every string that
crosses into the model to exactly one of three buckets.

## Bucket assignment

| Bucket | What goes in it |
|---|---|
| `index_tokens` | Routing files, taxonomies, manifests, index or INDEX-style files, table-of-contents reads, schema dumps, any "which document should I open" step — including a routing LLM call's own input. |
| `candidate_tokens` | Every document, chunk or record retrieved and shown to a model or a reranker, **including candidates later discarded**. Reranker input counts here. |
| `body_tokens` | Only the content that actually answered. If a 6k-token chunk was retrieved and 1.2k of it answered, `body_tokens` is 1.2k and the other 4.8k belongs in `candidate_tokens`. |

Double-counting is the usual error: a chunk counted in both `candidate_tokens` and
`body_tokens` inflates the total and deflates the ratio. Split it.

## Per retrieval shape

**Flat vector store.** `index_tokens` is usually 0 (the ANN index is not read by the
model). `candidate_tokens` is `top_k * chunk_size`, before reranking. Instrument at the
call that assembles the prompt, not at the vector-store client.

**Tree or hierarchical index.** The expensive shape. `index_tokens` is the sum of every
level read on the way down — L1 plus each L2 opened, plus any index re-read after a
wrong turn. Count re-reads; a lookup that backtracks pays twice. This is the leg that
dominates and the one no default instrumentation captures.

**Graph traversal.** `candidate_tokens` is every node and edge payload materialised
during the walk, at every hop, before ranking truncated the set. Count the pre-truncation
volume: that is what the traversal actually cost to produce.

**Agent with a search tool.** One lookup spans every tool call in the turn plus the tool
results. If the agent searched three times before answering, all three searches and all
three result sets belong to the same row. Do not record three rows.

## Where the counter goes

Prefer the provider's usage field on each call and sum per lookup — it is the billed
number and needs no tokenizer agreement. If usage is unavailable, tokenize the exact
strings sent, with the same tokenizer on both sides of any comparison (r6). Character
counts divided by four are an estimate, and an estimate in this format acquires the
authority of a measurement (f6). If neither is available, do not produce a ledger.

## Judging `correct`

Coarse and binary, against a criterion stated once in `sampling`: did the delivered body
contain what was needed to answer, judged by whoever asked. This exists only to make
`tokens_per_correct_answer` computable and to catch cost reductions that are really
quality regressions (f5). It is not a retrieval evaluation — use
`rag-eval-retrieval-metrics` for that.
