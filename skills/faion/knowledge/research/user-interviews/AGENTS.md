# User Interviews

## Summary

**One-sentence:** Produces a user-interview report (Mom Test script + diarized transcripts + behavioural-ask outcome per session + frequency-counted insight list) so customer-discovery conversations produce evidence, not compliments.

**Ефективно для:** Solopreneurs whose 'user interviews' keep returning enthusiastic compliments and zero usable insight.

**One-paragraph:** Founders skip user interviews or conduct them poorly: leading questions, pitching instead of listening, accepting 'I would' as data. This methodology pins each session to a Mom Test script (past behaviour, not hypotheticals), enforces a behavioural ask at session end, requires diarized transcripts, and produces a frequency-counted insight list. Output is consumed by problem-validation-2026 and value-proposition-design.

## Applies If (ALL must hold)

- Pre-MVP discovery: understand the problem before building.
- Post-launch retention research: why are users churning?
- Pricing or positioning research where survey data is too thin.
- New segment exploration where you have no prior data.

## Skip If (ANY kills it)

- When A/B testing answers the question faster.
- When the segment is unreachable within a reasonable window.
- When the team has no capacity for diarized transcription + synthesis.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| recruit list with cold/warm tags | array | researcher |
| hypothesis or decision the interview informs | string | PM |
| Mom Test script | markdown | researcher |
| diarized recording setup | tool | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `solo/research/researcher/research-repo-file-naming-convention` | Downstream — transcripts land in the named repo. |
| `solo/research/researcher/problem-validation-2026` | Downstream — consumes the report for tier-scoring. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 failure modes with detector + repair | ~800 |
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
| `templates/user-interviews.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/user-interviews.md.j2` | Markdown skeleton with the required fields. |
| `templates/user-interviews.md` | Markdown skeleton with the required fields. Generated from `templates/user-interviews.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-user-interviews.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[problem-validation-2026]] — related methodology.
- [[value-proposition-design]] — related methodology.
- [[use-case-mapping]] — related methodology.
- [[single-interview-fast-loop-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/user-interviews.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/user-interviews.json",
  "title": "User Interviews Output Contract",
  "type": "object",
  "required": [
    "session_id",
    "respondent",
    "script_used",
    "transcript_path",
    "behavioural_ask_outcome",
    "insights",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "session_id": {
      "type": "string",
      "description": "stable id"
    },
    "respondent": {
      "type": "object",
      "description": "Pnnn + cold/warm flag"
    },
    "script_used": {
      "type": "string",
      "description": "path to Mom Test script"
    },
    "transcript_path": {
      "type": "string",
      "description": "path to diarized transcript"
    },
    "behavioural_ask_outcome": {
      "type": "string",
      "description": "yes-with-evidence | no | pending"
    },
    "insights": {
      "type": "array",
      "description": "\u22651 insight with frequency_count \u22651 and citation",
      "items": {
        "type": "object"
      },
      "minItems": 1
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
  "session_id": "sample-session_id",
  "respondent": {
    "k": "v"
  },
  "script_used": "sample-script_used",
  "transcript_path": "sample-transcript_path",
  "behavioural_ask_outcome": "sample-behavioural_ask_outcome",
  "insights": [
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
