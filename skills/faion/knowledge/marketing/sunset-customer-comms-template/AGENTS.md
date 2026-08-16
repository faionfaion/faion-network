# Sunset Customer Comms Template

## Summary

**One-sentence:** Produces a versioned sunset-comms artefact (cause sentence, timeline, migration path, named owner) that closes the gap 'p1-solo-saas-builder/Pivot from failed v1 to v2'.

**Ефективно для:** Solo SaaS builders pivoting from a failed v1 to v2 who need a single auditable comms record instead of drafting bespoke announcements every time.

**One-paragraph:** Sunset/pivot comms are recurring for solo SaaS builders and almost always bespoke under pressure. This template codifies the comms artefact: one cause sentence in plain language, a published timeline, a migration path (to v2 OR a competitor OR a refund), and a single named owner. Output is versioned and replayable so the next pivot doesn't restart from scratch.

## Applies If (ALL must hold)

- A v1 product has paying users AND a v2 is decided (or shutdown is decided).
- Operator can name one accountable owner for the comms.
- A real cause sentence can be written in one honest line.
- A migration path (v2 / competitor / refund) is decided.

## Skip If (ANY kills it)

- No paying users on v1 — write a public farewell post instead.
- v2 decision not made — defer; comms without decision is noise.
- Pivot is silent / cancelled — no artefact needed.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| v1 paying-user roster | csv | billing export |
| v2 decision document (one page) | markdown | founder decision |
| cause sentence (one honest line) | string | founder decision |
| named comms owner | name + handle | founder |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/marketing/shutdown-customer-email-pack` | Paired shutdown variant when no v2. |

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
| `draft_announce_post` | sonnet | Cause + timeline + migration in one post. |
| `compute_migration_split` | haiku | Roster split by migration path. |
| `review_for_honesty` | opus | Catches corporate-speak. |

## Templates

| File | Purpose |
|---|---|
| `templates/sunset-customer-comms-template.json` | JSON Schema for the output contract. |
| `templates/sunset-customer-comms-template.md.j2` | Markdown skeleton with the required fields. |
| `templates/sunset-customer-comms-template.md` | Markdown skeleton with the required fields. Generated from `templates/sunset-customer-comms-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in example (passes the validator). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-sunset-customer-comms-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[shutdown-customer-email-pack]] — full-shutdown variant.
- [[social-proof-harvest]] — preserves goodwill quotes from migrating users.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/sunset-customer-comms-template.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/sunset-customer-comms-template.json",
  "title": "Sunset Customer Comms Template Output Contract",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "cause_sentence",
    "timeline",
    "migration_path",
    "communication_channels",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "description": "kebab-case slug"
    },
    "owner": {
      "type": "string",
      "description": "named human"
    },
    "cause_sentence": {
      "type": "string",
      "description": "one honest line"
    },
    "timeline": {
      "type": "object",
      "description": "{announce_date, migration_window_days, v1_off_date}"
    },
    "migration_path": {
      "type": "object",
      "description": "{primary: v2|competitor|refund, terms}"
    },
    "communication_channels": {
      "type": "array",
      "description": "email + in-app + status-page",
      "items": {
        "type": "object"
      },
      "minItems": 1
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
  "artefact_id": "sample-artefact_id",
  "owner": "sample-owner",
  "cause_sentence": "sample-cause_sentence",
  "timeline": {
    "key": "value"
  },
  "migration_path": {
    "key": "value"
  },
  "communication_channels": [
    {
      "key": "value"
    }
  ],
  "version": "sample-version",
  "last_reviewed": "2026-05-23"
}
```
