# Backlog Management

## Summary

**One-sentence:** Produces a DEEP-compliant backlog config (Ready / Upcoming / Backlog / Icebox buckets + type-tagged items + INVEST-compliant Ready entries + weekly grooming cadence).

**Ефективно для:** Solopreneur PMs whose backlog crossed ~80 items and degraded into a dumping ground because grooming lapsed and intake had no triage.

**One-paragraph:** Backlogs become dumping grounds when treated as storage rather than strategic tools. Without type tags and explicit promotion criteria, every item looks equal and planning degrades into opinion contests. This methodology applies DEEP (Detailed top, Emergent bottom, Estimated, Prioritized) and INVEST to enforce a 4-bucket model (Ready / Upcoming / Backlog / Icebox) with type-tagged items, Given/When/Then AC, and a 180-day archive rule. Output is consumed by sprint planning + roadmap reviews.

## Applies If (ALL must hold)

- Backlog has crossed ~80 items and signal is degrading; weekly grooming has lapsed.
- Multiple input streams (support, sales, eng, ideas) need triaging into a single ranked list.
- Refining the top of backlog into Ready items before sprint planning.
- Auditing backlog health (DEEP/INVEST compliance) before a quarterly review.

## Skip If (ANY kills it)

- Pre-PMF prototype phase with fewer than 20 items — a simple Trello/Notion list is sufficient.
- One-off project with fixed scope and end date — use a WBS or kanban board instead.
- Operator will not run weekly grooming; an unmaintained managed backlog is a longer dumping ground.
- Replacing prioritization frameworks — backlog management organises items; RICE/MoSCoW prioritises them. Run prioritisation first.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| backlog source-of-truth (tracker) | URL | operator |
| intake streams enumerated | array | operator |
| prioritisation method chosen | enum (RICE / MoSCoW / stack) | founder |
| weekly grooming calendar slot | calendar entry | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/feature-prioritization-rice` | Upstream prioritisation method. |
| `solo/product/product-manager/feature-prioritization-moscow` | Alternative upstream prioritisation method. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `intake_capture` | haiku | Add new items to Backlog bucket without evaluation. |
| `groom_ready_items` | sonnet | INVEST + AC refinement on top-of-backlog items. |
| `audit_health` | opus | DEEP/INVEST audit + archive synthesis. |

## Templates

| File | Purpose |
|---|---|
| `templates/backlog-management.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/backlog-management.md` | Markdown skeleton with the required fields. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-backlog-management.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[feature-prioritization-rice]] — related methodology.
- [[feature-prioritization-moscow]] — related methodology.
- [[mvp-scoping]] — related methodology.
- [[continuous-discovery]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/backlog-management.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/backlog-management.json",
  "title": "Backlog Management Output Contract",
  "type": "object",
  "required": [
    "backlog_url",
    "buckets",
    "ready_items",
    "type_distribution",
    "grooming_cadence",
    "prioritisation_method",
    "archive_proposal_count",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "backlog_url": {
      "type": "string",
      "description": "tracker URL"
    },
    "buckets": {
      "type": "object",
      "description": "ready/upcoming/backlog/icebox counts"
    },
    "ready_items": {
      "type": "array",
      "description": "items in Ready bucket with type, story, AC, estimate, source",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "type_distribution": {
      "type": "object",
      "description": "feature/bug/tech_debt/research counts"
    },
    "grooming_cadence": {
      "type": "object",
      "description": "day_of_week + duration_hours"
    },
    "prioritisation_method": {
      "type": "string",
      "description": "RICE | MoSCoW | stack"
    },
    "archive_proposal_count": {
      "type": "integer",
      "description": "items proposed for archive this grooming"
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
