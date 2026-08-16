# Trade-off Stakeholder Communication

## Summary

**One-sentence:** Generates a stakeholder-tailored trade-off briefing that preserves the key risk for every audience (exec, PM, engineer, ops) and writes the ADR Consequences section.

**One-paragraph:** Architecture trade-offs must be communicated differently to executives, product managers, engineers, and operations — but the key risk must survive every translation. This methodology emits four artefacts from one trade-off: an exec-summary (≤120 words, lists the gain + the survivable downside), a PM-brief (impact on roadmap + dependencies), an engineer-note (the chosen option's mechanics + what we sacrificed), and an ops-runbook-delta (what changes in oncall). All four MUST converge on the same risk paragraph — divergence is the bug.

**Ефективно для:**

- Solo architect presenting a Type-1 (irreversible) decision to non-technical founders before commit.
- Generating the ADR Consequences section from a decision matrix or ATAM scorecard.
- Post-mortem of a decision where the trade-off materialised — communicating what we knew vs what happened.
- Briefing a junior engineer on why the simpler option was rejected.

## Applies If (ALL must hold)

- Decision affects ≥2 stakeholder roles (not just an internal refactor).
- Decision is Type-1 (hard/expensive to reverse) OR involves a multi-month commitment.
- An ADR or decision record will be created as the durable artefact.
- Stakeholders have been identified by role (not generic personas).

## Skip If (ANY kills it)

- Type-2 reversible small-scope decision — a 3-line ADR comment is enough; full briefing is noise.
- Stakeholder roles not yet identified — the agent will invent personas and the briefing binds nobody.
- Pure code-style debate (tabs vs spaces) — not an architecture trade-off.
- Solo project with no external stakeholders — write the engineer-note only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision record (options + criteria + chosen) | markdown / table | architect's draft ADR |
| Stakeholder map | role → name → primary concern | from PM or project lead |
| Quality-attribute scorecard | option × attribute matrix | trade-off-analysis methodology |
| Reversibility classification | Type-1 / Type-2 + cost-to-reverse | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[architecture-decision-records]] | Defines the ADR shell this Consequences section drops into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (risk preservation, role-fit, single-source-of-truth, ≤120-word exec, no-omission gate) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the 4-artefact bundle + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: risk-laundering, persona-drift, single-author-no-review, hidden-trade-off | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (extract risk → draft per-role → cross-check convergence → ADR insert → review) | 700 |
| `content/05-examples.xml` | essential | Worked example: monolith → microservices ADR briefing for 4 roles | 600 |
| `content/06-decision-tree.xml` | essential | Routes by reversibility + stakeholder count + risk severity | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `trade_off_stakeholder_communication_extract_risk` | sonnet | Cross-input synthesis to compress the survivable downside. |
| `trade_off_stakeholder_communication_draft_per_role` | sonnet | Role-tailored prose; mechanical but judgement-heavy. |
| `trade_off_stakeholder_communication_convergence_check` | opus | Reads all 4 drafts and verifies the same risk paragraph survives. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the 4-artefact briefing bundle |
| `templates/briefing-bundle.md.j2` | Markdown skeleton with exec/PM/engineer/ops sections + the shared risk paragraph |
| `templates/briefing-bundle.md` | Markdown skeleton with exec/PM/engineer/ops sections + the shared risk paragraph Generated from `templates/briefing-bundle.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/adr-consequences.md.j2` | Drop-in Consequences block for the parent ADR |
| `templates/adr-consequences.md` | Drop-in Consequences block for the parent ADR Generated from `templates/adr-consequences.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in bundle for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-trade-off-stakeholder-communication.py` | Validate briefing bundle against schema + check risk convergence | Pre-commit; CI on each ADR change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[trade-off-technical-debt]]
- [[quality-attributes-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) reversibility — Type-2 short-circuits to engineer-note-only, (b) stakeholder count — <2 roles skips full bundle, and (c) risk severity — high-severity decisions force the convergence-check rule. Every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/trade-off-stakeholder-communication.json",
  "type": "object",
  "required": [
    "decision_id",
    "decision_title",
    "reversibility",
    "key_risk",
    "artefacts"
  ],
  "properties": {
    "decision_id": {
      "type": "string",
      "pattern": "^ADR-[0-9]{3,5}$"
    },
    "decision_title": {
      "type": "string",
      "minLength": 8,
      "maxLength": 120
    },
    "reversibility": {
      "type": "string",
      "enum": [
        "type-1",
        "type-2"
      ]
    },
    "key_risk": {
      "type": "string",
      "minLength": 24,
      "maxLength": 320
    },
    "artefacts": {
      "type": "object",
      "required": [
        "exec_summary",
        "pm_brief",
        "engineer_note",
        "ops_delta"
      ],
      "properties": {
        "exec_summary": {
          "type": "object",
          "required": [
            "body",
            "word_count",
            "embeds_key_risk"
          ],
          "properties": {
            "body": {
              "type": "string"
            },
            "word_count": {
              "type": "integer",
              "maximum": 120
            },
            "embeds_key_risk": {
              "type": "boolean",
              "const": true
            }
          }
        },
        "pm_brief": {
          "type": "object",
          "required": [
            "body",
            "roadmap_impact",
            "dependency_changes",
            "embeds_key_risk"
          ]
        },
        "engineer_note": {
          "type": "object",
          "required": [
            "body",
            "sacrificed",
            "embeds_key_risk"
          ],
          "properties": {
            "sacrificed": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "string"
              }
            }
          }
        },
        "ops_delta": {
          "type": "object",
          "required": [
            "body",
            "runbook_changes",
            "alert_changes",
            "embeds_key_risk"
          ]
        }
      }
    },
    "convergence_check_passed": {
      "type": "boolean"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "decision_id": "ADR-0023",
  "decision_title": "Adopt Postgres-only persistence; defer Redis cache to Phase 2",
  "reversibility": "type-1",
  "key_risk": "Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
  "artefacts": {
    "exec_summary": {
      "body": "We are standardising on Postgres for the next 18 months and deferring Redis. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth. Re-evaluate Q3.",
      "word_count": 40,
      "embeds_key_risk": true
    },
    "pm_brief": {
      "body": "Phase 2 cache rollout becomes P0. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
      "roadmap_impact": "Phase 2 (Q3) adds a 4-week cache rollout task.",
      "dependency_changes": [
        "Phase 2 milestone requires cache layer"
      ],
      "embeds_key_risk": true
    },
    "engineer_note": {
      "body": "Postgres-only Phase 1. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
      "sacrificed": [
        "Sub-millisecond p99 read latency",
        "Independent cache scaling"
      ],
      "embeds_key_risk": true
    },
    "ops_delta": {
      "body": "Single oncall surface. Key risk: Read-heavy endpoints will hit p95 latency ceiling at ~5x current load; Phase 2 cache rollout is on the critical path for 10x growth.",
      "runbook_changes": [
        "Postgres pool saturation entry"
      ],
      "alert_changes": [
        "p95 latency 250ms read endpoints"
      ],
      "embeds_key_risk": true
    }
  },
  "convergence_check_passed": true
}
```
