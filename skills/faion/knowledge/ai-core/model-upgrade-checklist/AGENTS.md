# Model Upgrade Checklist

## Summary

**One-sentence:** Produces a model/provider upgrade safety checklist — typed input set, named owner, traceable decisions, eval gate, rollout policy, version + last_reviewed.

**One-paragraph:** Upgrading a model in production (Sonnet 4.5 → 4.6, GPT-4o → GPT-4.1) is non-trivial: subtle quality regressions, prompt-cache cache-busting, output format drift. This methodology produces a typed checklist with the inputs that justified the upgrade (prompt set, gold eval, cost band, latency band), a named owner, an eval gate, a rollout policy with kill-switch, and a `last_reviewed` field. Output is auditable and re-runnable on the next upgrade.

**Ефективно для:** ML-engineer, що піднімає prod-модель на нову версію і потребує явного safety pass з eval gate + rollout discipline + named owner.

## Applies If (ALL must hold)

- Task is "upgrade existing prod model to new generation / version".
- Inputs (current model id, target version, prompt set, gold eval, cost/latency bands) are available.
- Downstream consumer (executor or auditor) will read the artefact.
- Tier == geek.

## Skip If (ANY kills it)

- Team already maintains a working checklist for this upgrade.
- Greenfield prototype with no production users.
- Regulatory / compliance overrides in-methodology guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current model id + sha-pinned prompt set | doc | repo |
| Target model version | string | vendor changelog |
| Gold eval (≥30 hand-labelled items) | JSONL | eval repo |
| Cost + latency band targets | YAML | finops / SLO |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/model-migration-checklist` | Sibling: full provider migration. |
| `geek/ai/ml-engineer/model-evaluation` | Defines the eval the upgrade must satisfy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned + last_reviewed, traceable decision. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the upgrade checklist. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: invented inputs, plural owner, post-hoc rationale, stale record, no eval baseline. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes by input completeness + downstream consumer. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-instance upgrade judgement. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|---|---|
| `templates/model-upgrade-checklist.json` | JSON schema for the output contract. |
| `templates/model-upgrade-checklist.md.j2` | Markdown skeleton with required fields. |
| `templates/model-upgrade-checklist.md` | Markdown skeleton with required fields. Generated from `templates/model-upgrade-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-model-upgrade-checklist.py` | Enforce output contract. | After subagent return, before consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Model / provider upgrade safety pass`

## Decision tree

The tree at `content/06-decision-tree.xml` triages: typed input set + named owner + downstream consumer? → ship the checklist; otherwise → skip + escalate. Walk it before authoring so the upgrade plan has an eval gate and a named owner.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/model-upgrade-checklist.json`

```json
{
  "_purpose": "JSON Schema for the Model Upgrade Checklist output contract.",
  "_consumes": "upgrade-checklist.json from subagent",
  "_produces": "validation report for validate-model-upgrade-checklist.py",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/model-upgrade-checklist",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "current_model",
    "target_model",
    "eval_baseline_id",
    "rollout"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 1
    },
    "owner": {
      "type": "string",
      "minLength": 2,
      "not": {
        "pattern": "(?i)^(team|we|us|engineering|the (team|squad|group))$"
      }
    },
    "decision": {
      "type": "string",
      "minLength": 1
    },
    "rationale": {
      "type": "string",
      "minLength": 30
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ]
      },
      "minItems": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "current_model": {
      "type": "string",
      "minLength": 1
    },
    "target_model": {
      "type": "string",
      "minLength": 1
    },
    "eval_baseline_id": {
      "type": "string",
      "minLength": 1
    },
    "rollout": {
      "type": "object",
      "required": [
        "stages",
        "kill_switch_armed"
      ],
      "properties": {
        "stages": {
          "type": "array",
          "items": {
            "enum": [
              "shadow",
              "canary_1pct",
              "canary_5pct",
              "canary_25pct",
              "100pct"
            ]
          },
          "minItems": 1
        },
        "kill_switch_armed": {
          "type": "boolean",
          "const": true
        }
      }
    }
  }
}
```
