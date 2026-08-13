# AI Acceptance Criteria Hallucination Checklist

## Summary

**One-sentence:** Produces a per-story checklist that vets AI-generated acceptance criteria for plausible-but-wrong shapes: invented happy paths, missing edge cases, fabricated metrics, contradictory constraints, before ACs enter sprint.

**Ефективно для:** BAs gating AI-generated acceptance criteria; QA leads catching AC hallucinations before sprint start; PMs reviewing AI-drafted stories.

**One-paragraph:** This methodology pins the recurring decision around "ai-ac-hallucination-checklist" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Acceptance criteria drafted by an LLM (or LLM-assisted).
- Story will enter a sprint backlog after this gate.
- Owner exists for the AC review.
- Story is for a software / agent feature, not pure research.

## Skip If (ANY kills it)

- ACs are fully human-authored — apply standard AC review.
- Story is a spike / research task with no production output.
- Single-story experiment with no downstream impact.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI-drafted acceptance criteria | Markdown / Gherkin | BA |
| Source requirement record | spec id | BA |
| Definition-of-done reference | Markdown | engineering lead |
| Owner for review | handle / email | team roster |
| Existing edge-case catalogue | Markdown | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ai-transcript-to-traceable-requirement]]` | source requirement has a provenance trail |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_checklist_pass` | haiku | Mechanical AC walk-through. |
| `synthesize_revision` | sonnet | Per-AC judgment when a check fails. |
| `escalate_ambiguity` | opus | When two checks contradict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-ac-hallucination-checklist.json` | JSON Schema for the AI Acceptance Criteria Hallucination Checklist output contract |
| `templates/ai-ac-hallucination-checklist.md` | Markdown skeleton with the required fields |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-ac-hallucination-checklist.py` | Enforce the AI Acceptance Criteria Hallucination Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- [[ai-story-truth-checklist]] — sister checklist on user stories.
- [[ai-transcript-to-traceable-requirement]] — upstream traceability.
- [[ai-enabled-business-analysis]] — parent methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ai-ac-hallucination-checklist.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/ai-ac-hallucination-checklist.json",
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
      "pattern": "^aiah-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
