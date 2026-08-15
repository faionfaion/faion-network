<!--
purpose: Artefact identity as a Field/Value table. 235 templates open with an `| artefact_id |` row; 65 carry this exact five-row form. It is the identity block of the output-skeleton family.
consumes: the identity field values
produces: a two-column identity table
depends-on: nothing
token-budget-impact: ~70 tokens
variables:
  - name: artefact_id
    type: string
    required: true
    description: Stable identifier for this artefact instance, conventionally <slug>-YYYY-MM-DD.
  - name: owner
    type: string
    required: true
    default: "named human (no group terms)"
    description: One named human. Never a team, never "us", never "TBD".
  - name: last_touched
    type: string
    required: true
    default: "ISO-8601 timestamp"
    description: When this artefact was last edited.
  - name: template_version
    type: string
    required: true
    default: "1.1.0"
    description: Version of the template this artefact was produced from.
  - name: status
    type: string
    required: true
    default: "draft \| ready_for_review \| approved \| archived"
    description: Lifecycle status. Default lists the permitted values for an unfilled skeleton.
-->
| Field | Value |
|-------|-------|
| artefact_id | {{artefact_id}} |
| owner | {{owner}} |
| last_touched | {{last_touched}} |
| template_version | {{template_version}} |
| status | {{status}} |
