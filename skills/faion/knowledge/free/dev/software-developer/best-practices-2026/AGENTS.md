---
slug: best-practices-2026
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Stacks evolve faster than training data.
content_id: "9d51bb92a40a964e"
tags: [best-practices, typescript, react, python, ai-coding, testing]
---
# Software Development Best Practices 2026

## Summary

**One-sentence:** Stacks evolve faster than training data.

**One-paragraph:** Stacks evolve faster than training data. Without an explicit current-state reference, agents default to training-era patterns: React 17 hooks, Optional[X] over X | None, outdated tsconfigs. This document provides a 2026-snapshot reference of current-stable practices across AI-assisted coding, TypeScript 5, React 19 / Next.js 15, Python 3.12/3.13, and AI-assisted testing. Use as a baseline for constitution extraction and code audits.

## Applies If (ALL must hold)

- Bootstrapping a new TypeScript repo and pulling the strict tsconfig.json baseline.
- Designing a Next.js 15 App Router architecture: deciding Server vs Client boundaries.
- Modernizing a Python codebase to PEP 742 (TypeIs), PEP 705 (ReadOnly), asyncio.TaskGroup.
- Selecting AI coding tools (Claude Code, Cursor, Copilot) for a workflow segment.
- Selecting AI testing tools (Katalon, mabl, testRigor) and wiring them into CI.
- Auditing agent-generated code against "what current looks like."
- Writing or updating a project's .aidocs/constitution.md to encode 2026-current standards.

## Skip If (ANY kills it)

- Legacy / LTS environments (Python 3.10, Node 18, React 17) — patterns here require newer runtimes.
- Embedded / WASM / extension contexts where RSC or pino are irrelevant.
- Static-site generators (Astro, Hugo, Gatsby) — the React 19 / Next.js 15 sections don't apply.
- Solo prototypes where strict tsconfig kills momentum; start strict on team projects.
- Greenfield tasks better served by a more specific sibling methodology.

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

- parent skill: `free/dev/software-developer/`
