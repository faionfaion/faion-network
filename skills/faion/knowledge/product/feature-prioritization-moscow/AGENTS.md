# Feature Prioritization MoSCoW

## Summary

**One-sentence:** Produces a MoSCoW prioritisation config (Must / Should / Could / Won't buckets with explicit caps + cycle-bound scope + a single tiebreaker rule).

**Ефективно для:** Solopreneur PMs whose 'priority high' lists are all green and a feature freeze passes without anyone agreeing on the actual cut line.

**One-paragraph:** MoSCoW is widely used and widely abused — Must lists grow until every item is critical and the prioritisation collapses. This methodology enforces explicit caps (Must ≤ 60% of capacity, Won't bucket actively used, cycle-bound scope, a written tiebreaker rule) and gates a feature into Must only when it has a Definition of Done and rollback plan. Output is consumed by sprint planning + the launch-tier-decision-frame.

## Applies If (ALL must hold)

- Operator runs cycle-bound sprints / releases with a fixed capacity (story points or hours).
- Cross-stakeholder demands compete for the same scope.
- Operator can name capacity in concrete units.
- Tiebreaker rule is acceptable to all stakeholders.

## Skip If (ANY kills it)

- Pure flow / kanban shop with no cycle boundary — use stack-rank instead.
- Operator does not enforce caps — MoSCoW collapses to 'everything is Must'.
- Feature set < 10 items — overhead exceeds benefit.
- Replacing RICE / WSJF without capacity grounding — wrong tool.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| feature list | array | operator |
| cycle capacity (story points / hours) | number | team velocity |
| named tiebreaker rule | string | stakeholder agreement |
| DoD checklist | array | team standard |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/backlog-management` | Upstream — backlog feeds candidates. |
| `solo/product/product-manager/feature-prioritization-rice` | Sibling — RICE may rank within Must bucket. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `bucket_items` | haiku | Assign each item to Must/Should/Could/Won't. |
| `validate_caps` | sonnet | Check Must ≤ 60% of capacity, Won't non-empty. |
| `tiebreaker_application` | opus | Apply tiebreaker rule when capacity exceeded. |

## Templates

| File | Purpose |
|---|---|
| `templates/feature-prioritization-moscow.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/feature-prioritization-moscow.md.j2` | Markdown skeleton with the required fields. |
| `templates/feature-prioritization-moscow.md` | Markdown skeleton with the required fields. Generated from `templates/feature-prioritization-moscow.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/moscow-matrix.md.j2` | MoSCoW worksheet with per-requirement effort and capacity %. |
| `templates/moscow-matrix.md` | MoSCoW worksheet with per-requirement effort and capacity %. Generated from `templates/moscow-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-feature-prioritization-moscow.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[feature-prioritization-rice]] — related methodology.
- [[backlog-management]] — related methodology.
- [[mvp-scoping]] — related methodology.
- [[rice-for-one-person-cheatsheet]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-prioritization-moscow.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/feature-prioritization-moscow.json",
  "title": "Feature Prioritization MoSCoW Output Contract",
  "type": "object",
  "required": [
    "cycle_id",
    "capacity",
    "buckets",
    "tiebreaker_rule",
    "must_cap_pct",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "cycle_id": {
      "type": "string",
      "description": "sprint / release id"
    },
    "capacity": {
      "type": "number",
      "description": "story points or hours"
    },
    "buckets": {
      "type": "object",
      "description": "must / should / could / wont arrays"
    },
    "tiebreaker_rule": {
      "type": "string",
      "description": "named rule"
    },
    "must_cap_pct": {
      "type": "number",
      "description": "0-60"
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
