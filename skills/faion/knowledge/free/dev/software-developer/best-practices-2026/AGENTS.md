# Software Development Best Practices 2026

## Summary

A 2026-snapshot reference of current-stable practices across AI-assisted coding, TypeScript 5, React 19 / Next.js 15, Python 3.12/3.13, and AI-assisted testing. Intended as a constitutional source: agents extract relevant clauses into `.aidocs/constitution.md` and make decisions from there, not from this file directly.

## Why

Stacks evolve faster than training data. Without an explicit current-state reference, agents default to training-era patterns: React 17 hooks, `Optional[X]` over `X | None`, outdated tsconfigs. This document provides a versioned baseline that can be diffed against a project's actual config and used to open upgrade tasks.

## When To Use

- Bootstrapping a new TypeScript repo and pulling the strict `tsconfig.json` baseline.
- Designing a Next.js 15 App Router architecture: deciding Server vs Client boundaries.
- Modernizing a Python codebase to PEP 742 (`TypeIs`), PEP 705 (`ReadOnly`), `asyncio.TaskGroup`.
- Selecting AI coding tools (Claude Code, Cursor, Copilot) for a workflow segment.
- Selecting AI testing tools (Katalon, mabl, testRigor) and wiring them into CI.
- Auditing agent-generated code against "what current looks like."

## When NOT To Use

- Legacy / LTS environments (Python 3.10, Node 18, React 17) — patterns here require newer runtimes.
- Embedded / WASM / extension contexts where RSC or `pino` are irrelevant.
- Static-site generators (Astro, Hugo, Gatsby) — the React 19 / Next.js 15 sections don't apply.
- Solo prototypes where strict tsconfig kills momentum; start strict on team projects.
- Greenfield tasks better served by a more specific sibling methodology.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-assisted-dev.xml` | AI tool selection matrix (Copilot / Cursor / Claude Code), prompt engineering rules, risk of AI-generated defects. |
| `content/02-typescript-5.xml` | Strict tsconfig baseline, decorators, const type parameters, mapped/template/conditional types. |
| `content/03-react19-nextjs15.xml` | Server vs Client component rules, Server Actions, Next.js 15 route structure, performance data. |
| `content/04-python-3-13.xml` | Python 3.13 features (no-GIL experimental, JIT experimental), asyncio patterns, modern type hint syntax. |
| `content/05-ai-testing.xml` | AI testing tool comparison, self-healing tests, agent-generated test review checklist. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig-strict.json` | 2026-recommended strict tsconfig baseline. |
| `templates/bp2026-drift.sh` | Drift-detector: checks tsconfig, package.json, pyproject.toml against the 2026 baseline. |
