---
slug: ai-accessibility-automation-2026
tier: geek
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for integrating AI-powered tools into accessibility workflows: automated WCAG scanning, AI-assisted issue triage and code remediation, VPAT 2.
content_id: "5612b610ab8b56d7"
tags: [accessibility, wcag, automation, compliance, a11y]
---
# AI Accessibility Automation 2026

## Summary

**One-sentence:** Methodology for integrating AI-powered tools into accessibility workflows: automated WCAG scanning, AI-assisted issue triage and code remediation, VPAT 2.

**One-paragraph:** Methodology for integrating AI-powered tools into accessibility workflows: automated WCAG scanning, AI-assisted issue triage and code remediation, VPAT 2.5 draft generation, and ADA Title II video captioning pipelines. AI augments detection (covering 60–70% of automatable issues) while humans own AT testing, complex judgment, and legal sign-off.

## Applies If (ALL must hold)

- Establishing a continuous accessibility baseline in CI/CD where every PR is scanned before merge
- Scaling audits across 100+ pages where manual review is impractical
- Generating ADA/VPAT documentation for procurement or legal requirements
- Integrating video captioning and audio description workflows for ADA Title II compliance (2026)
- Post-launch regression monitoring to catch regressions introduced by routine updates

## Skip If (ANY kills it)

- As the only validation method — AI covers 60–70%; the rest requires human + AT testing
- Replacing user testing with people with disabilities — automation cannot validate cognitive accessibility or AT compatibility
- Auditing complex interactive patterns (custom data grids, drag-and-drop, real-time updates) — dynamic AT behavior is not captured by static scanners
- On SPAs requiring authentication without session management — scanners will scan only the login page
- As legal compliance proof without human expert review and sign-off

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

- parent skill: `geek/ux/ux-ui-designer/`
