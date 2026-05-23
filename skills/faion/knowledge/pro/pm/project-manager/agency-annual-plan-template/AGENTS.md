---
slug: agency-annual-plan-template
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: One-page agency annual plan with quarterly revenue + utilisation targets, named milestone owners, and quarterly checkpoint cadence.
content_id: "0f53aff3fc4dd89f"
complexity: medium
produces: spec
est_tokens: 3800
tags: [agency, annual-plan, pm, template]
---
# Agency Annual Plan Template

## Summary

**One-sentence:** One-page agency annual plan with quarterly revenue + utilisation targets, named milestone owners, and quarterly checkpoint cadence.

**One-paragraph:** The agency annual plan replaces multi-tab spreadsheets with a one-page artefact: quarterly revenue targets (split project / retainer / productised), utilisation targets, milestone owners, and explicit investment lines with budget caps. The plan is reviewed quarterly against actuals via a fixed-shape checkpoint that captures variance + reason + corrective action. Designed for micro-agencies (1-10 FTE) that drown in spreadsheets and miss the strategic thread.

**Ефективно для:**

- Solo / micro-agency owner planning the year in one sitting.
- Agencies with retainer + project mix needing margin discipline.
- Agencies running quarterly partner reviews against a plan.
- Agencies pivoting model (project → productised) needing a target.

## Applies If (ALL must hold)

- Agency revenue spans ≥2 revenue lines (project / retainer / productised).
- Owner has authority to commit quarterly budgets.
- Plan will be reviewed at least quarterly.
- Prior-year actuals available for delta + variance baseline.

## Skip If (ANY kills it)

- Single-line revenue (one client) — plan overhead exceeds value.
- Pre-revenue agency — use a 90-day plan instead.
- Quarterly review cadence not protected — plan rots.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prior-period output | MD / CSV | agency |
| Current pipeline / roadmap | list | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Engagement of partners / sponsors anchors the artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — one-page rule, per-line revenue split, named milestone owners, investment cap, quarterly checkpoint | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agency-annual-plan-template artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping artefact state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from prior-period output. |
| `fill-evidence` | sonnet | Select correct evidence per row. |
| `synthesise-decisions` | opus | Cross-period synthesis for corrective decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/annual-plan.md` | One-page annual plan skeleton. |
| `templates/quarterly-checkpoint.md` | Quarterly variance checkpoint template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-annual-plan-template.py` | Schema-validate artefact JSON. | Pre-commit + before review. |

## Related

- [[agency-cash-flow-friday-routine]]
- [[agency-pnl-tracker-template]]
- [[agency-pipeline-hygiene-15min]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agency-annual-plan-template input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
