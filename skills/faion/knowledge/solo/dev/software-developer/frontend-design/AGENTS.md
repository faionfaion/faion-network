---
slug: frontend-design
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A multi-phase workflow for solopreneur-scale UI projects: fix requirements (type, style, tech), generate 3-5 truly distinct design variants differing in navigation pattern and information density, render them to screenshots for comparison, select one based on human taste, define design tokens before components, scaffold Storybook with pinned versions, and deliver components colocated with stories and tests.
content_id: "5ae6e00f1000265b"
tags: [frontend-design, ui-design, design-tokens, storybook, component-library]
---
# Frontend Design

## Summary

**One-sentence:** A multi-phase workflow for solopreneur-scale UI projects: fix requirements (type, style, tech), generate 3-5 truly distinct design variants differing in navigation pattern and information density, render them to screenshots for comparison, select one based on human taste, define design tokens before components, scaffold Storybook with pinned versions, and deliver components colocated with stories and tests.

**One-paragraph:** A multi-phase workflow for solopreneur-scale UI projects: fix requirements (type, style, tech), generate 3-5 truly distinct design variants differing in navigation pattern and information density, render them to screenshots for comparison, select one based on human taste, define design tokens before components, scaffold Storybook with pinned versions, and deliver components colocated with stories and tests. Tokens come first; components inherit from them to prevent color hardcoding and post-hoc drift.

## Applies If (ALL must hold)

- Greenfield frontend (landing, dashboard, marketing site) where visual direction is open.
- Component library bootstrap before product features land (storybook.faion.net pattern).
- Rebrand / redesign passes that need 3-5 explored variants before committing.
- Solopreneur-scale projects (faion.net portfolio sites: ruslan, viktoria, art) — designer + dev are the same person + agents.
- Translating brand brief or PRD into concrete tokens (colors, type scale, spacing) and components.

## Skip If (ANY kills it)

- Active production UI with established design system — variant brainstorming is wasted; iterate on tokens instead.
- Pure backend or CLI projects.
- Brownfield refactors where scope is "make this page faster", not "redesign".
- Native mobile (iOS/Android) — patterns assume web (HTML/CSS/JSX); use platform-native tools.
- Engineering-driven internal admin tools where utility outweighs aesthetics.

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

- parent skill: `solo/dev/software-developer/`
