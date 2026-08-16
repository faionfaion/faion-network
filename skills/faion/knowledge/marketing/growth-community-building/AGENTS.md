# Growth Community Building

## Summary

**One-sentence:** Generates a four-stage community launch playbook-step (Seed 50 → Nurture rituals → Scale pairing → Monetize) with pre-seeded conversations and one platform locked in.

**Ефективно для:** Solo founders launching a Discord/Slack/Circle community as a growth or retention lever, who tend to over-invite before seeding any conversation.

**One-paragraph:** Most indie communities die because the founder invites 500 people into an empty room. This methodology produces a four-stage launch step — Seed (50 hand-picked + 5-10 planted conversations) → Nurture (3 rituals: daily standup, weekly office hours, monthly AMA) → Scale (member-to-member pairing) → Monetize (community as product feature). It rejects multi-platform launches, requires a named host, and enforces a 'no empty room' rule before any public invitation wave.

## Applies If (ALL must hold)

- Community is positioned as a product or retention lever, not a vanity channel.
- One platform is chosen (Discord OR Slack OR Circle OR Telegram — not multiple).
- A named host is committed to ≥3 rituals/week.
- Founder can hand-pick the first 50 seed members.

## Skip If (ANY kills it)

- Founder wants to launch on three platforms simultaneously — community fragments.
- No human can be the public face — agent-only communities read hollow.
- Product has <100 paying users AND community is treated as 'marketing'.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| platform pick (Discord/Slack/Circle/Telegram) | string | founder decision |
| seed list of 50 hand-picked names + handles | csv | founder rolodex |
| named host with calendar holds for 3 rituals/week | name + schedule | founder or co-host |
| 5-10 pre-written conversation prompts | list of strings | internal content bank |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-social-media-strategy` | Audience-source layer feeding seed list. |

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
| `draft_welcome_kit` | sonnet | Branded language + guidelines + ritual prompts. |
| `score_community_health` | haiku | Deterministic metric tally. |
| `review_moderation_edge_cases` | opus | Human-context judgement at scale. |

## Templates

| File | Purpose |
|---|---|
| `templates/growth-community-building.json` | JSON Schema for the output contract. |
| `templates/growth-community-building.md.j2` | Markdown skeleton with the required fields. |
| `templates/growth-community-building.md` | Markdown skeleton with the required fields. Generated from `templates/growth-community-building.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/community-guidelines.md.j2` | Markdown skeleton for a community's published guidelines page. |
| `templates/community-guidelines.md` | Markdown skeleton for a community's published guidelines page. Generated from `templates/community-guidelines.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/launch-checklist.md.j2` | Community launch checklist scaffolding for the Seed → Nurture → Scale → Monetize stages. |
| `templates/launch-checklist.md` | Community launch checklist scaffolding for the Seed → Nurture → Scale → Monetize stages. Generated from `templates/launch-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-growth-community-building.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[growth-social-media-strategy]] — seed audience funnel.
- [[social-proof-harvest]] — testimonial source from active members.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/growth-community-building.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/growth-community-building.json",
  "title": "Growth Community Building Output Contract",
  "type": "object",
  "required": [
    "community_id",
    "host",
    "platform",
    "seed_members",
    "planted_conversations",
    "rituals",
    "guidelines",
    "health_targets",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "community_id": {
      "type": "string",
      "description": "kebab-case slug"
    },
    "host": {
      "type": "string",
      "description": "named human accountable for rituals"
    },
    "platform": {
      "type": "string",
      "description": "discord|slack|circle|telegram"
    },
    "seed_members": {
      "type": "array",
      "description": "\u226550 entries with name + handle + reason",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "planted_conversations": {
      "type": "array",
      "description": "5-10 conversation prompts with author",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "rituals": {
      "type": "array",
      "description": "\u22653 with cadence + owner + agenda",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "guidelines": {
      "type": "string",
      "description": "community guidelines markdown"
    },
    "health_targets": {
      "type": "object",
      "description": "{dau_mau: 0.25, weekly_active_members_pct: 0.4}"
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
  "community_id": "sample-community_id",
  "host": "sample-host",
  "platform": "value",
  "seed_members": [
    {
      "key": "value"
    }
  ],
  "planted_conversations": [
    {
      "key": "value"
    }
  ],
  "rituals": [
    {
      "key": "value"
    }
  ],
  "guidelines": "sample-guidelines",
  "health_targets": {
    "key": "value"
  },
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
