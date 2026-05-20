---
slug: account-health-scoring-model
tier: pro
group: product
domain: product-operations
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "f700c890e089bec4"
summary: Green/yellow/red account health score model for micro-agencies with sub-20 retainer clients, built from observable signals not just NPS.
tags: [account-health, retention, customer-success, micro-agency, scoring, qbr]
---
# Account Health Scoring Model (Sub-20 Accounts)

## Summary

**One-sentence:** Green/yellow/red account health score model for micro-agencies with sub-20 retainer clients, built from observable signals not just NPS.

**One-paragraph:** Generic retention metrics (NPS, churn rate, MRR) work at SaaS scale (1000+ customers) but mislead at micro-agency scale (3-20 retainer clients) where each client is statistically unique. Mechanism: score each account on 6 observable signals — (1) retainer utilization variance, (2) decision-maker engagement frequency, (3) scope-creep delta vs. SOW, (4) payment punctuality, (5) referral / advocacy signal, (6) executive sponsor stability. Each signal scores 0/1/2; sum → green (10-12), yellow (5-9), red (0-4). Run weekly; trigger a retention action when score drops 2+ in a week or sits red for 2 consecutive weeks. Primary output: account-health dashboard + escalation triggers.

## Applies If (ALL must hold)

- you operate a service business with 3-20 active retainer clients
- you have at least 3 months of history on signals (utilization, invoices, communications)
- the same person owns "account health" across clients (you, the founder, or one account lead)
- retention is the priority over net-new growth this quarter

## Skip If (ANY kills it)

- &gt; 20 accounts — sample size for SaaS-style scoring becomes viable, use NPS + cohort analysis instead
- &lt; 3 accounts — every account is bespoke, scoring overhead exceeds value
- pre-retainer pipeline (sales lead scoring) — different signals, different rubric
- one-shot project model — no recurring revenue to retain

## Prerequisites (must be true before starting)

- retainer utilization data per client (hours used, hours bought, by month)
- communication log (Slack/email cadence per client)
- invoice payment record (issued date → paid date)
- SOW scope text per client + a record of scope-creep incidents
- list of decision-makers and executive sponsors per account
- prior 3-month history for each signal

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/quarterly-retainer-review-script` | QBR cadence consumes the health score for slide 2 |
| `pro/marketing/gtm-strategist/ops-customer-success-metrics` | Source of utilization + engagement signals |
| `pro/pm/project-manager/agency-pnl-tracker-template` | Provides revenue-side weighting for tier mapping |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 6-signal model, observable not opinion, threshold cutoffs, weekly cadence, escalation triggers | ~900 |
| `content/02-output-contract.xml` | essential | Per-account score schema, weekly dashboard schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (NPS-only, founder optimism bias, signal staleness, no escalation action, score laundering, sample-size confusion) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_signal_scoring` | haiku | Deterministic 0/1/2 mapping from numeric thresholds |
| `weekly_dashboard_rollup` | haiku | Template fill: score per account + trend arrow |
| `escalation_trigger_synthesis` | sonnet | Cross-signal reasoning: which combination is red flag |
| `retention_action_recommendation` | opus | Cross-input judgment — recommended action per red account |

## Templates

| File | Purpose |
|------|---------|
| `templates/account-health-card.md` | Per-account score card with 6 signals, trend, action |
| `templates/weekly-dashboard.md` | All accounts on one page with traffic-light status |
| `templates/signal-thresholds.md` | The cutoffs for each 0/1/2 score per signal |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-account-health.py` | Pull signals from sources, produce per-account score | Weekly (Mondays) |
| `scripts/detect-escalation-trigger.py` | Flag accounts hitting trigger conditions | After scoring |

## Related

- parent skill: `pro/product/product-operations/`
- peer methodologies: `quarterly-retainer-review-script`, `agency-pnl-tracker-template`, `retainer-conversion-script`
- external: [Gainsight Customer Health Scoring](https://www.gainsight.com/guides/customer-health-score/) · [ChurnZero Playbook](https://churnzero.com/blog/customer-health-score/) · [SaaSholic Mid-market CS](https://saastr.com/)
