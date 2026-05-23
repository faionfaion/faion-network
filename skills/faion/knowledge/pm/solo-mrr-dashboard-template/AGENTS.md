# Solo MRR Dashboard Template

## Summary

**One-sentence:** A copy-pasteable single-sheet spec for MRR, gross/net churn, ARPU, LTV, and customer count — pulled directly from Stripe's API, calibrated for one operator.

**One-paragraph:** Generic ops-metrics methodologies define MRR conceptually but assume a finance team to compute it. Solo operators need the actual fields: which Stripe object to read, how to handle annual plans (÷12), how to treat refunds (subtract in month M only, never retro-delete), how to roll up by month (frozen snapshot on the 5th of next month). This methodology fixes ONE formula per metric so reported numbers stop drifting between investor updates, support replies, and the founder's head.

**Ефективно для:**

- Solo SaaS operator reporting MRR in investor updates, public dashboards, or weekly review.
- Migrating off ChartMogul/Baremetrics to a single sheet (when MRR &lt; $50k).
- Calibrating churn definition between gross and net before quoting it externally.
- Fixing number drift caused by retroactive Stripe backfills.

## Applies If (ALL must hold)

- Product bills recurring revenue via Stripe / Paddle / Lemon Squeezy.
- Operator is the only person reporting financials.
- MRR is between $0 and $50k.
- Monthly + annual plans coexist (or will soon).

## Skip If (ANY kills it)

- Billing is one-off purchases (no recurring) — use a different revenue dashboard.
- Finance team owns the source of truth — don't fork it.
- MRR &gt; $50k and a real subscription-analytics tool (ChartMogul / Baremetrics) already runs.
- Multi-product SaaS where MRR mix is non-trivial — needs a richer breakout.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Read-only Stripe API key with `subscriptions:read` and `invoices:read` | env var | platform |
| Google Sheet / Notion / Coda surface to host the dashboard | sheet | operator |
| List of all active plans with `interval` (month/year) and `unit_amount` | sheet | operator |
| Closed-snapshot tab (append-only) | sheet | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[side-project-financial-runway]] | MRR feeds the leave-job runway model. |
| [[solo-burnout-tripwires]] | MRR-to-effort tripwire reads the canonical MRR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: annual÷12, refunds subtract not retro, frozen snapshot 5th, single formula per metric, customer = subscription not user | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for the monthly dashboard artefact + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: annual-as-spike, retro-delete-refund, definition-drift | ~600 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `stripe_fetch` | haiku | Read-only API pull. |
| `metric_compute` | haiku | Deterministic per-formula. |
| `snapshot_freeze` | haiku | Append-only write. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dashboard-spec.json` | One-month dashboard skeleton |
| `templates/formula-card.md` | One-pager: 5 canonical formulas |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-mrr-dashboard-template.py` | Validate monthly dashboard artefact against 02-output-contract schema | 5th of every month |

## Related

- [[side-project-financial-runway]]
- [[solo-burnout-tripwires]]
- [[reporting-dashboards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by plan interval handling, refund treatment, snapshot freshness, formula multiplicity, and customer definition onto a rule from `content/01-core-rules.xml`. Walk it on the 5th of every month before publishing investor updates.
