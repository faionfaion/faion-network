# Fine-tune Kickoff Checklist

## Summary

**One-sentence:** Produces a kickoff-gate checklist (eval baseline, data quality bar, hold-out slice, eval-during-training cadence, rollback plan) that fine-tune jobs MUST pass before training spend is approved.

**One-paragraph:** Every fine-tune-openai-* methodology covers HOW to train. None covers the kickoff gate: did we even confirm fine-tuning is the right tool, do we have eval + hold-out, does the data pass quality checks, is rollback wired in. This methodology produces the 12-item gate the team signs before sending the first training file. Single artefact: `kickoff-checklist.json` with all items marked yes/no/n-a + owner.

**Ефективно для:** ml-engineer pre-training gate, founder/CTO sign-off on training spend, FinOps challenges, the team running fine-tune for the third time and tired of avoidable failures.

## Applies If (ALL must hold)

- Team has decided to fine-tune (e.g. via `[[finetune-cost-vs-prompt-decision]]`).
- Training dataset candidate exists (≥1k examples).
- Eval set exists for the workload.
- A named owner (ml engineer) will run the job.

## Skip If (ANY kills it)

- Still in fine-tune vs prompt debate — run `[[finetune-cost-vs-prompt-decision]]` first.
- LoRA/QLoRA experiment with ≤ $10 budget — overhead > savings.
- Provider-hosted automated tuning where ALL checks are vendor-default — verify vendor defaults instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Decision record (FT recommended) | JSON | `[[finetune-cost-vs-prompt-decision]]` output |
| Training dataset | JSONL with `messages` per row | data lake |
| Eval set + baseline score | JSONL + float | eval harness |
| Rollback plan | text | runbook |
| Provider account + budget cap | account id + $ | finops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[finetune-cost-vs-prompt-decision]]` | Upstream — gates whether to even run this. |
| `[[eval-set-stratified-sampling-recipe]]` | Hold-out design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: decision record present, baseline score, hold-out 10%, dedup, PII scrub, train-loss watch, rollback wired | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the checklist + valid/invalid examples | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: no hold-out, leaky dedup, no rollback, eval-during-training missing | ~600 |
| `content/06-decision-tree.xml` | essential | Gate-pass tree | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Fill items from artefacts | haiku | Mechanical extraction. |
| Check hold-out is disjoint from train | sonnet | Bounded set ops. |
| Approve / reject narrative | opus | High-stakes summary. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kickoff-checklist.schema.json` | JSON Schema for the artefact. |
| `templates/kickoff-checklist.example.json` | Worked filled example. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finetune-kickoff-checklist.py` | Validate the checklist JSON against schema + rules. | Before training submission. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[finetune-cost-vs-prompt-decision]]` — upstream gate
- `[[eval-set-stratified-sampling-recipe]]` — hold-out design

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: decision record present, ≥1k examples, eval baseline known, owner named → run; else skip and resolve upstream gaps.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/kickoff-checklist.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ft-kickoff-checklist",
  "title": "Fine-tune kickoff checklist",
  "type": "object",
  "required": [
    "workload",
    "owner",
    "created_at",
    "decision_record_ref",
    "baseline",
    "dataset",
    "holdout",
    "training_plan",
    "rollback",
    "budget_cap_usd"
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
          "TBD"
        ]
      }
    },
    "created_at": {
      "type": "string",
      "format": "date"
    },
    "decision_record_ref": {
      "type": "string",
      "pattern": "^.+$"
    },
    "budget_cap_usd": {
      "type": "number",
      "minimum": 1
    },
    "baseline": {
      "type": "object",
      "required": [
        "score",
        "eval_harness_commit"
      ],
      "properties": {
        "score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "eval_harness_commit": {
          "type": "string",
          "minLength": 7
        }
      }
    },
    "dataset": {
      "type": "object",
      "required": [
        "total_examples",
        "dedup_dropped",
        "pii_audit_pass"
      ],
      "properties": {
        "total_examples": {
          "type": "integer",
          "minimum": 1000
        },
        "dedup_dropped": {
          "type": "integer",
          "minimum": 0
        },
        "pii_audit_pass": {
          "type": "boolean",
          "const": true
        }
      }
    },
    "holdout": {
      "type": "object",
      "required": [
        "fraction",
        "disjoint_from_train",
        "stratified"
      ],
      "properties": {
        "fraction": {
          "type": "number",
          "minimum": 0.1,
          "maximum": 0.3
        },
        "disjoint_from_train": {
          "type": "boolean",
          "const": true
        },
        "stratified": {
          "type": "boolean",
          "const": true
        }
      }
    },
    "training_plan": {
      "type": "object",
      "required": [
        "eval_cadence",
        "max_epochs"
      ],
      "properties": {
        "eval_cadence": {
          "enum": [
            "per-epoch",
            "every-n-steps"
          ]
        },
        "max_epochs": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10
        }
      }
    },
    "rollback": {
      "type": "object",
      "required": [
        "plan",
        "canary_metric",
        "dry_run_passed"
      ],
      "properties": {
        "plan": {
          "type": "string",
          "minLength": 50
        },
        "canary_metric": {
          "type": "string"
        },
        "dry_run_passed": {
          "type": "boolean"
        }
      }
    }
  }
}
```

### `templates/kickoff-checklist.example.json`

```json
{
  "workload": "support-classifier",
  "owner": "ml-eng@example.com",
  "created_at": "2026-05-22",
  "decision_record_ref": "rfc/2026-05-15-ft-support-classifier.json",
  "budget_cap_usd": 1000,
  "baseline": {
    "score": 0.78,
    "eval_harness_commit": "a1b2c3d"
  },
  "dataset": {
    "total_examples": 6500,
    "dedup_dropped": 420,
    "pii_audit_pass": true
  },
  "holdout": {
    "fraction": 0.1,
    "disjoint_from_train": true,
    "stratified": true
  },
  "training_plan": {
    "eval_cadence": "per-epoch",
    "max_epochs": 3
  },
  "rollback": {
    "plan": "Flip feature flag ft.support.v2=off to resume Sonnet prompt route. On-call owns. Tested in staging 2026-05-21.",
    "canary_metric": "support_classifier.f1_p95",
    "dry_run_passed": true
  }
}
```
