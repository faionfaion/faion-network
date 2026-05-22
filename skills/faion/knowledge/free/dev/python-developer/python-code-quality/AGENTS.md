---
slug: python-code-quality
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern Python code quality in 2025-2026 centers on a streamlined toolchain that replaces the traditional Black + isort + flake8 stack with Ruff - an all-in-one linter and formatter written in Rust that runs 10-100x faster.
content_id: "27c7e1be1a30850c"
tags: [code-quality, linting, type-checking, testing, ruff]
---
# Python Code Quality

## Summary

**One-sentence:** Modern Python code quality in 2025-2026 centers on a streamlined toolchain that replaces the traditional Black + isort + flake8 stack with Ruff - an all-in-one linter and formatter written in Rust that runs 10-100x faster.

**One-paragraph:** Modern Python code quality in 2025-2026 centers on a streamlined toolchain that replaces the traditional Black + isort + flake8 stack with Ruff - an all-in-one linter and formatter written in Rust that runs 10-100x faster. Combined with mypy/pyright for type checking, pre-commit hooks for CI gates, pytest for testing, and bandit for security scanning.

## Applies If (ALL must hold)

- Setting up the lint + format + type-check + security gate on a new Python repo (Ruff + mypy + bandit + pytest-cov + pre-commit).
- Migrating a legacy repo off flake8 + black + isort + autoflake + pyupgrade to Ruff in a single pass.
- Onboarding a Django/FastAPI codebase to strict typing — adding mypy --strict or pyright strict and fixing the long tail iteratively.
- Wiring CI quality gates: zero Ruff errors, zero mypy errors on touched files, 80%+ coverage, no high/critical bandit findings.
- Reviewing PRs with an agent that runs the full quality stack and reports findings (style, types, security, complexity) per file.

## Skip If (ANY kills it)

- One-off scripts, hackathon code, notebook spikes — friction from tooling exceeds value; rely on the editor's built-in linter.
- Repos where the user explicitly chose a different stack (Pylint + Black + flake8). Don't impose Ruff if the team owns its choice.
- Generated code (protobuf stubs, *.pyi, migration files) — exclude from Ruff/mypy via extend-exclude instead of "fixing".
- Code that must run on Python <3.8 — modern Ruff/mypy releases drop those targets; pin older tool versions instead.
- When a refactor and a quality cleanup land in the same PR — split them; reviewers can't tell behavioural changes from formatter noise.

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

- parent skill: `free/dev/python-developer/`
