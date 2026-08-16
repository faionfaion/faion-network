# Streaming Response UX

## Summary

**One-sentence:** Produces a streaming-UX spec for one feature surface (chat / inline-AI / copilot): cursor, cancel, partial-state, error recovery, edit-during-stream, scroll lock, plus TTFT + abort-rate telemetry thresholds.

**Ефективно для:** front-end engineers shipping LLM chat / copilot UX where token-by-token streaming feels broken on jitter; PMs writing acceptance criteria for streaming UX; SREs adding TTFT / abort-rate telemetry to a streaming surface.

**One-paragraph:** This methodology pins the recurring decision around "streaming-response-ux" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Feature uses LLM streaming (SSE / WebSocket / chunked HTTP).
- Users see model output as it generates, not after completion.
- Expected stream length > 500ms median.
- Owner exists for the streaming surface after ship.

## Skip If (ANY kills it)

- Stream completes in <500ms median — batched UX is simpler and cheaper.
- Users are agents/bots, not humans — telemetry-only is sufficient.
- Model already returns structured JSON only — streaming text rules don't apply.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Wire-protocol decision | ADR | tech lead |
| Client framework version | string | frontend lead |
| Telemetry pipeline endpoint | URL | SRE |
| Surface owner | handle / email | team roster |
| Latency budget | ms (target + p95) | PM |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip / variant router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_ux_rules` | haiku | Bounded template fill from prereqs. |
| `synthesize_surface_spec` | sonnet | Per-surface judgment with bounded inputs. |
| `review_for_trust_collapse` | opus | Cross-input synthesis when failures cascade. |

## Templates

| File | Purpose |
|------|---------|
| `templates/streaming-response-ux.json` | JSON Schema for the Streaming Response UX output contract |
| `templates/streaming-response-ux.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a streaming-response-ux record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a streaming-response-ux record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-streaming-response-ux.py` | Enforce the Streaming Response UX output contract | After subagent returns, before downstream consumer reads |

## Related

- [[ai-feature-ux-pattern-library]] — adjacent UX-pattern catalogue.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/streaming-response-ux.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/streaming-response-ux.json",
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
      "pattern": "^srux-[a-z0-9-]+$"
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
