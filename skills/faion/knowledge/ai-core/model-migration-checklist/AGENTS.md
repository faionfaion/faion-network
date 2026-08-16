# Model Migration Checklist

## Summary

**One-sentence:** Produces a model-provider/generation migration checklist — typed input set, named owner, traceable decisions, version + last_reviewed for staleness.

**One-paragraph:** Migrating LLM provider or model generation rarely fails on the SDK; it fails on the prompt, the eval, and the unspoken assumptions. This methodology turns the migration into a typed artefact: input list (current model, target model, prompt set, gold eval, cost band, latency band), named owner, decisions traceable to those inputs, and a `last_reviewed` field. Output is a checklist a downstream engineer can execute or audit without re-deriving the rationale.

**Ефективно для:** ML-engineer, що мігрує OpenAI → Anthropic / Sonnet → Opus / GPT-4o → Gemini і хоче явну, ревьюваєму, ownable migration plan замість wiki-page heroics.

## Applies If (ALL must hold)

- Task is "migrate LLM provider or model generation" with production traffic at stake.
- Inputs (current model, target, prompt set, gold eval, cost/latency bands) are available.
- Downstream consumer (executor or auditor) will read the artefact.
- Tier == geek.

## Skip If (ANY kills it)

- Team already maintains a working checklist for this gap.
- Greenfield prototype with no production users.
- Regulatory / compliance overrides in-methodology guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Current model + sha-pinned prompt set | doc | repo |
| Target model id | string | architecture decision |
| Gold eval (≥30 hand-labelled items) | JSONL | eval repo |
| Cost + latency band targets | YAML | finops / SLO |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/llm-integration/model-onboarding-checklist` | Sibling: onboarding a new model. |
| `geek/ai/ml-engineer/model-evaluation` | Defines the eval the migration must satisfy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned + last_reviewed, traceable decision. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the migration checklist. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: invented inputs, plural owner, post-hoc rationale, stale record, missing eval baseline. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes by input completeness + downstream consumer. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-instance migration judgement. |
| `review_for_compliance` | opus | Cross-input synthesis. |

## Templates

| File | Purpose |
|---|---|
| `templates/model-migration-checklist.json` | JSON schema for the output contract. |
| `templates/model-migration-checklist.md.j2` | Markdown skeleton with required fields. |
| `templates/model-migration-checklist.md` | Markdown skeleton with required fields. Generated from `templates/model-migration-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-model-migration-checklist.py` | Enforce output contract. | After subagent return, before consumer reads. |

## Related

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Migrate LLM provider / model generation`

## Decision tree

The tree at `content/06-decision-tree.xml` triages: typed input set + named owner + downstream consumer? → ship the checklist; otherwise → skip + escalate. Walk it before authoring so the migration plan is owned and auditable.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/model-migration-checklist.json`

```json
{
  "_purpose": "JSON Schema for the Model Migration Checklist output contract.",
  "_consumes": "migration-checklist.json from subagent",
  "_produces": "validation report for validate-model-migration-checklist.py",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/model-migration-checklist",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "from_model",
    "to_model",
    "eval_baseline_id"
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
    "from_model": {
      "type": "string",
      "minLength": 1
    },
    "to_model": {
      "type": "string",
      "minLength": 1
    },
    "eval_baseline_id": {
      "type": "string",
      "minLength": 1
    },
    "rollout": {
      "type": "object",
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
          }
        },
        "kill_switch": {
          "type": "boolean"
        }
      }
    }
  }
}
```
