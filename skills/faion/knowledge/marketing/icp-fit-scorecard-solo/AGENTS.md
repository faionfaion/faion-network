# ICP Fit Scorecard (Solo)

## Summary

**One-sentence:** Per-customer ICP score (0-100) across 5 weighted signals — pain, budget, urgency, fit, accessibility — driving a keep / nurture / remove decision and onboarding tone per customer.

**One-paragraph:** Solo founders cannot afford "all customers welcome". This scorecard scores each active and prospective customer on 5 signals — pain match (0-25), budget fit (0-20), urgency (0-15), product fit (0-25), accessibility (0-15) — summing to 0-100. Bands route the action: 70+ keep + invest, 40-69 nurture, &lt;40 remove (sunset offer or polite no). Re-scored quarterly. Output is a row per customer in a flat sheet + an aggregated histogram + a monthly remove-list for proactive sunsetting.

**Ефективно для:**

- Solo SaaS with 30-300 customers and a known anti-ICP problem (high-support customers from outside the target band).
- Quarterly persona / pricing recalibration where you need real per-customer evidence, not gut feel.
- Onboarding-tone tuning: keep customers get founder-touch, nurture get default flow, remove get a sunset email.
- Building a defensible signal for raise-prices conversations ("we removed N customers, the remaining cohort scores 60+").

## Applies If (ALL must hold)

- Operator has 30+ active customers and can pull per-customer activity + revenue data.
- Operator has authority to remove customers (sunset offer, refund, polite no) — not blocked by contract.
- A documented ICP persona exists (even if rough).
- The cost of supporting a bad-fit customer is non-trivial (≥1h support/month per).

## Skip If (ANY kills it)

- Fewer than 30 customers — anchoring on so few is over-fitting; iterate qualitatively first.
- Pure transactional product where every customer is one-time — scorecard overhead does not pay back.
- Operator cannot act on the output (no permission to sunset / no budget to invest in keepers).
- All customers are enterprise-procured with multi-year contracts you cannot exit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ICP persona doc | markdown | founder |
| Customer activity export (last 90d) | CSV | analytics |
| Revenue per customer (MRR / LTV) | CSV | billing |
| Support-ticket volume per customer (90d) | CSV | helpdesk |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[pricing-experiment-runbook]] | Scorecard outputs feed the "who to grandfather" decision in a price change. |
| [[hook-bank-template]] | Reply patterns from spiked hooks help refine ICP pain signal. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: 5 weighted signals, 100-cap, band thresholds, quarterly re-score, evidence per signal, remove-action defined | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for customer scorecard rows + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix): vanity-band, no-act, evidence-skip, retro-score | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: gather data → score 5 signals → band → review action → execute → re-score quarterly | 800 |
| `content/05-examples.xml` | essential | Worked example: 80-customer SaaS scoring + remove list of 8 | 700 |
| `content/06-decision-tree.xml` | essential | Tree routing observable signals → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal_score_compute` | haiku | Mechanical arithmetic. |
| `evidence_attachment` | sonnet | Bounded comparison of citation vs claim. |
| `band_decision_review` | sonnet | Apply band thresholds to action set. |
| `remove_communication` | sonnet | Tone-sensitive sunset email per customer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scorecard.csv` | Per-customer scorecard skeleton (one row per customer) |
| `templates/sunset-email.md.j2` | Sunset/remove email template |
| `templates/sunset-email.md` | Sunset/remove email template Generated from `templates/sunset-email.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable scorecard for validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-icp-fit-scorecard-solo.py` | Validate scorecard rows + math against 02-output-contract schema | Pre-commit / quarterly review |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[pricing-experiment-runbook]]
- [[hook-bank-template]]
- [[ih-build-update-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps customer count, ICP persona availability, signal coverage, and authority-to-act to a rule from `01-core-rules.xml`, telling the agent whether to apply the scorecard, block on missing inputs, or skip the methodology entirely. Walk it on every fresh invocation; do not cache outcomes.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/scorecard.csv`

```csv
customer_id,pain_match,budget_fit,urgency,product_fit,accessibility,total,band,evidence_pain,evidence_budget,evidence_urgency,evidence_fit,evidence_access,remove_action_due
cus_REPLACE,0,0,0,0,0,0,nurture,REPLACE,REPLACE,REPLACE,REPLACE,REPLACE,
```

### `templates/_smoke-test.json`

```json
{
  "version": "1.1.0",
  "scored_at": "2026-05-23",
  "rows": [
    {
      "customer_id": "cus_smoke_1",
      "pain_match": 22,
      "budget_fit": 18,
      "urgency": 12,
      "product_fit": 23,
      "accessibility": 13,
      "total": 88,
      "band": "keep",
      "evidence": {
        "pain_match": "ticket #1 cites exact problem the product solves",
        "budget_fit": "Pro plan since week 1",
        "urgency": "deadline in onboarding survey",
        "product_fit": "uses 7 of 8 core features",
        "accessibility": "responds within 24h"
      }
    }
  ],
  "histogram": {
    "keep": 1,
    "nurture": 0,
    "remove": 0,
    "median": 88
  },
  "remove_list": []
}
```
