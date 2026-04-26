# Django Services Architecture

## Summary

Pattern for isolating Django business logic into a `services/` layer of plain Python functions
(or classes only when DI is required). Services own all DB-mutating operations, outbound API
calls, and transactional boundaries; views/serializers stay HTTP-only. Core rule: service
functions take domain primitives (never `request`), use keyword-only optional args, wrap
multi-write paths in `transaction.atomic()`, and raise domain exceptions — never DRF ones.

## Why

Fat views hide business logic behind HTTP context, making it untestable without a DRF client
and unreusable from Celery tasks or management commands. A thin service function with a clear
signature and Google-style docstring is testable with a plain `pytest` call, reusable from any
entry point, and reviewable for import-boundary violations by an automated agent.

## When To Use

- Adding any DB-mutating logic (create/update/delete) that would otherwise live in a view
- Coordinating multi-model writes needing a single transactional boundary
- Wrapping outbound API/SMTP/SMS calls so views/serializers stay thin
- Making business logic unit-testable without HTTP or DRF context
- Sharing an operation between a view, Celery task, and management command

## When NOT To Use

- Pure functions (validation, formatting, calculation) — those go in `utils/`
- Trivial single-model `obj.field = x; obj.save()` called from one view
- Read-only queryset chaining — keep on the manager / `objects`
- DRF view-only concerns (permission checks, serializer wiring)

## Content

| File | What's inside |
|------|---------------|
| `content/01-service-rules.xml` | Decision tree, function-vs-class rule, lazy imports, keyword-only args |
| `content/02-implementation.xml` | Docstring style, transaction.atomic, update_fields, domain exceptions |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-module.py` | Service module skeleton with lazy imports and domain exception |
