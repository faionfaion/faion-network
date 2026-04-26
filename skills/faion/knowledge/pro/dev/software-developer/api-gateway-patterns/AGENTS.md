# API Gateway Patterns

## Summary

Centralized API gateway for microservices: routing, JWT/mTLS auth, rate limiting per consumer, CORS, request tracing via `X-Request-ID`, circuit breakers, and edge caching. Covers Kong (declarative `kong.yml`), AWS API Gateway (Serverless/Terraform), Nginx, and BFF (Backend-for-Frontend) aggregation. Gateway must stay stateless and "boring" — no business logic in plugins.

## Why

Duplicating auth, rate-limiting, and tracing in every microservice is an operations burden and a security inconsistency risk. A gateway centralizes cross-cutting concerns as config-as-code, enables canary routing without service changes, and enforces quotas for public APIs. The "smart gateway" antipattern (business logic in Lua/JS plugins) creates a new monolith owned by the platform team — this methodology enforces the boundary.

## When To Use

- Multi-service backend needing centralized auth, rate limiting, request tracing, CORS
- Migrating monolith to microservices: front old + new behind one gateway, then peel off routes
- Public APIs with plan-based quotas (free/pro) — Kong, AWS APIGW, Apigee handle usage plans natively
- BFF per channel (web, mobile, partner) with different auth/aggregation needs

## When NOT To Use

- Single-service apps — a gateway is one more thing to operate
- Sub-1ms latency hot paths — each gateway hop adds 1–5ms; use a sidecar service mesh instead
- Internal east-west service-to-service traffic — service mesh (Linkerd, Istio) fits better
- Teams that cannot afford Kong/Envoy + config plane operational complexity

## Content

| File | What's inside |
|------|---------------|
| `content/01-gateway-rules.xml` | Core rules: stateless gateway, rate limit by consumer not IP, timeouts, circuit breakers, X-Request-ID |
| `content/02-examples.xml` | Kong YAML, AWS API Gateway serverless.yml, Nginx config, BFF aggregation examples and antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/kong-route.yml` | Kong declarative route with JWT + rate-limiting + correlation-id plugins |
| `templates/nginx-gateway.conf` | Nginx reverse proxy with upstream, rate limit zone, CORS, health check |
| `templates/bff-aggregator.py` | FastAPI BFF aggregating 3 upstream services with httpx + asyncio.gather + timeout handling |
| `templates/prompt-gateway-route.txt` | Subagent prompt for adding a route + auth + rate-limit + smoke test |
