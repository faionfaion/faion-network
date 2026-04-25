# Agent Integration — API Gateway Design

## When to use
- Designing the front door for a new microservices/serverless system: routing, auth, rate-limit, circuit-breakers, observability in one place.
- Generating Kong, AWS API Gateway, Traefik, Envoy, APISIX, or Apollo Router config from an OpenAPI/AsyncAPI spec.
- Refactoring a "fat" gateway that's accumulated business logic — agent identifies what to push down to services.
- Adding GraphQL Federation (Apollo Router supergraph) over REST/GraphQL subgraphs.
- Codifying multi-level rate limits (global / per-API / per-consumer / per-route) and adaptive throttling rules.

## When NOT to use
- Single monolith with one host — a reverse proxy (nginx, Caddy) is enough; gateway adds latency and ops cost.
- Internal east-west traffic between services on a service mesh — that's mesh territory (Istio/Linkerd), not edge gateway.
- Simple Lambda + Function URL deployments where API Gateway adds no value over direct invocation.
- Real-time bidirectional streams that need persistent connections at scale — use AppSync, dedicated WS gateway, or NATS/Centrifugo.

## Where it fails / limitations
- Agents will happily put business logic in gateway plugins (Lua, Wasm) — debt accumulates silently and the gateway becomes a deploy bottleneck.
- Generated rate-limit configs often pick arbitrary numbers (1000 RPS) without tying to backend capacity or SLO; meaningless until validated under load.
- LLMs frequently mix Kong DB-mode and DB-less syntax, AWS REST API and HTTP API features, or Envoy v2 and v3 xDS.
- mTLS, JWT validation, and OAuth introspection configs need cert chains and JWKS URLs that agents hallucinate; verify with `curl` / `openssl`.
- GraphQL Federation: Apollo v1 vs v2 directives (`@key`, `@shareable`, `@external`) regularly mixed up; agent-generated supergraphs fail composition checks.
- Circuit breaker thresholds need real failure-rate data; agent defaults (5 failures / 30s) are fine for hello-world but wrong for high-traffic.

## Agentic workflow
Drive design with sonnet (pick gateway product + patterns), generate config with haiku from `templates.md`, then opus reviews for security and anti-patterns. Always pair the gateway agent with the security and observability methodology folders in context — auth and tracing are inseparable from gateway design. Output: gateway config (Kong YAML / CFN / xDS), OpenAPI doc, OTEL pipeline, and load-test script. Reject diffs without all four.

### Recommended subagents
- `faion-sdd-executor-agent` — owns gateway feature in SDD, reads `templates.md` for the chosen product, gates on quality checks.
- `password-scrubber-agent` — runs against generated configs; gateway YAML is a dense secret-leak surface (API keys, JWT secrets, mTLS keys, upstream credentials).
- `nero-sdd-executor-agent` — for NERO-internal gateways (e.g., n8n / mediamanager BE) with NERO conventions.

### Prompt pattern
```
Generate Kong DB-less config for these routes from the attached OpenAPI:
- Auth: JWT (RS256, JWKS at https://auth.example.com/.well-known/jwks.json)
- Rate-limit: 100 r/s per consumer, 1000 r/s global, redis backend
- Observability: OTEL exporter to localhost:4317
- CORS: only allow https://app.example.com
Emit declarative YAML, no Lua plugins, no inline secrets. Add comments where I must
fill in values from a secret store.
```

