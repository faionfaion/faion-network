---
slug: ai-generated-layout-review-checklist
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "03339666530262c9"
summary: Ten-point checklist for reviewing AI-generated mockups (v0, Galileo, Figma Make, Midjourney UI prompts) before they enter a design system or ship to engineering.
tags: [ai-generated-design, ux-review, v0, galileo, figma, design-system, a11y, design-tokens]
---

# AI-Generated Layout Review Checklist

## Summary

**One-sentence:** Ten-point checklist for reviewing AI-generated mockups (v0, Galileo, Figma Make, Midjourney UI prompts) before they enter a design system or ship to engineering.

**One-paragraph:** Gives the human designer leverage when an AI hands them a fait-accompli mock that "just needs to ship". Mechanism: a fixed 10-point review covering research grounding, design-token compliance, a11y, edge cases, motion, copy, IA, brand fit, file hygiene, and ownership/attestation. Each check carries a hard verdict; the reviewer cannot APPROVE until every check has either passed or has a written justification. Primary output: a review decision plus an annotated mockup recorded in the design-system tracker.

## Applies If (ALL must hold)

- mockup_generated_by ∈ {v0.dev, Galileo, Figma Make, Magician, Uizard, Visily, AI-prompted Figma, MJ-or-similar image gen}
- mockup_targets ∈ {production_screen, design_system_token, marketing_landing}
- design_system_exists == true (tokens, components, IA documented)
- reviewer is a designer (or designer-lead human) — not just engineering

## Skip If (ANY kills it)

- mockup is exploratory only, will not ship (sketch / moodboard / divergence-phase artifact) — review is overhead
- mockup is for an internal-only admin tool with no end users beyond the team — checklist is too heavy, do a 3-point version
- design system does not exist yet — use design-foundations-bootstrap methodology instead
- the engagement is a one-off audit, not ongoing — apply enterprise design-review process

## Prerequisites

- design system with named tokens (color, type, spacing, radius, motion, elevation) accessible in JSON or Figma library
- user research artifact relevant to the screen (job-to-be-done, persona, recent usability test, support-ticket cluster)
- a11y baseline (WCAG 2.2 AA target; documented contrast and focus-state requirements)
- brand guideline that defines tone, voice, photography rules

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/jobs-to-be-done` | Provides the research grounding the reviewer checks against in c01 |
| `pro/ux/accessibility-specialist/wcag-22-checklist` | Source of truth for a11y verdicts in c03 |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 10 checks with detector + verdict policy | ~1300 |
| `content/02-output-contract.xml` | essential | Review-decision schema + forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 reviewer failure modes specific to AI-generated layouts | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `token_compliance_scan` | haiku | Mechanical compare of mock colors/typography to JSON token export |
| `a11y_contrast_audit` | haiku | Deterministic — pixel sampler + ratio calc |
| `per-check_verdict` | sonnet | Bounded judgment per check |
| `research_grounding_synthesis` | opus | Cross-document synthesis (research + mockup + brand) |

## Templates

| File | Purpose |
|------|---------|

## Scripts

| File | Purpose |
|------|---------|

## Related

- parent skill: `geek/ux/ux-ui-designer/SKILL.md`
- peer methodologies: `pro/ux/accessibility-specialist/wcag-22-checklist`, `solo/ux/ui-designer/design-system-foundations`
- external: [Vercel v0 design-system constraints docs] · [Nielsen Norman Group "AI-Generated UI: Designer's Role" (2024)](https://www.nngroup.com/) · [WCAG 2.2 spec](https://www.w3.org/TR/WCAG22/) · [Figma Make limitations doc (2025)]
