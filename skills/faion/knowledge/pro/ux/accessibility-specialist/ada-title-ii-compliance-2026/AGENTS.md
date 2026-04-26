# ADA Title II Compliance 2026

## Summary

Compliance methodology for US state and local government entities required to meet WCAG 2.1 Level AA under the DOJ ADA Title II final rule: large entities (50K+ population) by April 24, 2026; smaller entities by April 24, 2027. Covers full scope (web, mobile apps, multimedia, PDFs, third-party content), the six-step remediation roadmap, accessibility statement requirements, VPAT/ACR documentation, training, and procurement standards.

## Why

Non-compliance risks DOJ investigation, private lawsuits, loss of federal funding, and multi-year consent decrees. The scope is broader than HTML: mobile apps, PDFs, video captions, interactive forms, and third-party social embeds are all in scope. Overlay tools (accessibility.widget) do not constitute compliance — the DOJ has explicitly warned against them. VPAT 2.5 INT alone is not proof of conformance; courts require real test evidence.

## When To Use

- US state/local government entity or federal-funded program building or auditing public-facing digital services.
- Vendor responding to government RFP requiring VPAT/ACR and remediation plan.
- Procurement officer evaluating third-party SaaS for accessibility risk before contract award.
- Pre-litigation triage after a DOJ complaint or Title II demand letter.
- Drafting or reviewing accessibility statements, procurement clauses, or staff training plans.

## When NOT To Use

- Private commercial sites unrelated to government funding — ADA Title III and WCAG 2.2 AA apply; different case law.
- EU-only products — use `regulatory-compliance-2026` for EAA + EN 301 549.
- Internal-only tools not used by the public — Section 504/508 may apply instead of the Title II web rule.
- Greenfield design — apply `accessibility-first-design` from day one to avoid remediation cost.

## Content

| File | What's inside |
|------|---------------|
| `content/01-scope-and-requirements.xml` | Full scope definition, WCAG 2.1 AA principle table, video/audio/document requirements, exemptions. |
| `content/02-remediation-roadmap.xml` | Six-step compliance roadmap (audit → gap analysis → roadmap → implementation → monitoring → documentation), accessibility statement template, training and procurement requirements. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vpat-cell-generator.sh` | Shell script converting axe JSON to VPAT 2.5 conformance table (Does Not Support entries per WCAG criterion). |
