# API Monitoring

## Summary

Instrument every production API endpoint with Prometheus metrics (RED method: Rate, Errors, Duration), structured JSON logging with a `request_id` correlator, and separate liveness/readiness health probes. Define SLOs before adding metrics — the metrics exist to measure SLO compliance, not the other way around.

## Why

Without bounded Histogram labels and a `request_id` thread, diagnosing a p95 spike requires guessing across unrelated log lines. Liveness probes that call the database cascade into restart storms when the DB is slow. Burn-rate alerts (multi-window) detect SLO burn faster with fewer false pages than static thresholds.

## When To Use

- Any HTTP/gRPC/GraphQL service in production with paying users or SLOs
- Adding a new endpoint — instrument before launch, not after the first incident
- Setting up readiness probes for k8s/systemd/load-balancer drain
- Diagnosing a regression (p95 spiked, error rate climbing) via correlated metrics + logs

## When NOT To Use

- Throwaway prototype on localhost — Prometheus scrape config is not a learning goal
- Internal cron job with one user — exit code + email is enough
- When no SLO is defined yet — pick SLOs first, then add metrics

## Content

| File | What's inside |
|------|---------------|
| `content/01-metrics-health.xml` | Prometheus middleware, metric names/labels, RED method, health probe patterns |
| `content/02-logging-alerting.xml` | Structured logging middleware, request_id injection, Prometheus alert rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/metrics_middleware.py` | FastAPI Prometheus middleware: REQUEST_COUNT + REQUEST_LATENCY Histogram |
| `templates/health_endpoints.py` | FastAPI liveness + readiness probes with DB and Redis dependency checks |
| `templates/alert_rules.yml` | Prometheus alert rules: HighErrorRate, SlowResponses, HighRateLimitHits |

## Scripts

none
