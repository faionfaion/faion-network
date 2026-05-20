---
slug: accessibility-evaluation
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A five-stage audit process for WCAG 2.
content_id: "60402fd298e36068"
tags: [wcag, accessibility, a11y, audit, testing]
---
# Accessibility Evaluation

## Summary

**One-sentence:** A five-stage audit process for WCAG 2.

**One-paragraph:** A five-stage audit process for WCAG 2.1/2.2 AA conformance: automated scan (axe, Pa11y, Lighthouse) → triage → scripted keyboard testing (Playwright) → screen reader verification (NVDA/JAWS/VoiceOver) → structured report. Automated tools catch 30-40% of issues; stages 3-4 are mandatory to reach meaningful coverage. Screen reader verification requires a human — no LLM can reproduce AT speech buffers.

## Applies If (ALL must hold)

- Pre-release WCAG 2.1/2.2 AA audit before launch.
- Regression check after design system upgrades or major refactors.
- Procurement / RFP responses requiring VPAT or ACR documentation.
- Post-incident remediation when a complaint or lawsuit names specific WCAG criteria.
- CI gating on PRs touching shared library components.

## Skip If (ANY kills it)

- Early lo-fi wireframe stage — use accessibility-first-design heuristics, not a full audit.
- Pure ATAG or UAAG compliance — different rule sets; this methodology covers WCAG content/UI scope only.
- Native iOS/Android — use Accessibility Inspector (Xcode) and Accessibility Scanner (Android).
- PDF or document accessibility — use PAC 2024 or Adobe Acrobat Pro checker.

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
