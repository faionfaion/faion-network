<!-- purpose: Service-level observability spec listing pillar status + SLO + alert rules -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~350 tokens when loaded as context -->

# {{service_name}} — observability spec

## Pillars

- [ ] Structured JSON logs with trace_id + span_id
- [ ] RED metrics on every endpoint (rate / errors / duration)
- [ ] OTel tracing with W3C propagation
- [ ] PII redaction in spans + logs

## OTel config

- SDK: {{language SDK + version}}
- Endpoint: {{OTLP_ENDPOINT}}
- Propagator: `tracecontext,baggage`
- Resource attrs: service.name={{service_name}}, service.version={{semver}}, deployment.environment={{env}}

## SLO

| Metric | Target | Alert |
|--------|--------|-------|
| Availability | 99.9% | error rate > 0.1% for 5min |
| p99 latency | < {{p99_ms}}ms | p99 > target for 5min |

## RED metrics

| Metric | Type | Labels |
|--------|------|--------|
| `http_requests_total` | counter | method, route, status |
| `http_request_errors_total` | counter | method, route, status |
| `http_request_duration_seconds` | histogram | method, route |

## PII redaction list

- request.body for /api/auth/* endpoints
- http.user.email → http.user.email_hash
- http.user.phone → omit
- network.peer.address → /24-truncated
