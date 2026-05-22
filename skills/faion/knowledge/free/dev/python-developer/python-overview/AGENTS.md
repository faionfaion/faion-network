---
slug: python-overview
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A routing-layer methodology for classifying a Python project's domain (web / data / ML / automation / embedded), selecting the right toolchain (Python version, package manager, linter, type checker), and routing to the correct framework-specific methodology.
content_id: "5b00f0f44b883e01"
tags: [python, routing, toolchain, performance, profiling]
---
# Python Ecosystem Overview

## Summary

**One-sentence:** A routing-layer methodology for classifying a Python project's domain (web / data / ML / automation / embedded), selecting the right toolchain (Python version, package manager, linter, type checker), and routing to the correct framework-specific methodology.

**One-paragraph:** A routing-layer methodology for classifying a Python project's domain (web / data / ML / automation / embedded), selecting the right toolchain (Python version, package manager, linter, type checker), and routing to the correct framework-specific methodology. Use this as a first-pass router — not as implementation instructions. Once domain and stack are locked, load the specific methodology.

## Applies If (ALL must hold)

- Routing "we need a Python solution for X" to the correct domain and methodology
- Onboarding a new repo: surveying imports to map them to a domain bucket
- Picking Python version, package manager, and lint/typecheck stack at project bootstrap
- Auditing a codebase for outdated tooling (black + isort + flake8 → ruff; pip → uv)
- Deciding whether a hot loop should be rewritten in Rust (only after profiling)

## Skip If (ANY kills it)

- Inside a feature task already scoped to a specific framework — load the specific methodology instead
- Non-Python work
- Choosing between Python web frameworks — route to python-web-frameworks which has the decision matrix
- Performance work where a real profile already exists — this overview's optimization table is qualitative only

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
