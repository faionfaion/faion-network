# Agent Integration — Microservices Design

## When to use
- Multiple teams (or future teams) need independent deploy cadence — release coupling is the actual pain.
- A bounded context has clearly different scaling profile (CPU-heavy ML inference vs. CRUD admin) — splitting unlocks targeted scaling.
- Regulatory boundary (PII, payments) needs to be physically isolated from the rest of the system.
- Polyglot stack is justified by domain (Python ML service alongside a Node BFF).
- An existing modular monolith has stable seams that have been validated for ≥6 months.
- Greenfield design where the bounded contexts are *known* (not guessed) from prior product experience.

## When NOT to use
- Solo founder / single team / pre-PMF — you'll pay the distributed-systems tax with no organizational return. Build a modular monolith.
- Bounded contexts are not yet stable — splitting now bakes in the wrong seams; refactoring across services is 10× the cost of refactoring inside a monolith.
- Team has no platform engineering capability — observability, CI/CD, schema registry, service mesh are not optional.
- "Microservices because Netflix" — cargo-culting a pattern that solved their org problem, not yours.
- Tight transactional invariants across the would-be services — distributed transactions and sagas are expensive; stay in one DB.
- Latency-critical path that fans out to many services adds tail latency you can't afford.

## Where it fails / limitations
- **Distributed monolith.** Services that deploy in lockstep, share a database, or call each other synchronously in long chains are a monolith with extra YAML.
- **Data ownership confusion.** "Each service owns its data" is famously violated by reporting / analytics / search needs. Without CDC + a separate analytical store, ownership lines blur.
- **Testing in production.** Local docker-compose with all services rarely matches prod topology; integration testing slips to staging or prod.
- **Operational tax.** Cost per service: CI pipeline, deploy hook, on-call runbook, SLO, dashboard, dependency map. 10 services = 10× the toil unless you templatize.
- **Schema coupling via sync APIs.** Service A's REST contract is Service B's runtime dependency. Without a contract test suite, every PR risks breaking consumers.
- **Latency budgets.** Each hop adds 1-10ms; a 7-hop request pattern silently violates p99 budgets.
- **Inter-service auth and tenancy.** mTLS / JWT / SPIFFE is a separate infrastructure project, not a checkbox.
- **Cascading failure.** Without circuit breakers, retries, bulkheads, one slow dependency takes down the system. The README hints at this; production needs explicit chaos testing.

## Agentic workflow
Drive microservices design as a four-pass pipeline: (1) a domain-decomposition agent runs Event Storming + bounded-context analysis on the product spec and proposes service boundaries with their public events; (2) a contract-first agent generates OpenAPI / AsyncAPI specs per service before any code; (3) a scaffolding agent (one per service) generates the FastAPI / Express skeleton, Dockerfile, health endpoints, and message bus client from the contracts; (4) a topology-review agent flags sync call chains > 2 hops, missing circuit breakers, missing idempotency keys, and shared databases. The single highest-leverage rule for agents: **always block on the topology review** — generated code that compiles can still be a distributed monolith.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — execute service-by-service tasks as SDD items with quality gates: every PR must include a contract test, a health endpoint, and a circuit-breaker config.
- A purpose-built **bounded-context analyst** (worth creating): given a product spec, output `services.md` with `Service | Owned data | Public events | Public commands | Latency budget`.
- A purpose-built **contract drift detector** (worth creating): on any PR touching `openapi.yaml` or `events-contracts/`, fail if a field changes without a deprecation window or version bump.
- A purpose-built **topology auditor** (worth creating): parses service call graphs (e.g., from Tempo/Jaeger traces) and flags sync chains, fan-out hotspots, missing timeouts.
- `password-scrubber-agent` — events and request payloads carry PII; scrub fixtures and dumps before sharing.

### Prompt pattern
Decomposition:
```
Given the product spec in <spec>, propose 3-7 services. For each:
name, single-sentence purpose, owned aggregates, owned data tables,
3-5 public events emitted, 3-5 public commands accepted, expected
RPS, p99 latency budget. Reject any service that owns no data
or has no public events ("anemic service"). Output a Mermaid
service diagram.
```

