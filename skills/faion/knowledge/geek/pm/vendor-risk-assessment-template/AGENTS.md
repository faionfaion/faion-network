---
slug: vendor-risk-assessment-template
tier: geek
group: pm
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "268b9b9fd721d391"
complexity: medium
produces: spec
est_tokens: 3000
summary: Produces a SOC2 / GDPR-aligned vendor risk assessment (subprocessors, DPA, data-residency, encryption-at-rest, retention) so annual audit prep stops being a Q4 fire-drill.
tags: [pm, geek, vendor-risk, soc2, gdpr, dpa, audit-prep]
---
# Vendor Risk Assessment Template

## Summary

**One-sentence:** Produces a SOC2 / GDPR-aligned vendor risk assessment artefact (subprocessors, DPA reference, data-residency, encryption-at-rest, retention, breach-notification SLA) so annual audit prep stops being a Q4 fire-drill.

**One-paragraph:** Procurement-management literature is generic; SaaS teams need a SOC2-aligned vendor-risk template covering subprocessors, DPA, data-residency, encryption-at-rest, retention, breach-notification SLA, and a status flag (active / pending-review / deprecated). This methodology pins that artefact: single-instance per vendor, every input typed and source-cited, named human owner, semver + last_reviewed (90-day staleness window), and each section grounded in the specific compliance question it answers. The output lives in the audit folder and feeds directly into the auditor's evidence package.

**Ефективно для:** EM / compliance lead, який не хоче перетворювати щорічний SOC2-аудит на Q4 fire-drill.

## Applies If (ALL must hold)

- A vendor is being onboarded OR an annual SOC2 / GDPR review is due.
- The vendor handles customer data OR system credentials (otherwise lighter procurement suffices).
- Operator has the DPA / subprocessor list / data-flow diagram before starting.
- A named human owner exists for the assessment.

## Skip If (ANY kills it)

- The team already maintains a current vendor-risk assessment for this vendor — replace, do not duplicate.
- Vendor processes no customer or credential data (e.g. dev-only feature flag tool with no PII).
- Compliance context overrides this template (e.g. HIPAA-only); defer to legal.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Vendor DPA | PDF / URL | vendor's legal page |
| Subprocessor list | URL or CSV | vendor's compliance page |
| Data-flow diagram | image / mermaid | this product's compliance folder |
| Named owner | role + person | compliance team roster |
| Audit evidence root | dir path | `compliance/<year>/<vendor>/` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | Operating context for who runs the assessment. |
| `geek/pm/vendor-eval-framework` | Sibling rubric for pre-purchase selection; this one is post-purchase risk. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound-scope, typed-input, named-owner, versioned, grounded-in-rationale | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Vendor-handles-data gate + DPA-present branch | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-from-dpa` | haiku | Field extraction from structured PDF. |
| `synthesize-risk-rating` | sonnet | Per-axis judgment from extracted fields + data-flow. |
| `review_for_compliance` | opus | Cross-vendor synthesis when stakes are high (multiple high-risk vendors). |

## Templates

| File | Purpose |
|------|---------|
| `templates/vendor-risk-assessment-template.json` | JSON schema for the vendor risk assessment output contract. |
| `templates/vendor-risk-assessment-template.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-risk-assessment-template.py` | Enforce vendor-risk output contract (DPA present, subprocessor list non-empty, owner is person, semver + last_reviewed). | Before assessment is filed to compliance folder. |

## Related

- [[vendor-eval-framework]] — sibling pre-purchase selection methodology.
- [[team-charter-working-agreement]] — peer versioned-artefact methodology sharing the same envelope.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether the vendor handles customer data or credentials. If no → skip and document. If yes → check DPA + subprocessor list available. If missing → block and request from vendor. Otherwise → emit the assessment using the rule set.
