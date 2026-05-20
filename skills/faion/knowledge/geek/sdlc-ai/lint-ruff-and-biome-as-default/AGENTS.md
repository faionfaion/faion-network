---
slug: lint-ruff-and-biome-as-default
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For new Python projects, ruff is the SOLE linter and formatter — it replaces black, flake8, isort, pyupgrade, autoflake and pydocstyle, ships 900+ rules, and runs 10–100x faster than the previous Python toolchain.
content_id: "44abccf90399f43e"
tags: [ruff, biome, linting, formatting, python]
---
# Ruff for Python and Biome for JS/TS as the Sole Linter+Formatter

## Summary

**One-sentence:** For new Python projects, ruff is the SOLE linter and formatter — it replaces black, flake8, isort, pyupgrade, autoflake and pydocstyle, ships 900+ rules, and runs 10–100x faster than the previous Python toolchain.

**One-paragraph:** For new Python projects, ruff is the SOLE linter and formatter — it replaces black, flake8, isort, pyupgrade, autoflake and pydocstyle, ships 900+ rules, and runs 10–100x faster than the previous Python toolchain. For new JavaScript/TypeScript/JSX/CSS/GraphQL projects, biome is the SOLE linter and formatter — it replaces ESLint and Prettier with 491 rules and a single config file. Both tools have --fix / --write flags that AI agents call after every code edit.

## Applies If (ALL must hold)

- Any new Python project — start with ruff in pyproject.toml, no other linter or formatter.
- Any new JS/TS project — start with biome in biome.json, no ESLint, no Prettier.
- Any agent-driven workflow where the inner loop is "edit → format → test"; both tools' speed makes the inner loop sub-second.
- Any monorepo migrating off black/flake8/isort or ESLint/Prettier — migrate one package at a time.

## Skip If (ANY kills it)

- Legacy projects with deeply customized ESLint plug-ins that have no biome equivalent yet — migrate incrementally rather than mid-sprint.
- Projects that ship a public ESLint/Prettier config as a product (e.g., a shareable preset) — biome is not yet a drop-in replacement for that consumption pattern.
- One-off scripts not part of a package; running a formatter on a single ad-hoc file is overhead.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
