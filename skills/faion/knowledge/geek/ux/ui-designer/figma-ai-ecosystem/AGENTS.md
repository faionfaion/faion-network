---
slug: figma-ai-ecosystem
tier: geek
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Figma's AI suite is UI-only with no agent API.
content_id: "6ba71d5e338c9818"
tags: [figma, ai, design, agent-boundary, api]
---
# Figma AI Ecosystem

## Summary

**One-sentence:** Figma's AI suite is UI-only with no agent API.

**One-paragraph:** Figma's AI suite is UI-only with no agent API. Practical surfaces are REST API and Webhooks. Agent role: prompt preparation, validation, post-publish audits.

## Applies If (ALL must hold)

- Generating structured prompts for Figma Make that a designer then pastes and executes
- Using Figma Webhooks to trigger downstream agent workflows (spec generation, audit, asset export) on file changes
- Auditing Figma Sites published pages with Lighthouse and axe after a human publishes
- Applying non-destructive image editing (erase, isolate, expand) within Figma — human-operated, agent can post-process exported results
- Evaluating Figma's AI suite before committing to Adobe Firefly or standalone generative tools

## Skip If (ANY kills it)

- Production-quality code output is required — Figma Make outputs prototype-grade code, not deployable code
- The design system is token-driven and complex — Figma AI tools do not reliably respect custom token systems
- Deterministic, reproducible outputs are required — all Figma AI features are non-deterministic
- The artifact must be version-controlled at code level — Figma files are binary; Sites output is not Git-tracked
- WCAG compliance is required from day one — Figma AI outputs consistently miss accessibility requirements

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

- parent skill: `geek/ux/ui-designer/`
