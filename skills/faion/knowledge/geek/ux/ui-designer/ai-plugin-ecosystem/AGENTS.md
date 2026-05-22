---
slug: ai-plugin-ecosystem
tier: geek
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Figma AI plugins (Magician, Automator, Content Reel, Stark, Similayer, Diagram) automate repetitive design tasks within the Figma canvas.
content_id: "94feebfd638a43bc"
tags: [figma-plugins, figma-automation, accessibility-audit, design-automation, rest-api]
---
# AI Plugin Ecosystem

## Summary

**One-sentence:** Figma AI plugins (Magician, Automator, Content Reel, Stark, Similayer, Diagram) automate repetitive design tasks within the Figma canvas.

**One-paragraph:** Figma AI plugins (Magician, Automator, Content Reel, Stark, Similayer, Diagram) automate repetitive design tasks within the Figma canvas. Critically, agents cannot trigger plugin runs programmatically — the Figma REST API is the actual agent integration surface. Use plugins for human-driven workflows; use the REST API for automated pipelines.

## Applies If (ALL must hold)

- Automating repetitive Figma operations (renaming layers, bulk style changes, exporting assets) via Figma REST API
- Running accessibility audits across a design file before handoff (contrast ratio computation from REST API data)
- Generating placeholder content at scale and pushing it via Figma REST `PATCH /v1/files/{key}/nodes`
- Evaluating which plugin combination covers a team's workflow gaps before investing in custom UXP development
- Running WCAG contrast checks externally without requiring the Stark plugin

## Skip If (ANY kills it)

- Plugin output must be reproducible without human intervention — most AI plugins are not deterministic
- Design decisions require brand or strategic judgment — plugins are automation tools, not decision-makers
- A plugin relies on a third-party AI API that could expose proprietary design data to external servers
- The design system is unstable — plugins that reference tokens/styles break when foundations change

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
