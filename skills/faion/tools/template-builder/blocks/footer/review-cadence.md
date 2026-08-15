<!--
purpose: Closing review stamp. Byte-identical in 74 templates. Review cadence is a property of the artefact class, not of its subject, so identity across 74 files is the shape working as intended.
consumes: last_reviewed, review_cadence
produces: an H2 Review section with two fields
depends-on: nothing
token-budget-impact: ~25 tokens
variables:
  - name: last_reviewed
    type: string
    required: true
    description: ISO-8601 date this artefact was last reviewed.
  - name: review_cadence
    type: enum
    required: true
    default: "quarterly"
    options: [weekly, monthly, quarterly, annually]
    description: How often this artefact is re-reviewed.
-->
## Review

- last_reviewed: `{{last_reviewed}}`
- review_cadence: `{{review_cadence}}`
