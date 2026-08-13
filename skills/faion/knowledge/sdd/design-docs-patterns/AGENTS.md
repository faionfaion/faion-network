# Design Docs Patterns

## Summary

**One-sentence:** Produces a design-doc spec (format selection rule + required sections + non-goals + ≥2 genuine alternatives + review deadline) so any feature >1 engineering day ships with a doc that captures the why.

**Ефективно для:** Solo devs whose 'I'll just code it' decisions keep getting re-debated three months later when someone asks why.

**One-paragraph:** Design docs collapse to no-doc or boilerplate copy when patterns aren't pinned. This methodology pins the format-selection rule (lightweight Google-style for team-scoped, heavier 6-pager / RFC for cross-org), required sections (context / goals / non-goals / proposed / alternatives / open questions), non-goals discipline, and the ≥2-genuine-alternatives bar. Output is consumed by ADR extraction and code-review-cycle.

## Applies If (ALL must hold)

- Feature implementation takes > 1 engineering day.
- Change has architectural or cross-cutting implications.
- Multiple alternatives genuinely exist.
- Decision will be revisited or questioned.

## Skip If (ANY kills it)

- Pure-copy changes with no logic.
- Trivial bug fixes with clear root cause.
- Decisions reversible inside a single PR.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| decision title | string | author |
| scope classification | small | team | cross-org | PM |
| alternatives shortlist | array | author |
| review audience list | array | PM |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/design-docs-big-tech` | Sibling — big-tech survey informs format selection. |
| `solo/sdd/sdd/architecture-decision-records` | Downstream — ADRs extract from accepted design docs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
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
| `templates/design-docs-patterns.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/design-docs-patterns.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-design-docs-patterns.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[design-docs-big-tech]] — related methodology.
- [[architecture-decision-records]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[living-documentation]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/design-docs-patterns.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/design-docs-patterns.json",
  "title": "Design Docs Patterns Output Contract",
  "type": "object",
  "required": [
    "doc_id",
    "title",
    "scope",
    "format",
    "sections",
    "non_goals",
    "alternatives",
    "review_deadline",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "doc_id": {
      "type": "string",
      "description": "stable id"
    },
    "title": {
      "type": "string",
      "description": "doc title"
    },
    "scope": {
      "type": "string",
      "description": "small | team | cross-org"
    },
    "format": {
      "type": "string",
      "description": "Google-lite | Amazon-6-pager | Uber-RFC | Stripe-ERD"
    },
    "sections": {
      "type": "object",
      "description": "required sections populated"
    },
    "non_goals": {
      "type": "array",
      "description": "\u22651 non-goal",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "alternatives": {
      "type": "array",
      "description": "\u22652 genuine",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "review_deadline": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    },
    "owner": {
      "type": "string",
      "description": "named author"
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
  "doc_id": "sample-doc_id",
  "title": "sample-title",
  "scope": "sample-scope",
  "format": "sample-format",
  "sections": {
    "k": "v"
  },
  "non_goals": [
    {
      "k": "v"
    }
  ],
  "alternatives": [
    {
      "k": "v"
    }
  ],
  "review_deadline": "2026-05-23",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
