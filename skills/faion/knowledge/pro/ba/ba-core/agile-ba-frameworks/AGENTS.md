# Agile BA Frameworks

## Summary

Maps BA competencies to agile frameworks (Scrum, SAFe, Disciplined Agile, IIBA Agile Extension) so an analyst can choose a canonical framework, audit adherence against the IIBA seven principles, and generate a framework-fit report. Distinct from the operational sprint-cadence BA work; this layer covers framework selection and constitution-level decisions.

## Why

71% of BAs practice agile yet scaled agile frameworks do not define an explicit BA role. Without a principled framework selection, teams conflate ceremonies with practices and organisations repeatedly litigate the same "where does the BA fit?" question. IIBA Agile Extension v2's seven principles provide an auditable checklist; Disciplined Agile supplies lifecycle-choice tooling; both are testable against project evidence.

## When To Use

- Picking an agile BA framework for a new initiative before the team commits to Scrum/SAFe/DA.
- Auditing an existing delivery against IIBA Agile Extension's seven principles to produce a gap report.
- Mapping BABOK v3 knowledge areas onto an agile horizon when a BA function migrates from waterfall.
- Choosing between Disciplined Agile lifecycles using the DA "Way of Working" decision tree.
- Writing a constitution or playbook section that codifies "how we do agile BA" with official source references.
- Preparing IIBA Agile Analysis Certification (AAC) study material or competency self-assessment.

## When NOT To Use

- Day-to-day backlog refinement and sprint-cadence artifact generation — use the business-analyst variant.
- Single-team Scrum with no scaling concern and no regulatory traceability need — overhead is not justified.
- Greenfield product discovery — use continuous-discovery, user-story-mapping, strategy-analysis instead.
- Non-software domains (marketing ops, HR change) — frameworks lean software; misapplied vocabulary creates false precision.
- Pure tooling questions (Jira API, Linear webhooks) — frameworks here are vendor-neutral.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework-overview.xml` | BA role in Scrum ceremonies and SAFe levels; five key BA responsibilities in scaled agile. |
| `content/02-framework-selection.xml` | IIBA seven principles audit, DA lifecycle decision rules, framework comparison matrix, agent workflow for fit assessment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-fit.md` | Framework comparison matrix and IIBA seven-principles scorecard skeleton. |
| `templates/sprint-ba-activities.md` | Per-ceremony BA activity checklist for Scrum sprints. |
