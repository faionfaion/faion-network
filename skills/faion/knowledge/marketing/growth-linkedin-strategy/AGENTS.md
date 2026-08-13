# Growth LinkedIn Strategy

## Summary

**One-sentence:** Generates a B2B LinkedIn authority playbook-step (positioning → 3 post-types weekly → 10 daily replies → DM trigger) optimised for solo inbound-lead generation.

**Ефективно для:** Solo B2B operators and consultants whose LinkedIn presence currently looks like a résumé and produces zero inbound — needs the discipline pivot from posting to engagement.

**One-paragraph:** LinkedIn rewards consistency + reply-density, not broadcast frequency. This methodology produces a per-week playbook-step: positioning statement (one ICP, one pain, one outcome), a 3-post-types weekly rotation (story / how-to / carousel), 10 strangers-replied-to daily, and a DM trigger phrase that converts profile visits into inbound calls. Output is consumed by a content scheduler + reply queue.

## Applies If (ALL must hold)

- Buyers are B2B (SMB founder, exec, or operator).
- Solo operator owns the LinkedIn profile and can post 3x/week.
- Operator can commit 30 minutes/day to engagement.
- Positioning statement (one ICP + one pain + one outcome) is decided.

## Skip If (ANY kills it)

- Buyers are pure B2C — LinkedIn ROI is structurally lower; switch platform.
- Operator refuses to use first-person voice; LinkedIn rewards personal posts.
- Profile is corporate-account only — personal brand is the unlock.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| positioning statement (ICP + pain + outcome) | single sentence | founder decision |
| 3 post-type templates filled with example | markdown | internal swipe file |
| daily 30-min engagement slot | calendar block | self-managed |
| DM trigger phrase + CTA | string | founder decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-social-media-strategy` | Cross-platform PACE umbrella. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_story_post` | sonnet | Personal narrative shaping for ICP pain. |
| `score_top_posts` | haiku | Numeric ranking from analytics export. |
| `triage_dms` | opus | Lead-quality judgement on inbound. |

## Templates

| File | Purpose |
|---|---|
| `templates/growth-linkedin-strategy.json` | JSON Schema for the output contract. |
| `templates/growth-linkedin-strategy.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-growth-linkedin-strategy.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-social-media-strategy]] — PACE umbrella.
- [[growth-twitter-x-growth]] — adjacent platform discipline.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-linkedin-strategy.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/growth-linkedin-strategy.json",
  "title": "Growth LinkedIn Strategy Output Contract",
  "type": "object",
  "required": [
    "operator",
    "positioning",
    "post_rotation",
    "daily_engagement_quota",
    "dm_trigger",
    "kpi_set",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named LinkedIn account owner"
    },
    "positioning": {
      "type": "object",
      "description": "{icp, pain, outcome}"
    },
    "post_rotation": {
      "type": "array",
      "description": "\u22653 typed posts (story/how-to/carousel) for the next week",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "daily_engagement_quota": {
      "type": "integer",
      "description": "\u226510 strangers-replied-to per day"
    },
    "dm_trigger": {
      "type": "string",
      "description": "exact trigger phrase + CTA"
    },
    "kpi_set": {
      "type": "object",
      "description": "{profile_visits, qualified_dms, inbound_calls, conversion_rate}"
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
  "positioning": {
    "key": "value"
  },
  "post_rotation": [
    {
      "key": "value"
    }
  ],
  "daily_engagement_quota": 1,
  "dm_trigger": "sample-dm_trigger",
  "kpi_set": {
    "key": "value"
  },
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
