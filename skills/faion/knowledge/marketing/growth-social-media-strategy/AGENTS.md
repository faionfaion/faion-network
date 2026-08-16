# Growth Social Media Strategy

## Summary

**One-sentence:** Produces a PACE strategy spec (Platform → Audience → Content → Engagement) that picks ≤2 primary platforms and locks one weekly atomization loop for a solo operator.

**Ефективно для:** Solo operators spread across five platforms with zero compounding traction — needs the discipline pivot from 'be everywhere' to 'one atomization loop'.

**One-paragraph:** Solo operators lose traction by trying to be everywhere. The PACE spec forces ≤2 primary platforms picked on Audience + Time-fit criteria, a weekly atomization loop (one long-form → 5 shorter cuts), and an engagement quota that scales with the size of the audience. Output is a 12-week strategy spec consumed by the content calendar + scheduler.

## Applies If (ALL must hold)

- Solo operator runs all content alone (no team).
- Operator has audience-growth or pipeline goals (not vanity reach).
- Operator can produce one long-form piece per week as the atomization seed.

## Skip If (ANY kills it)

- Operator has no clear ICP yet — pick ICP first, strategy after.
- Operator wants daily output on 4+ platforms — that's a content-team brief, not solo.
- Goal is paid-ads acquisition only — switch to paid-acquisition methodology.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| ICP definition (segment + pain + buying trigger) | single page | internal positioning doc |
| audience-fit matrix per platform candidate | scoring sheet | internal research |
| weekly time budget (hours) | integer | self-managed |
| long-form seed (blog / podcast / video) chosen | string | founder decision |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-linkedin-strategy` | Single-platform branch when LinkedIn chosen. |
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Single-platform branch when X chosen. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `score_platforms_for_icp` | sonnet | Per-instance judgement on fit. |
| `draft_atomization_plan` | sonnet | Long-form → 5-cut decomposition. |
| `review_for_burnout_risk` | opus | Cross-cutting capacity check. |

## Templates

| File | Purpose |
|---|---|
| `templates/growth-social-media-strategy.json` | JSON Schema for the output contract. |
| `templates/growth-social-media-strategy.md.j2` | Markdown skeleton with the required fields. |
| `templates/growth-social-media-strategy.md` | Markdown skeleton with the required fields. Generated from `templates/growth-social-media-strategy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/content-calendar.md.j2` | Markdown skeleton for a per-month cross-platform content calendar. |
| `templates/content-calendar.md` | Markdown skeleton for a per-month cross-platform content calendar. Generated from `templates/content-calendar.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-growth-social-media-strategy.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[growth-linkedin-strategy]] — LinkedIn-only branch.
- [[growth-twitter-x-growth]] — X-only branch.
- [[solo-content-calendar-template]] — downstream calendar.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-social-media-strategy.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/growth-social-media-strategy.json",
  "title": "Growth Social Media Strategy Output Contract",
  "type": "object",
  "required": [
    "operator",
    "primary_platforms",
    "atomization_loop",
    "weekly_time_budget_hours",
    "engagement_quota",
    "kpi_set",
    "review_cadence_weeks",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named owner of the strategy"
    },
    "primary_platforms": {
      "type": "array",
      "description": "\u22642 platforms with fit-score + audience size",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "atomization_loop": {
      "type": "object",
      "description": "{seed_type, weekly_cuts, channel_mapping}"
    },
    "weekly_time_budget_hours": {
      "type": "integer",
      "description": "\u226410 for solo"
    },
    "engagement_quota": {
      "type": "object",
      "description": "per-platform replies/day"
    },
    "kpi_set": {
      "type": "object",
      "description": "{audience_growth, qualified_engagement, pipeline_added}"
    },
    "review_cadence_weeks": {
      "type": "integer",
      "description": "default 12"
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
  "operator": "sample-operator",
  "primary_platforms": [
    {
      "key": "value"
    }
  ],
  "atomization_loop": {
    "key": "value"
  },
  "weekly_time_budget_hours": 1,
  "engagement_quota": {
    "key": "value"
  },
  "kpi_set": {
    "key": "value"
  },
  "review_cadence_weeks": 1,
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
