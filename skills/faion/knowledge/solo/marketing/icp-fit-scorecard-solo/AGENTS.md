---
slug: icp-fit-scorecard-solo
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-customer ICP score (0-100) across 5 weighted signals — pain, budget, urgency, fit, accessibility — driving keep / nurture / remove decisions and onboarding tone.
content_id: "d8397876225ccfbf"
complexity: medium
produces: rubric
est_tokens: 4400
tags: [icp, scoring, anti-customer, onboarding, solo-saas]
---
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
| `templates/sunset-email.md` | Sunset/remove email template |
| `templates/_smoke-test.json` | Minimum viable scorecard for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-icp-fit-scorecard-solo.py` | Validate scorecard rows + math against 02-output-contract schema | Pre-commit / quarterly review |

## Related

- [[pricing-experiment-runbook]]
- [[hook-bank-template]]
- [[ih-build-update-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps customer count, ICP persona availability, signal coverage, and authority-to-act to a rule from `01-core-rules.xml`, telling the agent whether to apply the scorecard, block on missing inputs, or skip the methodology entirely. Walk it on every fresh invocation; do not cache outcomes.
