---
slug: contractor-agreement-template-us-uk-eu
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a baseline contractor agreement (US 1099, UK IR35-aware, EU with DE/FR/PT/ES addenda) ready for attorney review before first signature.
content_id: "3038160f58087649"
complexity: medium
produces: spec
est_tokens: 4500
tags: [contractor, agreement, ip-assignment, jurisdiction, p5-agency]
---
# Contractor Agreement Template (US / UK / EU)

## Summary

**One-sentence:** Produces a baseline contractor agreement (US 1099, UK IR35-aware, EU with DE/FR/PT/ES addenda) ready for attorney review before first signature.

**One-paragraph:** P5 micro-agency founders (1-10 contractors, mixed US/UK/EU) currently improvise contracts — pull a US 1099 template off a blog, change $ to GBP, hope. The result is enforceability gaps (UK IR35 misclassification, EU contractor-vs-employee tests, German Scheinselbständigkeit) and IP assignments that do not transfer. This methodology provides three baseline templates plus a five-step selector: jurisdiction match, classification test, IP assignment language, payment + tax terms, termination + IP-survival. Templates are a starting point for attorney review, not a substitute.

**Ефективно для:**

- найм фрилансера або підрядника в US / UK / EU юрисдикціях.
- коли потрібна IP-assignment мова, що дійсно переноситься у відповідній юрисдикції.
- P5-micro-agency засновник, який підписує 1-10 контрактів на рік.
- перед першим підписанням з юристом — як baseline для review, не як substitute.

## Applies If (ALL must hold)

- Founder hires contractors (freelancers, sole traders, GmbH-of-one) in US, UK, or EU.
- Engagement is `contractor` not `employee` — founder wants to keep that classification.
- Founder is the engaging entity (company or sole trader), not a marketplace.
- Founder accepts the template is a baseline and will be reviewed by a qualified attorney before first signature.

## Skip If (ANY kills it)

- Hiring as employee (W-2, PAYE, EU employment contract) — different methodology, employment law.
- Hiring through an Employer-of-Record (Deel, Remote, Velocity Global) — they provide the contract.
- Hiring in a jurisdiction not in US/UK/EU — these templates do not generalize (India, LATAM, MENA have different classification rules).
- Engagement is open-source contribution / volunteer — use a contributor agreement instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Founder's legal entity | LLC / Ltd / GmbH / sole trader | corporate docs |
| Contractor jurisdiction | residence country (not nationality) | contractor |
| Scope, rate, term | engagement letter draft | founder |
| Attorney contact | name + email | founder's network |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/contractor-hiring-process` | sourcing + screening is assumed; this methodology covers the contract phase |
| `pro/ba/business-analyst/non-functional-requirements` | confidentiality / data-protection clauses reference NFR thinking |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-jurisdiction-match) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/05-examples.xml` | medium | One full worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

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
| `templates/contractor-uk.md` | UK contractor agreement with IR35 mitigation |
| `templates/contractor-eu.md` | EU baseline with DE/FR/PT/ES addenda |
| `templates/skeleton.json` | Signed contract metadata schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contractor-agreement-template-us-uk-eu.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[contractor-hiring-process]]
- [[vendor-management]]
- [[ops-legal-compliance-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Contractor Agreement Template (US / UK / EU) methodology when in doubt about scope or fit.
