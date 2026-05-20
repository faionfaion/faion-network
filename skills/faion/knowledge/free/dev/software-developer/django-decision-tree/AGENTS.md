---
slug: django-decision-tree
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A deterministic decision framework for placing code in Django applications, partitioning functionality into views (HTTP handling), services (business logic and DB writes), utils (pure functions), integrations (third-party API wrappers), tasks (async/background work), models (data definitions), and serializers (validation and formatting).
content_id: "851e97dc44d4ae18"
tags: [django, architecture, code-placement, layering]
---
# Django Code Decision Tree

## Summary

**One-sentence:** A deterministic decision framework for placing code in Django applications, partitioning functionality into views (HTTP handling), services (business logic and DB writes), utils (pure functions), integrations (third-party API wrappers), tasks (async/background work), models (data definitions), and serializers (validation and formatting).

**One-paragraph:** A deterministic decision framework for placing code in Django applications, partitioning functionality into views (HTTP handling), services (business logic and DB writes), utils (pure functions), integrations (third-party API wrappers), tasks (async/background work), models (data definitions), and serializers (validation and formatting). The dependency direction is strict: views depend on services, services depend on models and utils, utils depend on nothing. This partition ensures every layer is independently testable and prevents the chaos of "where does this function belong?" arguments.

## Applies If (ALL must hold)

- Before writing ANY new function in a Django project — run the decision tree first to choose the file
- Refactoring existing code into proper architectural layers
- Code review to verify correct module placement
- Onboarding agents or new developers to the project's architecture

## Skip If (ANY kills it)

- Non-Django backends — the layer names (views, serializers, tasks) are Django-specific
- Microservices with no shared codebase — each service has its own architecture
- Trivial scripts or management commands with no reuse requirement

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
