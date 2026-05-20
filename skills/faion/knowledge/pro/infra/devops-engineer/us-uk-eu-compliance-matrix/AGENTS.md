---
slug: us-uk-eu-compliance-matrix
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3fdc39c931a0edca"
summary: Side-by-side obligation matrix across US (CCPA/CPRA, state privacy), UK (UK-GDPR, DPA 2018), and EU (GDPR, DSA, AI Act) so a micro-agency founder can check entity registration, data handling, contracts, and tax obligations per market without re-reading three statutes.
tags: [compliance, gdpr, ccpa, uk-gdpr, jurisdictions]
---

# US / UK / EU Compliance Matrix

## Summary

**One-sentence:** Side-by-side obligation matrix across US (CCPA/CPRA, state privacy), UK (UK-GDPR, DPA 2018), and EU (GDPR, DSA, AI Act) so a micro-agency founder can check entity registration, data handling, contracts, and tax obligations per market without re-reading three statutes.

**One-paragraph:** A solo founder or micro-agency selling across US, UK, and EU faces ~40 distinct obligations spread across 7 statutes. Existing methodologies are jurisdiction-specific. This methodology codifies a 7-row matrix (entity-registration, data-processing-basis, DPA / processor terms, cookie / consent, marketing email, AI-act provisions, sales-tax / VAT) with the obligation in each of the 3 jurisdictions and a per-row "first action when launching here". NOT legal advice — output marks every row with `requires_legal_review: true`. Output: `ComplianceMatrix` JSON + a markdown table for the founder's compliance binder.

## Applies If (ALL must hold)

- founder serves customers OR processes personal data from ≥ 2 of {US, UK, EU}
- annual revenue OR data-subject count above any one jurisdiction's de-minimis threshold (e.g. CCPA's 100k consumers, GDPR's "regular processing")
- founder has NOT engaged dedicated counsel per jurisdiction yet
- product processes personal data (almost any SaaS qualifies)

## Skip If (ANY kills it)

- single jurisdiction operator — use the local jurisdiction's specific methodology
- already retained counsel in all 3 jurisdictions — they own this
- highly regulated vertical (medical devices, banking) — sector regs dominate; matrix incomplete
- B2B-only with corporate accounts and no consumer PII — most rows reduce to vendor-DPA workflow

## Prerequisites

- list of jurisdictions where the founder has customers
- data-processing inventory (categories of data, sources, destinations)
- current contract templates (DPA, ToS, Privacy Policy)
- expected ARR per region (drives tax thresholds)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/data-residency-controls` | Technical implementation of matrix's data-residency rows |
| `pro/pm/project-manager/vendor-margin-defense-checklist` | Sister methodology covering vendor DPAs that flow into row 3 |
| `geek/sdlc-ai/gov-ai-governance` | EU AI Act provisions in row 6 |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 7-row coverage, legal-review marker, threshold check, currency, NOT-LEGAL-ADVICE banner | ~1100 |
| `content/02-output-contract.xml` | essential | `ComplianceMatrix` schema with per-row obligation and first-action | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: outdated statute, wrong threshold, missing AI act, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `jurisdiction_threshold_check` | sonnet | Numeric checks against current thresholds |
| `obligation_lookup_per_row` | sonnet | Pulls from versioned matrix data file |
| `first_action_recommendation` | sonnet | Bounded based on operator's revenue / data volume |
| `legal_review_flag_assembly` | haiku | Always-true addition per row |

## Templates

| File | Purpose |
|------|---------|
| `templates/compliance-matrix.json` | Output schema |
| `templates/matrix-source.yaml` | Versioned statute / threshold source data |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/build-matrix.py` | Compose matrix from versioned source data | Quarterly review |
| `scripts/statute-freshness-check.py` | Compare matrix-source to ICO / EDPB / state-AG announcements | Monthly cron |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodologies: `data-residency-controls`, `vendor-margin-defense-checklist`
- external: [GDPR (EU 2016/679)](https://gdpr-info.eu/) · [UK ICO — Guide to UK GDPR](https://ico.org.uk/) · [California Attorney General — CCPA / CPRA](https://oag.ca.gov/privacy/ccpa) · [EU AI Act 2024](https://artificialintelligenceact.eu/) · [EDPB Guidelines](https://www.edpb.europa.eu/) · [IRS Pub 519 — US Tax for Foreign Persons](https://www.irs.gov/pub/irs-pdf/p519.pdf)
