# Tool Trust Boundary Model

## Summary

**One-sentence:** Produces a trust-boundary spec for an agent / tool surface: hard-wall sensitive ops, soft-wall confirmable ops, observable ops; with prompt-injection + jailbreak defences per boundary.

**Ефективно для:** platform security owners gating LLM-agent tool launches; LLM-agent developers hardening a multi-tool agent; CISOs reviewing AI-tool exposure to prompt injection and jailbreak.

**One-paragraph:** This methodology pins the recurring decision around "tool-trust-boundary-model" into a typed artefact governed by 5 testable rules. Inputs are typed and sourced; the output is contract-checked; a named accountable owner signs every record. The decision tree at `content/06-decision-tree.xml` routes preconditions and variant signals to a run / skip / variant outcome, with every conclusion referencing a rule id in `content/01-core-rules.xml`.

## Applies If (ALL must hold)

- Agent has ≥2 tools with differing blast radii (read / write / external).
- Inputs include untrusted content (user text / web pages / retrieved docs).
- Owner exists for the boundary spec.
- Compliance regime touches the surface (SOC2 / HIPAA / GDPR / EU AI Act).

## Skip If (ANY kills it)

- Single read-only tool with no write paths — overhead unjustified.
- Agent runs on fully trusted internal corpus only — air-gapped.
- Prototype with no production users yet.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool inventory + cards | directory | platform repo |
| Input source taxonomy (trust levels) | JSON / Markdown | security lead |
| Compliance regime list | Markdown | legal / compliance |
| Owner for boundary spec | handle / email | team roster |
| Existing incident corpus | logs | incident db |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[tool-card-template]]` | tool card carries the boundary class |

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
| `classify_tools` | sonnet | Per-tool classification needs judgment on blast radius. |
| `draft_defences` | sonnet | Defence selection per boundary. |
| `escalate_high_risk` | opus | Cross-tool composition risk. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-trust-boundary-model.json` | JSON Schema for the Tool Trust Boundary Model output contract |
| `templates/tool-trust-boundary-model.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a tool-trust-boundary-model record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a tool-trust-boundary-model record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-trust-boundary-model.py` | Enforce the Tool Trust Boundary Model output contract | After subagent returns, before downstream consumer reads |

## Related

- [[tool-card-template]] — boundary class lives on the card.
- [[tool-call-schema-design-checklist]] — gates each tool through this model.
- [[tool-deprecation-lifecycle]] — boundary refresh on tool swap.

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) variant detected per the methodology-specific signal? Routes to run / skip / variant. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tool-trust-boundary-model.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/tool-trust-boundary-model.json",
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
      "pattern": "^ttb-[a-z0-9-]+$"
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
