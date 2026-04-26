# Agile BA Frameworks

## Summary

A mapping of business analysis competencies onto Scrum ceremonies and scaled agile framework (SAFe) levels. Defines what a BA does in each Scrum phase (Sprint 0, refinement, planning, execution, review, retrospective) and at each SAFe level (Team, Program, Large Solution, Portfolio). Includes agile-specific techniques (user story mapping, example mapping, story splitting, impact mapping, event storming) and the relevant certifications (AAC, SAFe SA, POPM, CPOA).

## Why

Business analysts struggle to find their role in agile frameworks: SAFe does not define a BA role; traditional BA activities do not map to sprints; BAs either disappear from teams or duplicate Product Owner work. An explicit mapping shows where BA skills (domain modeling, dependency analysis, capability definition) add value that Product Owners cannot cover alone.

## When To Use

- Onboarding a BA into a Scrum team that has never had a dedicated BA function
- Scaling from one Scrum team to a SAFe program and needing to define BA responsibilities at program and portfolio levels
- Sprint retrospective revealed that stories arrive at planning without sufficient detail — BA process needs to be inserted upstream
- Team is adopting BDD (Cucumber, SpecFlow) and needs a BA to drive example mapping and acceptance criteria authoring
- Organization is evaluating agile BA certifications for team members

## When NOT To Use

- Kanban or continuous-flow teams without sprint boundaries — the sprint-phase mapping does not apply
- Teams where the Product Owner already performs all BA activities and the overhead of a BA role is not justified
- Pure technical/infrastructure work where there are no business stakeholder requirements to elicit
- SAFe adoption is not yet decided — apply plain Scrum BA practices first, scale only when teams exist at multiple levels

## Content

| File | What's inside |
|------|---------------|
| `content/01-scrum-mapping.xml` | BA activities per Scrum phase, response-time target for ad-hoc clarification, Sprint 0 responsibilities |
| `content/02-safe-mapping.xml` | SAFe level-to-BA-role mapping, key activities per level, certifications with salary data |
| `content/03-techniques.xml` | Agile BA techniques with when-to-use guidance (story mapping, example mapping, story splitting, impact mapping, event storming) |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-ba-activities.md` | Sprint activity checklist: pre-sprint refinement, planning, execution, review, and retrospective BA tasks |
