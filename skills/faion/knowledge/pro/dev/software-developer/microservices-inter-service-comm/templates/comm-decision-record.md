<!-- purpose: ADR template for one inter-service communication decision -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400 tokens when loaded as context -->

# ADR-XXX: {{call_name}} communication style

## Context

- Caller: {{caller}}
- Downstream(s): {{downstream}}
- Expected QPS: {{qps}}
- p99 latency budget: {{latency_budget_ms}}ms
- Downstream p99: {{p99_downstream_ms}}ms
- Fan-out consumers: {{fan_out_consumers}}
- Durability required: {{yes|no}}

## Decision

Use **{{rest|grpc|async-kafka|async-rabbitmq|async-sqs}}**.

## Rationale

- {{primary reason — durability / fan-out / latency / type-safety}}
- {{secondary reason}}

## Schema

- Registered at: {{schema_registry_url}}
- Compatibility rule: backward-only (consumers must work with N and N+1 versions of the producer).

## Idempotency

- Mechanism: {{Idempotency-Key header | idempotency_key field | event header key}}
- Server dedupe: {{Redis 24h TTL | DB unique constraint | consumer dedupe table}}

## Retries

- Policy: {{exponential backoff 3 attempts, max 5s, jitter | none for fire-and-forget | DLQ after 5 redeliveries}}

## Observability

- Tracing: {{OTel W3C trace context propagation}}
- Metrics: {{histogram of latency, counter of failures by code}}
- Alerts: {{p99 > budget for 5min, error rate > 1%}}

## Alternatives considered

- {{Alternative 1 — why rejected}}
- {{Alternative 2 — why rejected}}
