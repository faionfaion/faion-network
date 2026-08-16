# Engagement Pattern Memory

## Summary

**One-sentence:** Produces a per-engagement memory file (repo conventions + reviewer preferences + deploy quirks + recurring traps + glossary + resolved questions) so freelancers juggling multiple clients don't re-learn each one every session.

**Ефективно для:** Freelancers with 2-3 active clients who keep spending the first hour of every session re-learning what they already knew last week.

**One-paragraph:** Generic pattern-memory leaks one client's conventions into another. This methodology pins a per-engagement memory file (one per active client / repo) updated after each session with structured sections (repo conventions, reviewer preferences, deploy quirks, recurring traps, glossary, resolved questions). Files are versioned, indexed, and surfaced to the LLM agent on session start. Output is consumed by daily-ship-rubric and pattern-memory.

## Applies If (ALL must hold)

- Contractor / freelancer with ≥2 active engagements.
- Each engagement has distinct repo conventions or reviewer preferences.
- Operator uses an LLM agent where pre-session context matters.
- Memory write discipline is realistic (10-15 min at session end).

## Skip If (ANY kills it)

- Single-client operator — generic pattern-memory suffices.
- Engagements with identical conventions — no separation value.
- Operator already maintains per-client docs elsewhere with no LLM gap.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| list of active engagements | array | operator |
| memory file location convention | path | operator |
| session-start hook | tool config | operator |
| session-end discipline | habit | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/pattern-memory` | Parent — engagement memory is a per-client variant. |
| `solo/sdd/sdd/mistake-memory` | Sibling — engagement-scoped mistakes feed back into client memory. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/engagement-pattern-memory.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/engagement-pattern-memory.md.j2` | Markdown skeleton with the required fields. |
| `templates/engagement-pattern-memory.md` | Markdown skeleton with the required fields. Generated from `templates/engagement-pattern-memory.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-engagement-pattern-memory.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[pattern-memory]] — related methodology.
- [[mistake-memory]] — related methodology.
- [[daily-ship-rubric]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/engagement-pattern-memory.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/engagement-pattern-memory.json",
  "title": "Engagement Pattern Memory Output Contract",
  "type": "object",
  "required": [
    "engagement_id",
    "memory_file_path",
    "repo_conventions",
    "reviewer_preferences",
    "deploy_quirks",
    "recurring_traps",
    "glossary",
    "resolved_questions",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "engagement_id": {
      "type": "string",
      "description": "client / repo identifier"
    },
    "memory_file_path": {
      "type": "string",
      "description": "path to memory.md"
    },
    "repo_conventions": {
      "type": "object",
      "description": "linting / naming / commit format"
    },
    "reviewer_preferences": {
      "type": "object",
      "description": "per-named-reviewer preferences"
    },
    "deploy_quirks": {
      "type": "array",
      "description": "non-obvious deploy gotchas",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "recurring_traps": {
      "type": "array",
      "description": "\u22651 trap with detector + fix",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "glossary": {
      "type": "object",
      "description": "client-specific terms"
    },
    "resolved_questions": {
      "type": "array",
      "description": "questions + resolution dates",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "owner": {
      "type": "string",
      "description": "named contractor"
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
  "engagement_id": "sample-engagement_id",
  "memory_file_path": "sample-memory_file_path",
  "repo_conventions": {
    "k": "v"
  },
  "reviewer_preferences": {
    "k": "v"
  },
  "deploy_quirks": [
    {
      "k": "v"
    }
  ],
  "recurring_traps": [
    {
      "k": "v"
    }
  ],
  "glossary": {
    "k": "v"
  },
  "resolved_questions": [
    {
      "k": "v"
    }
  ],
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
