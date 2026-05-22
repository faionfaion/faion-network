---
slug: shadcn-ui-architecture
tier: solo
group: dev
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: shadcn/ui components are vendored (copied, not installed as packages) into components/ui/.
content_id: "f7d94871947a236f"
tags: [shadcn-ui, architecture, component-layering, tailwind, cva]
---
# shadcn/ui Architecture

## Summary

**One-sentence:** shadcn/ui components are vendored (copied, not installed as packages) into components/ui/.

**One-paragraph:** shadcn/ui components are vendored (copied, not installed as packages) into components/ui/. The architecture enforces three strict layers: ui/ primitives are mutated only via npx shadcn add; components/<feature>/ composes from ui/; lib/ holds pure utilities. All variants use cva(). Theme via CSS variables only — no hex literals in feature components.

## Applies If (ALL must hold)

- Mid-to-large React + Tailwind app using shadcn/ui that needs directory ownership rules.
- Multiple agents or teams contributing components — prevents ui/ becoming a junk drawer.
- Migrating from a closed UI library into a layered primitives → composite → feature structure.
- Monorepo where shadcn primitives live in a shared packages/ui/.

## Skip If (ANY kills it)

- App with fewer than 20 components — flat components/ is simpler.
- Stack is not React + Tailwind; these rules assume both.
- Project uses MUI/Mantine; different composition patterns apply.
- Pre-shadcn-init phase; set up shadcn-ui methodology first, then add architecture rules.

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

- parent skill: `solo/dev/frontend-developer/`
