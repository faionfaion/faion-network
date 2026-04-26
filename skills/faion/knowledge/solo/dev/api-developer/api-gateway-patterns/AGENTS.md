# API Gateway Patterns

## Summary

An API gateway is a single ingress that handles routing, TLS termination, authentication, rate limiting, CORS, request transformation, and observability for multiple backend services. Keep gateway config declarative and version-controlled (GitOps). Never store secrets inline; keep the gateway stateless; tune timeouts per route.

## Why

Centralizing cross-cutting concerns at the gateway removes the need for every service to reimplement JWT validation, rate limits, and CORS headers. GitOps of gateway config (`decK sync`, `terraform apply`) prevents config drift that causes silent production incidents. Stateless gateways scale horizontally; stateful ones create sticky-session failures.

## When To Use

- Multi-service backends needing one stable public URL regardless of internal topology
- Mobile + Web + Partner clients with different payload shapes (BFF pattern)
- Enforcing org-wide policies (mTLS, JWT, audit logging) without per-service duplication
- Strangler-fig migrations routing legacy paths to old service, new paths to new service

## When NOT To Use

- Single-service apps where Nginx + app middleware suffice — full gateway is operational overhead
- Latency-critical hot paths (real-time bidding, HFT) — prefer sidecar/mesh direct path
- Greenfield prototypes — start with a reverse proxy, add gateway when second service ships
- Pure static asset delivery (CDN handles routing, caching, TLS)

## Content

| File | What's inside |
|------|---------------|
| `content/01-gateway-functions.xml` | Core functions table, Kong/Nginx/AWS config examples, BFF composition pattern |
| `content/02-checklist.xml` | Gateway authoring rules: declarative config, stateless, timeouts, auth placement, observability |

## Templates

| File | Purpose |
|------|---------|
| `templates/kong.yml` | Kong declarative config: services, routes, JWT + rate-limit + CORS plugins, request-id injection |
| `templates/nginx-gateway.conf` | Nginx reverse proxy with upstream weighting, rate limiting, CORS, health check |
| `templates/kong-policy-guard.sh` | CI script: fails if any public route is missing auth + rate-limit + CORS plugins |

## Scripts

none
