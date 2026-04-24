# Agent Integration — Microservices Design

## When to use
- Multiple teams (≥3) blocked on each other's deploys; service boundaries cleanly map to team boundaries (Conway's Law in reverse).
- Independent scaling per workload — checkout traffic ≠ search traffic ≠ catalog traffic.
- Polyglot persistence is a real need (transactional Postgres for orders, document store for catalog, Redis for sessions).
- Compliance / blast-radius isolation: PCI scope, PHI scope, regional data residency must be kept off the main service.
- A monolith that's already been internally modularised (modular monolith) and the seams are clearly load-bearing.
- Long-running async workflows where event-driven decoupling beats request/response chains.

## When NOT to use
- Solo / 2-person teams. Operational overhead (CI per service, deploy choreography, observability) eats more capacity than it returns.
- Pre-product-market-fit. Domain boundaries are unstable; you'll re-cut them three times and pay full distributed-systems tax each rewrite.
- Sub-millisecond synchronous chains (high-frequency trading, real-time bidding). Network hops kill the budget.
- "Microservices for resume." A modular monolith with clean module boundaries delivers most benefits without the distributed pain.
- Tight transactional boundaries across "services" — if every command spans 3 services and 2-phase coordination, the boundary is wrong.

## Where it fails / limitations
- **Distributed monolith.** Services exist but call each other synchronously for every operation. The README's anti-pattern section calls this out — agents reproduce it constantly because it "feels" like microservices.
- **Eventual-consistency UX.** User places an order, navigates to "My Orders," sees nothing because the read projection lags. Without read-your-writes (sticky session on write store, optimistic UI, command-side return) it looks like data loss.
- **Saga rollback is hard.** README's saga is correct in skeleton but compensation in real systems must be idempotent, observable, and bounded. Half-compensated states leak.
- **Service-discovery fragility.** Consul/Eureka/K8s DNS each have failure modes (split brain, stale entries, slow propagation). The circuit-breaker example helps but doesn't fix discovery itself.
- **Schema explosion.** Every event payload is a public API forever. Without a schema registry + compatibility checks, services break each other on deploy.
- **Trace gaps.** Without `traceparent` propagation across HTTP + bus, debugging a "where did the order go?" requires manual log spelunking across 5 services.
- **Versioning drift.** Service A sends `OrderCreated v2`; service B still parses v1. No integration test caught it because tests stubbed v1.
- **Auth/Z bloat.** Every service redoing JWT validation; if logic drifts (one accepts expired tokens, another doesn't) you have a security incident.
- **Local-dev impossibility.** Running 12 services + Kafka + Postgres + Redis + Consul on a laptop is unsustainable; teams default to "shared dev cluster" which becomes a queue.

## Agentic workflow
Drive microservices design as a five-stage pipeline: (1) a domain agent extracts bounded contexts and proposes service boundaries from the spec; (2) a contract agent generates OpenAPI/AsyncAPI/Protobuf schemas and registers them; (3) a code-gen agent produces the per-service skeleton (API + domain + infra) following the README's structure; (4) a resilience agent wires circuit breakers, retries, timeouts, and saga/process-manager skeletons; (5) a review agent runs the anti-pattern checklist (sync chains > 2 hops, shared DB, missing trace propagation, command without idempotency key, event without schema version). Persist the service map, contracts, and event catalogue in `.aidocs/product_docs/service-map.md` so subsequent feature work doesn't re-derive boundaries. Pair with `pro/dev/code-quality/cqrs-pattern/` and `pro/dev/code-quality/event-sourcing-implementation/` for the read-side.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = one service slice (API + handler + repo + outbox + consumer). Opus for boundary cuts; sonnet for routine slice work.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — service configs + Helm values + `.env` files leak DB credentials, JWT secrets, broker URIs. Run before commit.
- A **boundary-review-agent** (worth adding under `agents/`): linter that flags synchronous client calls inside a request handler that don't sit behind a circuit breaker, missing `traceparent` propagation, missing schema-registry registration on event publish, shared-table imports across services.
- `faion-feature-executor` skill — sequential mode keeps contract → producer → consumer → integration-test ordering correct. Out-of-order execution publishes events no one consumes.

### Prompt pattern
Boundary pass:
```
You are a microservices architect. Given the spec in <spec>:
(a) Identify bounded contexts; for each: aggregates owned, language
    of the domain, team(s) responsible.
(b) Propose services; for each: name, ownership, sync API surface
    (OpenAPI), async events emitted (AsyncAPI subjects), data store.
(c) For every cross-service operation, classify as: sync request,
    async event, or saga. Reject any sync chain > 2 hops; rewrite as
    saga or precomputed projection.
```

Anti-pattern review pass:
```
You are reviewing a microservices PR. Flag:
(1) HTTP client call inside a request handler without circuit
    breaker / timeout,
(2) shared-DB import across service module boundaries,
(3) event class without schema_version + occurred_at,
(4) command without idempotency_key,
(5) saga without compensation paths for every step,
(6) missing traceparent propagation on outbound HTTP / bus message,
(7) JWT validation logic copy-pasted vs. shared lib.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `kind` / `k3d` / `minikube` | Local Kubernetes for service-mesh testing | https://kind.sigs.k8s.io |
| `kubectl` + `helm` | Cluster + chart management | https://helm.sh |
| `istioctl` / `linkerd` | Service mesh install + diagnostics | https://istio.io / https://linkerd.io |
| `consul` CLI | Service registry + KV + intentions | https://www.consul.io |
| `nats` CLI | JetStream subjects, streams, consumers | https://nats.io |
| `kcat` (Kafka) | Inspect events, replay from offset | https://github.com/edenhill/kcat |
| `temporal` CLI | Workflow definitions + replays for sagas | https://temporal.io |
| `buf` | Protobuf lint + breaking-change detection | https://buf.build |
| `spectral` | OpenAPI / AsyncAPI lint | https://stoplight.io/open-source/spectral |
| `dapr` CLI | Sidecar runtime for service-to-service + bindings | https://dapr.io |
| `kustomize` | Per-env overlays for k8s manifests | https://kustomize.io |
| `argocd` CLI | GitOps sync for service deploys | https://argo-cd.readthedocs.io |
| `tilt` / `skaffold` / `mirrord` | Inner dev loop against a real cluster | https://tilt.dev / https://mirrord.dev |
| `chaos-mesh` / `litmus` | Failure injection (network, pod kill, latency) | https://chaos-mesh.org |
| `k6` / `vegeta` | Load testing per-service | https://k6.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kubernetes (managed: EKS/GKE/AKS) | SaaS / OSS | yes | Default substrate; agents drive via `kubectl` + Helm. |
| Istio / Linkerd | OSS | yes | mTLS, traffic shifting, retries at mesh; reduces in-app boilerplate. |
| Consul / Nacos / Eureka | OSS | yes | Service discovery + KV + intentions. |
| Apache Kafka / Confluent / Redpanda | OSS / SaaS | yes | Event backbone + schema registry. |
| NATS JetStream | OSS / Synadia | yes | Lightweight bus alt; ergonomic for small fleets. |
| RabbitMQ | OSS / CloudAMQP | yes | Mature broker; quorum queues for HA. |
| AWS SQS + SNS + EventBridge | SaaS | yes | Managed event plumbing without ops overhead. |
| Temporal / Cadence | OSS / Cloud | yes | Owns saga / orchestration; commands stay thin. |
| Apicurio / Confluent Schema Registry / Buf Schema Registry | OSS / SaaS | yes | Compatibility checks on every publish. |
| Datadog / Honeycomb / Grafana Tempo + Loki + Mimir | SaaS / OSS | yes | Traces, logs, metrics at scale; agents query via API. |
| OpenTelemetry Collector | OSS | yes | Vendor-neutral telemetry pipeline; configure once, ship anywhere. |
| Backstage | OSS | yes | Service catalog + golden paths; agents read TechDocs to learn boundaries. |
| Dapr | OSS | yes | Sidecar abstracts pubsub/state/secret store; cuts boilerplate. |
| Hashicorp Vault | OSS / Cloud | yes | Service auth + dynamic DB creds. |
| AWS App Mesh / Cloud Map | SaaS | yes | If already on AWS, native alt to Istio + Consul. |

## Templates & scripts
See `templates.md` for service skeletons and `examples.md` for full inter-service flows. The README ships circuit breaker + saga + service registry. Add a per-service `service.yaml` manifest containing: name, owner, sync API ref, async events emitted/consumed, data store, SLOs. Inline boundary lint:

```bash
#!/usr/bin/env bash
# microservices-lint.sh — boundary anti-pattern scan
set -euo pipefail
root="${1:?usage: microservices-lint.sh SERVICES_DIR}"
fail=0
echo "## Sync HTTP chain depth (must be ≤2 within a request handler)"
grep -rEn 'await self\._client\.|httpx\.|http\.Client' "$root" -A 2 \
  | awk -F: '{print $1}' | sort -u \
  | while read -r f; do
      n=$(grep -cE 'await .+_client\.|httpx\.' "$f" || true)
      [[ "$n" -ge 3 ]] && { echo "deep chain: $f ($n)"; fail=1; }
  done
echo "## Outbound calls without timeout"
grep -rEn 'AsyncClient\(' "$root" | grep -vE 'timeout=' && fail=1 || true
echo "## Events without schema_version"
grep -rEn 'class .*Event' "$root" -A 8 \
  | awk '/class .*Event/{n=$0; ok=0} /schema_version/{ok=1} /^--/ {if(!ok)print n; ok=0}' \
  | tee /tmp/ms.evt && [[ -s /tmp/ms.evt ]] && fail=1 || true
echo "## Commands without idempotency_key"
grep -rEn 'class .*Command' "$root" -A 8 \
  | awk '/class .*Command/{n=$0; ok=0} /idempotency_key|command_id/{ok=1} /^--/ {if(!ok)print n; ok=0}' \
  | tee /tmp/ms.cmd && [[ -s /tmp/ms.cmd ]] && fail=1 || true
echo "## Cross-service shared DB imports"
grep -rEn 'from services\.[a-z_]+\.infrastructure\.database' "$root" \
  | grep -vE 'self_service' && fail=1 || true
exit "$fail"
```

## Best practices
- **Boundaries follow data ownership.** A service owns its tables. No cross-service SQL. Replicate via events into a read model if needed.
- **Async by default, sync when proven needed.** REST/gRPC is fine for queries; mutations across services should publish events and let consumers project.
- **Idempotency-key on every command.** Caller generates it; handler dedups. Without this, retries double-charge.
- **Schema registry is non-optional.** Every event has `schema_version`, `occurred_at`, `aggregate_id`. Compatibility checks block breaking changes pre-merge.
- **Outbox pattern for atomicity.** Write the event to the same DB transaction as the state change; a relay process publishes to the bus. Eliminates "wrote DB but bus lost the event."
- **Circuit breakers on every outbound call.** Config from a central place; per-call timeouts shorter than the request budget. README's circuit breaker is the right shape; wire `httpx` timeout in addition.
- **Saga/process manager owns orchestration.** Don't put multi-step workflows inside a command handler — Temporal/Cadence/Camunda/in-house. README's saga skeleton is fine for choreography; for >3 steps, prefer orchestrated.
- **Distributed tracing is the API.** Every inbound request opens a span; every outbound call propagates `traceparent`. Otherwise debugging cost dominates.
- **One service, one team, one repo (or per-service folder in monorepo).** Cross-team commits to a service are a smell.
- **Local dev: stub external services.** `wiremock`, `localstack`, `testcontainers`. Don't expect engineers to run 12 services to ship a feature.
- **Versioning policy up front.** "Additive only, deprecate before remove, support N-1 for 90 days." Pick now, stop arguing per-PR.
- **Service-level SLOs published.** Each service declares latency/error budgets; downstream callers consume them when sizing timeouts.

## AI-agent gotchas
- **Sync-chain reflex.** Asked to "let order service get user info," agents call `user_service.get_user(...)` synchronously inside the request handler. Constrain to async event + local cache lookup; reject sync chains >2 hops.
- **Distributed monolith on a single repo.** Agents copy the same `User` class into every service module and import across boundaries. Lint the imports.
- **Forgotten timeout.** Agents create `AsyncClient(base_url=...)` without `timeout=`; default is "wait forever." Pin timeouts in templates.
- **Saga without compensation.** Agents emit happy-path saga, skip the compensation branches. Force a checklist: every "do" step has a paired "undo."
- **Event payload bloat.** Agents copy entity state into events ("OrderCreated with full Order JSON"). Events should be intent + minimal facts.
- **Hardcoded service URLs.** `http://order-service:8000` baked in; agents skip env/config injection. Force config-driven addresses.
- **Hallucinated mesh APIs.** Agents invent Istio CRDs (`TrafficPolicy`, `RouteSpec`) that don't exist. Pin to the version's CRD list.
- **Trace propagation gaps.** Agents start a span on inbound but don't pass `traceparent` on outbound HTTP/bus. Provide a single helper and require its use.
- **Local-dev sprawl.** Agents add a new service without updating `docker-compose.yml`/Tilt config. Force "if you add a service, you update local-dev manifest."
- **Human-in-loop on boundary changes.** Splitting a service is a one-way door. Block auto-merge on changes that move tables/aggregates between services.
- **Auth re-implementation.** Agents copy JWT-validation code into each new service. Provide one `auth-middleware` lib and require its import.

## References
- Newman, S. "Building Microservices," 2nd ed. O'Reilly, 2021.
- Richardson, C. "Microservices Patterns." Manning, 2018. https://microservices.io/patterns/
- Fowler, M. "Microservices." https://martinfowler.com/articles/microservices.html
- 12-Factor App. https://12factor.net
- Indu, M. "Mastering Microservices with Java."
- Burns, B. "Designing Distributed Systems." O'Reilly.
- Kleppmann, M. "Designing Data-Intensive Applications." (chapters on replication, partitioning, transactions).
- Vernon, V. "Implementing Domain-Driven Design" — bounded contexts.
- Confluent — Outbox & event sourcing patterns. https://www.confluent.io/learn-more/outbox-pattern/
- Temporal docs. https://docs.temporal.io
- AsyncAPI spec. https://www.asyncapi.com
- Sibling methodologies in this repo: `pro/dev/software-developer/clean-architecture/`, `pro/dev/software-developer/continuous-delivery/`, `pro/dev/code-quality/cqrs-pattern/`, `pro/dev/code-quality/event-sourcing-basics/`, `pro/dev/code-quality/domain-driven-design/`.
