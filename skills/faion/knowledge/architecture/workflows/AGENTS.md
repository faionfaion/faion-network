# Architecture Workflows

## Summary

**One-sentence:** Picks one of seven canonical architecture workflows (system-design, review, ADR, tech-eval, ATAM/CBAM, Strangler migration, design-doc review) and emits its named step sequence + role assignments.

**One-paragraph:** Seven repeatable workflow types for architecture activities, each materialised as a named pipeline of steps. This methodology selects the right workflow for a given trigger (new system, decision pending, migration, audit), instantiates it with concrete role assignments (clarifier, designer, critic, documenter), and emits a state machine that materialises each step's artefact to disk for review. Output: a workflow-instance with step list, expected artefacts per step, and review gates.

**Ефективно для:**

- Solo architect needing a default playbook for the next recurring activity (design, review, ADR, migration).
- Onboarding: handing a new architect a stepped checklist instead of tribal knowledge.
- Audit-grade documentation showing "we followed an evaluation method" (ATAM/CBAM).
- Standardising recurring architecture rituals so the ceremony itself becomes the deliverable.

## Applies If (ALL must hold)

- Activity is recurring (≥3 times/year) — workflow ceremony pays back only with reuse.
- Output will be reviewed by ≥1 other person (peer, stakeholder, auditor).
- Trigger maps to one of seven canonical workflows.
- Operator has authority to enforce step gates (cannot skip review).

## Skip If (ANY kills it)

- One-person, one-decision context with no review — workflow ceremony costs more than the decision value.
- Pure code-level refactor — use design-pattern methodologies, not workflows.
- Tight time-boxed prototype (<3 days) — workflows assume room for review cycles.
- Trigger does not match any of the seven workflows — use general SDD instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger | one of {new-system, review-needed, decision-pending, tech-eval, atam, migration, design-doc} | requester |
| Stakeholder map | role → name → primary concern | PM / project lead |
| Time budget | calendar window per step + review gates | architect |
| Existing artefacts | ADRs / diagrams / specs to feed into the workflow | repo / docs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[architecture-decision-records]] | Step `record-decision` of every workflow emits an ADR. |
| [[trade-off-stakeholder-communication]] | Review gates use the stakeholder-briefing bundle. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (named workflow, role per step, materialised artefact, review gate, abort condition) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for workflow-instance + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: ceremony-without-substance, skipped-gate, role-overload, frozen-workflow | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (classify trigger → select workflow → assign roles → run steps → close) | 700 |
| `content/05-examples.xml` | essential | Worked example: ATAM workflow for monolith → microservices migration | 600 |
| `content/06-decision-tree.xml` | essential | Routes trigger → workflow type → step list | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workflows_classify_trigger` | haiku | Pattern match trigger → workflow type. |
| `workflows_assign_roles` | sonnet | Stakeholder map → role table for each step. |
| `workflows_run_step` | sonnet | Per-step subagent invocation (clarifier, designer, critic). |
| `workflows_review_gate` | opus | Cross-step review across artefacts. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the workflow-instance artefact |
| `templates/workflow-instance.md.j2` | Markdown skeleton with steps + role table + review gates |
| `templates/workflow-instance.md` | Markdown skeleton with steps + role table + review gates Generated from `templates/workflow-instance.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable filled-in workflow-instance for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-workflows.py` | Validate workflow-instance against schema + step-gate completeness | Pre-commit; CI on each workflow instance |

## Related

- [[architecture-decision-records]]
- [[trade-off-stakeholder-communication]]
- [[quality-attributes-analysis]]
- [[system-design-process]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) trigger category — maps trigger to one of seven workflows, (b) review depth — adds review gates for type-1 decisions, and (c) completion — requires every step's artefact present on disk before close. Every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/architecture-workflows.json",
  "type": "object",
  "required": [
    "instance_id",
    "workflow_type",
    "trigger",
    "abort_condition",
    "steps"
  ],
  "properties": {
    "instance_id": {
      "type": "string",
      "pattern": "^WF-[0-9]{3,5}$"
    },
    "workflow_type": {
      "type": "string",
      "enum": [
        "system-design",
        "architecture-review",
        "adr",
        "tech-eval",
        "atam-cbam",
        "strangler-migration",
        "design-doc-review"
      ]
    },
    "trigger": {
      "type": "string",
      "minLength": 8
    },
    "abort_condition": {
      "type": "string",
      "minLength": 8
    },
    "steps": {
      "type": "array",
      "minItems": 2,
      "items": {
        "type": "object",
        "required": [
          "n",
          "name",
          "role",
          "artefact_path",
          "artefact_format",
          "review_gate"
        ]
      }
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "instance_id": "WF-0042",
  "workflow_type": "atam-cbam",
  "trigger": "Monolith vs microservices for Phase 3 scale-up",
  "abort_condition": "Stakeholder map cannot be assembled within 2 working days",
  "steps": [
    {
      "n": 1,
      "name": "scope-utility-tree",
      "role": "clarifier",
      "artefact_path": "atam/utility-tree.md",
      "artefact_format": "md",
      "review_gate": false,
      "decision_type": "none"
    },
    {
      "n": 2,
      "name": "score-options",
      "role": "designer",
      "artefact_path": "atam/scorecard.json",
      "artefact_format": "json",
      "review_gate": true,
      "reviewer": "lead-architect",
      "decision_type": "type-1"
    },
    {
      "n": 3,
      "name": "write-adr",
      "role": "documenter",
      "artefact_path": "adr/ADR-0031.md",
      "artefact_format": "md",
      "review_gate": true,
      "reviewer": "ceo",
      "decision_type": "type-1"
    }
  ]
}
```
