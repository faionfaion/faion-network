# Outcome Based Roadmaps

## Summary

**One-sentence:** Produces an outcome-based roadmap spec (≤3 outcomes per quarter + opportunities → solutions → confidence + No-Date-Promises rule + reviewer cadence).

**Ефективно для:** Solopreneur PMs whose roadmap is a feature gantt with promised dates that miss by 200%, eroding stakeholder trust each cycle.

**One-paragraph:** Feature-gantt roadmaps lock the team to promised dates and lose the optionality that outcomes-first planning preserves. This methodology produces a roadmap built around outcomes (≤3 per quarter), with each outcome carrying opportunities → solutions → confidence levels and a No-Date-Promises rule (delivery windows by month-range, not exact dates). Output is consumed by stakeholder communication + OKR alignment + the launch-tier-decision-frame.

## Applies If (ALL must hold)

- Operator has quarter-bounded planning (≥1 quarter horizon).
- Stakeholders accept outcomes-first framing (not feature commitments).
- Operator can name 1-3 outcomes worth pursuing.
- Operator can publish a public roadmap surface.

## Skip If (ANY kills it)

- Operator forced to promise exact delivery dates (contracts) — use date-bound roadmap instead.
- No instrumented outcomes — outcome-based framing has nothing to anchor.
- Single-product operator with no stakeholders — roadmap is overkill, use OKRs alone.
- Pre-MVP — fix MVP scoping first.
- Pure execution phase with fully scoped and validated work — nothing left for the roadmap to hold open.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| quarter dates | ISO range | calendar |
| candidate outcomes | array | founder |
| instrumented metrics per outcome | object | analytics |
| public roadmap surface URL | URL | operator |
| not-doing list | list | strategy review |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/okr-setting` | Upstream — OKRs anchor outcomes. |
| `solo/product/product-manager/continuous-discovery` | Upstream — discovery feeds opportunities. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes with detector + repair | ~1100 |
| `content/04-procedure.xml` | essential | 6 step-by-step procedure | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end examples incl. a concrete churn quarter | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_roadmap_skeleton` | haiku | Template fill outcomes/opportunities. |
| `attach_confidence_per_solution` | sonnet | Bounded judgement on confidence per solution. |
| `stakeholder_comms_synthesis` | opus | Synthesis for stakeholder-facing comms. |

## Templates

| File | Purpose |
|---|---|
| `templates/outcome-based-roadmaps.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/outcome-based-roadmaps.md.j2` | Markdown skeleton with the required fields. |
| `templates/outcome-based-roadmaps.md` | Markdown skeleton with the required fields. Generated from `templates/outcome-based-roadmaps.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-outcome-based-roadmaps.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[okr-setting]] — related methodology.
- [[continuous-discovery]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.
- [[outcome-based-roadmaps-advanced]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/outcome-based-roadmaps.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/outcome-based-roadmaps.json",
  "title": "Outcome Based Roadmaps Output Contract",
  "type": "object",
  "required": [
    "quarter",
    "outcomes",
    "solutions",
    "public_url",
    "quarter_review",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "quarter": {
      "type": "string",
      "description": "yyyy-Qn"
    },
    "outcomes": {
      "type": "array",
      "description": "\u22643 outcome objects with target metrics + opportunities[]",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "solutions": {
      "type": "array",
      "description": "linked to opportunities with confidence + delivery_window_month_range",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "public_url": {
      "type": "string",
      "description": "stakeholder-facing URL"
    },
    "quarter_review": {
      "type": "object",
      "description": "shipped/slipped lists + adjustments"
    },
    "owner": {
      "type": "string",
      "description": "named owner"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "quarter": "sample-quarter",
  "outcomes": [
    {
      "k": "v"
    }
  ],
  "solutions": [
    {
      "k": "v"
    }
  ],
  "public_url": "sample-public_url",
  "quarter_review": {
    "k": "v"
  },
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
