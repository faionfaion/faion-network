# Model Eval Control Bands

## Summary

**One-sentence:** Produces a versioned Model Eval Control Bands artefact — typed inputs + named owner + decisions traceable to source artefacts + last_reviewed gate.

**One-paragraph:** Eval methodologies define metrics but rarely how to set + maintain control bands so drift is detectable without false alarms. This methodology turns "Daily eval-suite run + drift triage" into a typed artefact: per-metric upper/lower bounds, an alerting policy, a named accountable owner, a rationale citing the input distributions and historical variance that justified the bounds, and a `last_reviewed` field that flags stale records on read. Every decision in the output cites the input artefact that justified it; batching multiple unrelated decisions through one pass is rejected.

**Ефективно для:** ML-engineer, що тримає daily eval-suite + drift triage і потребує зрозумілих, ревьюваних control bands замість туманних "anything off" alerts.

## Applies If (ALL must hold)

- Task is an instance of `role-ml-engineer/Daily eval-suite run + drift triage` or a near variant.
- All artefacts named in Prerequisites are available before starting.
- Output will be consumed by a downstream agent or human reviewer.
- Tier == geek.

## Skip If (ANY kills it)

- Team already maintains a working artefact for this gap — replace, do not duplicate.
- Greenfield prototype with no production users.
- Regulatory / compliance overrides in-methodology guidance.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval-suite metric definitions | YAML | eval repo |
| Historical metric series (≥30 days) | CSV / Parquet | observability |
| Owner registry | dir or doc | team handbook |
| Last-rotation policy | doc | governance |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/ml-engineer/model-evaluation` | Defines the metrics this bands. |
| `geek/ai/ml-engineer/llm-observability-stack` | Source of the historical series. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned + last_reviewed, traceable decision. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for the control-bands artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: invented inputs, "team" owner, post-hoc rationale, stale record, unbounded drift definition. | ~900 |
| `content/06-decision-tree.xml` | essential | Routes by input completeness + ownership presence. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_inputs_summary` | haiku | Template fill on bounded inputs. |
| `synthesize_decision` | sonnet | Per-instance judgement on band placement. |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|---|---|
| `templates/model-eval-control-bands.json` | JSON schema for the output contract. |
| `templates/model-eval-control-bands.md` | Markdown skeleton with required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-model-eval-control-bands.py` | Enforce output contract: artefact_id, owner non-plural, rationale references inputs, version + last_reviewed present. | After subagent return, before consumer reads. |

## Related

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `role-ml-engineer/Daily eval-suite run + drift triage`

## Decision tree

The tree at `content/06-decision-tree.xml` triages: are inputs typed + owner named + downstream consumer present? → produce control-bands record; otherwise → skip + escalate gap. Walk it before authoring so you don't ship an unowned drift policy.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/model-eval-control-bands.json`

```json
{
  "_purpose": "JSON Schema for the Model Eval Control Bands output contract.",
  "_consumes": "control-bands-record.json from subagent",
  "_produces": "validation report for validate-model-eval-control-bands.py",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/model-eval-control-bands",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed",
    "bands"
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
    "bands": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "metric",
          "lower",
          "upper"
        ],
        "properties": {
          "metric": {
            "type": "string"
          },
          "lower": {
            "type": "number"
          },
          "upper": {
            "type": "number"
          },
          "alerting": {
            "enum": [
              "warn",
              "page",
              "block"
            ]
          }
        }
      }
    }
  }
}
```
