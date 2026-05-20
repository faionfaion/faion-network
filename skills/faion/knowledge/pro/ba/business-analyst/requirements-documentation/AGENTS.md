---
slug: requirements-documentation
tier: pro
group: ba
domain: business-analyst
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured methodology for documenting requirements across the hierarchy: business requirements (why), stakeholder requirements (user needs), and solution requirements (functional and non-functional).
content_id: "0b8ba53b7d51c38b"
tags: [requirements, documentation, babok, acceptance-criteria, specification]
---
# Requirements Documentation

## Summary

**One-sentence:** A structured methodology for documenting requirements across the hierarchy: business requirements (why), stakeholder requirements (user needs), and solution requirements (functional and non-functional).

**One-paragraph:** A structured methodology for documenting requirements across the hierarchy: business requirements (why), stakeholder requirements (user needs), and solution requirements (functional and non-functional). Uses SMART criteria, acceptance criteria in Given/When/Then form, and a requirements baseline to enable traceability, testing, and change control. Without documentation: requirements exist only in people's heads, different team members have different understanding, developers build the wrong thing, testing cannot verify, and changes cannot be tracked.

## Applies If (ALL must hold)

- Producing the canonical spec.md for an SDD feature: business requirements (BR), stakeholder requirements, functional requirements (FR), non-functional requirements (NFR), and acceptance criteria — all in one machine-readable document.
- Migrating loose Notion / Confluence / Google Doc requirement notes into a Markdown + YAML-frontmatter requirements/REQ-XXX.md repository that diff/grep/Git can manage.
- Generating a Business Requirements Document (BRD) for stakeholder sign-off when an SDD spec is too dense for non-technical readers — a parallel artefact, not a replacement.
- Translating user-story backlogs (Jira, Linear, GitHub Issues) into the standard REQ-XXX format for regulated review (audits, SOC2, ISO).
- Pairing with requirements-traceability, requirements-lifecycle, and requirements-validation to close the Document → Trace → Validate loop.
- Pre-development: enforcing structure before code. Acceptance criteria in Given/When/Then form become Playwright/pytest scaffolds via codegen.

## Skip If (ANY kills it)

- Solo founder pre-PMF: a BRD is theatre when the spec changes weekly. Use opportunity-solution-trees plus living user stories.
- Pure ops tasks (cron edits, nginx vhost tweaks, infra rotations) — runbooks, not requirement docs.
- Discovery spikes whose deliverable is a learning, not a baseline — use research notes and a stop condition.
- When stakeholders refuse written sign-off — without an Approved gate, the document degrades to a status spreadsheet.
- One-off scripts where the cost of writing REQ-XXX exceeds the cost of just rewriting the script.

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
