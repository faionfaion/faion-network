<!--
purpose: Artefact identity as a bullet list keyed on artefact_id. Byte-identical in 189 templates across 8 domains after the owning slug is normalised out — the single most reused non-title fragment in the corpus.
consumes: the identity field values
produces: the identity list that opens the artefact body
depends-on: nothing
token-budget-impact: ~70 tokens
variables:
  - name: artefact_id
    type: string
    required: true
    default: "<slug>"
    description: Stable identifier for this artefact instance.
  - name: owner
    type: string
    required: true
    default: "<@handle>"
    description: One named human. Never a team, never "us", never "TBD".
  - name: last_reviewed
    type: string
    required: true
    description: ISO-8601 date this artefact was last reviewed.
  - name: version
    type: string
    required: true
    default: "1.0.0"
    description: Semantic version of this artefact instance.
  - name: decision
    type: string
    required: true
    default: "<go|hold|no-op>"
    description: The decision this artefact records.
  - name: rationale
    type: text
    required: true
    default: "<≥2 sentences citing an input by name>"
    description: Two or more sentences citing at least one input by name.
  - name: input_name
    type: string
    required: true
    default: "<input name>"
    description: Name of the first input the decision used.
  - name: input_source
    type: string
    required: true
    default: "<source path or URL>"
    description: Path or URL of that input.
-->
- artefact_id: {{artefact_id}}
- owner: {{owner}}
- last_reviewed: {{last_reviewed}}
- version: {{version}}
- decision: {{decision}}
- rationale: {{rationale}}
- inputs_used:
  - {{input_name}}: {{input_source}}