Topology audit:
```
Read the OpenAPI spec for each service in services/. For every
synchronous call between services, list: caller → callee, path,
timeout, retry policy, circuit breaker. Flag any call without a
timeout. Flag any chain longer than 2 sync hops. Flag any case
where caller and callee share a database. Output as a markdown
report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `kubectl` / `kustomize` / `helm` | Deploy services to k8s | https://kubernetes.io/docs/tasks/tools/ |
| `docker compose` | Local multi-service dev (caveat: not prod-equivalent) | https://docs.docker.com/compose/ |
| `buf` | Linting and breaking-change detection for protobuf / gRPC | https://buf.build |
| `oapi-codegen` / `openapi-generator` | Generate clients from OpenAPI specs (mandatory for contract-first) | https://github.com/OpenAPITools/openapi-generator |
| `schemathesis` | Property-based testing against an OpenAPI contract | https://schemathesis.readthedocs.io |
| `pact` (CLI + broker) | Consumer-driven contract testing across services | https://docs.pact.io |
| `dapr` CLI | Sidecar runtime for service invocation, pub/sub, state | https://docs.dapr.io |
| `linkerd` / `istioctl` | Service-mesh installation, sidecar injection, traffic policy | https://linkerd.io / https://istio.io |
| `kafkactl` / `rpk` | Inspect topics, consumers, lag for async services | https://github.com/deviceinsight/kafkactl ; https://docs.redpanda.com |
| `k6` / `locust` | Load test individual services and the gateway | https://k6.io ; https://locust.io |
| `claude` (Anthropic CLI) | Run decomposition / contract / audit passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kong / Tyk / KrakenD | OSS / SaaS API gateway | API yes | Rate limit, auth, routing in front of services. |
| AWS API Gateway / Cloudflare API Shield | SaaS | yes | Managed gateway; cheaper than self-hosting at low scale. |
| Linkerd | OSS service mesh | yes | mTLS + retries + golden metrics with the lowest ops cost. |
| Istio | OSS service mesh | yes | More features, more ops. Pick if you need authz policies. |
| Consul / Eureka | OSS service discovery | yes | If you don't have k8s DNS-based discovery. |
| RabbitMQ / Kafka / NATS / SQS | OSS / SaaS message bus | API yes | Async glue between services. NATS for low-latency, Kafka for replay. |
| Confluent Schema Registry / Buf BSR | SaaS | yes | Versioned event/contract storage; CI-checked. |
| Temporal.io | OSS + SaaS | SDK | Replaces brittle multi-service saga code with durable workflows. |
| Dapr | OSS sidecar | yes | Service invocation + pub/sub + state without coupling code to brokers. |
| Postman / Stoplight / Redocly | SaaS | yes | OpenAPI lifecycle: design, mock, doc, test. |
| LaunchDarkly / Flagsmith / Unleash | SaaS / OSS | yes | Per-service feature flags; required to ship microservices safely. |

## Templates & scripts
The README ships service structure, FastAPI skeleton, RabbitMQ producer/consumer, and an architecture diagram. The high-leverage missing piece is a **service generator** so every new service starts with the same observability and resilience defaults. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# new-service.sh — scaffold a new service with prod defaults.
# Usage: new-service.sh <service-name>
set -euo pipefail
name="${1:?usage: new-service.sh <service-name>}"
dir="services/$name"
[[ -e "$dir" ]] && { echo "$dir exists"; exit 1; }
mkdir -p "$dir"/{src/{api,domain,infrastructure},tests,deploy}

cat > "$dir/src/main.py" <<'PY'
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
app = FastAPI()
Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)
@app.get("/healthz")
async def live(): return {"status": "ok"}
@app.get("/readyz")
async def ready(): return {"status": "ok"}
PY

cat > "$dir/Dockerfile" <<'DOCK'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt . && pip install --no-cache-dir -r requirements.txt
COPY src/ src/
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
DOCK

cat > "$dir/openapi.yaml" <<'YAML'
openapi: 3.1.0
info: { title: $name, version: 0.1.0 }
paths: {}
YAML

cat > "$dir/.slo.yaml" <<'YAML'
service: $name
slos:
  - name: availability
    target: 99.9
    window: 30d
  - name: latency_p99
    target_ms: 300
    window: 7d
YAML
echo "scaffolded $dir"
```

