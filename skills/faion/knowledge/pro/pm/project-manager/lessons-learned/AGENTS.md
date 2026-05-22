---
slug: lessons-learned
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured knowledge-capture process that runs continuously throughout a project, not only at close-out.
content_id: "15d77bd37b2b85c5"
tags: [lessons-learned, postmortem, continuous-improvement, knowledge-management, rca]
---
# Lessons Learned

## Summary

**One-sentence:** Structured knowledge-capture process that runs continuously throughout a project, not only at close-out.

**One-paragraph:** Structured knowledge-capture process that runs continuously throughout a project, not only at close-out. Each lesson requires five fields: Situation (facts), Impact (quantified), Root Cause (5-whys), Lesson (generalizable, two sentences max), Recommendation (action verb + owner role + where applied). Lessons stored in a versioned, searchable repository; application rate tracked as an SLO.

## Applies If (ALL must hold)

- Capturing knowledge during and at the end of a project (milestone close, post-incident, full close-out).
- Building a searchable, structured organizational memory across many projects.
- Onboarding new PMs / engineers with curated patterns and anti-patterns.
- Feeding a continuous-improvement loop: lesson → updated checklist → applied next sprint / project.
- Post-incident reviews (PIR / blameless postmortems) when the incident touched scope / cost / schedule.

## Skip If (ANY kills it)

- One-person, one-week project — overhead exceeds value; a 5-line note in the README is enough.
- Already-mature org with strong RCA culture and a working knowledge base — just contribute, don't re-invent the methodology.
- Live incident — capture facts now, lessons later. Do not derail incident response with a retro.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/pm/project-manager/`
