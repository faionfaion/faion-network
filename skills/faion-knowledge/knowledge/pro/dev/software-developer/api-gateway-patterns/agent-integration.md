# Agent Integration — API Gateway Patterns

## When to use
- Multi-service backend that needs centralized auth (JWT, OAuth, mTLS), rate limiting, request tracing, and CORS — instead of duplicating per-service.
- Migrating a monolith to microservices: fronting old + new behind one gateway, then peeling off routes.
- Public APIs that need plan-based quotas (free / pro) — Kong, AWS API Gateway, Apigee handle usage plans natively.
- BFF (Backend-for-Frontend) per channel (web, mobile, partner) where each channel has different auth/aggregation needs.

## When NOT to use
- Single-service apps — adding a gateway is one more thing to operate.
- Strict low-latency hot paths (sub-1ms) — every gateway hop adds 1–5ms; consider sidecar service mesh (Linkerd, Istio) instead.
- Internal-only east-west traffic — service mesh fits better than a gateway for service-to-service.
- When you can't afford the operational complexity of Kong/Envoy plus its config plane.

## Where it fails / limitations
- **Smart gateway anti-pattern:** business logic in gateway plugins (Lua, JS, WASM) becomes a new monolith only the platform team can change. Keep gateways "boring" — auth, rate-limit, route, log.
- AWS API Gateway has hard limits: 30s integration timeout, 10MB payload, 30 routes/IP per second burst.
- Kong DB-mode vs DB-less: switching mid-flight loses state; pick one and stick.
- Nginx-as-gateway lacks dynamic config without `nginx-plus` or OpenResty/lua-resty hooks.
- API composition / aggregation in the gateway hides downstream failures — partial responses make debugging hard.
- Rate limit by `$binary_remote_addr` is wrong behind a load balancer — use `X-Forwarded-For` with `set_real_ip_from`.

## Agentic workflow
A gateway is config-as-code. Subagents should generate `kong.yml` / `serverless.yml` / `nginx.conf` snippets paired with a smoke-test (curl scripts or Pact contract tests) that proves the route, auth, and rate-limit behave. For multi-environment, drive via Terraform (AWS API Gateway, Kong, GCP API Gateway) so changes are PR-reviewable. Always include a "blue/green route" template so agents can canary new backends.

### Recommended subagents
- `faion-sdd-executor-agent` — drives gateway-config + smoke-test cycle.
- A `gateway-route` subagent (project-local) — adds a route + auth + rate-limit + healthcheck + Terraform/declarative config in one diff.

### Prompt pattern
```
Add /api/v2/orders → order-service-v2:8080 to kong.yml.
- Plugin: jwt (claim exp), rate-limiting (60/min/consumer), correlation-id
- Strip path: false. Preserve host header.
- Add a healthcheck route /health/v2 returning 200 from the service
- Smoke test: scripts/gateway/smoke-orders.sh that calls /api/v2/orders
  with valid+invalid token and asserts 200/401
Do NOT add request-transformer or response logic. Keep gateway boring.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `deck` (decK) | Sync Kong declarative config | https://docs.konghq.com/deck/ |
| `kong config db_import` | Import declarative kong.yml | https://docs.konghq.com/gateway/latest/reference/cli/ |
| `aws apigatewayv2` / `aws apigateway` | Manage AWS API Gateway from CLI | https://docs.aws.amazon.com/cli/latest/reference/apigateway/ |
| `serverless` | Deploy AWS API Gateway + Lambda from `serverless.yml` | https://www.serverless.com |
| `terraform` | Provision Kong/AWS/GCP gateways idempotently | https://registry.terraform.io |
| `nginx -t` | Validate config before reload | core |
| `hey` / `vegeta` | Load test rate limits | https://github.com/rakyll/hey |
| `httpie` / `curl` | Smoke test routes | https://httpie.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Kong Gateway | OSS + SaaS (Konnect) | Yes | Declarative config, plugin ecosystem; `deck sync` for diffs |
| AWS API Gateway | SaaS | Yes | Drive via Terraform or `serverless`; raw `aws` CLI is awkward |
| Cloudflare API Shield / Workers | SaaS | Yes | Edge gateway with WAF; agents can deploy via Wrangler |
| Apigee | SaaS | Partial | Heavy XML policy files — agents struggle without examples |
| Tyk | OSS + SaaS | Yes | API definitions are JSON, easy for LLM editing |
| Envoy / Istio Ingress | OSS | Yes | YAML config; pair with Helm/Kustomize for agent edits |
| Traefik | OSS | Yes | Auto-discover from k8s annotations or labels — minimal config |
| KrakenD | OSS | Yes | Declarative aggregation gateway; great for BFF |

## Templates & scripts
See `templates.md` for Kong/AWS/Nginx skeletons. BFF aggregation pattern (FastAPI):

```python
# bff/dashboard.py
from fastapi import FastAPI, Header, HTTPException
import httpx, asyncio

