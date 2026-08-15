<!--
purpose: Provenance table keyed Claim/Link. Byte-identical in 74 templates, mostly infra and marketing. Kept separate from the Source/Citation table on purpose: the column names are the contract, and parameterising them would make the block agree with everything and mean nothing.
consumes: one evidence row
produces: an H2 Evidence section with a two-column table
depends-on: nothing
token-budget-impact: ~35 tokens
variables:
  - name: evidence_claim
    type: string
    required: true
    default: "<claim>"
    description: The claim this row anchors, stated so it can be checked.
  - name: evidence_link
    type: string
    required: true
    default: "<https://...>"
    description: URL or path that supports the claim.
-->
## Evidence

| Claim | Link |
|-------|------|
| `{{evidence_claim}}` | `{{evidence_link}}` |
