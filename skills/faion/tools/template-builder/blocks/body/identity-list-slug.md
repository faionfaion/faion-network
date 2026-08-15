<!--
purpose: Artefact identity as a backticked bullet list keyed on slug plus produced_at. 113 templates carry it verbatim; it is the identity form of the infra/marketing skeleton family.
consumes: the identity field values
produces: the identity list that opens the artefact body
depends-on: nothing
token-budget-impact: ~55 tokens
variables:
  - name: slug
    type: string
    required: true
    description: Methodology slug this artefact was produced from.
  - name: owner
    type: string
    required: true
    default: "<name>"
    description: One named human. Never a team, never "us", never "TBD".
  - name: owner_role
    type: string
    required: true
    default: "<role>"
    description: The owner's role, for rotation.
  - name: version
    type: string
    required: true
    default: "1.0.0"
    description: Semantic version of this artefact instance.
  - name: last_reviewed
    type: string
    required: true
    description: ISO-8601 date this artefact was last reviewed.
  - name: produced_at
    type: string
    required: true
    default: "<ISO-8601 datetime>"
    description: ISO-8601 timestamp this artefact was produced.
-->
- slug: `{{slug}}`
- owner: `{{owner}}` / `{{owner_role}}`
- version: `{{version}}`
- last_reviewed: `{{last_reviewed}}`
- produced_at: `{{produced_at}}`
