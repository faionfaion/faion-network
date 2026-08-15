<!--
purpose: The artefact title line. 2,902 of 3,242 templates open their body with a single H1; the six recurring suffix forms ("", " — <artefact_id>", " — Spec", " — Artefact", " — Artefact Skeleton", " — <file>.md") cover 628 of them, which is why the suffix is a parameter and not six blocks.
consumes: artefact_title, title_suffix
produces: one H1 line
depends-on: nothing
token-budget-impact: ~10 tokens
variables:
  - name: artefact_title
    type: string
    required: true
    description: Human-readable name of the artefact, title case. Usually the methodology name.
  - name: title_suffix
    type: string
    required: false
    default: ""
    description: Text appended after the title, e.g. " — Spec" or " — Artefact". Empty for a bare title.
-->
# {{artefact_title}}{{title_suffix}}