app = FastAPI()

@app.get("/api/dashboard")
async def dashboard(authorization: str = Header(...)):
    headers = {"Authorization": authorization, "X-Request-ID": "..."}
    async with httpx.AsyncClient(timeout=2.0) as c:
        try:
            user, orders, notifs = await asyncio.gather(
                c.get("http://user-svc/me", headers=headers),
                c.get("http://order-svc/me/orders?limit=5", headers=headers),
                c.get("http://notify-svc/me/unread", headers=headers),
            )
        except httpx.TimeoutException:
            raise HTTPException(504, "upstream timeout")
    return {
        "user": user.json() if user.is_success else None,
        "orders": orders.json() if orders.is_success else [],
        "notifications": notifs.json() if notifs.is_success else [],
    }
```

## Best practices
- Keep gateway stateless — auth state lives in tokens, rate-limit state in Redis.
- Implement circuit breakers per upstream (Kong's `proxy-cache` + `request-termination`, Envoy's `outlier_detection`) — never let one slow service take the gateway down.
- Cache idempotent GETs at the gateway with short TTL (10–60s) — kills 80% of dashboard traffic.
- Version the gateway config in git; deploy via CI, never via web UI.
- Add a `X-Request-ID` header at ingress (`$request_id` in nginx, `correlation-id` plugin in Kong) and propagate to all upstreams for tracing.
- Set timeouts shorter than client timeouts (gateway 5s, client 10s) so the gateway returns 504 cleanly.
- Use mTLS for internal service-to-service even behind the gateway — defense in depth.
- For AWS API Gateway, prefer HTTP API (v2) over REST API (v1) unless you specifically need WAF/usage plans — 70% cheaper, lower latency.

## AI-agent gotchas
- Agents put business logic in Kong plugins (Lua) — push back hard. Reserve plugins for cross-cutting concerns.
- They generate gateway YAML without smoke tests, so a typo'd path silently 404s in prod.
- LLMs forget to enable `preserve_host` on Kong, breaking apps that rely on the original `Host` header for tenant routing.
- They configure rate-limiting per-IP behind a CDN, where every request comes from the CDN's IPs — must use `consumer` or `x-forwarded-for`.
- AWS API Gateway: agents miss the difference between `proxy+` (passthrough) and per-method routing; usage plans need API keys + stages, which is easy to misconfigure.
- Human-in-loop checkpoint: every gateway change should require a load test against staging — agents can't tell if you just halved your throughput.
- Verify cost impact for SaaS gateways (AWS APIGW = $1/M requests; Kong Konnect per service hour) — agents won't.

## References
- "Microservices Patterns" — Chris Richardson, ch. 8 (API Gateway)
- microservices.io — API Gateway pattern: https://microservices.io/patterns/apigateway.html
- Kong docs: https://docs.konghq.com/gateway/latest/
- AWS API Gateway dev guide: https://docs.aws.amazon.com/apigateway/latest/developerguide/
- Sam Newman — "Building Microservices, 2nd ed.": ch. 5
- Phil Calçado — "Pattern: BFFs": https://philcalcado.com/2015/09/18/the_back_end_for_front_end_pattern_bff.html
