---
slug: vpat-acr-template
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a VPAT 2.5 Accessibility Conformance Report with per-criterion status, evaluation method, and remarks suitable for procurement and ADA documentation.
content_id: "e36e4ce1488a55ed"
complexity: medium
produces: report
est_tokens: 4200
tags: [vpat, acr, section-508, wcag, procurement]
---
# VPAT / ACR Template

## Summary

**One-sentence:** Generates a VPAT 2.5 Accessibility Conformance Report with per-criterion status, evaluation method, and remarks suitable for procurement and ADA documentation.

**One-paragraph:** A VPAT (Voluntary Product Accessibility Template) ACR (Accessibility Conformance Report) is the standard evidence packaging required by US Section 508 procurement and increasingly by EU EN 301 549. The current version is VPAT 2.5 (ITI, 2024). This methodology generates a structured ACR with per-success-criterion conformance status (Supports / Partially Supports / Does Not Support / Not Applicable), evaluation method, scope, and remarks per row. The output is consumable by procurement teams and forms the evidence base for an ADA / Section 508 compliance claim.

**Ефективно для:**

- Responding to a procurement RFP that requires a VPAT.
- Documenting WCAG 2.2 conformance for Section 508 / EN 301 549.
- Building the public 'accessibility' page evidence.
- Coordinating remediation: ACR rows that are 'partial' become the backlog.

## Applies If (ALL must hold)

- Underlying WCAG 2.2 audit data is available (per-SC results).
- Author has authority to publish a public-facing conformance document.
- Product is publicly available or sold to government / enterprise.
- There is a named accessibility lead who signs off the ACR.

## Skip If (ANY kills it)

- WCAG 2.2 audit not yet run — produce the audit first (`wcag-22-compliance`).
- Internal-only product not sold via procurement — public ACR overkill.
- Author has no sign-off authority — escalate first.
- Earlier ACR from same version still current (≤6 months) — update, do not duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| WCAG 2.2 audit | per-SC sc_results JSON | wcag-22-compliance methodology |
| Product scope | what's in/out of conformance scope | PM |
| Accessibility lead | named owner who signs off | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wcag-22-compliance]] | upstream — provides per-SC results |
| [[w3c-design-tokens-standard]] | background — contrast tokens feed multiple SC rows |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `import-audit` | haiku | Mechanical mapping. |
| `synthesize-remarks` | sonnet | Plain-language summarisation. |
| `review-for-compliance` | opus | Cross-row consistency requires synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vpat-acr-template.md` | Markdown VPAT 2.5 ACR skeleton |
| `templates/vpat-acr-template.json` | JSON skeleton matching the output schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vpat-acr-template.py` | Validate vpat-acr-template artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[wcag-22-compliance]]
- [[w3c-design-tokens-standard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on upstream audit availability, VPAT edition, and signature presence. Any gate failure halts publication.
