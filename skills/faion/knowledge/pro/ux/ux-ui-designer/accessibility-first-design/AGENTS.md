---
slug: accessibility-first-design
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A design-phase methodology that prevents 70-80% of WCAG 2.
content_id: "041bb0f6779595cb"
tags: [wcag, accessibility, design-system, tokens, inclusive-design]
---
# Accessibility-First Design

## Summary

**One-sentence:** A design-phase methodology that prevents 70-80% of WCAG 2.

**One-paragraph:** A design-phase methodology that prevents 70-80% of WCAG 2.2 issues before engineering begins. Enforce contrast ratios (4.5:1 body, 3:1 large/UI), touch targets (44x44px), visible focus states, semantic HTML structure, and motion controls at the design token and component-spec level. Issues caught at design time cost 5-10x less than post-launch remediation.

## Applies If (ALL must hold)

- Starting a new product, design system, or major redesign.
- Establishing design-token contrast rules and focus-state baselines for a component library.
- Onboarding new designers — the checklist is the working agreement.
- Pre-handoff QA: validating Figma frames before engineering begins.

## Skip If (ANY kills it)

- Pure code-fix sprints where designs are frozen — code-level a11y patterns (semantic HTML, ARIA, focus management) are the right tool.
- Marketing landing pages with one-off visual gimmicks — apply principles but don't gate launch on WCAG 2.2 AAA.
- When the design hasn't started — load design first; applying checklists too early constrains ideation.

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
