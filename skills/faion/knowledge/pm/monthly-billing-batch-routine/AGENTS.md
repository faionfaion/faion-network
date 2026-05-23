# Monthly Billing Batch Routine

## Summary

**One-sentence:** Micro-agency monthly invoice + contractor-pay batch routine: build customer invoices, queue contractor payouts, reconcile, surface to founder for approval.

**One-paragraph:** Monthly Billing Batch Routine defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Micro-agency / studio founder with 2-15 customers and 1-10 contractors.
- Monthly billing cadence (not weekly), with mid-month contractor payouts.
- One human reviewer (founder) is the approval gate.
- An auditable ledger (spreadsheet, Xero, Wave) is the source-of-truth.

## Applies If (ALL must hold)

- Recurring monthly invoice cycle is in place (date locked).
- Founder has authority to send invoices and queue contractor payouts.
- Contractor rate cards or signed SoWs are accessible.
- Prior month's batch (if any) is accessible for delta.

## Skip If (ANY kills it)

- Sub-monthly cadence — use freelance-weekly-invoice-cadence instead.
- Single-customer agency — overhead does not pay back; ad-hoc is fine.
- Cannot access source-of-truth ledger (system down, access pending).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `monthly-billing-batch-routine_template_fill` | haiku | Bounded template fill, no judgement. |
| `monthly-billing-batch-routine_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `monthly-billing-batch-routine_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the monthly billing batch artefact. |
| `templates/invoice-row.md` | Per-customer invoice line skeleton with evidence + reason. |
| `templates/payout-row.md` | Per-contractor payout line skeleton with evidence + rate-card link. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monthly-billing-batch-routine.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
