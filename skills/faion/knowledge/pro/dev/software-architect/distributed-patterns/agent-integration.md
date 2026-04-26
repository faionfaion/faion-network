# Agent Integration — Distributed System Patterns

## When to use
- Designing or reviewing a saga across 3+ services (orchestration vs choreography pick).
- Adding resilience (Circuit Breaker, Bulkhead, Retry+Jitter) to existing service-to-service calls.
- Generating Outbox table + relay code from an entity model to fix dual-writes.
- CQRS / Event Sourcing schema design for an audit-heavy or temporal-query domain.
- Reviewing idempotency keys and dedup tables on POST endpoints and message consumers.
- Drafting compensating-action catalogs for an existing saga.

## When NOT to use
- Simple request/response between two services with single-DB writes — patterns add overhead.
- Strong-consistency requirements where 2PC on a single DBMS is sufficient.
- Prototypes / pre-PMF code; pattern overhead delays learning.
- Pure synchronous monoliths — Saga and Outbox add zero value.
- Domains where eventual consistency is unacceptable (regulatory ledger entries) — use 2PC instead.

## Where it fails / limitations
- Agents over-apply Saga to flows that are local transactions in disguise.
- LLMs frequently emit non-idempotent compensating actions ("refund" without dedup key) — must be reviewed.
- Event Sourcing schema-evolution (upcasters, snapshotting) is poorly handled by code generation; needs human design.
- Circuit-breaker thresholds emitted by the model are hand-wavy; require traffic data to tune.
- Raft/Paxos implementation is never something to generate — always use a battle-tested lib (etcd, ZooKeeper, Hazelcast).
- Out-of-order events: agent will rarely add the version/correlation-ID guards needed.

## Agentic workflow
Run a planner subagent to pick patterns from the brief (consistency, latency, scale), then a coder subagent to emit Outbox tables, saga step handlers, compensations, and Resilience4j/Polly configs. Force a separate failure-mode reviewer pass that walks each step and asks "what if step N fails after step N-1 succeeded?" — capture compensations explicitly. Keep planner on Opus (trade-off heavy), coder on Sonnet, reviewer on Sonnet with chain-of-thought enabled.

### Recommended subagents
- `distributed-architect` (Opus) — pattern selection, consistency/availability trade-offs.
- `saga-coder` (Sonnet) — orchestration definitions (Temporal/Camunda/Step Functions) + handlers.
- `resilience-coder` (Sonnet) — circuit-breaker, bulkhead, retry+jitter wiring.
- `failure-mode-reviewer` (Sonnet) — exhaustive what-if walkthrough; demands compensations + idempotency proof.

### Prompt pattern
```
You are distributed-architect. Flow: order -> payment -> inventory -> shipping.
Consistency: eventual ok, no double-charge. Volume: 100 rps peak.
Output: 1) saga style (choreography/orchestration) with rationale, 2) per-step
compensation, 3) idempotency key strategy, 4) outbox vs CDC choice, 5) 2 alt
designs and why rejected.
```