```
Audit this Envoy config for anti-patterns: business logic in filters, missing
circuit-breakers, single point of failure, sync transformations, missing rate-limit
on /admin. List specific line numbers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `deck` | Kong declarative config sync | `brew install kong/deck/deck` |
| `kongctl` | Kong Konnect cloud control | https://docs.konghq.com/konnect/ |
| `aws apigatewayv2` | AWS HTTP/WS API CLI ops | bundled in awscli |
| `traefik` | Embeds CLI for config validation | `brew install traefik` |
| `envoy --validate-yaml` | Static config validation | https://www.envoyproxy.io/docs/envoy/latest/ |
| `apisix-cli` | APISIX config and plugin management | https://apisix.apache.org/docs/apisix/installation-guide/ |
| `rover` | Apollo Federation supergraph composition + checks | `npm i -g @apollo/rover` |
| `openapi-cli` (Redocly) | Lint OpenAPI specs that drive gateway routes | `npm i -g @redocly/cli` |
| `spectral` | OpenAPI/AsyncAPI rule-based linting | `npm i -g @stoplight/spectral-cli` |
| `k6` / `wrk` / `hey` | Load test gateway under realistic traffic | https://k6.io/ |
| `oha` | Quick HTTP load test, terminal UI | `cargo install oha` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kong (OSS / Konnect) | OSS + SaaS | Yes | `deck` makes config diff/sync trivial; rich plugin docs LLMs handle well. |
| AWS API Gateway | SaaS | Yes | CFN/SAM/CDK; agent must distinguish REST vs HTTP API features. |
| Traefik | OSS | Yes | File / Kubernetes CRD config; GitOps-friendly. |
| Envoy + xDS | OSS | Partial | Powerful but verbose; LLMs slip between v2/v3 schemas. |
| APISIX | OSS | Yes | Etcd-backed; admin API is REST and scriptable. |
| Apigee X | SaaS | Limited | UI-driven; agent can drive via apigeecli but iteration is slow. |
| Tyk | OSS + SaaS | Yes | Dashboard + API; OpenAPI native import. |
| Apollo Router | SaaS + OSS | Yes | Rust-based router with `rover` for supergraph composition. |
| Cloudflare API Shield | SaaS | Partial | Schema/rate management; mostly UI, some Terraform support. |
| AWS WAF | SaaS | Yes | Pair with API Gateway/CloudFront; managed rule groups via CDK. |

## Templates & scripts
See `templates.md` for Kong, AWS APIGW, Traefik, Envoy, Apollo Router boilerplate. Inline route-emitter from OpenAPI for Kong DB-less:

```python
#!/usr/bin/env python3
# openapi_to_kong.py — emit Kong services/routes from OpenAPI paths.
import sys, yaml, json
spec = yaml.safe_load(open(sys.argv[1]))
upstream = sys.argv[2]
out = {"_format_version": "3.0", "services": [{
    "name": "api", "url": upstream, "routes": []
}]}
for path, ops in spec["paths"].items():
    for method in ops:
        if method.lower() not in {"get","post","put","patch","delete"}: continue
        out["services"][0]["routes"].append({
            "name": f"{method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}",
            "methods": [method.upper()],
            "paths": [path.replace("{", ":").replace("}", "")],
            "strip_path": False,
        })
print(yaml.safe_dump(out, sort_keys=False))
```

## Best practices
- Treat gateway as plumbing; routing, auth, rate-limit, observability only. No domain logic, no orchestration loops.
- Drive config from OpenAPI/AsyncAPI specs; agent generates gateway config from spec, never the other way around.
- Multi-level rate limits: enforce per-consumer first (cheap), per-route second, global as a hard ceiling.
- Always terminate TLS at the gateway and re-encrypt to upstream when crossing trust boundaries; never run plaintext past the edge.
- Strip internal headers (`X-Internal-*`, JWTs after validation) before forwarding; agents forget this and leak tokens to upstreams.
- Pin gateway version and store config as code (deck, CDK, Helm); GitOps lets the agent open PRs for diff review.
- Bench every config change with `k6` against last-known-good before merging — gateway misconfig is a P0 incident.

## AI-agent gotchas
- "Wildcard upstreams" — agents emit `paths: ["/"]` catch-all routes; explicitly require enumerated paths.
- Auth bypass: agents add JWT plugins on services but forget anonymous routes (`/health`, `/metrics`); demand explicit anonymous list.
- Generated CORS configs are usually `Access-Control-Allow-Origin: *` — must be locked to known domains in prod.
- Apollo Federation: never accept a supergraph without running `rover supergraph compose --config` to verify; LLMs miss `@inaccessible` and `@override`.
- Rate limit storage: agents pick "local" mode by default which doesn't share counters across nodes; force `redis` or `cluster` for multi-node.
- Circuit breaker on health-check upstreams: agents wire breakers on `/health` polls, causing self-inflicted outages; exclude health from the circuit.
- Streaming/large-payload routes (uploads, SSE, WS): agents apply default request body buffering; large uploads OOM the gateway. Always set `request_buffering: false` or use direct-to-S3 patterns.
- Human-in-loop checkpoint required before applying any IAM / WAF / mTLS change; one bad regex blocks all traffic.

## References
- Kong Gateway docs — https://docs.konghq.com/gateway/
- AWS API Gateway Developer Guide — https://docs.aws.amazon.com/apigateway/
- Traefik docs — https://doc.traefik.io/traefik/
- Envoy proxy docs — https://www.envoyproxy.io/docs/envoy/latest/
- Apollo Federation v2 — https://www.apollographql.com/docs/federation/
- APISIX docs — https://apisix.apache.org/docs/
- Microservices.io API Gateway pattern — https://microservices.io/patterns/apigateway.html
- OpenTelemetry collector deployment patterns — https://opentelemetry.io/docs/collector/deployment/gateway/
