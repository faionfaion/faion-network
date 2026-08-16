<!--

purpose: ADR template for one inter-service communication decision
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400 tokens when loaded as context
-->



# ADR-XXX: <call_name> communication style

## Context

- Caller: <caller>
- Downstream(s): <downstream>
- Expected QPS: <qps>
- p99 latency budget: <latency_budget_ms>ms
- Downstream p99: <p99_downstream_ms>ms
- Fan-out consumers: <fan_out_consumers>
- Durability required: <durability_required>

## Decision

Use **<communication_style>**.

## Rationale

- <primary_rationale>
- <secondary_rationale>

## Schema

- Registered at: <schema_registry_url>
- Compatibility rule: backward-only (consumers must work with N and N+1 versions of the producer).

## Idempotency

- Mechanism: <idempotency_mechanism>
- Server dedupe: <dedupe_mechanism>

## Retries

- Policy: <retry_policy>

## Observability

- Tracing: <tracing_propagation>
- Metrics: <metrics>
- Alerts: <alerts>

## Alternatives considered

- <alternative_1>
- <alternative_2>
