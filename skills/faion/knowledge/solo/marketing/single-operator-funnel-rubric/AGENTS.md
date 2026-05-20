---
slug: single-operator-funnel-rubric
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Single Operator Funnel Rubric — a Friday-metrics diagnostic for solo founders that maps visit → signup → paid → retained to one-person evidence sources without an analytics team.
content_id: "8a087eb8a2016947"
tags: [single-operator-funnel-rubric, marketing, solo]
---
# Single Operator Funnel Rubric

## Summary

**One-sentence:** A four-stage funnel rubric (visit → signup → paid → retained) designed for one person to fill in 20 minutes every Friday using only sources a solo founder already has — no GA setup project, no analytics hire.

**One-paragraph:** Solo founders need to diagnose where the funnel actually breaks but the conventional rubrics assume a marketing team plus a product analyst plus a BI tool. The single-operator rubric maps each stage to one acceptable evidence source the founder already has (e.g. Plausible / Cloudflare for visits, Stripe for paid, Postgres count for retained) and refuses to add a stage the founder cannot measure honestly. The output is a single Friday-evening pulse that compounds week-over-week and surfaces the broken stage before MRR damage.

## Applies If (ALL must hold)

- a one-person operator runs the entire revenue funnel (no analytics support)
- the product has a measurable signup event and a paid conversion event
- the founder can spare a recurring 20-minute Friday slot
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- a marketing team / analyst already owns funnel reporting
- the product has no payment events yet (the rubric assumes paid is a real stage)
- the founder cannot honestly measure even one stage (fix instrumentation first)

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: four-stage cap, one evidence source per stage, week-over-week deltas, broken-stage flag, 20-minute time budget |

## Related

- upstream playbook: `p1-solo-saas-builder/Friday metrics check & MRR pulse`
- parent skill: `solo/marketing/`
- related methodology: `solo/marketing/weekly-growth-review-rhythm`
