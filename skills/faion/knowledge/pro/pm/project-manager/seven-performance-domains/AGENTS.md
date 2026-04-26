# Seven Performance Domains (PMBoK 8)

## Summary

PMBoK 8 reorganises project management into seven performance domains: Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk. Quality, Communications, and Procurement are integrated throughout rather than standalone domains. Each domain maps to observable artefacts and measurable outcomes. The canonical domain list is fixed — agents must never invent an 8th domain or reintroduce "Integration Management" or "Quality" as standalone items.

## Why

Domains are the smallest mental model that covers the full scope of a project. Each project artefact belongs under exactly one domain, making gap analysis mechanical: walk the seven, check artefact presence, flag missing ones as risks. PMBoK 8 replaces PMBoK 7's eight domains (Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) and PMBoK 6's ten knowledge areas, so teams migrating between editions need a translation layer.

## When To Use

- Structuring a project charter or status pack around a known taxonomy (charter → closure)
- Auditing an existing project plan: walk each domain and surface missing artefacts
- Building a weekly project status dashboard (one panel per domain, RAG per outcome)
- Tailoring methodology selection — domains are stable; processes inside them vary by approach
- Onboarding a PM agent: seven domains is the smallest anchor that still covers everything

## When NOT To Use

- Pure-Scrum teams with Product Owner / Scrum Master where Scrum events already cover domains implicitly — domain mapping is busywork
- Solopreneur projects under 1 week with a single deliverable — governance and finance collapse to "did I ship, did I get paid"
- Shops still on PMBoK 6 (process groups + knowledge areas) in mid-project — switching narrative mid-project confuses sponsors
- Domain-driven design conversations — the word "domain" overloads the term

## Content

| File | What's inside |
|------|---------------|
| `content/01-domains.xml` | Seven canonical domains with key artefacts, outcomes, and integrated areas; PMBoK 7 → 8 delta |
| `content/02-domain-audit.xml` | Domain audit workflow, gap-to-risk mapping, agent rules for fixed output ordering |

## Templates

| File | Purpose |
|------|---------|
| `templates/domain-audit.py` | Python: walk seven domains against a project root, emit JSON gap matrix |
