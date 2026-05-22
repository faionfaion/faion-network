---
slug: django-quality-logging
tier: free
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django production logging + Sentry configuration report (settings diff + structlog wiring + Sentry init + check --deploy verdict).
content_id: "aaccb3570c512681"
complexity: medium
produces: report
est_tokens: 3200
tags: [django, logging, structlog, sentry, observability]
---

# Django Structured Logging and Observability

## Summary

**One-sentence:** Configure structlog + django-structlog + Sentry so every production Django request emits JSON logs with bound request context and unhandled exceptions land in Sentry with scrubbed PII.

**One-paragraph:** Production Django needs structured JSON logging (structlog + django-structlog RequestMiddleware for automatic request_id / user_id / ip binding), Sentry error tracking with DjangoIntegration + send_default_pii=False + scrubbed before_send, and `manage.py check --deploy --fail-level WARNING` gating in CI. Freeform string logging is noise; structured events with bound context are signals that enable alerts and incident investigation across Datadog / Loki / CloudWatch.

**Ефективно для:** Django shops moving from stdlib logging to structured pipelines (Datadog, Loki, CloudWatch ingestion); pre-launch hardening for any user-facing Django app; quarterly observability audits.

## Applies If (ALL must hold)

- Any Django project shipping to production where incident investigation matters.
- Logging migration from stdlib logging to structlog for cloud log aggregation.
- Setting up Sentry error tracking for a new or existing Django project.
- Projects deploying to platforms that ingest JSON logs natively (GCP, AWS, Datadog).
- Multi-service systems where correlated trace IDs across services are needed.

## Skip If (ANY kills it)

- Throwaway prototypes — stdlib logging with console output is sufficient.
- Self-hosted projects without log aggregation infrastructure — freeform logs are acceptable when no one is querying them programmatically.
- Codebases already on a different structured logging solution (e.g., python-json-logger) — don't migrate for its own sake.

## Prerequisites

| Artifact | Format | Source |
|----------|--------|--------|
| `config/settings/base.py` | Python module | repo |
| `config/settings/production.py` | Python module | repo |
| `MIDDLEWARE` list | Python list literal | settings file |
| `SENTRY_DSN` | env var | `.env` or secret store |
| `requirements*.txt` or `pyproject.toml` | dep manifest | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `python-code-quality` | logger discipline (no print, no bare except) precedes structlog wiring |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (structlog, Sentry, LLM-prompt context, no-print, secrets) | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the logging audit report + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 6-step procedure from audit → install → wire → verify → ship | ~500 |
| `content/05-examples.xml` | optional | end-to-end worked example: greenfield Django 5.2 logging setup | ~400 |
| `content/06-decision-tree.xml` | essential | route between "install structlog", "migrate stdlib", "skip" | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Settings diff generation | sonnet | mechanical patching, deterministic |
| Sentry before_send scrubber design | sonnet | enumerated PII keys |
| Migration narrative + risk write-up | opus | judgment on rollout staging |
| Validation runner | sonnet | runs script, parses output |

## Templates

| File | Purpose |
|------|---------|
| `templates/logging.py` | structlog + LOGGING dict skeleton for `settings/base.py` |
| `templates/sentry_init.py` | sentry_sdk.init + scrub_sensitive_data scrubber |
| `templates/audit-report.md` | output skeleton matching `02-output-contract` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-quality-logging.py` | validates the audit report against the schema in `02-output-contract.xml` | after report is generated, before commit |

## Related

- [[python-code-quality]] — no-print + specific exception baseline
- [[django-quality-security]] — `check --deploy` shares the same gate
- [[django-quality-queries]] — `django.db.backends` log level interacts with N+1 detection

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is this a public-facing Django service shipping to prod?" through "is log aggregation already in place?" to one of three conclusions: full structlog+Sentry rollout, structlog-only (no Sentry), or skip-this-methodology (prototype). Used to avoid migrating a hobby project to JSON logs nobody queries.
