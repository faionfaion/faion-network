# Tool Consolidation Decision Rule

## Summary

**One-sentence:** Tool Consolidation Decision Rule: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Vendor / tool consolidation review'.

**One-paragraph:** Addresses the gap surfaced by 'p5-micro-agency-founder/Vendor / tool consolidation review': Cross-tool-migration covers mechanics but not the decision logic (cut / consolidate / replace / renegotiate). Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tool consolidation decision rule artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Micro-agency накопичила 12+ SaaS-інструментів з overlap і no-clear-owner ситуацією.
- Vendor/tool consolidation review потребує decision-rule, не "спробуємо новий tool".
- Founder хоче cut костів без втрати критичних workflows.

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Vendor / tool consolidation review' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tool consolidation decision rule artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Vendor / tool consolidation review' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Tool Consolidation Decision Rule |

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
| `templates/tool-consolidation-decision-rule.md.j2` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/tool-consolidation-decision-rule.md` | Filled artefact skeleton conforming to 02-output-contract.xml Generated from `templates/tool-consolidation-decision-rule.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/tool-consolidation-decision-rule.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in version exercised by scripts/validate-tool-consolidation-decision-rule.py --self-test |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-tool-consolidation-decision-rule.py --self-test Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-consolidation-decision-rule.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p5-micro-agency-founder/Vendor / tool consolidation review`
- pro/pm/p5-micro-agency-founder

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tool-consolidation-decision-rule.schema.json`

```json
{
  "__faion_header__": {
    "purpose": "JSON Schema for tool-consolidation-decision-rule",
    "consumes": "validated against artefacts produced by the methodology",
    "produces": "schema document for validator script",
    "depends_on": "content/02-output-contract.xml",
    "token_budget_impact": "small"
  },
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/tool-consolidation-decision-rule.json",
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
