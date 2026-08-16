# Single Interview Fast Loop Template

## Summary

**One-sentence:** Produces a single-interview fast-loop spec (30-min prep + 60-min interview + 60-min synthesis inside 36h, anchored to one decision) so single-shot interviews compound into evidence instead of evaporating.

**Ефективно для:** Solo PMs and founders who keep landing one-off interview slots that should produce evidence but instead get lost in the inbox.

**One-paragraph:** Existing interview playbooks assume batch studies. PMs and solo founders increasingly run one interview when the opportunity appears — a churned customer, a discovery call, a power user with 30 free minutes. This methodology pins a tight prep (one hypothesis + 5 must-asks + one decision the interview informs) and a hard 24-hour synthesis deadline so the learning lands while context is hot. Output is consumed by problem-validation-2026 and the broader user-interviews insight ledger.

## Applies If (ALL must hold)

- Exactly one interview opportunity (no batch study).
- There is a specific decision or hypothesis this interview should inform.
- Interviewer can commit 30 min prep + 60 min interview + 60 min synthesis inside ~36 hours.
- Tier solo or higher.

## Skip If (ANY kills it)

- Batch study (≥4 interviews planned) — use user-interviews instead.
- No decision attached — the interview is small-talk, not research.
- Synthesis cannot land inside 36h — the loop's compounding value dies.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| one hypothesis or decision | string | PM |
| 5 must-ask questions | list | researcher |
| interview slot confirmed | calendar | operator |
| synthesis template ready | markdown | researcher |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Parent — single loop is a degenerate case of the batch loop. |
| `solo/research/researcher/problem-validation-2026` | Downstream — single-loop insights feed the evidence ledger. |

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
| `templates/single-interview-fast-loop-template.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/single-interview-fast-loop-template.md.j2` | Markdown skeleton with the required fields. |
| `templates/single-interview-fast-loop-template.md` | Markdown skeleton with the required fields. Generated from `templates/single-interview-fast-loop-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-single-interview-fast-loop-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[user-interviews]] — related methodology.
- [[problem-validation-2026]] — related methodology.
- [[validation-paralysis-breaker]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/single-interview-fast-loop-template.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/single-interview-fast-loop-template.json",
  "title": "Single Interview Fast Loop Template Output Contract",
  "type": "object",
  "required": [
    "loop_id",
    "decision_under_test",
    "must_asks",
    "interview_at",
    "synthesis_due_at",
    "synthesis_outcome",
    "citation_path",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "loop_id": {
      "type": "string",
      "description": "stable id"
    },
    "decision_under_test": {
      "type": "string",
      "description": "the one decision the loop informs"
    },
    "must_asks": {
      "type": "array",
      "description": "3\u20135 past-tense questions",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "interview_at": {
      "type": "string",
      "description": "ISO datetime",
      "format": "date-time"
    },
    "synthesis_due_at": {
      "type": "string",
      "description": "interview_at + \u226436h",
      "format": "date-time"
    },
    "synthesis_outcome": {
      "type": "string",
      "description": "decide-yes | decide-no | park | re-interview"
    },
    "citation_path": {
      "type": "string",
      "description": "path to transcript in research repo"
    },
    "owner": {
      "type": "string",
      "description": "named researcher"
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
  "loop_id": "sample-loop_id",
  "decision_under_test": "sample-decision_under_test",
  "must_asks": [
    {
      "k": "v"
    }
  ],
  "interview_at": "2026-05-23T12:00:00Z",
  "synthesis_due_at": "2026-05-23T12:00:00Z",
  "synthesis_outcome": "sample-synthesis_outcome",
  "citation_path": "sample-citation_path",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
