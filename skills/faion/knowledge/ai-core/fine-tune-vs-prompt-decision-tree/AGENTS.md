# Fine-tune vs Prompt+RAG Decision Tree

## Summary

**One-sentence:** Produces an opinionated decision-record on WHEN fine-tune beats prompt + RAG + routing on the four axes (quality, cost, latency, maintenance), with revisit triggers, so engineers stop over-fine-tuning.

**One-paragraph:** Faion ships fine-tuning-openai-* (HOW) and lora-qlora (HOW). What is missing is the opinionated WHEN: a tree that, given quality gap, cost target, latency target, and ops budget, returns one of {prompt-improve, RAG, route, fine-tune, hybrid}. This methodology produces a one-page artefact with the four axis scores, the tree's decision, and the named revisit triggers (volume jumps 3x, new model ships at -50% price, eval drift). Sister to `[[finetune-cost-vs-prompt-decision]]` (numbers-first); this one is the decision graph.

**Ефективно для:** RFC review of any "let's fine-tune X" proposal, ml-engineer triage, CTO checkpoint before training spend, FinOps challenges, post-mortem after a fine-tune flop.

## Applies If (ALL must hold)

- Production workload has a measurable eval (score in [0,1]).
- Cost, quality, OR latency is below the product's target.
- A list of alternatives tried (better prompt, RAG, routing, distillation) exists OR will be filled.
- Owner is a named human, not a team alias.

## Skip If (ANY kills it)

- No eval set — build evals first.
- Compliance forces on-prem FT — decision is pre-made, document it instead.
- Research/exploration with no production users — methodology does not pay back.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval baseline | score in [0,1] | eval harness |
| Cost baseline | $/k tokens × volume | provider invoice |
| Latency target + current | ms | observability |
| Alternatives tried | list with eval lift each | engineering log |
| Maintenance burden estimate | qualitative + 1-3 score | eng manager |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[finetune-cost-vs-prompt-decision]]` | Numbers-first sibling. |
| `[[fine-tune-vs-prompt-economic-model]]` | Spreadsheet template. |
| `[[finetune-kickoff-checklist]]` | Downstream if FT is chosen. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4 axes scored, alternatives enumerated, ≥2-of-4 axes need FT, revisit triggers, owner | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: 1-axis decision, skipped RAG, no revisit triggers, anchoring on FT | ~600 |
| `content/05-examples.xml` | recommended | Worked decision: routing beats FT for a chat-classifier | ~600 |
| `content/06-decision-tree.xml` | essential | The actual decision graph | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Score the 4 axes | sonnet | Light judgment. |
| Enumerate alternatives | sonnet | Bounded knowledge. |
| Pick the path | opus | High-stakes synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.schema.json` | JSON Schema for the artefact. |
| `templates/decision-record.md.j2` | Markdown writeup skeleton. |
| `templates/decision-record.md` | Markdown writeup skeleton. Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tune-vs-prompt-decision-tree.py` | Validate the artefact against schema + rules. | Pre-commit in the RFC log. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[finetune-cost-vs-prompt-decision]]` — numbers sister
- `[[finetune-kickoff-checklist]]` — next step if FT is chosen
- `[[fine-tune-vs-prompt-economic-model]]` — spreadsheet model

## Decision tree

The decision tree at `content/06-decision-tree.xml` runs four axis checks: if 0 axes failing → no change; if quality alone → prompt-improve; if cost + latency → routing/distillation; if all four → fine-tune.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-record.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ft-vs-prompt-decision-tree",
  "title": "Fine-tune vs prompt decision tree artefact",
  "type": "object",
  "required": [
    "workload",
    "owner",
    "created_at",
    "axes",
    "alternatives_tried",
    "recommendation",
    "revisit_triggers"
  ],
  "additionalProperties": true,
  "properties": {
    "workload": {
      "type": "string"
    },
    "owner": {
      "type": "string",
      "not": {
        "enum": [
          "team",
          "everyone",
          "TBD"
        ]
      }
    },
    "created_at": {
      "type": "string",
      "format": "date"
    },
    "axes": {
      "type": "object",
      "required": [
        "quality",
        "cost",
        "latency",
        "maintenance"
      ],
      "properties": {
        "quality": {
          "type": "object",
          "required": [
            "score",
            "note"
          ],
          "properties": {
            "score": {
              "type": "integer",
              "minimum": 1,
              "maximum": 5
            },
            "note": {
              "type": "string",
              "minLength": 5
            }
          }
        },
        "cost": {
          "type": "object",
          "required": [
            "score",
            "note"
          ],
          "properties": {
            "score": {
              "type": "integer",
              "minimum": 1,
              "maximum": 5
            },
            "note": {
              "type": "string",
              "minLength": 5
            }
          }
        },
        "latency": {
          "type": "object",
          "required": [
            "score",
            "note"
          ],
          "properties": {
            "score": {
              "type": "integer",
              "minimum": 1,
              "maximum": 5
            },
            "note": {
              "type": "string",
              "minLength": 5
            }
          }
        },
        "maintenance": {
          "type": "object",
          "required": [
            "score",
            "note"
          ],
          "properties": {
            "score": {
              "type": "integer",
              "minimum": 1,
              "maximum": 5
            },
            "note": {
              "type": "string",
              "minLength": 5
            }
          }
        }
      }
    },
    "alternatives_tried": {
      "type": "array",
      "minItems": 4,
      "items": {
        "type": "object",
        "required": [
          "alt",
          "lift",
          "status"
        ],
        "properties": {
          "alt": {
            "enum": [
              "prompt-improve",
              "rag",
              "routing",
              "distillation"
            ]
          },
          "lift": {
            "type": [
              "number",
              "null"
            ]
          },
          "status": {
            "enum": [
              "tried",
              "untried",
              "skipped"
            ]
          }
        }
      }
    },
    "recommendation": {
      "enum": [
        "no-change",
        "prompt-improve",
        "rag",
        "routing",
        "distillation",
        "fine-tune",
        "hybrid"
      ]
    },
    "revisit_triggers": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "string",
        "minLength": 10
      }
    }
  }
}
```
