# purpose: per-incident RAG failure triage form
# consumes: failing query + answer + retrieved context
# produces: JSON matching 02-output-contract schema
# depends-on: content/01-core-rules.xml r1-r4
# token-budget-impact: zero at runtime; form only

incident_id: inc-YYYY-MM-DD-NNN
query: "..."
retrieved_chunk_ids: [...]
answer: "..."

Primary label (one of): retrieval-fail | generation-fail | chunk-boundary | stale-doc | wrong-doc-ranked | prompt-leak
Secondary label (optional, same set): 
Evidence (≤200 chars): "..."
Reviewer id: 
Disagreement? (y/n): 
