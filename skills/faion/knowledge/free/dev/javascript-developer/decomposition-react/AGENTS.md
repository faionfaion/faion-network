---
slug: decomposition-react
tier: free
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM-friendly code organization for React and Next.
content_id: "aefbf4cd201e87cc"
tags: [react, component-architecture, typescript, hooks, nextjs]
---
# React Decomposition Patterns

## Summary

**One-sentence:** LLM-friendly code organization for React and Next.

**One-paragraph:** LLM-friendly code organization for React and Next.js projects. Break god components (600+ lines, 20+ hooks) into focused pieces: reusable UI components in components/ui/, feature-specific logic in features/, custom hooks in hooks/, data fetching in services/, types in types/, and shared utilities in utils/. Target 30-80 lines per file for maximum LLM context efficiency.

## Applies If (ALL must hold)

- Refactoring god components (200+ lines, 10+ hooks, mixed API/UI/state).
- Greenfield React/Next.js where early directory layout predicts team velocity for months.
- Reducing per-file token counts so agents can read whole files in single tool calls.
- Migrating from flat components/ layout to feature-based modules with co-located hooks, types, services, stores.

## Skip If (ANY kills it)

- Tiny apps (<20 components) — feature/services/stores split is overhead and makes scaffolding slower.
- One-shot prototypes and spikes — premature decomposition adds lines for less value.
- Codebases dominated by Server Components — file-size reasoning differs; `.server.tsx` boundaries override the layout.
- UI-only design-system repositories (Storybook component libraries) — they need a different shape (`packages/ui/<Component>`).

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

- parent skill: `free/dev/javascript-developer/`
