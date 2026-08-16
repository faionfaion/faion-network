# Tweet Thread Launch Template

## Summary

**One-sentence:** Produces a 7-tweet launch-thread spec (hook → demo gif → problem → solve → price → CTA → social proof) tuned for indie-hacker X audiences and Product Hunt launch day.

**Ефективно для:** Indie hackers shipping on Product Hunt or solo launches who keep writing the launch thread on launch morning under pressure with no template discipline.

**One-paragraph:** The same 7-tweet shape outperforms ad-hoc launch threads by 3-5x on indie-hacker X. This template fixes the structure (hook, demo gif, problem, solve, price, CTA, social proof), enforces a tested-hook-variant rule, requires a real demo gif (not a screenshot), and refuses launches without ≥1 pre-launch social-proof quote. Output is a 7-tweet draft consumed by the launch scheduler.

## Applies If (ALL must hold)

- A real product (paid or free with email capture) is ready to launch.
- A demo gif or short video (<30s) exists showing the core use.
- Pricing decision is final.
- At least one social-proof quote (early customer or testing user) is on file.

## Skip If (ANY kills it)

- No product to launch yet — write distribution-first idea-validation post instead.
- Demo gif absent — film one before threading; static screenshots underperform.
- Product is a hard-B2B sale where X is not the buyer channel.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| product URL + one-liner | URL + string | founder decision |
| demo gif (<30s, 1080p, captions baked in) | gif/mp4 | internal video |
| pricing decision (final) | string | founder decision |
| ≥1 social-proof quote (permission logged) | string + handle | social-proof-harvest output |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/marketing/swipe-file-tweet-hooks` | Hook variants source. |
| `solo/marketing/social-proof-harvest` | Quote source with consent. |

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
| `draft_3_hook_variants` | sonnet | Per-launch creative variants. |
| `score_hook_against_swipe` | haiku | Bounded similarity scoring. |
| `review_launch_thread` | opus | Final pre-publish judgement. |

## Templates

| File | Purpose |
|---|---|
| `templates/tweet-thread-launch-template.json` | JSON Schema for the output contract. |
| `templates/tweet-thread-launch-template.md.j2` | Markdown skeleton with the required fields. |
| `templates/tweet-thread-launch-template.md` | Markdown skeleton with the required fields. Generated from `templates/tweet-thread-launch-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-tweet-thread-launch-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[swipe-file-tweet-hooks]] — hook bank.
- [[social-proof-harvest]] — quote source.
- [[twitter-x-monetization-thread-to-product]] — funnel after launch.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tweet-thread-launch-template.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/tweet-thread-launch-template.json",
  "title": "Tweet Thread Launch Template Output Contract",
  "type": "object",
  "required": [
    "launch_id",
    "operator",
    "tweets",
    "demo_gif_url",
    "hook_variants_tested",
    "social_proof_quote",
    "scheduled_for",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "launch_id": {
      "type": "string",
      "description": "kebab-case slug"
    },
    "operator": {
      "type": "string",
      "description": "named launcher"
    },
    "tweets": {
      "type": "array",
      "description": "exactly 7 tweets with id + text + media",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "demo_gif_url": {
      "type": "string",
      "description": "<30s gif/mp4 URL"
    },
    "hook_variants_tested": {
      "type": "array",
      "description": "\u22653 variants with pre-launch impressions",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "social_proof_quote": {
      "type": "object",
      "description": "{quote, handle, consent_logged_at}"
    },
    "scheduled_for": {
      "type": "string",
      "description": "ISO timestamp",
      "format": "date-time"
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
  "launch_id": "sample-launch_id",
  "operator": "sample-operator",
  "tweets": [
    {
      "key": "value"
    }
  ],
  "demo_gif_url": "sample-demo_gif_url",
  "hook_variants_tested": [
    {
      "key": "value"
    }
  ],
  "social_proof_quote": {
    "key": "value"
  },
  "scheduled_for": "2026-05-23T12:00:00Z",
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
