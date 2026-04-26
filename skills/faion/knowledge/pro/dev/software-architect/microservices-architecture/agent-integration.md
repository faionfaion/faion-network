# Agent Integration — Microservices Architecture

## When to use
- Decomposing an existing monolith into bounded contexts (Strangler Fig planning).
- Greenfield service-boundary design from a domain brief (events, capabilities, ownership).
- Drafting per-service API specs (OpenAPI / gRPC proto) once boundaries are agreed.
- Reviewing a PR that introduces cross-service calls — checking sync vs async, timeouts, retries.
- Generating skeleton service repos with consistent layout (controller/service/repo + observability).
- Writing ADRs explaining decomposition choices for stakeholders.

## When NOT to use
- Teams under 10 engineers, immature DevOps, or no container orchestration — modular monolith first.
- Pre-PMF products: domain boundaries unstable, agent will codify the wrong cuts.
- Strict-consistency, low-latency core systems (HFT, payment authorization core) — sync monolith wins.
- When org chart cannot match Conway's Law to the proposed services.

## Where it fails / limitations
- Agents over-decompose into nano-services (one CRUD per service) — fix the prompt with min-service-size constraint.
- Generated boundaries follow noun-based ("UserService", "OrderService") rather than capability/process boundaries.
- Async-vs-sync choice defaults to REST for everything; agent ignores Kafka/queues unless prompted.
- Distributed-tracing context propagation rarely emitted unless explicitly required.
- API versioning strategies skipped or inconsistent across services in the same PR.
- Backfill / data migration plans missing when extracting from monolith.

## Agentic workflow
Use a domain-analyst to identify bounded contexts and aggregates from the brief; then a service-decomposer to propose service boundaries with capability mapping; then per-service template-coder subagents to scaffold each repo from a shared template. Run a contract-reviewer pass to ensure no service shares a database, every cross-service call has a timeout/retry/circuit-breaker, and each service has health/readiness probes plus an OpenAPI spec. Decomposition should be Opus; scaffolding can be Haiku/Sonnet.

### Recommended subagents
- `domain-analyst` (Opus) — DDD-style bounded-context discovery from requirements.
- `service-decomposer` (Opus) — capability mapping, ownership, dependency graph.
- `service-scaffold` (Haiku) — generates service repo from approved template.
- `api-contract-reviewer` (Sonnet) — OpenAPI/proto review, versioning, idempotency, error model.
- `migration-planner` (Sonnet) — Strangler Fig steps, dual-write phases, cutover plan.

### Prompt pattern
```
You are domain-analyst. Source: <PRD or monolith summary>. Output:
1) bounded contexts with ubiquitous-language glossary,
2) aggregates per context (root + invariants),
3) integration events between contexts,
4) shared kernel vs anti-corruption-layer recommendations.
No service names yet.
```

