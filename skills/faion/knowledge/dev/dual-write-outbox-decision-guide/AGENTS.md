# Dual Write Outbox Decision Guide

## Summary

**One-sentence:** Outbox vs CDC vs dual-write decision guide

**One-paragraph:** Dual Write Outbox Decision Guide codifies a recurring "monolith-to-services migration architecture" decision into a decision record artefact with a typed input contract, a JSON-schema-checked output, and a decision tree that routes between the operational variants. It exists because adjacent methodologies cover the surrounding topic without pinning the precise output shape this task produces. The artefact carries owner, version, last-reviewed date, and citations to every input used, so downstream agents and human reviewers can consume it without re-deriving the rationale.

**Ефективно для:**

- A team that already runs the parent activity but has no canonical decision record shape.
- Multi-agent workflows that need a contract-checked artefact instead of free-form prose.
- Pre-merge / pre-release gates where a missing field must block the pipeline.
- Audit scenarios — every decision must trace to a named input + a named owner.

## Applies If (ALL must hold)

- Task is an instance of "monolith-to-services migration architecture" or a closely-adjacent variant.
- All Prerequisites artefacts exist or can be produced before the run starts.
- Output will be consumed by a downstream agent or human reviewer (not discarded).
- Tier `pro` or higher is unlocked for the operator (gating enforced by tier-manifest).

## Skip If (ANY kills it)

- A working team-owned artefact already covers this gap — replace, do not duplicate.
- The decision being made is a greenfield prototype with no production users.
- Regulatory or legal context overrides any in-methodology guidance — defer to counsel.
- Single-use throwaway task — overhead of the contract is not justified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent context for the parent activity | Markdown / JSON | last 30 days of activity |
| Write access to artefact store | repo / wiki / decision log | platform owner |
| Named accountable owner | string (handle / email / role) | RACI / org chart |
| Baseline conventions | `CLAUDE.md` / `AGENTS.md` / `CONVENTIONS.md` | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_artefact` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/dual-write-outbox-decision-guide.json` | JSON Schema for the decision record output contract |
| `templates/dual-write-outbox-decision-guide.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dual-write-outbox-decision-guide.py` | Enforce Dual Write Outbox Decision Guide output contract against the JSON Schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream activity: `monolith-to-services migration architecture`
- methodology family: `pro/dev/` (gap-p2 batch, F-059..F-066)

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions satisfied, stake level, downstream-consumer presence, regime overlay) to a concrete rule from `01-core-rules.xml`. Use it when in doubt about whether to run this methodology, defer to a peer, or skip outright.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/dual-write-outbox-decision-guide.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/dual-write-outbox-decision-guide.json",
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
      "pattern": "^[a-z][a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 3
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 30
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
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "produces": {
      "const": "decision-record"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "dual-write-outbox-decision-guide-2026-05-23-001",
  "owner": "alice@example.com",
  "decision": "Adopt the canonical decision-record shape per r1-bound-scope.",
  "rationale": "Driven by parent-activity-context (last sprint events) and owner-roster (CODEOWNERS maps area to alice).",
  "inputs_used": [
    {
      "name": "parent-activity-context",
      "source": "repo://docs/parent.md"
    },
    {
      "name": "owner-roster",
      "source": "repo://CODEOWNERS"
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "produces": "decision-record"
}
```
