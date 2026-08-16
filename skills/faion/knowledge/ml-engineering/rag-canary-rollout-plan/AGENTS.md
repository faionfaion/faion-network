# RAG Canary Rollout Plan

## Summary

**One-sentence:** Produces a RAG-feature canary rollout plan — fixed 1/5/25/100 curve, golden-eval gate per step, sampled online quality scoring, 60s kill switch.

**One-paragraph:** RAG quality regresses in ways that latency and error-rate canaries do not see. This methodology fixes the canary curve at 1% (24h hold) → 5% (24h) → 25% (48h) → 100%, gates each step with a golden-eval pass and online rubric-based quality scoring (5-10% sampled, ≥200 samples/hour during the 5% step), and enforces a ≤60-second kill switch by atomic in-memory routing flip (no deploy). Output: a versioned rollout-plan + per-step gate result + online-quality event + rollback receipt — all typed against the schema so step promotion can be automated.

**Ефективно для:** ML-engineer / SRE, що випускає новий retriever / prompt / model у RAG-пайплайн і хоче ловити quality drop без чекання на user complaints.

## Applies If (ALL must hold)

- RAG feature with measurable answer-quality rubric (groundedness, relevance, completeness, no-hallucination).
- Gateway can atomically flip versions in ≤60 seconds (in-memory routing table).
- Golden eval suite exists and is updated within the last 90 days.
- LLM-as-judge or human review queue available for online sampling.

## Skip If (ANY kills it)

- No measurable quality rubric — return to rubric design first.
- Gateway requires a deploy or cache warm-up to flip versions (rebuild gateway first).
- Internal-only tool with no SLO and no users (no canary needed).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Versioned retriever + prompt + reranker config | git sha | repo |
| Golden eval suite (≥200 items) | JSONL | eval repo |
| Online rubric definition with weights | YAML | rubric repo |
| Atomic-flip gateway | service | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/ml-engineer/rag-pipeline-design` | Defines the pipeline shape that is being rolled out. |
| `geek/ai/ml-engineer/rag-evaluation` | Provides the eval that gates each step. |
| `geek/ai/ml-engineer/llm-observability-stack` | Source of the online-quality sink. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: fixed curve, golden eval per step, sampled online quality, 60s kill switch, atomic flip. | ~900 |
| `content/02-output-contract.xml` | essential | Schema for rollout plan + per-step gate result + online quality event + rollback receipt. | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: slow kill switch, sampling too thin, stale eval, skipped steps, no kill-switch rehearsal, judge drift. | ~900 |
| `content/04-procedure.xml` | medium | Steps: plan → golden eval pass at 1% → 24h hold → online sample → promote/rollback → repeat at 5/25/100. | ~800 |
| `content/06-decision-tree.xml` | essential | Routes by gate-state and quality-band at each step. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft-rollout-plan` | sonnet | Schema fill from prior templates. |
| `score-sampled-traffic` | haiku | LLM-as-judge for cheap online scoring. |
| `decide-rollback` | opus | Cross-signal synthesis on borderline cases. |

## Templates

| File | Purpose |
|---|---|
| `templates/rollout-plan.json` | JSON schema for the rollout plan. |
| `templates/rollout-plan.md.j2` | Markdown skeleton for the human-readable plan. |
| `templates/rollout-plan.md` | Markdown skeleton for the human-readable plan. Generated from `templates/rollout-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/step-gate-result.json` | Per-step gate result schema. |
| `templates/rollback-receipt.json` | Rollback receipt schema (records the 60s contract). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-rag-canary-rollout-plan.py` | Validate the plan: 4 steps, sample_rate ≥0.05 during 5%, kill_switch criteria ≥4, atomic flip = true. | Pre-commit + per-step gate. |

## Related

- [[rag-pipeline-design]]
- [[rag-evaluation]]
- [[retrieval-drift-alerting-recipe]]
- [[router-shadow-deploy-protocol]]

## Decision tree

The tree at `content/06-decision-tree.xml` enumerates the per-step gate path: golden eval pass + online quality within band + latency p95 within +20% → promote; else → rollback within 60s. Walk it before promoting any step; never skip the hold.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rollout-plan.json`

