# Python Ecosystem Overview

## Summary

**One-sentence:** Routing methodology: classify Python project domain (web/data/ML/automation/embedded) and route to the right framework methodology.

**One-paragraph:** A routing-layer methodology for classifying a Python project's domain (web / data / ML / automation / embedded), selecting the right toolchain (Python version, package manager, linter, type checker), and routing to the correct framework-specific methodology. First-pass router — not implementation instructions. Once domain and stack are locked, load the specific methodology.

**Ефективно для:** тиму, який отримав запит 'нам треба Python для X' і повинен швидко вибрати домен/стек/конкретну методологію — закриває петлю між неоднозначним запитом і чітким маршрутом.

## Applies If (ALL must hold)

- Routing 'we need a Python solution for X' to the correct domain and methodology.
- Onboarding a new repo: surveying imports to map them to a domain bucket.
- Pre-flight before any deeper Python methodology — decide stack first.
- Auditing a polyglot codebase to spot the Python pockets.

## Skip If (ANY kills it)

- Already know the framework (FastAPI, Django) — go directly there.
- Pure infra / DevOps work — Python is incidental.
- Non-Python projects mistakenly tagged python.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Project brief | text | stakeholder / spec |
| Existing repo (if any) | git | to survey imports |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | First-load routing methodology; no upstream dependency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: classify domain first, lock Python version per domain, pick package manager (uv default), load only matching downstream methodologies, never route to multiple frameworks. | ~800 |
| `content/02-output-contract.xml` | essential | Output: decision record with domain, stack, methodology list, Python version. Forbidden: 'web app maybe data app' double routing. | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: domain ambiguity, multi-framework routing, ignoring existing imports. | ~600 |
| `content/05-examples.xml` | medium | Three worked examples: 'we need a REST API' → FastAPI, 'we have CSVs to clean' → pandas + scripts, 'we have a Django shop' → Django stack. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: persistent HTTP service? → web. Batch CSV/parquet? → data. Train model? → ML. Cron jobs? → automation. Hardware? → embedded. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-domain` | sonnet | Judgement call on brief + imports. |
| `emit-decision-record` | haiku | Template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Domain + stack + methodology list + Python version skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-overview.py` | Verify decision record has exactly one domain, one framework, pinned Python version. | Pre-commit when decision record changes. |

## Related

- [[python-basics]]
- [[python-modern-2026]]
- [[python-fastapi]]
- [[python-code-quality]]

## Decision tree

The tree at content/06-decision-tree.xml is the canonical first step for any Python project — it classifies the work into one of five domains (web / data / ML / automation / embedded) and emits the next methodology to load. Always start here.
