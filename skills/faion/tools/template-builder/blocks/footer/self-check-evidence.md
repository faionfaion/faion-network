<!--
purpose: Closing checklist for evidence-bearing artefacts, ending in the validator invocation. 67 templates carry the evidence line; 44 of them use a shorter four-item wording without the pinned version and the validator row. This block is the long form.
consumes: template_version, slug
produces: an H2 Self-check section with five checkboxes
depends-on: scripts/validate-<slug>.py in the owning methodology
token-budget-impact: ~60 tokens
variables:
  - name: template_version
    type: string
    required: true
    default: "1.1.0"
    description: The template version a filled artefact must pin.
  - name: slug
    type: string
    required: true
    description: Methodology slug — names the validator script scripts/validate-<slug>.py.
-->
## Self-check

- [ ] template_version pinned to {{template_version}}
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-{{slug}}.py --file artefact.json` exits 0
