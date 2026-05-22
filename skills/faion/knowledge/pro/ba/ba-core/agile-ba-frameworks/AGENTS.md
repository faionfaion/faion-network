---
slug: agile-ba-frameworks
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Maps BA competencies to agile frameworks (Scrum, SAFe, Disciplined Agile, IIBA Agile Extension) so an analyst can choose a canonical framework, audit adherence against the IIBA seven principles, and generate a framework-fit report.
content_id: "93920e12432fb573"
tags: [agile, framework, ba, scrum, safe]
---
# Agile BA Frameworks

## Summary

**One-sentence:** Maps BA competencies to agile frameworks (Scrum, SAFe, Disciplined Agile, IIBA Agile Extension) so an analyst can choose a canonical framework, audit adherence against the IIBA seven principles, and generate a framework-fit report.

**One-paragraph:** Maps BA competencies to agile frameworks (Scrum, SAFe, Disciplined Agile, IIBA Agile Extension) so an analyst can choose a canonical framework, audit adherence against the IIBA seven principles, and generate a framework-fit report. Distinct from the operational sprint-cadence BA work; this layer covers framework selection and constitution-level decisions.

## Applies If (ALL must hold)

- Picking an agile BA framework for a new initiative before the team commits to Scrum/SAFe/DA.
- Auditing an existing delivery against IIBA Agile Extension's seven principles to produce a gap report.
- Mapping BABOK v3 knowledge areas onto an agile horizon when a BA function migrates from waterfall.
- Choosing between Disciplined Agile lifecycles using the DA "Way of Working" decision tree.
- Writing a constitution or playbook section that codifies "how we do agile BA" with official source references.
- Preparing IIBA Agile Analysis Certification (AAC) study material or competency self-assessment.

## Skip If (ANY kills it)

- Day-to-day backlog refinement and sprint-cadence artifact generation — use the business-analyst variant.
- Single-team Scrum with no scaling concern and no regulatory traceability need — overhead is not justified.
- Greenfield product discovery — use continuous-discovery, user-story-mapping, strategy-analysis instead.
- Non-software domains (marketing ops, HR change) — frameworks lean software; misapplied vocabulary creates false precision.
- Pure tooling questions (Jira API, Linear webhooks) — frameworks here are vendor-neutral.

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

- parent skill: `pro/ba/ba-core/`
