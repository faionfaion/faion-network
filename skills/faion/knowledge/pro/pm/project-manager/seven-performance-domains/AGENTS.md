---
slug: seven-performance-domains
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: PMBoK 8 reorganises project management into seven performance domains: Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk.
content_id: "bced1b3067d8a829"
tags: [pmbok, domains, governance, project-planning, audit]
---
# Seven Performance Domains (PMBoK 8)

## Summary

**One-sentence:** PMBoK 8 reorganises project management into seven performance domains: Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk.

**One-paragraph:** PMBoK 8 reorganises project management into seven performance domains: Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk. Quality, Communications, and Procurement are integrated throughout rather than standalone domains. Each domain maps to observable artefacts and measurable outcomes. The canonical domain list is fixed — agents must never invent an 8th domain or reintroduce "Integration Management" or "Quality" as standalone items.

## Applies If (ALL must hold)

- Structuring a project charter or status pack around a known taxonomy (charter → closure)
- Auditing an existing project plan: walk each domain and surface missing artefacts
- Building a weekly project status dashboard (one panel per domain, RAG per outcome)
- Tailoring methodology selection — domains are stable; processes inside them vary by approach
- Onboarding a PM agent: seven domains is the smallest anchor that still covers everything

## Skip If (ANY kills it)

- Pure-Scrum teams with Product Owner / Scrum Master where Scrum events already cover domains implicitly — domain mapping is busywork
- Solopreneur projects under 1 week with a single deliverable — governance and finance collapse to "did I ship, did I get paid"
- Shops still on PMBoK 6 (process groups + knowledge areas) in mid-project — switching narrative mid-project confuses sponsors
- Domain-driven design conversations — the word "domain" overloads the term

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
