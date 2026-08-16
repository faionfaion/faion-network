# Launch Comms Kit Template

## Summary

**One-sentence:** Produces a launch comms kit spec (one tweet thread + one PH copy + one mailing-list draft + one HN show-post + one changelog entry) sharing a single positioning sentence.

**Ефективно для:** Solopreneurs shipping a launch event (PH / HN / Show / mailing list) who scatter ad-hoc copy across channels and end up with five different positioning sentences.

**One-paragraph:** A launch event hits 4-6 channels (PH, HN, mailing list, X thread, changelog, optional podcast) and each channel begs a different copy shape. Without a kit template, the founder writes each piece in isolation and ships five different positioning sentences. This methodology produces a spec where ONE positioning sentence anchors all channel-specific drafts, a launch-day timeline binds the publishes, and a post-launch retro slot is pre-booked. Output is consumed by the launch-day operator and by the post-launch retro log.

## Applies If (ALL must hold)

- Operator is shipping a launch event with ≥3 channels.
- A single positioning sentence has been chosen and won't change mid-launch.
- Launch day is scheduled with a fixed window (12-72h).
- Operator has access to all channel accounts (PH, HN, X, mailing list).

## Skip If (ANY kills it)

- Soft-launch with one channel only — the kit is overkill.
- Operator does NOT have a single positioning sentence yet — fix positioning first.
- Launch is gated by review / approval not under operator control — defer kit until window confirmed.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| positioning sentence (≤140 chars) | string | founder |
| launch-day window | datetime range | calendar |
| channel list with credentials | object | operator |
| PH / HN account standing | boolean | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/launch-tier-decision-frame` | Upstream — decides which tier the launch is gunning for. |
| `solo/marketing/tweet-thread-launch-template` | Channel-specific copy for the X thread piece. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_channel_pieces` | haiku | Template-fill from positioning sentence per channel. |
| `positioning_consistency_check` | sonnet | Cross-channel comparison: do all 5 pieces share the same positioning sentence? |
| `launch_retro_synthesis` | opus | Post-launch outcome review across channels. |

## Templates

| File | Purpose |
|---|---|
| `templates/launch-comms-kit-template.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/launch-comms-kit-template.md.j2` | Markdown skeleton with the required fields. |
| `templates/launch-comms-kit-template.md` | Markdown skeleton with the required fields. Generated from `templates/launch-comms-kit-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-launch-comms-kit-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[launch-tier-decision-frame]] — related methodology.
- [[tweet-thread-launch-template]] — related methodology.
- [[shutdown-customer-email-pack]] — related methodology.
- [[launch-comms-kit-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/launch-comms-kit-template.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/launch-comms-kit-template.json",
  "title": "Launch Comms Kit Template Output Contract",
  "type": "object",
  "required": [
    "launch_name",
    "positioning_sentence",
    "launch_window",
    "channels",
    "publish_timeline",
    "retro_at",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "launch_name": {
      "type": "string",
      "description": "named launch"
    },
    "positioning_sentence": {
      "type": "string",
      "description": "\u2264140 chars canonical sentence"
    },
    "launch_window": {
      "type": "object",
      "description": "ISO start/end"
    },
    "channels": {
      "type": "object",
      "description": "per-channel draft objects (PH/HN/X/mail/changelog)"
    },
    "publish_timeline": {
      "type": "array",
      "description": "per-channel publish_at ISO datetimes",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "retro_at": {
      "type": "string",
      "description": "ISO datetime for T+7 retro"
    },
    "owner": {
      "type": "string",
      "description": "named human owner"
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
  "launch_name": "sample-launch_name",
  "positioning_sentence": "sample-positioning_sentence",
  "launch_window": {
    "k": "v"
  },
  "channels": {
    "k": "v"
  },
  "publish_timeline": [
    {
      "k": "v"
    }
  ],
  "retro_at": "sample-retro_at",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
