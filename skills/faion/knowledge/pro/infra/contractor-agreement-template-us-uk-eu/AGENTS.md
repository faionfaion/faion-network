---
slug: contractor-agreement-template-us-uk-eu
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a1ef25f11abc55fa"
summary: Jurisdiction-aware contractor agreement template (US, UK, EU variants) with IP assignment, classification tests, payment terms, and termination — for micro-agencies hiring across the three core markets.
tags: [contractor, agreement, ip-assignment, micro-agency, p5-agency, jurisdiction]
---
# Contractor Agreement Template (US / UK / EU)

## Summary

**One-sentence:** Three jurisdiction-aware contractor agreement templates (US, UK, EU) covering IP assignment, worker classification, payment, confidentiality, and termination — the documents a P5 micro-agency founder uses when hiring across borders.

**One-paragraph:** P5 micro-agency founders (1-10 contractors, mixed US/UK/EU) currently improvise contracts: pull a US 1099 template off a blog, change "$" to "GBP", hope. The result is enforceability gaps (UK IR35 misclassification, EU contractor-vs-employee tests, German Scheinselbständigkeit) and IP assignments that don't transfer in the relevant jurisdiction. This methodology provides three baseline templates (US 1099/W8-BEN, UK contractor/IR35-aware, EU freelancer with country-specific addenda for DE/FR/PT/ES) plus a five-step selector: jurisdiction match, classification tests, IP assignment language, payment + tax terms, termination + IP-survival. Note: methodology authors are not attorneys; templates are a starting point for legal review, not a substitute.

## Applies If (ALL must hold)

- Founder hires contractors (freelancers, sole traders, GmbH-of-one) in US, UK, or EU.
- Engagement is "contractor" not "employee" — founder wants to keep that classification.
- Founder is the engaging entity (company or sole trader), not a marketplace.
- Founder accepts the template is a baseline and will be reviewed by a qualified attorney before first signature.

## Skip If (ANY kills it)

- Hiring as employee (W-2, PAYE, EU employment contract) — different methodology, employment law.
- Hiring through an Employer-of-Record (Deer, Remote, Velocity Global) — they provide the contract.
- Hiring in a jurisdiction not in US/UK/EU — these templates do not generalize (India, LATAM, MENA have different classification rules).
- Engagement is open-source contribution / volunteer — use a contributor agreement instead.

## Prerequisites

- Founder's legal entity established (LLC, Ltd, GmbH, sole trader) — entity is the contracting party.
- Contractor's jurisdiction confirmed (residence, not nationality).
- Scope, rate, and term agreed in principle.
- Engagement letter or scope-of-work draft.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/contractor-hiring-process` | Sourcing and screening assumed; this methodology covers the contract phase only. |
| `pro/ba/business-analyst/non-functional-requirements` | Confidentiality / data-protection clauses reference NFR thinking. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: jurisdiction-match, classification tests, IP-assignment specifics, payment+tax, termination | ~1000 |
| `content/02-output-contract.xml` | essential | Signed-contract artifact shape, addendum index, e-sign metadata | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: wrong jurisdiction, IR35 trap, vague IP assignment, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-template-variant` | haiku | Lookup by contractor jurisdiction |
| `populate-deal-specifics` | sonnet | Insert scope, rate, term, parties |
| `risk-flag-pass` | opus | Cross-clause review for inconsistencies (e.g., UK IR35 flags) |

## Templates

| File | Purpose |
|------|---------|
| `templates/contractor-us.md` | US 1099-NEC contractor agreement skeleton |
| `templates/contractor-uk.md` | UK contractor agreement with IR35 mitigation language |
| `templates/contractor-eu.md` | EU baseline with DE/FR/PT/ES addenda |
| `templates/ip-assignment-clauses.md` | Stand-alone IP-assignment language tested per jurisdiction |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/classification-risk-check.py` | Self-check on classification-risk indicators (control, exclusivity, equipment) | Pre-attorney review |

## Related

- parent skill: `pro/infra/devops-engineer/` (engaged adjacent to ops-legal-compliance-checklist)
- peer methodology: `ops-legal-compliance-checklist`, `vendor-management`, `payroll-vs-contractor`
- external: HMRC IR35 guidance, IRS 1099 rules, EU Directive 2019/1152 transparent working conditions, German Scheinselbständigkeit case law