```json
{
  "_purpose": "JSON Schema for the RAG canary rollout plan.",
  "_consumes": "rollout-plan.json from subagent",
  "_produces": "validation report for validate-rag-canary-rollout-plan.py",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/rag-canary-rollout-plan",
  "type": "object",
  "required": [
    "feature_id",
    "target_version",
    "baseline_version",
    "steps",
    "golden_eval",
    "online_quality",
    "kill_switch"
  ],
  "properties": {
    "feature_id": {
      "type": "string",
      "minLength": 1
    },
    "target_version": {
      "type": "string",
      "minLength": 1
    },
    "baseline_version": {
      "type": "string",
      "minLength": 1
    },
    "steps": {
      "type": "array",
      "minItems": 4,
      "maxItems": 4,
      "items": {
        "type": "object",
        "required": [
          "percent",
          "hold_hours",
          "min_samples"
        ],
        "properties": {
          "percent": {
            "enum": [
              1,
              5,
              25,
              100
            ]
          },
          "hold_hours": {
            "type": "integer",
            "minimum": 12
          },
          "min_samples": {
            "type": "integer",
            "minimum": 100
          }
        }
      }
    },
    "golden_eval": {
      "type": "object",
      "required": [
        "suite_id",
        "thresholds"
      ],
      "properties": {
        "suite_id": {
          "type": "string"
        },
        "thresholds": {
          "type": "object",
          "required": [
            "primary_no_regression",
            "secondary_max_regression_pct",
            "p95_latency_max_delta_pct"
          ],
          "properties": {
            "primary_no_regression": {
              "type": "boolean",
              "const": true
            },
            "secondary_max_regression_pct": {
              "type": "number",
              "maximum": 5
            },
            "p95_latency_max_delta_pct": {
              "type": "number",
              "maximum": 20
            }
          }
        }
      }
    },
    "online_quality": {
      "type": "object",
      "required": [
        "rubric_id",
        "sample_rate",
        "floor_composite_score"
      ],
      "properties": {
        "rubric_id": {
          "type": "string"
        },
        "sample_rate": {
          "type": "number",
          "minimum": 0.05,
          "maximum": 0.2
        },
        "floor_composite_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      }
    },
    "kill_switch": {
      "type": "object",
      "required": [
        "criteria",
        "atomic_flip",
        "rehearsed_within_days"
      ],
      "properties": {
        "criteria": {
          "type": "array",
          "minItems": 4,
          "items": {
            "type": "string"
          }
        },
        "atomic_flip": {
          "type": "boolean",
          "const": true
        },
        "rehearsed_within_days": {
          "type": "integer",
          "maximum": 90
        }
      }
    }
  }
}
```

### `templates/step-gate-result.json`

```json
{
  "_purpose": "Schema for the per-step canary gate result.",
  "_consumes": "step-gate-result.json from rollout runner",
  "_produces": "evidence record consumed by promote/rollback logic",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/rag-canary-step-gate-result",
  "type": "object",
  "required": [
    "step_id",
    "percent",
    "golden_pass",
    "composite_score",
    "p95_latency_delta_pct",
    "decision"
  ],
  "properties": {
    "step_id": {
      "type": "string"
    },
    "percent": {
      "enum": [
        1,
        5,
        25,
        100
      ]
    },
    "golden_pass": {
      "type": "boolean"
    },
    "composite_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "p95_latency_delta_pct": {
      "type": "number"
    },
    "decision": {
      "enum": [
        "promote",
        "hold",
        "rollback"
      ]
    }
  }
}
```

### `templates/rollback-receipt.json`

```json
{
  "_purpose": "Schema for the rollback receipt \u2014 records the \u226460s contract.",
  "_consumes": "rollback-receipt.json from gateway",
  "_produces": "evidence of meeting kill-switch SLO",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "0 \u2014 schema-only",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/rag-canary-rollback-receipt",
  "type": "object",
  "required": [
    "feature_id",
    "from_version",
    "to_version",
    "triggered_at",
    "completed_within_seconds",
    "reason"
  ],
  "properties": {
    "feature_id": {
      "type": "string"
    },
    "from_version": {
      "type": "string"
    },
    "to_version": {
      "type": "string"
    },
    "triggered_at": {
      "type": "string",
      "format": "date-time"
    },
    "completed_within_seconds": {
      "type": "integer",
      "maximum": 60
    },
    "reason": {
      "type": "string"
    }
  }
}
```
