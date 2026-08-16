# Value Proposition Design

## Summary

**One-sentence:** Produces a value-proposition-canvas spec (customer profile jobs/pains/gains + value map relievers/creators + alignment-gap list) so positioning is anchored on evidence, not adjective stacking.

**Ефективно для:** Solo founders whose pitch deck still describes 'faster, easier, better' instead of named customer jobs.

**One-paragraph:** Value propositions written without explicit customer-jobs anchoring drift to adjective stacking. This methodology pins each value-prop draft to Osterwalder's two-sided canvas: customer profile (jobs / pains / gains) on one side, value map (products / pain-relievers / gain-creators) on the other, with an explicit alignment-gap list for every mismatch. Output is consumed by launch-comms-kit and positioning iterations.

## Applies If (ALL must hold)

- Pre-launch positioning needs grounding in customer language.
- Pivoting positioning after low conversion or message rejection.
- Adjacent-segment expansion needs a fresh value map.
- Pitch deck or landing page draft missing customer-job anchor.
- One primary segment is named — a canvas covering several segments is split before it is run.

## Skip If (ANY kills it)

- When no customer interviews are accessible — canvas without evidence is fiction.
- Commodity products competing on price only.
- Internal tools with one captive user base.
- Only one side of the canvas can be sourced — a customer profile with no offer, or an offer with no interviews, is not a canvas.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| customer interview transcripts | files | user-interviews output |
| current product feature list | array | PM |
| competitor positioning grid | spec | researcher |
| draft value-prop statement (if any) | string | founder |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Upstream — interview data feeds the customer profile. |
| `solo/research/researcher/jobs-to-be-done` | Upstream — JTBD output feeds the 'jobs' field. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source, plus a skip-this-methodology fallback | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~1000 |
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
| `templates/value-proposition-design.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/value-proposition-design.md.j2` | Markdown skeleton with the required fields. |
| `templates/value-proposition-design.md` | Markdown skeleton with the required fields. Generated from `templates/value-proposition-design.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-value-proposition-design.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[user-interviews]] — related methodology.
- [[problem-validation-2026]] — related methodology.
- [[jobs-to-be-done]] — related methodology.
- [[use-case-mapping]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/value-proposition-design.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/value-proposition-design.json",
  "title": "Value Proposition Design Output Contract",
  "type": "object",
  "required": [
    "customer_profile",
    "value_map",
    "alignment_gaps",
    "value_prop_statement",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "customer_profile": {
      "type": "object",
      "description": "jobs + pains + gains arrays with citations"
    },
    "value_map": {
      "type": "object",
      "description": "products + pain_relievers + gain_creators arrays"
    },
    "alignment_gaps": {
      "type": "array",
      "description": "pain/gain ids with no matching reliever/creator",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "value_prop_statement": {
      "type": "string",
      "description": "\u2264140 chars; cites a named job"
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

### `templates/_smoke-test.json`

```json
{
  "customer_profile": {
    "k": "v"
  },
  "value_map": {
    "k": "v"
  },
  "alignment_gaps": [
    {
      "k": "v"
    }
  ],
  "value_prop_statement": "sample-value_prop_statement",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
