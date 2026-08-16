# Tm To Fp Conversion Playbook

## Summary

**One-sentence:** Tm To Fp Conversion Playbook: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)': A common but undocumented commercial transition. faion has scope-management and change-control but no end-to-end T&M-to-FP conversion playbook with the data audit + estimate + reserves recipe. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tm to fp conversion playbook artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- T&M engagement переходить у fixed-price у 6-тижневому вікні з ризиком scope-вибуху.
- Outsource-провайдер веде conversion без втрати margin або client trust.
- Потрібен auditable playbook з conversion-gate, не ad-hoc негоціації.

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tm to fp conversion playbook artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Tm To Fp Conversion Playbook |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/tm-to-fp-conversion-playbook.md.j2` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/tm-to-fp-conversion-playbook.md` | Filled artefact skeleton conforming to 02-output-contract.xml Generated from `templates/tm-to-fp-conversion-playbook.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/tm-to-fp-conversion-playbook.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in version exercised by scripts/validate-tm-to-fp-conversion-playbook.py --self-test |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-tm-to-fp-conversion-playbook.py --self-test Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tm-to-fp-conversion-playbook.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p4-outsource-specialist/T&M to fixed-price contract conversion (6 weeks)`
- pro/pm/p4-outsource-specialist

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tm-to-fp-conversion-playbook.schema.json`

```json
{
  "__faion_header__": {
    "purpose": "JSON Schema for tm-to-fp-conversion-playbook",
    "consumes": "validated against artefacts produced by the methodology",
    "produces": "schema document for validator script",
    "depends_on": "content/02-output-contract.xml",
    "token_budget_impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/tm-to-fp-conversion-playbook.json",
  "type": "object",
  "required": ["artefact_id", "owner", "decision", "version", "last_reviewed", "inputs_used"],
  "properties": {
    "artefact_id": { "type": "string", "pattern": "^[a-z][a-z0-9-]+$" },
    "owner": { "type": "string", "minLength": 2 },
    "decision": { "type": "string", "minLength": 2 },
    "rationale": { "type": "string" },
    "version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "last_reviewed": { "type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$" },
    "inputs_used": { "type": "array", "items": { "type": "string" }, "minItems": 1 }
  }
}
```
