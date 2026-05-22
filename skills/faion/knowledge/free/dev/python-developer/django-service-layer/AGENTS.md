---
slug: django-service-layer
tier: free
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces Django service functions (kwarg-only writes wrapped in transaction.atomic, full_clean before save, domain exceptions, on_commit dispatch) centralising business logic outside views.
content_id: "187d5dc932500074"
complexity: medium
produces: code
est_tokens: 2900
tags: [django, service-layer, hacksoft, transactions, architecture]
---

# Django Service Layer Pattern

## Summary

**One-sentence:** Centralise every write operation in a keyword-only service function inside `apps/<app>/services.py` that wraps the work in `transaction.atomic()`, calls `full_clean()` before save, raises domain exceptions, and dispatches Celery tasks via `transaction.on_commit()`.

**One-paragraph:** Business logic in views cannot be tested without HTTP machinery; logic in serializers bypasses the service transaction; logic in model `save()` overrides leaks across managers and admin actions. The service layer is the single place where writes happen. Each service takes keyword-only arguments, opens one `transaction.atomic()` for multi-model writes, validates model instances with `full_clean()` before `save()`, raises domain exceptions (NotFoundError, ValidationError, PermissionDeniedError) instead of HTTP exceptions, and queues side-effects (emails, Celery tasks) via `transaction.on_commit()` so they only fire after a successful commit.

**Ефективно для:** any Django app following HackSoft styleguide; views growing fat with logic; logic duplicated across view + Celery + admin; refactor to enable management commands to reuse the same code path.

## Applies If (ALL must hold)

- Any write operation that modifies one or more models.
- Business logic that spans multiple models (create order + create order items).
- Operations with side effects (send email, queue background task, write to audit log).
- Admin actions, Celery tasks, and management commands that implement business rules.
- Any logic that needs to be called from more than one entry point (view + task + management command).

## Skip If (ANY kills it)

- Trivial wrappers that do nothing but `Model.objects.create()` — add no value.
- Read-only operations — those belong in `selectors.py`.
- View-only glue (parsing request, setting HTTP headers) — that stays in the view.
- Orchestration scripts / management commands that call existing services — they consume services, they are not services themselves.

## Prerequisites

| Artifact | Format | Source |
|----------|--------|--------|
| `apps/<app>/models.py` | Python | repo |
| `core/exceptions.py` (domain exception base) | Python | repo |
| Existing view / admin / Celery call site holding the write | Python | repo |
| `transaction.atomic` import path verified | Python | Django stdlib |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `django-selectors` | reads belong in selectors; services consume their output |
| `django-quality-logging` | structlog discipline for logger calls inside services |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: kwarg-only, atomic, full_clean, domain exceptions, on_commit | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for service-function metadata + signature examples | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: extract → contract → atomic → exceptions → on_commit | ~500 |
| `content/05-examples.xml` | optional | worked example: order creation with multi-model atomic write + on_commit notification | ~400 |
| `content/06-decision-tree.xml` | essential | route between service, selector, view, model.save() override | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Signature design | sonnet | kwarg-only template |
| Transaction boundary placement | opus | nested atomic / savepoint judgement |
| Domain exception design | opus | exception hierarchy decisions |
| on_commit refactor of side effects | sonnet | mechanical wrap of `task.delay` calls |

## Templates

| File | Purpose |
|------|---------|
| `templates/service_create.py` | service skeleton for create with full_clean + on_commit |
| `templates/service_update.py` | service skeleton for partial update |
| `templates/exceptions.py` | domain exception base classes (ApplicationError + subtypes) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-service-layer.py` | AST check: kwarg-only, transaction.atomic present for multi-model writes, no `.delay(` outside on_commit, raises domain exceptions | pre-commit / CI |

## Related

- [[django-selectors]] — read counterpart
- [[django-serializers]] — views call services with `serializer.validated_data`
- [[django-testing]] — services are tested directly without HTTP

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is this a write?" through "multi-model?" and "side-effects?" to one of: service in `services.py`, inline (single-line `.create`), selector (read), or view (HTTP glue). Used to keep `services.py` from filling with trivial wrappers and to keep model `save()` overrides empty.
