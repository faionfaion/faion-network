---
slug: agile-ba-frameworks
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A mapping of business analysis competencies onto Scrum ceremonies and scaled agile framework (SAFe) levels.
content_id: "93920e12432fb573"
tags: [agile, scrum, safe, business-analysis, frameworks]
---
# Agile BA Frameworks

## Summary

**One-sentence:** A mapping of business analysis competencies onto Scrum ceremonies and scaled agile framework (SAFe) levels.

**One-paragraph:** A mapping of business analysis competencies onto Scrum ceremonies and scaled agile framework (SAFe) levels. Defines what a BA does in each Scrum phase (Sprint 0, refinement, planning, execution, review, retrospective) and at each SAFe level (Team, Program, Large Solution, Portfolio). Includes agile-specific techniques (user story mapping, example mapping, story splitting, impact mapping, event storming) and the relevant certifications (AAC, SAFe SA, POPM, CPOA).

## Applies If (ALL must hold)

- Onboarding a BA into a Scrum team that has never had a dedicated BA function
- Scaling from one Scrum team to a SAFe program and needing to define BA responsibilities at program and portfolio levels
- Sprint retrospective revealed that stories arrive at planning without sufficient detail — BA process needs to be inserted upstream
- Team is adopting BDD (Cucumber, SpecFlow) and needs a BA to drive example mapping and acceptance criteria authoring
- Organization is evaluating agile BA certifications for team members

## Skip If (ANY kills it)

- Kanban or continuous-flow teams without sprint boundaries — the sprint-phase mapping does not apply
- Teams where the Product Owner already performs all BA activities and the overhead of a BA role is not justified
- Pure technical/infrastructure work where there are no business stakeholder requirements to elicit
- SAFe adoption is not yet decided — apply plain Scrum BA practices first, scale only when teams exist at multiple levels

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

- parent skill: `pro/ba/business-analyst/`
