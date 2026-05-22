---
slug: python-web-frameworks
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A routing-layer methodology for choosing between Django, FastAPI, and Flask.
content_id: "22d245cea438bc99"
tags: [python, django, fastapi, flask, framework-selection]
---
# Python Web Frameworks

## Summary

**One-sentence:** A routing-layer methodology for choosing between Django, FastAPI, and Flask.

**One-paragraph:** A routing-layer methodology for choosing between Django, FastAPI, and Flask. Lock the choice in constitution.md before writing any code — do not let agents switch frameworks mid-feature. Use this methodology only for the framework decision; once the choice is made, load the framework-specific methodology (python-fastapi, django-models, etc.) and skip this one.

## Applies If (ALL must hold)

- Greenfield Python web project where framework choice is still open
- Migration planning: comparing an existing Flask/Django app against FastAPI
- Hybrid review: FastAPI for public APIs + Django for admin sharing a DB schema
- Tech-debt audit: deciding if a Flask app has outgrown its minimalism
- Onboarding: routing "where do I add X?" to the right framework's conventions

## Skip If (ANY kills it)

- Single-framework codebase where team has already committed — load only that framework's specific methodology
- Choosing between Litestar/Sanic/Quart/Starlette — this methodology covers only Django/FastAPI/Flask
- Non-web Python work (ML batch jobs, scripts, CLIs) — wrong abstraction layer
- Performance-critical pure async scenarios where FastAPI is already chosen

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
