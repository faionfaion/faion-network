---
slug: regulatory-compliance-2026
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Accessibility regulation landscape shifted April 2026 (ADA Title II Final Rule → WCAG 2.
content_id: "becb9815e2337741"
tags: [accessibility, compliance, wcag, ada, eaa, regulatory]
---
# Regulatory Compliance 2026

## Summary

**One-sentence:** Accessibility regulation landscape shifted April 2026 (ADA Title II Final Rule → WCAG 2.

**One-paragraph:** Accessibility regulation landscape shifted April 2026 (ADA Title II Final Rule → WCAG 2.1 AA), June 2025 (EU Accessibility Act effective date), and ongoing (AODA, Section 508). Map your product surfaces (website, native app, kiosk, e-book) to applicable regulations. Document conformance against WCAG 2.1 AA minimum. Publish an accessibility statement with dated testing methodology, feedback channel, and remediation commitment. Schedule audits at least annually; flag every major release for incremental audit. Treat WCAG 2.2 AA as the design baseline even where 2.1 is the legal minimum — gap-closing later is more expensive. Avoid overlay widgets that claim to "auto-fix" a11y; they have lost cases in US courts. Train content authors — most violations enter via CMS, not engineering.

## Applies If (ALL must hold)

- Pre-launch a11y audit for a US/EU public-facing site or app (post-ADA April 2026 / EAA June 2025).
- Drafting an accessibility statement and conformance documentation per WCAG 2.1/2.2 AA.
- Mapping product surface area (web, native, kiosk, e-book) to specific regulations (ADA Title II, EAA, AODA, Section 508).
- Quarterly/annual a11y audit cycle planning + remediation backlog.

## Skip If (ANY kills it)

- Implementation-level a11y fixes — see `accessibility-evaluation`, `wcag-22-compliance`, `testing-with-assistive-technology`.
- Privacy/data regulation (GDPR, CCPA, HIPAA) — different methodology.
- Pure design tokens / visual contrast — covered in `accessibility-first-design`.

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

- parent skill: `pro/ux/ux-ui-designer/`
