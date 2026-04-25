# Agent Integration — API Gateway Patterns

## When to use
- Multi-service backends (microservices, modular monoliths) needing one ingress for routing, TLS, auth, rate limiting, request transformation, and observability.
- Public APIs that front several internal services and need a stable public URL grammar regardless of internal evolution.
- Mobile + Web + Partner clients with different needs — Backend-for-Frontend (BFF) pattern lives at the gateway tier.
- Migrations from monolith to services — gateway routes legacy paths to legacy app, new paths to new services, providing a strangler-fig.
- Enforcing org-wide policies (mTLS, JWT validation, header injection, audit logging) without forcing every service to reimplement.

## When NOT to use
- Single-service apps where Nginx + app middleware suffice; a full gateway is operational overhead.
- Latency-critical hot paths (real-time bidding, HFT) where every hop matters; for those, sidecar / mesh-only auth and direct service-to-service is faster.
- Greenfield prototypes — start with a reverse proxy, add gateway when the second service ships.
- Pure static asset delivery (CDN handles routing, caching, TLS).
- Cases where service-mesh (Istio, Linkerd) already provides the L7 policy you need.

## Where it fails / limitations
- **Single point of failure.** Gateway down = whole API down. Mitigation: multi-AZ, autoscaling, blue/green deploys, smoke probes.
- **Performance bottleneck.** All traffic funnels through gateway; CPU-heavy plugins (jwt verify, transform, lua) can crater p99. Mitigation: profile per plugin; offload heavy work to app or sidecar.
- **Plugin sprawl.** Easy to enable too much (cors, jwt, oauth, rate-limit, transform, request-id, prometheus). Surface area for bugs grows; ordering matters. Audit plugin chain.
- **Stateful gateway anti-pattern.** Sticky sessions tie clients to nodes, complicates scaling. Keep gateway stateless; push session to backend / Redis.
- **Misaligned timeouts.** Gateway timeout < service timeout = mid-flight disconnects; gateway > service = orphan workloads. Tune per route.
- **Auth duplication.** Both gateway and service validate JWT; CPU waste, divergent logic. Pick one (gateway for coarse, service for fine-grained).
- **Hidden routing logic.** Path rewrites and header transforms invisible to service teams; debugging requires gateway access. Document every route in code/repo.
- **Config drift.** Manual UI edits in Kong / AWS console vs declarative YAML diverge. Always GitOps the gateway config.
- **Cost surprise.** AWS API Gateway charges per request; high-traffic APIs cost more there than self-hosted Kong on Fargate. Model costs before commit.
- **TLS termination only at edge.** Internal traffic plaintext; insiders can sniff. Terminate at gateway and re-encrypt to backends (mTLS / TLS) for sensitive data.

## Agentic workflow
Drive gateway work in five stages: (1) a **route-author** subagent encodes routes/services in a single declarative config (`kong.yml`, `serverless.yml`, Nginx + Jinja, or Envoy YAML) versioned in repo; (2) a **plugin-curator** subagent attaches policies (auth, rate-limit, CORS, request-id, transform) per route group from a documented catalog — no ad-hoc additions; (3) a **policy-tester** subagent runs integration tests via `httpx` / `pytest` hitting a containerized gateway with mocked upstreams, asserting headers / status / body; (4) a **deploy-orchestrator** subagent applies config via `decK` / Terraform / `aws cloudformation deploy`; (5) `faion-sdd-executor-agent` runs the standard quality gate. Always shadow-mirror traffic to staging gateways before production rollouts of new plugins.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs lint, container build, integration tests against ephemeral gateway.
- A purpose-built **kong-config-author** — emits `kong.yml` services + routes + plugins, refusing inline credentials.
- An **envoy-config-author** — emits Envoy YAML clusters + listeners + filter chains.
- A **bff-composer** — implements API composition handlers that fan out via `httpx.AsyncClient` to N upstreams with `asyncio.gather`, including circuit-breaker via `pybreaker` / `tenacity`.
- A **plugin-policy-linter** — checks every public route has auth + rate-limit + cors plugins; warns on routes missing observability plugins.
- A **route-table-renderer** — produces a markdown table of all routes for SRE review.
- A **deploy-bot** — runs `decK sync` (Kong) or `serverless deploy` (AWS) only after policy-linter passes.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scans gateway YAML for hard-coded secrets.

