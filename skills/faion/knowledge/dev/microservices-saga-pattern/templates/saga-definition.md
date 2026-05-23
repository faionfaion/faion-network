<!-- purpose: Saga spec template (steps + compensations + coordination + outbox) -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~450 tokens when loaded as context -->

# {{saga_name}} — saga definition

## Coordination

- Style: {{orchestration | choreography}}
- Orchestrator: {{temporal | camunda | step-functions | n/a}}

## Steps

| # | Service | Action | Compensation | Idempotency Key |
|---|---------|--------|--------------|-----------------|
| 1 | {{svc}} | {{action}} | {{comp}} | (saga_id, step_id) |
| 2 | ... | ... | ... | ... |

## Outbox

- Every step writes via transactional outbox (insert into `outbox` table in same DB tx).
- CDC: Debezium → Kafka topic `{{topic}}.events`.

## Failure handling

- On step N failure: orchestrator executes comp(N-1) → comp(N-2) → ... → comp(1) in reverse order.
- All compensations are idempotent (dedupe via saga_id + step_id).

## Chaos test plan

- [ ] Kill step 1 → no compensations needed (nothing committed).
- [ ] Kill step 2 → comp(1) executes; verify state consistent.
- [ ] Kill step N → comp(N-1)..comp(1) execute in reverse.
- [ ] Duplicate step delivery → no double-effect (idempotency works).

## Observability

- Saga ID propagated in every event/span as `saga.id` attribute.
- Dashboards: saga.completion_rate, saga.compensation_count, saga.duration_p99.
