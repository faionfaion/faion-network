# Agency Cash-Flow Friday Routine

## Summary

**One-sentence:** 15-minute weekly cash-flow routine — 5-item checklist covering AR, AP, payroll, fixed costs, runway — committed each Friday with named action when amber.

**One-paragraph:** A fixed weekly ritual replacing 'check the bank account when something feels off' with a 15-minute Friday checklist. Each item has a green/amber/red trigger and a named action if amber. The output is a one-line ledger entry per Friday plus action items routed to owners. Designed for solo founders and micro-agencies where one missed week of cash discipline kills the business.

**Ефективно для:**

- Solo founder or micro-agency where one missed week of cash hygiene is existential.
- Agencies with seasonal AR cycles needing weekly visibility.
- Agencies running a runway-based decision model (not a quarterly-budget model).
- Operators easily distracted from finance by client work.

## Applies If (ALL must hold)

- Owner has authority over outflows + can chase AR.
- Banking + invoice systems support 15-min weekly export.
- Friday slot is calendar-protected.
- Net inflow + runway can be computed in under 5 minutes.

## Skip If (ANY kills it)

- Larger agency (>10 FTE) with dedicated finance — cadence misfits.
- Owner not authorised to chase AR or hold AP — checklist toothless.
- Agency with VC runway > 18 months — weekly cadence overkill.

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
| `content/01-core-rules.xml` | essential | 5 testable rules — 15-min cap, 5-item checklist, named action when amber, ledger entry, runway trigger | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agency-cash-flow-friday-routine artefact | 800 |
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
| `templates/friday-checklist.md` | 5-item checklist with green/amber/red triggers. |
| `templates/ledger.md` | Weekly ledger row template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-cash-flow-friday-routine.py` | Schema-validate artefact JSON. | Pre-commit + before review. |

## Related

- [[agency-pnl-tracker-template]]
- [[agency-annual-plan-template]]
- [[agency-pipeline-hygiene-15min]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agency-cash-flow-friday-routine input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
