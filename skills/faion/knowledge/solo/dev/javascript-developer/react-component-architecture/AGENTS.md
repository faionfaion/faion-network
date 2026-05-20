---
slug: react-component-architecture
tier: solo
group: dev
domain: javascript-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Scalable React component structure using feature-based modules, colocation, and compound component patterns.
content_id: "cd2901f848c11557"
tags: [react, typescript, component-architecture, nextjs, patterns]
---
# React Component Architecture

## Summary

**One-sentence:** Scalable React component structure using feature-based modules, colocation, and compound component patterns.

**One-paragraph:** Scalable React component structure using feature-based modules, colocation, and compound component patterns. The core rule: establish the CVA/variant pattern in one reference component (Button) before generating others — agents copy existing patterns reliably when a reference exists; barrel files must export types alongside components.

## Applies If (ALL must hold)

- New React or Next.js project deciding folder structure before writing any components
- Refactoring a flat `components/` folder that has grown beyond 20 files
- Reviewing a component for single-responsibility violations before merging a PR
- Generating a new UI primitive (Button, Input, Card) following the codebase's established variant system

## Skip If (ANY kills it)

- Very small apps (1-3 pages, fewer than 10 components) — structure overhead exceeds benefit
- Pure server-rendered applications with minimal interactivity — use Next.js server components pattern
- Component libraries consumed externally — those have different export and versioning constraints

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

- parent skill: `solo/dev/javascript-developer/`
