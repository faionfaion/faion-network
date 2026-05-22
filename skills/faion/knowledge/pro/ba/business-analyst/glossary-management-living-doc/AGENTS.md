---
slug: glossary-management-living-doc
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Lifecycle methodology for a project glossary: intake, definition, conflict resolution, deprecation, propagation to dev/QA/support so the same term means the same thing everywhere.
content_id: "77df93bd5c7e79d9"
tags: [ba, glossary, ubiquitous-language, terminology, traceability, ddd]
---

# Glossary Management (Living Doc)

## Summary

**One-sentence:** A glossary lifecycle that turns project terminology from a stale Confluence page into a versioned, intake-managed, conflict-resolved living document that propagates to dev / QA / support docs.

**One-paragraph:** Solves the recurring BA pain where business terms drift between PRDs, code, tests, and support copy until the team is debating which "customer" the bug ticket means. Mechanism: define a single intake channel for new terms, a definition template (term, definition, scope, owner, status, examples, aliases, conflicts-with), a resolution path for conflicts (pick winner OR split into two terms), a deprecation flow (mark term deprecated, route to replacement, track usage to zero), and propagation hooks into product docs, code constants, test plans, and support macros. Primary output: a glossary entry that travels with the term across every artifact in the project.

## Applies If (ALL must hold)

- project has >= 3 distinct stakeholder groups (e.g., product, eng, support)
- >= 1 documented incident traceable to terminology drift (bug from misinterpreted requirement, mistargeted support reply)
- a documentation surface exists (Confluence, Notion, internal wiki, repo /docs) where the glossary will live
- BA or product owner is willing to be the glossary maintainer (single owner, not committee)

## Skip If (ANY kills it)

- single-person team — implicit shared vocabulary is sufficient until team grows
- one-off project with no expected maintenance phase — glossary debt does not accumulate
- product is consumer-facing with stable, well-known vocabulary (e.g., e-commerce: "cart", "checkout") — glossary effort yields little
- team unwilling to update glossary as part of every PRD / spec — without enforcement, glossary stays stale

## Prerequisites

- single named glossary maintainer (the BA, by default)
- documentation tool with versioning + search
- existing terminology debt inventory (list of terms suspected to drift)
- agreement that PRDs and specs MUST link to glossary entries for new terms

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/requirements-traceability` | Glossary entries link to requirement IDs; traceability consumes this |
| `pro/ba/business-analyst/ubiquitous-language-ddd` | DDD ubiquitous-language patterns inform glossary scope per bounded context |
| `pro/comms/hr-recruiter/onboarding-pack` | New-hire onboarding references the glossary; consume the hook spec |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: single-source-of-truth, scoped-definitions, conflict-resolution-protocol, deprecation-with-replacement, propagation-hook-required | ~1000 |
| `content/02-output-contract.xml` | essential | Glossary-entry schema + intake / deprecation / conflict-resolution contracts + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (term sprawl, ghost terms, scope explosion, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `term_extraction_from_doc` | haiku | Scan PRD / spec, propose new terms not yet in glossary |
| `definition_drafting` | sonnet | Synthesize a candidate definition from usage contexts |
| `conflict_resolution_proposal` | opus | When two definitions collide, requires deep synthesis across stakeholders |
| `propagation_diff_check` | sonnet | Compare glossary entry vs code constants / test plan / support macros |

## Templates

| File | Purpose |
|------|---------|
| `templates/glossary-entry.json` | JSON Schema for one term entry |
| `templates/glossary-page.md` | Markdown page template for the maintained glossary surface |
| `templates/conflict-resolution-record.md` | Record of a resolution: parties, dispute, decision, date |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-glossary-entry.py` | Validates entry against schema + checks for circular alias chains | On every glossary edit |
| `scripts/term-usage-audit.py` | Scans docs / code / tests for term usage, flags terms missing from glossary OR deprecated terms still in use | Weekly + at every release |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodologies: `requirements-traceability`, `ubiquitous-language-ddd`, `acceptance-criteria-quality`
- external: [Domain-Driven Design (Evans, 2003)](https://www.domainlanguage.com/ddd/) · [Diataxis Documentation Framework](https://diataxis.fr/) · [Google Tech Writing Glossary Guide](https://developers.google.com/tech-writing/two/glossaries)
