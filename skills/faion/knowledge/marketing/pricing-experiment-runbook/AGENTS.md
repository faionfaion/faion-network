# Pricing Experiment Runbook (Stripe Solo)

## Summary

**One-sentence:** Run a Stripe-based pricing experiment on a solo SaaS without breaking grandfathered customers — pre-commit plan, pin grandfather coupon, validate Stripe via pre-flight script, force go/no-go memo at end.

**One-paragraph:** `ops-pricing-strategy` covers pricing models in the abstract; this runbook covers the operational mechanics of actually changing a price on Stripe in production. Failures are concrete: grandfathered customers accidentally re-billed at the new price, currency-conversion errors at the EU VAT moment, refund-storm from a poorly-announced increase, A/B test that statistically never closes. The runbook pins six gates: (1) pre-commit Plan with variant + audience + exposure + duration + metric + termination rule, (2) grandfathering pinned to Stripe coupon or old Price object (never goodwill), (3) scripts/stripe-pre-flight.py green within 7 days of go-live, (4) currency + tax_behavior explicit per Price, (5) measurement instrumented (trial-to-paid, MRR delta, refund rate, support tickets), (6) Decision Memo within 48h of end_date. Primary output: a one-page Plan + Stripe config checklist + post-experiment Decision Memo.

**Ефективно для:**

- Solo SaaS on Stripe Billing with ≥30 active subs running a real price change.
- Migrating between Price objects without churning existing customers.
- Cross-border (multi-currency, multi-tax) pricing experiments.
- Founders who need a forced go/no-go discipline instead of "leave it running".

## Applies If (ALL must hold)

- Product is on Stripe Billing (Subscriptions or Checkout) with at least 30 active subscriptions.
- Founder has Stripe Dashboard access AND Stripe-API access (curl / SDK).
- Proposed pricing change is a real change (price, tier structure, billing period) not a copy edit.
- Founder controls landing page and pricing page (can make timely changes).

## Skip If (ANY kills it)

- Fewer than 30 active subscriptions — statistical inference unreliable; iterate qualitatively first.
- Pricing change is contractually negotiated per customer (enterprise) — handle per-contract, not as an experiment.
- Product uses a non-Stripe processor — Stripe-specific steps do not apply; adapt principles via provider docs.
- Founder is in the middle of a Stripe Radar dispute spike — pricing changes amplify dispute risk; stabilise first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stripe Test Mode environment mirroring live (subs, products, prices) | Stripe account | platform |
| 90-day baseline: MRR, trial-to-paid, churn rate | metrics export | analytics |
| Recipient list for customer-facing announcement | CSV | CRM |
| Tax setup verified (Stripe Tax enabled OR manual VAT/GST configured) | Stripe config | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[gumroad-ops-playbook]] | Sibling channel mechanics; useful when MoR comparison comes up. |
| [[lemon-squeezy-ops-playbook]] | Merchant-of-record alternative when EU VAT load is the issue. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pre-commit plan, grandfather pin, pre-flight, currency/tax explicit, forced decision memo | 900 |
| `content/02-output-contract.xml` | essential | Required fields + forbidden patterns + JSON Schema for plan / preflight / memo | 700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (symptom/root-cause/fix): re-bill, never-closes, refund storm, currency drift, tax mismatch, missing memo | 900 |
| `content/04-procedure.xml` | essential | 7-step procedure: baseline → plan → grandfather → Stripe config → pre-flight → run → memo | 900 |
| `content/05-examples.xml` | essential | Worked example: indie SaaS price bump $19→$29 with 12-month grandfather window | 800 |
| `content/06-decision-tree.xml` | essential | Tree routing observables (subs count, grandfather pinned, pre-flight, dispute spike) → rule id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `experiment_design_pre_commit` | opus | Cross-input synthesis of audience + variant + duration + metric. |
| `stripe_config_checklist_generation` | haiku | Template fill once experiment design is set. |
| `customer_announcement_drafting` | sonnet | Tone-sensitive copy with grandfathering details. |
| `post_experiment_decision_memo` | opus | Cross-metric synthesis: significance + business impact + qualitative signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment-plan.md.j2` | One-page Plan with all required fields |
| `templates/experiment-plan.md` | One-page Plan with all required fields Generated from `templates/experiment-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/stripe-config-checklist.md.j2` | Step-by-step Stripe Dashboard + API checklist |
| `templates/stripe-config-checklist.md` | Step-by-step Stripe Dashboard + API checklist Generated from `templates/stripe-config-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/grandfather-coupon.json` | Stripe coupon JSON template for grandfathering |
| `templates/customer-announcement.md.j2` | Email template for the customer-facing announcement |
| `templates/customer-announcement.md` | Email template for the customer-facing announcement Generated from `templates/customer-announcement.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-memo.md.j2` | Post-experiment go/no-go memo skeleton |
| `templates/decision-memo.md` | Post-experiment go/no-go memo skeleton Generated from `templates/decision-memo.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable plan+preflight+memo for validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pricing-experiment-runbook.py` | Validate plan + preflight + decision memo against 02-output-contract schema | Pre-commit / pre-publish gate |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[gumroad-ops-playbook]]
- [[lemon-squeezy-ops-playbook]]
- [[icp-fit-scorecard-solo]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps subscription count, grandfather mechanism, Stripe pre-flight status, currency coverage, and dispute risk to a rule from `01-core-rules.xml`, telling the agent whether to greenlight the experiment, block on a missing gate, or skip the methodology entirely. Walk it on every fresh invocation; do not cache outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/grandfather-coupon.json`

```json
{
  "id": "grandfather_REPLACE_quarter",
  "name": "Grandfather window \u2014 REPLACE",
  "percent_off": 100,
  "duration": "repeating",
  "duration_in_months": 12,
  "applies_to": {
    "products": [
      "prod_REPLACE_new"
    ]
  },
  "metadata": {
    "experiment_id": "REPLACE-experiment-id",
    "grandfathered_before": "REPLACE-YYYY-MM-DD"
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "plan": {
    "experiment_id": "exp-smoke",
    "start_date": "2026-06-01",
    "end_date": "2026-07-30",
    "duration_days": 60,
    "variant_old": {
      "stripe_price_id": "price_old"
    },
    "variant_new": {
      "stripe_price_id": "price_new"
    },
    "audience": "new_signups_only",
    "exposure_rule": "random 50/50 by signup-id hash",
    "success_metric_primary": "trial_to_paid_conversion_pct",
    "success_metric_threshold": 0.18,
    "significance_target": "p<0.05",
    "guardrail_metrics": [
      "refund_rate",
      "dispute_rate"
    ],
    "grandfathering": {
      "audience": "all subs before start",
      "mechanism": "100% off coupon",
      "stripe_coupon_id": "grandfather_smoke",
      "window_months": 12
    },
    "currencies_in_test": [
      "usd"
    ],
    "tax_behavior": "exclusive"
  },
  "stripe_preflight": {
    "passed_at": "2026-05-28T09:00:00Z",
    "checks_run": [
      "new_price_exists",
      "old_price_active",
      "coupon_attached",
      "no_orphan_subs"
    ]
  },
  "decision_memo": {
    "written_at": "2026-07-31T18:00:00Z",
    "decision": "adopt_new",
    "metric_readouts": {
      "new": 0.21,
      "old": 0.17
    },
    "qualitative_signals": "no spike",
    "next_action": "Move all signups to price_new on 2026-08-01."
  }
}
```
