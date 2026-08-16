# Fine-tune Cost vs Prompt Decision

## Summary

**One-sentence:** Produces a one-page decision record (problem type, data volume, eval lift bar, $/inference target) that blocks bad fine-tune calls and routes the team to prompt + RAG + routing when the math says so.

**One-paragraph:** Teams over-reach for fine-tuning because the cost story is opaque. This methodology forces a one-page artefact with four numbers (training cost, hosting/inference $/k tokens, eval lift % vs prompt baseline, break-even volume) and a single recommendation: fine-tune, prompt-improve, RAG, route, or hybrid. The frame is intentionally narrow — engineers either justify with numbers or pick a cheaper path.

**Ефективно для:** ml-engineer kickoff gate, p7-llm-agent-developer cost reviews, FinOps challenges, RFC reviewers blocking ill-justified training spend, founders deciding the AI roadmap.

## Applies If (ALL must hold)

- A team is seriously considering fine-tuning a model for a production workload.
- A baseline (prompt-only) eval result exists for the workload.
- Inference volume (req/day) and unit cost ($/k tokens) for current provider are known.
- A named decision owner (eng manager or staff) will sign the record.

## Skip If (ANY kills it)

- No baseline eval — build evals before debating fine-tune.
- Research/exploration only, no production constraint — methodology overhead does not pay back.
- Compliance forces on-prem fine-tune — decision is pre-made.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Baseline eval score | float in [0,1] | eval harness |
| Daily request volume | int | analytics |
| Current $/k tokens | float | provider invoice |
| Candidate training set size | int (examples) | data lake |
| Lift bar (min Δscore to justify) | float in [0,1] | product owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[fine-tune-vs-prompt-decision-tree]]` | Sister methodology, more branches; this one is the artefact. |
| `[[fine-tune-vs-prompt-economic-model]]` | Spreadsheet for the math; this is the writeup. |
| `[[finetune-kickoff-checklist]]` | Run after this records "fine-tune". |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: lift bar declared, break-even shown, two-of-five strong-signals required, owner signs, expiry date | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision-record + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vibes-based pick, no break-even, no recheck date, hidden ops cost | ~600 |
| `content/05-examples.xml` | recommended | A worked decision: prompt-improve beats fine-tune at 50k req/day | ~600 |
| `content/06-decision-tree.xml` | essential | Pick-path tree | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Extract numbers from eval + invoice | haiku | Mechanical pull. |
| Compute break-even volume | sonnet | Arithmetic with care. |
| Draft recommendation narrative | sonnet | Bounded prose with citations. |
| Review against rules | opus | Cross-check; high stakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.schema.json` | JSON Schema for the artefact. |
| `templates/decision-record.md.j2` | Markdown skeleton (recommended writeup). |
| `templates/decision-record.md` | Markdown skeleton (recommended writeup). Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finetune-cost-vs-prompt-decision.py` | Validate the JSON record against schema + rules. | Before record is committed to the RFC log. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[fine-tune-vs-prompt-decision-tree]]`
- `[[fine-tune-vs-prompt-economic-model]]`
- external refs: OpenAI / Anthropic / Together fine-tune pricing pages, RAG vs FT recent benchmarks.

## Decision tree

The decision tree at `content/06-decision-tree.xml` routes: eval lift ≥ bar AND break-even ≤ 12 months AND data ≥ minimum → fine-tune; else prompt+RAG+routing; else skip.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-record.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ft-cost-prompt-decision",
  "title": "Fine-tune cost vs prompt decision record",
  "type": "object",
  "required": [
    "workload",
    "owner",
    "created_at",
    "recheck_at",
    "lift_bar",
    "baseline",
    "candidate",
    "break_even_months",
    "strong_signals",
    "recommendation"
  ],
  "additionalProperties": true,
  "properties": {
    "workload": {
      "type": "string",
      "minLength": 5
    },
    "owner": {
      "type": "string",
      "minLength": 2,
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
    "recheck_at": {
      "type": "string",
      "format": "date"
    },
    "lift_bar": {
      "type": "number",
      "minimum": 0.001,
      "maximum": 0.5
    },
    "baseline": {
      "type": "object",
      "required": [
        "score",
        "cost_per_k_tokens",
        "daily_volume"
      ],
      "properties": {
        "score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "cost_per_k_tokens": {
          "type": "number",
          "minimum": 0
        },
        "daily_volume": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "candidate": {
      "type": "object",
      "required": [
        "training_cost",
        "hosting_cost_per_k_tokens",
        "training_examples"
      ],
      "properties": {
        "training_cost": {
          "type": "number",
          "minimum": 0
        },
        "hosting_cost_per_k_tokens": {
          "type": "number",
          "minimum": 0
        },
        "training_examples": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "break_even_months": {
      "type": [
        "number",
        "null"
      ]
    },
    "strong_signals": {
      "type": "array",
      "items": {
        "enum": [
          "format-adherence",
          "latency-critical",
          "data-volume-5k+",
          "safety-policy-domain",
          "cost-amortises-12mo"
        ]
      },
      "uniqueItems": true
    },
    "recommendation": {
      "enum": [
        "fine-tune",
        "prompt-improve",
        "rag",
        "route",
        "hybrid"
      ]
    },
    "narrative": {
      "type": "string"
    }
  }
}
```
