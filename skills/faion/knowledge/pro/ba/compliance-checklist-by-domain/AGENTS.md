---
slug: compliance-checklist-by-domain
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "804391fddc66f319"
summary: Domain-indexed compliance checklist (GDPR / HIPAA / PSD2 / SOC2 / WCAG) BAs apply during requirements validation to catch missing non-functional and regulatory items before sign-off.
tags: [compliance, gdpr, hipaa, psd2, soc2, accessibility, requirements-validation]
---
# Compliance Checklist by Domain

## Summary

**One-sentence:** A domain-indexed compliance checklist (per-regulation, per-feature-type) the BA applies during requirements validation to catch the regulatory and non-functional requirements AI-generated user stories routinely miss.

**One-paragraph:** AI-generated user stories are good at "user wants to log in" and terrible at "user is in the EU and has GDPR Article 17 erasure rights, and the system must reflect deletion in &lt;= 30 days, and the audit log must persist a deletion event." Compliance items are non-obvious to the average LLM because they live in regulations the model wasn't tuned to cite. This methodology gives the BA a five-step process: (1) classify the feature by data and jurisdiction, (2) pull the regulation-by-feature-type matrix, (3) check each required clause against the requirements, (4) flag misses as MUST-fix or MAY-fix, (5) document the BA's sign-off. The matrix covers the five regulations most frequently encountered in P4 outsource work plus accessibility. Output: a compliance-gate annotation per feature.

## Applies If (ALL must hold)

- Requirements being validated come from a feature touching: personal data, payments, health data, financial data, or user-facing UI.
- Project operates in (or sells to) a jurisdiction with regulation (EU / UK / US / regulated industry).
- BA is on the validation pass — after initial requirements drafting, before sign-off.
- AI was involved in drafting requirements (or the team is small enough that the BA is the only compliance pass).

## Skip If (ANY kills it)

- Internal admin tools with no PII and no external users — most clauses are N/A.
- Pure infrastructure work (DB migration, caching layer) where compliance applies upstream, not at this feature.
- Project already has a dedicated compliance officer/legal team validating each feature — this methodology defers to them.
- Single-jurisdiction free product with no payments / health / financial data — apply only accessibility section.

## Prerequisites

- Requirements document or user-story set under review.
- Feature classification: data types involved, user jurisdiction, payment processing yes/no, health yes/no.
- The compliance matrix (templates/compliance-matrix.csv).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/requirements-documentation` | Output of validation references the existing requirements doc structure. |
| `pro/ba/business-analyst/non-functional-requirements` | NFR taxonomy assumed as context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: classify-first, matrix-driven, MUST/MAY flagging, jurisdiction explicit, sign-off required | ~900 |
| `content/02-output-contract.xml` | essential | Compliance-gate annotation shape; per-clause coverage; sign-off | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes including wishful "we're not in scope" and unwritten jurisdiction | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-feature-by-data-type` | sonnet | Bounded judgment from feature description |
| `pull-applicable-clauses` | haiku | Lookup against matrix |
| `cross-check-requirements` | opus | Compare clauses against existing requirements text |

## Templates

| File | Purpose |
|------|---------|
| `templates/compliance-matrix.csv` | Per-(regulation, feature-type) clause list with MUST/MAY |
| `templates/compliance-gate.md` | Annotation skeleton per feature |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/clauses-not-met.py` | Compare matrix vs requirements doc; report uncovered clauses | Before sign-off |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodology: `requirements-documentation`, `non-functional-requirements`, `risk-analysis`
- external: [GDPR Articles 6, 17, 32](https://gdpr-info.eu/) · [HIPAA Security Rule](https://www.hhs.gov/hipaa/) · [PSD2 SCA](https://www.eba.europa.eu/) · [SOC 2 Trust Services](https://www.aicpa-cima.com/) · [WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/)
