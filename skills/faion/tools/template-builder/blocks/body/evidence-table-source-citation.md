<!--
purpose: Provenance table keyed Source/Citation. Byte-identical in 58 templates across 5 domains. An evidence table is an evidence table — the column contract does not vary by methodology, so identity across 58 files is shape, not emptiness.
consumes: one evidence row
produces: an H2 Evidence section with a two-column table
depends-on: nothing
token-budget-impact: ~35 tokens
variables:
  - name: evidence_source
    type: string
    required: true
    default: "https://example.com/source-1"
    description: URL, path or system of record the claim came from.
  - name: evidence_citation
    type: string
    required: true
    default: "verbatim quote"
    description: The verbatim quote or locator inside that source.
-->
## Evidence

| Source | Citation |
|--------|----------|
| {{evidence_source}} | {{evidence_citation}} |