### Prompt pattern
Route addition:
```
Add a new route group /api/v1/invoices to kong.yml, fronted by
the invoices-service (URL invoices-svc.internal:8080).
Plugins on the group:
- jwt (claims_to_verify: [exp, iss], iss = "https://auth.example.com/")
- rate-limiting (Redis-backed, 1000/h per consumer; burst 50)
- cors (origins: https://app.example.com)
- request-transformer (add X-Request-ID:$(uuid), X-Service:invoices)
- prometheus (status_code_metrics: true)
Strip path prefix /api/v1.
Output a unified diff against ops/kong.yml only.
Reject inline secrets; reference Kong vault paths instead.
```

BFF composition:
```
Generate /api/dashboard handler aggregating user-svc, order-svc,
notification-svc with httpx.AsyncClient + asyncio.gather.
Add timeouts (1.5s per call) and pybreaker circuit breakers.
On partial failure, return 200 with degraded sections marked
{"error":"partial","detail":"..."}; never block on slow upstream.
Add OpenTelemetry span around each call. Cover with pytest using
respx fixtures simulating slow + failed upstreams.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `kong` | OSS API gateway | https://docs.konghq.com/gateway/ |
| `decK` | Declarative config sync for Kong | https://docs.konghq.com/deck/ |
| `envoy` | High-perf L7 proxy / gateway | https://www.envoyproxy.io |
| `nginx` | Battle-tested reverse proxy | https://nginx.org/en/docs/ |
| `traefik` | Cloud-native gateway with auto-discovery | https://doc.traefik.io/traefik/ |
| `serverless` | AWS API Gateway via IaC | https://www.serverless.com |
| `aws-cdk` / `terraform` | AWS API Gateway IaC | https://aws.amazon.com/cdk/ |
| `apisix` | OSS gateway with Lua / Wasm plugins | https://apisix.apache.org |
| `tyk` | OSS / SaaS gateway | https://tyk.io |
| `caddy` | TLS-first reverse proxy | https://caddyserver.com |
| `hey` / `k6` | Load test gateway | https://github.com/rakyll/hey |
| `pybreaker` / `tenacity` | Circuit breaker / retry libraries (Python) | https://github.com/danielfm/pybreaker |
| `httpx` | Async HTTP for BFF composition (Python) | https://www.python-httpx.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kong Gateway | OSS / SaaS (Konnect) | yes | Plugin ecosystem; `kong.yml` declarative; `decK` for GitOps. |
| AWS API Gateway | SaaS | yes | REST + HTTP + WebSocket APIs; Lambda / VPC integration; Cognito auth. |
| Cloudflare API Gateway / Workers | SaaS | yes | Edge gateway; routes + WAF + rate limit. |
| Google Cloud API Gateway / Apigee | SaaS | yes | Apigee for enterprise; OpenAPI-driven. |
| Azure API Management | SaaS | yes | OpenAPI ingest + policy XML. |
| Tyk | OSS / SaaS | yes | API management + portal. |
| Gravitee | OSS / SaaS | partial | API management + design studio. |
| Envoy + Istio | OSS | yes | Mesh-based ingress + east-west policy. |
| WSO2 API Manager | OSS | partial | Enterprise full-stack APIM. |
| Mulesoft Anypoint | SaaS | partial | Enterprise integration; heavy. |

## Templates & scripts
See `templates.md` for `kong.yml` and Nginx site templates. Use this script to lint Kong declarative config for missing org policies:

```bash
#!/usr/bin/env bash
# kong-policy-guard.sh — every public route must carry auth + rate-limit.
set -euo pipefail
CFG="${1:-ops/kong.yml}"
python - "$CFG" <<'PY'
import sys, yaml
cfg = yaml.safe_load(open(sys.argv[1]))
public_tag = "public"
fails = []
for svc in cfg.get("services", []):
    for route in svc.get("routes", []):
        tags = set(route.get("tags") or []) | set(svc.get("tags") or [])
        if public_tag not in tags:
            continue
        plugins = {p.get("name") for p in (svc.get("plugins") or []) + (route.get("plugins") or [])}
        for required in ("jwt", "rate-limiting", "cors"):
            if required not in plugins:
                fails.append(f"{svc.get('name')}/{route.get('name')}: missing plugin {required}")
