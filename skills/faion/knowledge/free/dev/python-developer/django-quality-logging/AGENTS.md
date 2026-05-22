---
slug: django-quality-logging
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production Django needs structured JSON logging (structlog + django-structlog for request context), Sentry error tracking, and LLM-optimized prompts for generating high-quality Django code.
content_id: "7b9b028c8425d5d0"
tags: [django, logging, structlog, sentry, observability]
---
# Django Structured Logging and Observability

## Summary

**One-sentence:** Production Django needs structured JSON logging (structlog + django-structlog for request context), Sentry error tracking, and LLM-optimized prompts for generating high-quality Django code.

**One-paragraph:** Production Django needs structured JSON logging (structlog + django-structlog for request context), Sentry error tracking, and LLM-optimized prompts for generating high-quality Django code. Freeform string logging is noise; structured events with bound context are signals that enable alerts and incident investigation.

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
