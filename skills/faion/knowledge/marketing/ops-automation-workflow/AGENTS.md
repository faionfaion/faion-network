# Ops Automation Workflow

## Summary

**One-sentence:** Generates an automation inventory + ROI-ranked backlog + design doc for each candidate automation — replaces repetitive ops tasks without sprawling no-code chains nobody owns.

**One-paragraph:** Ops Automation Workflow produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solopreneur with ≥10 hours / week of repetitive ops tasks who needs a ranked automation backlog with ROI math and a named owner per automation — before stacking another untracked Zap.

## Applies If (ALL must hold)

- ≥10 hours / week of repetitive manual ops tasks identified
- Stack with at least one automation surface (Zapier, n8n, Make, Apps Script)
- Founder authority to retire failing automations

## Skip If (ANY kills it)

- Tasks need human judgement on each instance — not automation candidates
- <5 hours / week of repetitive work — payback never lands
- No automation budget (tool or time to build) for the next 30 days

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repetitive-task inventory with hours/week | table | founder time log |
| Tool inventory (Zapier / n8n / Make / Apps Script) | list | billing exports |
| Cost per hour of founder time (USD) | number | p&l |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `ops-dashboard-setup` | Sibling — dashboard reads automation health signals. |
| `ops-customer-support` | Many candidate automations come from support inbox. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-inventory-before-build, r2-roi-ranked, r3-named-owner-per-automation, r4-monitoring-required, r5-quarterly-cull | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ops-automation-workflow` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ops-automation-workflow` | haiku | Schema check + threshold checks; deterministic. |
| `review-ops-automation-workflow` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-automation-workflow.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ops-automation-workflow.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/ops-automation-workflow.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/ops-automation-workflow.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/automation-audit.md.j2` | Time-and-frequency audit of manual tasks, ranking automation candidates by ROI. |
| `templates/automation-audit.md` | Time-and-frequency audit of manual tasks, ranking automation candidates by ROI. Generated from `templates/automation-audit.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/automation-design-doc.md.j2` | Design doc for one automation -- trigger, workflow steps, error handling, manual fallback, monitoring. |
| `templates/automation-design-doc.md` | Design doc for one automation -- trigger, workflow steps, error handling, manual fallback, monitoring. Generated from `templates/automation-design-doc.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/automation-inventory.md.j2` | Running register of active automations by domain (lead, lifecycle, ops, content) with status and review date. |
| `templates/automation-inventory.md` | Running register of active automations by domain (lead, lifecycle, ops, content) with status and review date. Generated from `templates/automation-inventory.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ops-automation-workflow.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ops-dashboard-setup]]
- [[ops-customer-support]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ops-automation-workflow.json`

```json
{
  "artefact_id": "ops-automation-workflow-<project>-<period>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "inventory": [],
  "backlog": [],
  "hour_cost_usd": 0.0,
  "owner": "<@handle>",
  "next_review": "2026-05-23"
}
```
