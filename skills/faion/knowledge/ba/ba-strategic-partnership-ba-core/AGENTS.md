# BA Strategic Partnership

## Summary

**One-sentence:** Produces a stance review naming what BA-as-partner means in this engagement — decision rights, escalation paths, value contracts.

**One-paragraph:** Produces a stance review naming what BA-as-partner means in this engagement — decision rights, escalation paths, value contracts. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Engagement-renewal або new-engagement розмова з C-level, де BA треба позиціонувати як partner, а не requirements-gatherer.
- Multi-vendor програма, де BA accountability/consultancy boundary треба зафіксувати документально.
- Pivot у scope (наприклад, BA → product-strategy), де стара стanca застаріла.
- Внутрішній conflict між sponsor view (clerk-of-works) і BA view (thinking partner) — потрібен письмовий arbiter.

## Applies If (ALL must hold)

- BA is being inserted into a senior leadership conversation (board, exec, founder) where positioning matters.
- BA scope is contested — sponsor wants a 'requirements gatherer', BA wants strategic partnership.
- Engagement renewal where BA value contribution must be articulated.
- Multi-vendor program where BA accountability vs. consultancy boundary needs to be drawn.

## Skip If (ANY kills it)

- Tactical task-level work where strategic posture is irrelevant.
- Pure execution engagement where decision rights are already named elsewhere.
- BA role is junior / supporting — strategic stance does not apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Engagement brief / SOW | Markdown / contract | sponsor |
| Sponsor expectations note | Email / interview transcript | sponsor |
| BA self-assessed positioning | Markdown | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | T1 approach informs partnership boundaries |
| [[stakeholder-analysis]] | stakeholder power map shapes partnership stance |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-positioning-inputs` | haiku | Collect SOW, expectations, self-assessment. |
| `draft-stance-review` | opus | Synthesise narrative under conflicting signals. |
| `redline-and-iterate` | sonnet | Refine wording against sponsor feedback. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stance-review.md.j2` | Stance review skeleton: what BA-as-partner means here, decision rights, escalation. |
| `templates/stance-review.md` | Stance review skeleton: what BA-as-partner means here, decision rights, escalation. Generated from `templates/stance-review.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/partnership-charter.md.j2` | One-page partnership charter signed by BA + sponsor. |
| `templates/partnership-charter.md` | One-page partnership charter signed by BA + sponsor. Generated from `templates/partnership-charter.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/stance-review-schema.json` | JSON Schema draft-07 for the ba-stance-reviewer agent output (axes, auto_block, kill_criterion). |
| `templates/ba-frame.sh` | Helper that frames a stakeholder ask into 3 questions + strawman outcome JSON. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[ba-planning]]
- [[stakeholder-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/stance-review-schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "StanceReview",
  "description": "Output schema for ba-stance-reviewer agent. auto_block=true if any axis < 2 OR kill_criterion.score < 1.",
  "type": "object",
  "required": [
    "artifact_id",
    "stance_overall",
    "axes",
    "auto_block"
  ],
  "properties": {
    "artifact_id": {
      "type": "string"
    },
    "stance_overall": {
      "type": "string",
      "enum": [
        "order_taker",
        "mixed",
        "strategic_partner"
      ]
    },
    "axes": {
      "type": "object",
      "required": [
        "problem_clarity",
        "outcome_orientation",
        "evidence_grounding",
        "enterprise_scope",
        "partner_voice",
        "kill_criterion"
      ],
      "properties": {
        "problem_clarity": {
          "$ref": "#/definitions/axis"
        },
        "outcome_orientation": {
          "$ref": "#/definitions/axis"
        },
        "evidence_grounding": {
          "$ref": "#/definitions/axis"
        },
        "enterprise_scope": {
          "$ref": "#/definitions/axis"
        },
        "partner_voice": {
          "$ref": "#/definitions/axis"
        },
        "kill_criterion": {
          "$ref": "#/definitions/axis"
        }
      }
    },
    "linked_okr_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "auto_block": {
      "type": "boolean"
    },
    "block_reason": {
      "type": [
        "string",
        "null"
      ]
    }
  },
  "definitions": {
    "axis": {
      "type": "object",
      "required": [
        "score",
        "evidence_quote",
        "rewrite"
      ],
      "properties": {
        "score": {
          "type": "integer",
          "minimum": 0,
          "maximum": 5
        },
        "evidence_quote": {
          "type": "string",
          "description": "Verbatim quote from artifact"
        },
        "rewrite": {
          "type": "string",
          "description": "Strategic-partner rewrite tied to OKR"
        }
      }
    }
  }
}
```

### `templates/ba-frame.sh`

```bash
# Usage: ba-frame "add a CSV export to the dashboard"
# Requires: llm CLI (pip install llm llm-anthropic) and MODEL env var or default.
set -euo pipefail
: "${MODEL:=claude-opus-4-7}"
ASK="${*:?usage: ba-frame <one-line stakeholder ask>}"
llm -m "$MODEL" --no-stream <<EOF
You are a strategic BA. The stakeholder said: "$ASK".
Refuse to design a solution. Output strict JSON:
{
  "problem_hypothesis": "...",
  "framing_questions": ["q1","q2","q3"],
  "strawman_outcome": {"kpi":"...","delta":"...","horizon_months":0}
}
Rules: no solution proposals, no feature descriptions,
  each framing question must be open-ended,
  KPI must reference a real metric category (revenue, cost, NPS, time, error rate).
EOF
```
