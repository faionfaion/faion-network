# Python Ecosystem Overview

## Summary

A routing-layer methodology for classifying a Python project's domain (web / data / ML / automation / embedded), selecting the right toolchain (Python version, package manager, linter, type checker), and routing to the correct framework-specific methodology. Use this as a first-pass router — not as implementation instructions. Once domain and stack are locked, load the specific methodology.

## Why

Python spans incompatible domains. Pulling all of PyTorch + Django + Celery into a simple API project is a common LLM over-reach. The right toolchain (uv, ruff, mypy) is not obvious from training data alone — agents default to outdated combos (pip + black + isort + flake8). Routing correctly at the start saves rework and prevents framework-mixing bugs.

## When To Use

- Routing "we need a Python solution for X" to the correct domain and methodology
- Onboarding a new repo: surveying imports to map them to a domain bucket
- Picking Python version, package manager, and lint/typecheck stack at project bootstrap
- Auditing a codebase for outdated tooling (`black` + `isort` + `flake8` → `ruff`; pip → uv)
- Deciding whether a hot loop should be rewritten in Rust (only after profiling)

## When NOT To Use

- Inside a feature task already scoped to a specific framework — load the specific methodology instead
- Non-Python work
- Choosing between Python web frameworks — route to `python-web-frameworks/` which has the decision matrix
- Performance work where a real profile already exists — this overview's optimization table is qualitative only

## Content

| File | What's inside |
|------|---------------|
| `content/01-toolchain.xml` | Python version selection, uv vs poetry, ruff, type checkers, testing tools |
| `content/02-domains.xml` | Web/data/ML/automation/embedded domain map; framework routing table |
| `content/03-performance.xml` | Optimization strategy table (algorithm → NumPy → Cython → PyO3); profiling first rule |
| `content/04-antipatterns.xml` | uv limitations, free-threading misuse, ruff ALL rules, wrong profiling targets, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap-python.sh` | Bootstrap a modern Python project: uv + ruff + mypy + pytest wired up |