Pair with a CI job that fails any merge to a service dir without an updated `openapi.yaml`, `.slo.yaml`, and runbook.

## Best practices
- **Bounded context first, deployment second.** Don't split until you have evidence the seam is stable; a wrong split is more painful than a too-large monolith.
- **Async by default for cross-service writes.** Every cross-service synchronous call is a fragility tax; prefer event-driven choreography or saga orchestration.
- **Contract-first, not code-first.** OpenAPI / AsyncAPI / proto in a separate repo, generated clients per consumer, contract tests in CI for both sides.
- **One service = one repo or one path with independent CI.** Anything less means you don't actually have independent deploys.
- **Every service ships an SLO + runbook.** No SLO ⇒ no on-call ⇒ no microservice. Use the README's `.slo.yaml` template as a hard requirement.
- **Idempotent message handlers.** Brokers redeliver; handlers must use `(message_id, …)` dedup tables.
- **Service catalog is mandatory.** Backstage / OpsLevel / a markdown registry — without it, agents can't navigate the topology and humans give up.
- **Per-service database.** "Don't share databases" is non-negotiable; if you must read across, use CDC + a read-only projection.
- **Local dev parity.** docker-compose for everything, Tilt / Skaffold for k8s, Telepresence to debug a single service against staging.
- **Kill switches and feature flags.** Every public endpoint behind a flag; this is the only way to deploy 10 services daily without incidents.

## AI-agent gotchas
- **Distributed-monolith generation.** Agents propose 7 services, all calling each other synchronously, all using one Postgres. Force a topology audit pass and reject shared DBs.
- **Anemic services.** Agents create services that only do CRUD on one table — that's a library, not a service. Require ≥3 public events per service and a real domain model.
- **Hallucinated middlewares.** Agents drop in `app.add_middleware(SomeAuthMiddleware)` for libraries that don't exist or are abandoned. Pin libraries via `requirements.txt` and run `pip install --dry-run` in CI.
- **Missing timeouts and retries.** Generated `httpx.AsyncClient` calls have a 10s default and infinite retries — both wrong. Force `timeout=2.0`, `retries=2`, circuit breaker, and bulkhead per call.
- **Sync-only message handlers.** Agents copy the producer pattern but consume synchronously without acknowledgements — messages get re-delivered forever. Require ack/nack discipline.
- **Schema-evolution amnesia.** Agents change OpenAPI fields freely; consumers break. Wire a `buf breaking` (proto) or `oasdiff` (OpenAPI) check in CI.
- **No correlation ID propagation.** Generated services log without `trace_id`/`correlation_id`. Standardize on W3C Trace Context middleware in every service template.
- **Per-service auth re-implemented.** Each service rolls its own JWT validation slightly differently. Centralize in a shared library or sidecar, never in service code.
- **Health-check theater.** Agents return `{"status": "ok"}` regardless of dependency state. Require readiness probes that actually check DB and broker connectivity.
- **Cascading deploy.** Agents deploy services in the wrong order on a breaking change. Hard rule: never let an autonomous agent merge a contract-breaking change; human gate required.

## References
- Newman, S. — "Building Microservices," 2nd ed. O'Reilly, 2021.
- Richardson, C. — "Microservices Patterns." Manning, 2018.
- Fowler / Lewis — "Microservices" (the original article). https://martinfowler.com/articles/microservices.html
- Microsoft — "Microservices architecture style." https://learn.microsoft.com/azure/architecture/guide/architecture-styles/microservices
- AWS — "Implementing microservices on AWS." https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/
- Backstage (service catalog). https://backstage.io
- Pact (contract testing). https://docs.pact.io
- Sibling: `pro/dev/software-architect/microservices-architecture/` — broader architectural view.
- Sibling: `pro/dev/software-architect/event-driven-architecture/` (this batch) — async backbone.
- Sibling: `pro/dev/software-architect/service-mesh/` — mesh deep-dive.
