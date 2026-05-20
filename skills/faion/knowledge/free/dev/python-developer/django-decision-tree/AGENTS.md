---
slug: django-decision-tree
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A comprehensive decision framework for Django development.
content_id: "851e97dc44d4ae18"
tags: [django, decision-making, architecture, frameworks, deployment]
---
# Django Decision Tree

## Summary

**One-sentence:** A comprehensive decision framework for Django development.

**One-paragraph:** A comprehensive decision framework for Django development. Makes the right architectural decisions early in a Django project to prevent costly refactoring later. Covers framework selection, API framework choices, architecture patterns, database selection, deployment strategies, and third-party package evaluation with real-world examples and trade-off analysis.

## Applies If (ALL must hold)

- Starting a new Django project and choosing between Django and alternatives (FastAPI, Flask, etc.).
- Selecting an API framework: Django REST Framework vs Django Ninja vs raw Django views.
- Evaluating architecture patterns for growing codebases — when to introduce a service layer or clean architecture.
- Choosing a database backend (PostgreSQL, MySQL, SQLite) based on project characteristics.
- Planning deployment strategy: PaaS vs VPS vs Kubernetes vs Serverless.
- Evaluating third-party packages for quality, maintenance, compatibility, and security.
- Code placement reviews — deciding where a new function belongs in the Django structure.
- Onboarding developers to project architecture and explaining design rationale.
- Architecture review of Django repo that has grown past 50 models.
- Third-party package vetting — comparing candidate Django packages by maintenance and compatibility.

## Skip If (ANY kills it)

- After spec sign-off with deployment chosen — re-running the full tree wastes cycles.
- When the choice is already constrained by infrastructure or team policy.
- Tiny scripts, ETL jobs, or single-page admin tools — Django is overkill.
- Greenfield projects where the bottleneck is product-market fit, not architecture.
- For a single feature inside an existing Django project — use code-placement guidance only.

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
