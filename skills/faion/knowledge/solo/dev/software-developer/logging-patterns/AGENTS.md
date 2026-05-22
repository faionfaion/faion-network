---
slug: logging-patterns
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Emit structured JSON logs with correlation IDs, mask sensitive fields, use appropriate log levels, attach context via middleware, integrate with aggregators, prevent PII leaks.
content_id: "1554d307ae7110f6"
tags: [logging, structured-logs, observability, json, correlation-id]
---
# Structured Logging Patterns

## Summary

**One-sentence:** Emit structured JSON logs with correlation IDs, mask sensitive fields, use appropriate log levels, attach context via middleware, integrate with aggregators, prevent PII leaks.

**One-paragraph:** Emit structured JSON logs with correlation IDs, mask sensitive fields, use appropriate log levels, attach context via middleware, integrate with aggregators, prevent PII leaks.

## Applies If (ALL must hold)

- Setting up logging for any new service (Python or TypeScript)
- Adding audit trails for compliance (payments, auth events)
- Integrating with OpenTelemetry for distributed tracing
- Diagnosing production incidents where correlation is required
- New service or module: agent scaffolds a structured-logging baseline (JSON formatter, contextvars, request middleware) before any business logic ships.
- Refactor of legacy print / console.log / fmt.Println debris into structured logs.
- Adding distributed tracing: pair trace_id / request_id injection across services so logs join with spans.
- Compliance/audit (SOC2, HIPAA, PCI): structured logs with retention policy and PII redaction.
- Onboarding a log aggregator (Loki, ELK, Datadog, CloudWatch): agents map fields to indices and dashboards.
- After a P1 incident: postmortems revealing missing logs become input for an agent that proposes new log calls and levels.
- Cost reduction: agents identify high-volume, low-value log lines and propose level downgrades or sampling.

## Skip If (ANY kills it)

- Short scripts or one-shot jobs — standard print/stderr is fine
- Test output — pytest captures output; structured logs add noise
- Very high-frequency inner loops — log outside the loop or sample
- Tiny throwaway scripts where stderr suffices.
- Hot paths where logging cost is measurable (per-row inside a 100k iteration loop) — sample or move to metrics.
- Security-sensitive code paths where any log line is a leak risk (raw payloads, secrets) — emit metric counters instead.
- Real-time / latency-critical signal paths (audio, video, trading) — buffered async logging only; never block.

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

- parent skill: `solo/dev/software-developer/`
