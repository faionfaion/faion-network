# Agency P&L Tracker Template

## Summary

**One-sentence:** Monthly micro-agency P&L tracker with revenue-line split (project / retainer / productised), contractor COGS, utilisation, and weekly utilisation sub-tracker.

**One-paragraph:** The micro-agency P&L tracker pins a one-row-per-month artefact that splits revenue (project / retainer / productised), tracks contractor cost separately from payroll, computes gross margin per line, and surfaces utilisation against billable capacity. A weekly utilisation sub-tracker feeds the monthly P&L. Designed for 1-10 FTE agencies that out-grow spreadsheets but don't yet need an accountant.

**Ефективно для:**

- Micro-agencies (1-10 FTE) needing finance visibility without an accountant.
- Agencies with mixed revenue (project + retainer + productised) needing per-line margin.
- Agencies whose utilisation rate is the leading profitability lever.
- Owners running annual planning needing monthly actuals.

## Applies If (ALL must hold)

- Agency has ≥3 months of invoicing history.
- Time-tracking system in place for utilisation computation.
- Owner authorised to view all financial data.
- Monthly close cadence is observed.

## Skip If (ANY kills it)

- Pre-revenue agency — too early.
- Solo, single-revenue-line consultant — overhead exceeds value.
- Established mid-size agency with full accounting — use proper books.

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
| `content/01-core-rules.xml` | essential | 5 testable rules — monthly cadence, 3-line revenue split, contractor in COGS, utilisation mandatory, variance vs plan | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agency-pnl-tracker-template artefact | 800 |
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
| `templates/pnl-monthly.md` | Monthly P&L template. |
| `templates/utilisation-weekly.md` | Weekly utilisation sub-tracker. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-pnl-tracker-template.py` | Schema-validate artefact JSON. | Pre-commit + before review. |

## Related

- [[agency-annual-plan-template]]
- [[agency-cash-flow-friday-routine]]
- [[agency-pipeline-hygiene-15min]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agency-pnl-tracker-template input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
