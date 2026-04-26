# Roadmap Design

## Summary

A roadmap is a strategic communication tool showing where the product is going and why — not a feature list with dates. Choose the format by uncertainty level: Now-Next-Later for medium uncertainty (default), timeline for committed work, outcome-themed for high uncertainty. Every initiative must link to a stated objective; every theme must have a measurable success metric.

## Why

Timeline roadmaps with hard dates always slip and erode trust. Now-Next-Later rarely does, because it communicates priority sequence without false precision. Linking every initiative to an objective prevents roadmaps from becoming wish lists and gives stakeholders a reason to agree with the ordering.

## When To Use

- Quarterly planning where strategy must be communicated to team, stakeholders, or customers.
- After RICE/MoSCoW prioritization — the roadmap is the consumable form of those rankings.
- Multiple audiences (engineering, sales, customers) need different slices of the same plan.
- Strategic alignment check: does planned work actually drive stated objectives?

## When NOT To Use

- Less than 4 weeks of work ahead — a sprint plan or kanban suffices.
- Pre-PMF discovery phase — use opportunity solution trees and continuous-discovery instead.
- High-uncertainty research with no shippable outcome — write a research charter instead.
- One-person, one-week feature — overhead is not justified.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Roadmap types, format decision matrix, 5-step design process, confidence levels |
| `content/02-examples.xml` | B2B SaaS and solo product Now-Next-Later roadmap examples |
| `content/03-antipatterns.xml` | Common failures: feature-date lists, "Later" rot, single artifact for all audiences |

## Templates

| File | Purpose |
|------|---------|
| `templates/now-next-later.md` | Internal roadmap with themes, confidence levels, dependencies, and "not doing" section |
| `templates/quarterly-outcome.md` | Quarterly roadmap tied to OKRs with initiative table per theme |
| `templates/external-roadmap.md` | Customer-facing roadmap with capability descriptions and disclaimer |
| `templates/roadmap-diff.py` | Script: diff two roadmap JSON snapshots and report moved/added/dropped initiatives |
