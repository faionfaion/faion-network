# Growth Twitter X Growth

## Summary

**One-sentence:** Generates a positioning-first X growth playbook-step (unique angle → 3-5 posts/day → 1-2 threads/week → 20-30 daily replies to larger accounts).

**Ефективно для:** Solo builders posting on X without a defined angle, getting baseline impressions, and frustrated that 'engagement isn't compounding'.

**One-paragraph:** X rewards angle + reply-density. This methodology produces a positioning-first growth step: a unique angle statement (what you say that nobody else says), a 3-5 posts/day baseline, 1-2 long threads per week, and 20-30 daily replies to accounts larger than yours. Output is a per-week schedule + reply target list consumed by the operator's posting tool.

## Applies If (ALL must hold)

- Operator commits ≥45 minutes/day to X.
- A unique-angle statement exists (one sentence: 'I post X that nobody else does').
- Operator can run at ≥3 posts/day for 90 days.
- Account is operator-owned (not a brand-owned company account).

## Skip If (ANY kills it)

- Buyers are not on X — pick a platform where they are.
- Operator refuses to share opinions (X rewards perspective, not safe content).
- Account is automated repost-only — algorithm suppresses pure aggregators.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| unique-angle statement (1 sentence) | string | founder decision |
| reply target list (20-30 accounts > 5x your size) | csv | manual curation |
| 3-5 daily posts queue with hook variants | queue | internal swipe file |
| thread topic backlog (≥6 weeks) | list | internal idea bank |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-social-media-strategy` | PACE umbrella. |
| `solo/marketing/swipe-file-tweet-hooks` | Hook variants source. |

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
| `draft_thread_outline` | sonnet | Structured argument with reveal arc. |
| `rank_reply_candidates` | haiku | Bounded scoring on a target list. |
| `audit_angle_drift` | opus | Cross-week judgement on positioning consistency. |

## Templates

| File | Purpose |
|---|---|
| `templates/growth-twitter-x-growth.json` | JSON Schema for the output contract. |
| `templates/growth-twitter-x-growth.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-growth-twitter-x-growth.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-social-media-strategy]] — PACE umbrella.
- [[swipe-file-tweet-hooks]] — hook bank.
- [[twitter-x-monetization-thread-to-product]] — monetization funnel.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-twitter-x-growth.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/growth-twitter-x-growth.json",
  "title": "Growth Twitter X Growth Output Contract",
  "type": "object",
  "required": [
    "operator",
    "unique_angle",
    "daily_post_target",
    "weekly_thread_target",
    "daily_reply_target",
    "reply_target_list",
    "kpi_set",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "operator": {
      "type": "string",
      "description": "named X account owner"
    },
    "unique_angle": {
      "type": "string",
      "description": "one-sentence positioning"
    },
    "daily_post_target": {
      "type": "integer",
      "description": "3-5"
    },
    "weekly_thread_target": {
      "type": "integer",
      "description": "1-2"
    },
    "daily_reply_target": {
      "type": "integer",
      "description": "20-30 to accounts >5x size"
    },
    "reply_target_list": {
      "type": "array",
      "description": "\u226520 accounts with handle + size_multiple",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "kpi_set": {
      "type": "object",
      "description": "{impressions, replies_from_strangers, link_clicks, qualified_follows}"
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
  "unique_angle": "sample-unique_angle",
  "daily_post_target": 1,
  "weekly_thread_target": 1,
  "daily_reply_target": 1,
  "reply_target_list": [
    {
      "key": "value"
    }
  ],
  "kpi_set": {
    "key": "value"
  },
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
