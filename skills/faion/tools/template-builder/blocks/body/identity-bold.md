<!--
purpose: Artefact identity as bold labels under a fill-me notice, closed by a rule. Byte-identical in 76 templates across dev, hr, architecture and backend — the identity block of the bracket-placeholder family.
consumes: the identity field values
produces: the notice, four bold identity lines and a horizontal rule
depends-on: nothing
token-budget-impact: ~55 tokens
variables:
  - name: artefact_id
    type: string
    required: true
    default: "[stable-slug]"
    description: Stable identifier for this artefact instance.
  - name: owner
    type: string
    required: true
    default: "[name <email> or role]"
    description: One named human, or a role with a rotation.
  - name: version
    type: string
    required: true
    default: "1.0.0"
    description: Semantic version of this artefact instance.
  - name: last_reviewed
    type: string
    required: true
    description: ISO-8601 date this artefact was last reviewed.
-->
> Replace bracketed placeholders before use.

**Artefact id:** `{{artefact_id}}`
**Owner:** `{{owner}}`
**Version:** `{{version}}`
**Last reviewed:** `{{last_reviewed}}`

---
