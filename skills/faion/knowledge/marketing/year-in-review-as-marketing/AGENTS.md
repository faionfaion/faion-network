# Year In Review As Marketing

## Summary

**One-sentence:** Year In Review As Marketing: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close'.

**One-paragraph:** Addresses the gap surfaced by 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close': How to turn the year-end close into a public retrospective that doubles as pipeline content — bridges ops + content marketing for solo operators. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a year in review as marketing artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Year-end close, що подвоюється як pipeline content.
- Solo operator або мікроагенція без окремого PR team.
- Bridges ops + content marketing в одному artefact.
- Versioned outcome review: чи retro справді приніс leads.

## Applies If (ALL must hold)

- task is an instance of 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working year in review as marketing artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Year In Review As Marketing |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/year-in-review-as-marketing.md.j2` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/year-in-review-as-marketing.md` | Markdown skeleton (5-line header) for the artefact body. Generated from `templates/year-in-review-as-marketing.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/year-in-review-as-marketing.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-year-in-review-as-marketing.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/`
- upstream playbook: `p3-technical-freelancer/Year-end tax, legal, and cash-flow close`
- pro/marketing/p3-technical-freelancer

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/year-in-review-as-marketing.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/year-in-review-as-marketing.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 3
    },
    "decision": {
      "type": "string",
      "minLength": 3
    },
    "rationale": {
      "type": "string",
      "minLength": 30
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```
