---
slug: logging-patterns
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Emit structured JSON logs with correlation IDs, level discipline, masked sensitive fields, and middleware-attached context for every request.
content_id: "b2318604d6400096"
complexity: medium
produces: code
est_tokens: 4000
tags: [logging, structured-logs, observability, json, correlation-id]
---
# Structured Logging Patterns

## Summary

**One-sentence:** Emit structured JSON logs with correlation IDs, level discipline, masked sensitive fields, and middleware-attached context for every request.

**One-paragraph:** Logs are JSON objects, never plain text. Every request carries a correlation_id propagated via middleware; every log line includes it. Levels follow a contract (ERROR for actionable, WARN for degraded, INFO for state changes, DEBUG for verbose). Sensitive fields (PII, secrets, tokens) are masked in a single pipeline stage. Logs ship to an aggregator (Loki, ELK, Datadog). Output is the logging module + middleware + redaction rules.

**Ефективно для:**

- Backend services where log volume + searchability matter.
- Multi-service architectures needing request tracing.
- Compliance contexts requiring PII redaction.
- Replacing print/log.info('...') with reviewable structured calls.

## Applies If (ALL must hold)

- Service emits logs as part of its operational story.
- Log aggregator exists (Loki, ELK, Datadog, Cloud Logging).
- Requests have an identifiable boundary (HTTP request, message consumption, worker job).
- PII or secrets may appear in logged payloads.

## Skip If (ANY kills it)

- Single-binary CLI where stderr is the only output channel.
- Embedded systems with no aggregator and constrained memory.
- Services that emit only metrics + traces, no logs by design.
- Logs go to a managed service that owns redaction + structure entirely.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Logging library chosen per language (structlog, zap, slog, winston) | config | platform |
| Log aggregator endpoint + index schema | config | platform |
| PII field list to redact (emails, phones, tokens) | policy | security |
| Correlation-ID source: request header, generated UUID, parent context | ADR | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-error-handling]] | Error logs carry structured fields matching error chain. |
| [[go-error-handling-patterns]] | Error wrapping preserves fields the logger surfaces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (JSON output, correlation_id everywhere, level discipline, no PII in logs, single redaction pipeline, no print statements) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for logging module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick library → middleware → redaction → level audit → aggregator | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `middleware_wiring` | sonnet | Plug correlation_id into request context. |
| `redaction_rules` | sonnet | Field-list-driven redaction pipeline. |
| `level_audit` | sonnet | Walk existing log calls; reclassify by contract. |

## Templates

| File | Purpose |
|------|---------|
| `templates/structlog-config.py` | structlog (Python) config with JSON renderer + processors |
| `templates/request-middleware.py` | Middleware: bind correlation_id + request context |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-logging-patterns.py` | Validate logging module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[api-error-handling]]
- [[go-error-handling-patterns]]
- [[django-celery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps service architecture, log destination, and PII exposure to a rule from `01-core-rules.xml`, telling the agent whether to apply the conventions or skip for managed/CLI cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
