# Validation Paralysis Breaker

## Summary

**One-sentence:** Produces a forced-decision validation record (72h budget + ship-or-park verdict + named risk + falsification trigger) so indie hackers exit validation loops in days, not months.

**Ефективно для:** Indie hackers stuck in eternal validation who keep running 'one more interview' instead of shipping a paying-user test.

**One-paragraph:** The indie-hacker validation paralysis anti-pattern: endless interviews, surveys, and 'just one more landing page' before any user pays. This methodology pins a hard 72-hour validation budget, a named falsification trigger, and a forced ship-or-park verdict at budget end. Output is a decision-record consumed by mvp-scoping and launch-tier-decision-frame.

## Applies If (ALL must hold)

- Operator has been 'validating' for >2 weeks without a paying-user test.
- Hypothesis is testable inside a 3-week tweet-to-launch sprint.
- Operator can write a falsification trigger up-front.
- Tier solo or higher.

## Skip If (ANY kills it)

- Hypothesis requires multi-party / regulated launch.
- Operator hasn't yet articulated a hypothesis — use problem-validation-2026 first.
- Already-paying users exist for an adjacent product — use feature-discovery.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| one-line hypothesis | string | founder |
| falsification trigger statement | string | founder |
| 72h budget start | datetime | operator |
| named risk and mitigation | string | founder |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/problem-validation-2026` | Upstream — provides the hypothesis under test. |
| `solo/product/mvp-scoping` | Downstream — ship verdict triggers MVP scoping. |

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
| `templates/validation-paralysis-breaker.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/validation-paralysis-breaker.md.j2` | Markdown skeleton with the required fields. |
| `templates/validation-paralysis-breaker.md` | Markdown skeleton with the required fields. Generated from `templates/validation-paralysis-breaker.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-validation-paralysis-breaker.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[problem-validation-2026]] — related methodology.
- [[mvp-scoping]] — related methodology.
- [[single-interview-fast-loop-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/validation-paralysis-breaker.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/validation-paralysis-breaker.json",
  "title": "Validation Paralysis Breaker Output Contract",
  "type": "object",
  "required": [
    "hypothesis",
    "falsification_trigger",
    "budget_start",
    "budget_end",
    "verdict",
    "named_risk",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "hypothesis": {
      "type": "string",
      "description": "one-line statement"
    },
    "falsification_trigger": {
      "type": "string",
      "description": "observable that would falsify"
    },
    "budget_start": {
      "type": "string",
      "description": "ISO datetime",
      "format": "date-time"
    },
    "budget_end": {
      "type": "string",
      "description": "budget_start + 72h",
      "format": "date-time"
    },
    "verdict": {
      "type": "string",
      "description": "ship | park | extend-once"
    },
    "named_risk": {
      "type": "string",
      "description": "the risk being taken or carried"
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
  "hypothesis": "sample-hypothesis",
  "falsification_trigger": "sample-falsification_trigger",
  "budget_start": "2026-05-23T12:00:00Z",
  "budget_end": "2026-05-23T12:00:00Z",
  "verdict": "sample-verdict",
  "named_risk": "sample-named_risk",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
