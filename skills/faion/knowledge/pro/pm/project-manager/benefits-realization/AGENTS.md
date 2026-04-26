# Benefits Realization

## Summary

Identify, quantify, assign ownership for, and track the business value that a project is expected to deliver after go-live. A Benefits Register stores each benefit with metric, baseline (frozen before launch), target, owner, and source system. The rule: every benefit must have a quantified target and a named owner before project approval — "soft benefits" without a metric do not count.

## Why

Projects routinely complete on time and on budget while delivering zero measurable business value. The gap is that outputs (a CRM system) do not automatically become outcomes (sales team adoption) or benefits (20% more deals closed). Benefits realization closes this loop by making post-delivery measurement a first-class project artefact, accountable to a business owner who survives project close.

## When To Use

- Business case approval requiring quantified ROI and a tracking plan
- Post-launch benefits review (3, 6, 12 months) across a project portfolio
- Investment committee asking "did the last N projects pay back?"
- Programs spanning years where outputs precede outcomes by 6-18 months
- PMO maturity step: adopting outcome-based metrics over output-based

## When NOT To Use

- Pre-revenue startup pre-PMF — benefits are speculative; track learning milestones instead
- Compliance-driven projects where the benefit is "stay legal" (binary, not quantifiable)
- Internal tooling with weak baseline data (no measurable "before" state)
- Crisis incident response — the benefit is "stopped bleeding", not a trackable KPI

## Content

| File | What's inside |
|------|---------------|
| `content/01-benefits-framework.xml` | Six-step process: identify, quantify, assign, plan, track, report; output/outcome/benefit distinction |
| `content/02-benefits-antipatterns.xml` | Common failures: no baseline, wrong owner, ignored after go-live, attribution errors, AI productivity over-claim |

## Templates

| File | Purpose |
|------|---------|
| `templates/benefits-register.md` | Register table: ID, benefit, category, owner, metric, baseline, target, status |
| `templates/benefits-report.md` | Post-launch report: executive summary, status per benefit, barriers, forecast |
| `templates/business-case-benefits.md` | Business case section: financial table (3-year), non-financial table, ROI/NPV |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/benefits-track.py` | Pull current metric values vs target from Looker/CSV, emit JSON status and % realized |
| `scripts/diff-in-diff.py` | Quick difference-in-differences for benefit attribution (ATT estimation) |