```
You are failure-mode-reviewer. Walk each saga step. For each, list:
- transient failures and retry policy,
- permanent failures and compensation,
- duplicate-delivery handling,
- ordering guarantees needed,
- timeout values.
Reject if any step has no compensation or no idempotency proof.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `temporal` CLI | Manage Temporal workflows, signals, queries | `brew install temporal`; docs.temporal.io |
| `camunda` Modeler / Zeebe CLI (`zbctl`) | BPMN editing, deploy/inspect workflows | docs.camunda.io |
| AWS Step Functions (`aws stepfunctions`) | State machine deploy, executions, history | aws.amazon.com/step-functions |
| `etcdctl` | Test leader election, locks, watches | etcd.io |
| `consul` CLI | KV, locks, sessions, service discovery | consul.io |
| `kafkactl` / `kcat` | Inspect topics, consumer groups, offsets | github.com/deviceinsight/kafkactl |
| `debezium-server` | CDC source for Outbox | debezium.io |
| `axon-cli` / Axon Server console | Event store inspection, replay | axoniq.io |
| `redis-cli` (with `SET NX PX`) | Verify Redlock-style locks | redis.io |
| `resilience4j-cli` (custom configs) | Validate circuit-breaker YAMLs | resilience4j.readme.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Temporal Cloud | SaaS + OSS | Yes | Workflows-as-code (Go/Java/TS/Python); LLMs handle TS/Python well. |
| Camunda 8 | SaaS + OSS | Partial | BPMN XML — LLM ok at simple flows, drift on complex gateways. |
| AWS Step Functions | SaaS | Yes | ASL JSON; agent emits and validates with `validate-state-machine-definition`. |
| Conductor (Netflix/OBS) | OSS | Yes | JSON workflow defs. |
| EventStoreDB | OSS + cloud | Yes | Event Sourcing native; gRPC/HTTP API. |
| Axon Framework + Axon Server | OSS + cloud | Partial | Java/Kotlin centric; sound for CQRS/ES. |
| Debezium | OSS | Yes | JSON connector configs; agent templates them. |
| Resilience4j / Polly | OSS libs | Yes | YAML/code configs; agent generates. |
| Istio / Envoy | OSS | Yes | Circuit breakers + retries via VirtualService/EnvoyFilter. |
| etcd / ZooKeeper / Consul | OSS | Yes | Use for leader election; never roll your own. |

## Templates & scripts
See `templates.md` for full Saga/Outbox/Resilience4j templates. Inline failure-mode worksheet for every saga step the agent must complete:

```yaml
# saga-step-checklist.yml
step: ChargePayment
inputs: {orderId, amount, idempotencyKey}
on_success: emit PaymentCharged
transient_failures:
  - timeout
  - 5xx from PSP
  retry: exp-backoff base=1s cap=30s, attempts=5, jitter=full
permanent_failures:
  - 4xx (invalid card)
  - fraud_block
  compensation: cancel_order(orderId, reason)
duplicate_delivery: dedup_table(idempotencyKey, ttl=24h)
ordering: per-orderId only
timeout: 10s end-to-end
sla: p99 < 2s
```

## Best practices
- Force the agent to choose orchestration vs choreography in writing — don't accept a hybrid by accident.
- Outbox is non-negotiable when you have DB writes + message publishing in the same flow; the agent often skips it.
- Idempotency keys live at the API boundary AND in the consumer dedup table — agent often picks one, not both.
- Compensations must be commutative + idempotent; reject "soft delete" compensations that leak state.
- Use Temporal/Step Functions over hand-rolled state machines whenever possible — agents emit safer code.
- Pin Resilience4j / Polly configuration via code, not annotations alone, so reviewers can grep policies.
- For Event Sourcing, demand snapshot strategy + upcaster plan before approving the schema.
- Add a "poison pill" branch (DLQ + alert) to every consumer the agent generates.

## AI-agent gotchas
- Models confuse "exactly-once delivery" (impossible) with "exactly-once processing" (possible via dedup) — call it out in the prompt.
- Generated retry loops often lack jitter → thundering herd; require `jitter` field in any retry config.
- Saga code without correlation IDs threaded through every event — agent forgets after step 3.
- Human checkpoint REQUIRED before: enabling new saga in prod, changing event schema (breaking consumers), modifying compensation logic, switching CDC source.
- Agent emits "stub" compensations like `// TODO: refund` — fail review on TODOs.
- Outbox relay polling intervals defaulted too aggressively (100ms) — DoS the DB; require ≥1s with batch.
- Circuit-breaker `slowCallThreshold` left unset — slow successes count as success and never trip.
- LLM picks 2PC for "safety" on cloud DBs that don't support XA — verify driver capabilities.

## References
- Chris Richardson, "Microservices Patterns" — saga, outbox, CQRS catalog.
- Microservices.io patterns: https://microservices.io/patterns/.
- Pat Helland, "Life beyond Distributed Transactions".
- Martin Kleppmann, "Designing Data-Intensive Applications", Ch. 7-9.
- Temporal docs: https://docs.temporal.io/.
- Resilience4j: https://resilience4j.readme.io/.
- Raft visualization: https://raft.github.io/.
