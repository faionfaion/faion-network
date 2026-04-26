# Financial Basics and Tracking

## Summary

Foundation financial tracking for solo and small-team SaaS/info-product businesses: revenue by source, expense categorization by percentage targets, monthly P&L model, and unit economics (LTV, CAC, gross margin, payback period, Rule of 40). The core rule: reconcile monthly within the first 5 days of the next month, separate personal and business banking from day 1, and define "customer" once — never change the formula silently.

## Why

Founders who do not track numbers cannot distinguish profitable from unprofitable growth, cannot forecast runway, and cannot make spend decisions. LTV:CAC below 3:1 signals the acquisition engine is broken; payback over 12 months signals cash-flow risk. Gross margin below 70% in a SaaS business points to structural COGS problems. These signals are invisible without monthly tracking.

## When To Use

- Bootstrapping financial visibility for the first time
- Generating a monthly P&L from Stripe + bank + accounting data
- Computing unit economics on demand from MRR/churn/ad-spend feeds
- Detecting expense-category drift (e.g. marketing exceeds 30% of revenue)
- Pre-investor or pre-acquisition: producing a clean unit-economics snapshot

## When NOT To Use

- Tax filing, audit, or official tax return work — needs a CPA
- Multi-currency consolidation with hedging — out of scope
- Equity, options, 409A valuations, cap tables — corporate finance domain
- Anything touching reg-CF, Reg-A, or public-market reporting
- Fraud investigation — agents can flag anomalies but cannot adjudicate

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Revenue tracking, expense categories with target percentages, P&L structure, financial ratios |
| `content/02-unit-economics.xml` | LTV/CAC/payback formulas, healthy ranges, Rule of 40, example calculations |
| `content/03-agent-rules.xml` | Agent safety rules: categorization drift, Stripe MRR pitfalls, chargeback lag, privacy constraints |

## Templates

| File | Purpose |
|------|---------|
| `templates/unit-economics.py` | Unit-economics snapshot: LTV, CAC, LTV:CAC, payback months, health flags |
| `templates/monthly-pnl.md` | Monthly P&L template: revenue, COGS, gross profit, OpEx, net profit |
