# Design Docs at Big Tech Companies

## Summary

**One-sentence:** Produces a design-docs reference report (per-company format + trigger rules + LLM-assistance limits + common mistakes) so solo and small-team operators pick the right design-doc shape for their scope.

**Ефективно для:** Solo devs cargo-culting Amazon 6-pagers for one-day features because they read a blog post once.

**One-paragraph:** Big-tech design-doc practices differ widely by company; copying the wrong format wastes a week per doc. This methodology surveys Google, Amazon, Uber, Spotify, Stripe, Netflix, Microsoft, Airbnb, Shopify, and Atlassian — covering document names (RFC / ERD / 6-Pager / ADR), review formats, and trigger rules. The core rules: write before coding; match weight to scope; always include 'do nothing' as an alternative. Output is consumed by design-docs-patterns.

## Applies If (ALL must hold)

- Operator considering which design-doc format to use.
- Cross-team or cross-org decision needs heavyweight review.
- Solo operator wants a 1-2 page version of big-tech practice.
- Onboarding new devs to the team's doc culture.

## Skip If (ANY kills it)

- One-day features — use a 1-paragraph note.
- Pure-content changes — no design rationale needed.
- Single-person hobby project with no future readership.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| decision scope | small | team | cross-org | PM |
| audience list | array | PM |
| review deadline | date | operator |
| template library | folder | repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/design-docs-patterns` | Sibling — patterns reference this survey. |
| `solo/sdd/sdd/architecture-decision-records` | Sibling — ADRs extract from design docs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
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
| `templates/design-docs-big-tech.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/design-docs-big-tech.md.j2` | Markdown skeleton with the required fields. |
| `templates/design-docs-big-tech.md` | Markdown skeleton with the required fields. Generated from `templates/design-docs-big-tech.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-design-docs-big-tech.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[design-docs-patterns]] — related methodology.
- [[architecture-decision-records]] — related methodology.
- [[living-documentation]] — related methodology.
- [[key-trends-summary]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/design-docs-big-tech.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/design-docs-big-tech.json",
  "title": "Design Docs at Big Tech Companies Output Contract",
  "type": "object",
  "required": [
    "doc_format",
    "scope",
    "audience",
    "page_budget",
    "review_deadline",
    "alternatives",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "doc_format": {
      "type": "string",
      "description": "RFC | ERD | 6-Pager | ADR | Custom"
    },
    "scope": {
      "type": "string",
      "description": "small | team | cross-org"
    },
    "audience": {
      "type": "array",
      "description": "named roles",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "page_budget": {
      "type": "integer",
      "description": "1..10"
    },
    "review_deadline": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    },
    "alternatives": {
      "type": "array",
      "description": "\u22652 including 'do nothing'",
      "items": {
        "type": "object"
      },
      "minItems": 1
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
  "doc_format": "sample-doc_format",
  "scope": "sample-scope",
  "audience": [
    {
      "k": "v"
    }
  ],
  "page_budget": 3,
  "review_deadline": "2026-05-23",
  "alternatives": [
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
