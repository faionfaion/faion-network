# Logging Patterns

## Summary

Emit structured JSON logs (via structlog or Pino) with a correlation ID on every log entry, mask sensitive fields before writing, and use appropriate log levels (DEBUG/INFO/WARNING/ERROR/CRITICAL). Attach request context via middleware at request start, not per-call.

## Why

Structured logs are machine-parseable — log aggregators (Datadog, Loki, CloudWatch) can filter and alert on JSON fields without regex. A missing request ID makes distributed debugging nearly impossible. Sensitive data in logs (passwords, tokens, PII) creates compliance and security incidents. Excessive DEBUG logs in hot paths degrade throughput.

## When To Use

- Setting up logging for any new service (Python or TypeScript)
- Adding audit trails for compliance (payments, auth events)
- Integrating with OpenTelemetry for distributed tracing
- Diagnosing production incidents where correlation is required

## When NOT To Use

- Short scripts or one-shot jobs — standard print/stderr is fine
- Test output — pytest captures output; structured logs add noise
- Very high-frequency inner loops — log outside the loop or sample

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Structured logging rules, log level guide, sensitive data masking rule |
| `content/02-implementation.xml` | structlog configuration with context vars; request middleware; business event pattern |
| `content/03-antipatterns.xml` | Log-and-throw, logging sensitive data, excessive logging, missing context |

## Templates

| File | Purpose |
|------|---------|
| `templates/structlog-config.py` | Production-ready structlog setup with context vars and sensitive data processor |
| `templates/request-middleware.py` | FastAPI request logging middleware with request ID propagation |