```
You are service-decomposer. Inputs: bounded contexts, team count=4, traffic
profile=<...>. Output: services table {name, capability, owner-team,
sync-deps, async-deps, data-store}; reject any service with <2 endpoints
or shared DB with another service.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `kubectl` | Deploy/inspect services on K8s | kubernetes.io/docs/tasks/tools/ |
| `helm` | Package per-service charts | helm.sh |
| `kustomize` | Per-env overlays | kustomize.io |
| `skaffold` / `tilt` | Multi-service local dev loops | skaffold.dev / tilt.dev |
| `docker compose` | Local multi-service runtime | docs.docker.com/compose/ |
| `openapi-generator` | Generate clients/servers from spec | openapi-generator.tech |
| `buf` | Protobuf lint, breaking-change detection | buf.build |
| `grpcurl` / `httpie` / `curl` | Probe services | github.com/fullstorydev/grpcurl |
| `jaeger` / `tempo` UIs | Distributed traces | jaegertracing.io |
| `argocd` / `flux` | GitOps deploy each service | argoproj.github.io / fluxcd.io |
| `kiali` | Service-mesh topology (Istio) | kiali.io |
| `dapr` CLI | Sidecar runtime for service-to-service | dapr.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kubernetes (EKS/AKS/GKE) | SaaS + OSS | Yes | YAML manifests are easy for agents. |
| Istio / Linkerd / Cilium | OSS | Yes | Service mesh for mTLS, traffic, retries. |
| Kafka / NATS / RabbitMQ | OSS + SaaS | Yes | Async backbone; agent wires producers/consumers. |
| Kong / Envoy / NGINX / API Gateway | OSS + SaaS | Yes | North-south traffic. |
| Apollo Federation / GraphQL Mesh | OSS + SaaS | Partial | BFF aggregation; complex schema stitching needs human review. |
| Backstage | OSS | Yes | Service catalog scaffolding via templates. |
| Dapr | OSS | Yes | Building-block APIs (state, pubsub, secrets) — abstracts brokers. |
| Spring Cloud / Micronaut / Quarkus | OSS | Yes | Java microservice frameworks. |
| FastAPI / NestJS / Go-kit / Echo | OSS | Yes | Polyglot service options. |
| Temporal | OSS + SaaS | Yes | Cross-service workflows replace ad-hoc orchestration. |

## Templates & scripts
See `templates.md` for service skeleton + docker-compose stack. Inline contract-quality gate to run on every microservices PR:

```bash
#!/usr/bin/env bash
# microservices-pr-gate.sh
set -euo pipefail
buf lint
buf breaking --against '.git#branch=main'
for f in services/*/openapi.yaml; do
  npx @redocly/cli@latest lint "$f"
done
# Disallow shared DB
grep -RIn 'jdbc:.*://shared-db' services/ && {
  echo "ERROR: shared DB usage detected"; exit 1; } || true
# Require timeouts on outbound clients
grep -RILn --include='*.go' --include='*.java' --include='*.ts' \
    -E 'NewHttpClient|HttpClient.newBuilder|new HttpClient\(\)' services/ |
  while read -r f; do
    grep -qE 'Timeout|setConnectTimeout|requestTimeout' "$f" || {
      echo "ERROR: client without timeout in $f"; exit 1; }
  done
# Require liveness + readiness probes
for d in services/*/k8s; do
  grep -q livenessProbe "$d"/*.yaml || { echo "no liveness in $d"; exit 1; }
  grep -q readinessProbe "$d"/*.yaml || { echo "no readiness in $d"; exit 1; }
done
echo "PR gate OK"
```

## Best practices
- Define minimum service size (e.g., ≥3 endpoints, ≥1 owner team) in the prompt to prevent nano-service drift.
- Force the agent to draw a dependency graph and reject cycles before merging the design.
- Each service: own DB, own pipeline, own on-call; if any of those is shared, it's a module, not a service.
- Versioning: agent must emit `/v1` paths or proto packages; deprecation policy in writing.
- Cross-service calls always need timeout + retry budget + circuit breaker; if missing, reject the PR.
- Distributed tracing (W3C `traceparent`) propagated end-to-end; agent should add middleware in scaffolding.
- Use Strangler Fig for monolith extraction — never big-bang; agent generates parallel-write phase explicitly.
- Document each service's SLO and error budget in its repo README before code lands.

## AI-agent gotchas
- Agents reuse the monolith's database schema across new services — manual review must catch shared FKs.
- "Aggregator" services proposed by the agent are usually a sign of wrong boundaries — push back.
- Generated REST clients lack timeouts; gRPC clients lack deadlines — both default to infinite.
- Async event schemas drift across services because the agent doesn't propose a schema registry; require Confluent SR / Apicurio.
- Human checkpoint REQUIRED before: extracting the first service from monolith, retiring monolith endpoints, changing event schemas, introducing a new database technology.
- Agents add gateways without rate limits or auth — the gate becomes the SPOF.
- LLM tends to skip readiness probes when only liveness is requested; both are needed.
- BFF endpoints generated by agent often N+1 — require explicit aggregation/dataloader.

## References
- Sam Newman, "Building Microservices" (2nd ed.).
- Chris Richardson, "Microservices Patterns".
- Eric Evans, "Domain-Driven Design"; Vaughn Vernon, "Implementing DDD".
- microservices.io pattern catalog.
- Martin Fowler: https://martinfowler.com/microservices/.
- 12-Factor App: https://12factor.net/.
- Team Topologies, Skelton & Pais.
