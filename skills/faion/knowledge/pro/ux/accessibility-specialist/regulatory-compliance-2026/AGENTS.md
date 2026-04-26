# Regulatory Compliance 2026

## Summary

Regional accessibility law matrix for 2026: ADA Title II (US government, April 2026 deadline), European Accessibility Act (EU e-commerce + banking, June 2025/2030), Section 508, AODA (Canada), and equivalent frameworks in the UK, Australia, and Asia-Pacific. Covers deadlines, WCAG standard mappings, documentation requirements (VPAT/ACR, accessibility statements), enforcement penalties, and exemptions.

## Why

Non-compliance risks vary by region: US ADA lawsuits average $5,000-$75,000 in settlements plus $50,000-$200,000 in legal fees; EU EAA fines reach 4% of annual revenue. Regulations differ in scope, standard version (WCAG 2.0 vs 2.1 vs EN 301 549), and enforcement mechanism. A single compliance checklist does not cover all jurisdictions; organizations must identify which regulations apply and what documentation is required.

## When To Use

- Determining which accessibility standard (WCAG 2.0/2.1/2.2, EN 301 549) applies to a given product and jurisdiction.
- Writing or auditing accessibility statements, VPATs, and ACRs.
- Setting up ongoing monitoring, training, and procurement standards for ADA/EAA compliance.
- Assessing risk before a product launch in a new region.
- Responding to a DOJ complaint or EU enforcement action.

## When NOT To Use

- Technical WCAG implementation — use `wcag-22-compliance` or `a11y-testing`.
- AT runtime testing — use `testing-with-assistive-technology`.
- XR/spatial products — apply WCAG + W3C XAUR; no dedicated regulation yet.
- Internal-only tooling with no public-facing interface — most regulations apply to public-facing services only.

## Content

| File | What's inside |
|------|---------------|
| `content/01-regulation-matrix.xml` | Jurisdiction table: US (ADA II, III, 508, CVAA), EU (EAA, WAD), Canada (AODA, ACA), UK, AU, and APAC. Deadlines, standards, enforcement. |
| `content/02-documentation-requirements.xml` | VPAT/ACR, accessibility statement, accessibility policy — what each must contain and when to update. |
| `content/03-enforcement-and-exemptions.xml` | US/EU/Canada/UK/AU penalties, proactive measures, common exemptions (archival, undue burden, fundamental alteration). |

## Templates

| File | Purpose |
|------|---------|
| `templates/accessibility-statement.txt` | Accessibility statement template covering conformance status, known limitations, contact, and date. |
