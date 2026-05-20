---
slug: a11y-basics
tier: pro
group: ux
domain: accessibility-specialist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The entry-level accessibility layer for web products: WCAG POUR principles, A/AA/AAA conformance levels, four evaluation types, five-minute quick-check protocol, and pre-commit gate criteria.
content_id: "3f3f6cb28d4c5f72"
tags: [accessibility, wcag, a11y, inclusion, compliance]
---
# Accessibility Basics

## Summary

**One-sentence:** The entry-level accessibility layer for web products: WCAG POUR principles, A/AA/AAA conformance levels, four evaluation types, five-minute quick-check protocol, and pre-commit gate criteria.

**One-paragraph:** The entry-level accessibility layer for web products: WCAG POUR principles, A/AA/AAA conformance levels, four evaluation types, five-minute quick-check protocol, and pre-commit gate criteria. Automated scanners catch only ~30% of issues; manual and assistive-tech testing is required.

## Applies If (ALL must hold)

- Onboarding a team or codebase to accessibility for the first time
- Pre-launch sanity sweep on a small site or feature where a full WCAG 2.2 conformance audit is overkill
- Wiring CI to catch the obvious 30% automated tools find: missing alt, unlabelled inputs, contrast failures, heading skips
- Educating a new agent or developer before they edit UI code

## Skip If (ANY kills it)

- Final compliance sign-off — use wcag-22-compliance and regulatory-compliance-2026
- Real assistive-technology testing flows (NVDA/VoiceOver/TalkBack) — use testing-with-assistive-technology
- Procurement / VPAT-ACR generation — use regulatory-compliance-2026
- XR/spatial experiences — use vr-design-patterns, ar-design-patterns, spatial-accessibility

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

- parent skill: `pro/ux/accessibility-specialist/`