if fails:
    print("\n".join(fails)); sys.exit(1)
print("OK")
PY
```

## Best practices
- **Declarative config in repo.** GitOps (`decK sync`, `terraform apply`, `serverless deploy`); no UI-driven edits.
- **Stateless gateway.** No sticky sessions; push state to backend / Redis.
- **Single source of auth.** Gateway validates token signatures + expiry; services do fine-grained authorization.
- **Per-route plugin policy.** Public routes carry auth + rate-limit + CORS + request-id + observability; internal routes need only request-id + observability.
- **Timeouts tuned per route.** Gateway timeout > expected service p99 + jitter; never infinite.
- **Circuit breakers in BFF/composition handlers.** `pybreaker` / `tenacity` with budgets; never block on slow upstream.
- **TLS edge-to-origin.** Terminate at gateway, re-encrypt to backends for sensitive routes; mTLS for service-to-service.
- **Observability everywhere.** OpenTelemetry traces from gateway through services; gateway emits Prometheus + access logs with `traceparent`.
- **Headers normalized.** Gateway injects `X-Request-ID`, propagates `traceparent`, strips inbound `Authorization` after validation if needed downstream.
- **Idempotency at gateway** for POST routes that mutate (`Idempotency-Key` header pass-through).
- **Canary / blue-green** for gateway config; route % of traffic, monitor, promote.
- **Document every route** in a generated table; SRE / on-call refer to it during incidents.
- **Cost monitoring.** AWS API Gateway billed per request + data; alarm on spend deltas.

## AI-agent gotchas
- **Hard-coded secrets in YAML.** Agent inlines API keys / JWT secrets; commits to git. Use Kong vault refs, AWS Secrets Manager refs, or env vars.
- **Plugin order ignored.** `request-transformer` after `rate-limiting` reads transformed headers — sequencing matters; agents emit defaults blindly.
- **Stripping `/v1` then service expects `/v1`.** Path rewrite mismatch causes 404. Test with integration suite.
- **CORS preflight overlooked.** Browser fails OPTIONS; agent debugs handler. Configure `cors` plugin for OPTIONS first.
- **Rate-limiting in-memory** in multi-replica deploys → counters local, total = N×limit. Always Redis policy.
- **Auth on internal routes.** Agent applies JWT to `/internal/...`; service-to-service calls fail. Tag and exclude.
- **Missing timeouts** lead to hung connections and gateway resource exhaustion. Lint for `timeout`/`connect_timeout`/`read_timeout`.
- **BFF composition without `asyncio.gather`** runs serial → 6× latency. Reject in code review.
- **No circuit breaker.** Slow upstream cascades; gateway thread starvation. Always wrap.
- **Logging full request body** at gateway — leaks PII / tokens. Allowlist log fields.
- **Custom Lua / Wasm plugin without sandbox limits.** Memory / CPU runaway. Set quotas.
- **AWS API Gateway request size limit** (10MB) bites file uploads; agents discover at integration. Document and route uploads via presigned S3.
- **WebSocket route on REST API Gateway type.** Wrong product; agents confuse `HTTP API` vs `WebSocket API`. Pick correct.
- **Forgetting to propagate `traceparent`.** Distributed traces stop at gateway. Add request-transformer plugin.
- **Plugin chain ordering across services.** Two services apply same plugin in conflicting order. Standardize via shared modules / overlay.

## References
- Kong Gateway docs: https://docs.konghq.com/gateway/latest/
- decK (Kong GitOps): https://docs.konghq.com/deck/
- AWS API Gateway: https://docs.aws.amazon.com/apigateway/
- Envoy filter docs: https://www.envoyproxy.io/docs/envoy/latest/configuration/http_filters/http_filters
- Nginx reverse proxy: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- Apache APISIX: https://apisix.apache.org/docs/
- API Gateway pattern: https://microservices.io/patterns/apigateway.html
- BFF pattern: https://samnewman.io/patterns/architectural/bff/
- OpenTelemetry: https://opentelemetry.io/docs/
- Sibling methodologies: `solo/dev/api-developer/api-rest-design/`, `solo/dev/api-developer/api-rate-limiting/`, `solo/dev/api-developer/api-authentication/`, `solo/dev/api-developer/api-error-handling/`.
