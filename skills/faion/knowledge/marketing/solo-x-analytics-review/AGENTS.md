# Solo X Analytics Review

## Summary

**One-sentence:** Produces a 20-minute weekly X analytics report (5 fixed metrics + 3x-baseline outlier rule + one named next-week experiment) for indie audience growth.

**Ефективно для:** Indie operators using X as the primary audience channel where 'engagement isn't compounding' because there's no weekly diagnostic rhythm and the wrong metrics get tracked.

**One-paragraph:** `plausible-analytics` covers site traffic, not platform analytics. An indie hacker using X as the primary audience channel needs a specialised weekly review that surfaces what kind of post the algorithm is rewarding for THEM right now, separates outliers from baseline, and converts the review into exactly one named experiment for the following week. This methodology fixes the five metrics (impressions, profile visits, follows, replies-from-strangers, link clicks), the outlier-detection rule (≥3x trailing-4-week median), and the experiment-naming convention.

## Applies If (ALL must hold)

- X / Twitter is the primary audience channel.
- Operator posts at least 4 times/week.
- There are at least 4 weeks of data to compare against.
- Operator wants audience-growth or product-pipeline outcomes (not vanity follows).

## Skip If (ANY kills it)

- Operator posts <4 times/week — sample size too small.
- X is a secondary channel — invest review time elsewhere.
- Goal is vanity follows; this rubric will reject the metric.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| X analytics CSV/JSON export (last 4 weeks) | csv | X analytics dashboard |
| trailing-4-week median per metric | computed table | self-managed |
| posting log with timestamps + hooks | list | internal log |
| named operator (single account owner) | name + handle | founder |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/marketing/single-operator-funnel-rubric` | Adjacent solo metrics rhythm. |
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Growth playbook this review feeds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | essential | One worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `compute_outliers` | haiku | Deterministic 3x-baseline filter. |
| `draft_next_week_experiment` | sonnet | Hypothesis + variable + success metric. |
| `review_qualified_followers` | opus | Quality judgement on follower mix. |

## Templates

| File | Purpose |
|---|---|
| `templates/solo-x-analytics-review.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/solo-x-analytics-review.md.j2` | Markdown skeleton with the required fields. |
| `templates/solo-x-analytics-review.md` | Markdown skeleton with the required fields. Generated from `templates/solo-x-analytics-review.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-solo-x-analytics-review.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[single-operator-funnel-rubric]] — paired Friday rhythm.
- [[growth-twitter-x-growth]] — growth playbook downstream.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/solo-x-analytics-review.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/solo-x-analytics-review.json",
  "title": "Solo X Analytics Review Output Contract",
  "type": "object",
  "required": [
    "operator",
    "week_iso",
    "metrics",
    "trailing_4w_median",
    "outliers",
    "top_post",
    "bottom_post",
    "qualified_follower_pct",
    "next_week_experiment",
    "time_spent_min",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named X account owner"
    },
    "week_iso": {
      "type": "string",
      "description": "ISO week tag"
    },
    "metrics": {
      "type": "object",
      "description": "{impressions, profile_visits, net_followers, replies_from_strangers, link_clicks}"
    },
    "trailing_4w_median": {
      "type": "object",
      "description": "median per metric"
    },
    "outliers": {
      "type": "array",
      "description": "posts where impressions \u22653x median",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "top_post": {
      "type": "object",
      "description": "{url, hook, variable_observed}"
    },
    "bottom_post": {
      "type": "object",
      "description": "{url, hook}"
    },
    "qualified_follower_pct": {
      "type": "number",
      "description": "0..1"
    },
    "next_week_experiment": {
      "type": "object",
      "description": "{hypothesis, variable, success_metric}"
    },
    "time_spent_min": {
      "type": "integer",
      "description": "\u226420"
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
