<!--
purpose: Closing reviewer approval. Byte-identical in 55 templates, all in ba. Two fields, both about who accepted the artefact — nothing subject-specific can be written here, which is why every copy is the same.
consumes: reviewer, approved
produces: an H2 Sign-off section with two fields
depends-on: nothing
token-budget-impact: ~20 tokens
variables:
  - name: reviewer
    type: string
    required: true
    default: "<name>"
    description: The named human who reviewed this artefact. Never the author.
  - name: approved
    type: string
    required: true
    default: "<yes / no>"
    description: Whether the reviewer approved it.
-->
## Sign-off

- reviewer: {{reviewer}}
- approved: {{approved}}
