# Continuous Discovery

## Summary

**One-sentence:** Produces a continuous-discovery config (weekly user-touchpoint cadence + opportunity-solution-tree + assumption-test queue + decision log) so discovery stops being a quarterly event.

**Ефективно для:** Solopreneur PMs running ad-hoc discovery sprints and losing institutional memory between bursts because conversations live in scattered docs.

**One-paragraph:** Discovery is a habit, not a quarterly event. Without a weekly touchpoint cadence and a structured opportunity-solution-tree the operator loses signal between research bursts and re-derives the same insights every quarter. This methodology produces a config: weekly cadence (≥1 customer touchpoint), an opportunity-solution-tree (outcome → opportunities → solutions → assumption tests), a running assumption-test queue, and a decision log. Output is consumed by the backlog (feeds new items) + roadmap.

## Applies If (ALL must hold)

- Operator can run ≥1 customer touchpoint per week (≥30 min).
- Operator has access to a customer pool / waitlist / paying users.
- Operator owns the discovery output (writes back to backlog and roadmap).
- A named outcome / KPI is being pursued (not 'just looking').

## Skip If (ANY kills it)

- Pre-product phase with zero customers — use a research methodology like Mom Test instead.
- Operator cannot commit weekly touchpoint — discovery degenerates to noise.
- No named outcome / KPI — opportunities have nothing to anchor to.
- Discovery is delegated entirely to a third party (agency) — supervise via separate methodology.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| named outcome / KPI | string | founder |
| customer pool URL or list | URL | operator |
| touchpoint slot calendar | recurring event | calendar |
| discovery output destination (backlog/roadmap URL) | URL | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/product/product-manager/backlog-management` | Downstream — opportunities feed backlog items. |
| `solo/product/product-manager/outcome-based-roadmaps` | Downstream — outcomes anchor the tree. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `schedule_touchpoints` | haiku | Weekly slot scheduling, no judgement. |
| `update_opportunity_tree` | sonnet | Bounded judgement: graft new opportunities under outcomes. |
| `synthesise-assumption-tests` | opus | Cross-touchpoint synthesis on which assumptions to test next. |

## Templates

| File | Purpose |
|---|---|
| `templates/continuous-discovery.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/continuous-discovery.md.j2` | Markdown skeleton with the required fields. |
| `templates/continuous-discovery.md` | Markdown skeleton with the required fields. Generated from `templates/continuous-discovery.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-continuous-discovery.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[backlog-management]] — related methodology.
- [[outcome-based-roadmaps]] — related methodology.
- [[mvp-scoping]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/continuous-discovery.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/continuous-discovery.json",
  "title": "Continuous Discovery Output Contract",
  "type": "object",
  "required": [
    "outcome",
    "touchpoints",
    "opportunity_tree",
    "assumption_tests",
    "decision_log",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "outcome": {
      "type": "string",
      "description": "named outcome / KPI"
    },
    "touchpoints": {
      "type": "array",
      "description": "\u22651/week, each with date, customer_id, summary",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "opportunity_tree": {
      "type": "object",
      "description": "outcome \u2192 opportunities \u2192 solutions"
    },
    "assumption_tests": {
      "type": "array",
      "description": "\u22651 per opportunity, each falsifiable",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "decision_log": {
      "type": "array",
      "description": "\u22651/week, each with rationale + cited touchpoint ids",
      "items": {
        "type": "object"
      },
      "minItems": 1
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
