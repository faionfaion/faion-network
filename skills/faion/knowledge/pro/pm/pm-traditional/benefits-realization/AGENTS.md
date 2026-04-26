# Benefits Realization

## Summary

Benefits realization tracks whether a project's promised business outcomes actually materialize after delivery. Each claimed benefit requires a named business-stakeholder owner (not the PM), a baseline measurement before go-live, a quantified target, a declared metric source, and a realization curve across multiple post-launch periods to detect benefit decay.

## Why

Projects deliver outputs; organizations must achieve outcomes to realize benefits. Without pre-launch baselines and post-launch tracking, "before" is unknown and "after" is unverifiable. Investment decisions for future projects are then made on claimed — not measured — ROI. Benefits that are not tracked within six months of go-live are rarely measured at all.

## When To Use

- Capital programs and transformation initiatives where the business case promised quantitative benefits (revenue, cost savings, NPS, cycle time).
- Portfolios where investment prioritization needs evidence: post-launch measurement informs the next funding round.
- Public-sector or regulated programs requiring benefit reporting (NHS, GDS, EU funding rules).
- ERP / CRM / cloud migration programs that historically delivered outputs but failed to deliver outcomes.
- M&A integrations where synergy realization is part of the deal thesis.

## When NOT To Use

- Pre-PMF startups — benefit realization assumes a stable benefit hypothesis; PMF is itself the benefit.
- Pure R&D / option-creating projects where the value is learning, not delivery.
- Projects whose benefits are entirely indirect or strategic — track those qualitatively.
- Tactical one-off projects under $50k where measurement cost exceeds benefit insight.
- Programs without a named benefit owner — without a business stakeholder accountable, tracking is theatre.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Output vs. outcome vs. benefit distinction; benefit types; six-step framework |
| `content/02-rules.xml` | Rules for benefit ownership, baseline discipline, attribution, decay tracking, and agentic workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/benefits-register.md` | Benefits register template with ID, owner, metric, baseline, target, status |
| `templates/realization-report.md` | Post-launch benefit realization report template with RAG status |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/benefits_status.py` | Computes realization % and RAG (GREEN/YELLOW/RED) from register.yaml + measurements.yaml |
