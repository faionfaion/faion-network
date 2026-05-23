---
slug: lb-health-checks
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates /health + /health/live + /health/ready endpoints (Python/Node/Go) with bounded dependency probes + LB probe config (intervals + thresholds).
content_id: "a775bf79af9726e3"
complexity: medium
produces: code
est_tokens: 4800
tags: [load-balancing, health-checks, kubernetes, haproxy, nginx]
---
# Load Balancer Health Check Implementation

## Summary

**One-sentence:** Generates /health + /health/live + /health/ready endpoints (Python/Node/Go) with bounded dependency probes + LB probe config (intervals + thresholds).

**One-paragraph:** Health checks are the mechanism by which load balancers remove dead backends from rotation. Implement three endpoints: `/health` (basic process alive, used by LB), `/health/live` (Kubernetes liveness — restarts the pod on failure), `/health/ready` (readiness — removes from LB pool without restart, deep dependency probe). Configure check intervals between 10–30 s with tuned healthy / unhealthy thresholds per backend type and ALWAYS bound the readiness probe with a per-dependency timeout (`5 s` is the typical default).

**Ефективно для:**

- New service behind LB: відразу wired liveness + readiness + deep probe.
- Existing service flapping in pool: розділити /live vs /ready, додати threshold tuning.
- Kubernetes: livenessProbe restart pod, readinessProbe usuwa з LB без restart.
- Deep probe з DB/Redis/Queue — return 503 коли downstream падає.
- gRPC service: `grpc.health.v1.Health/Check` за стандартом.

## Applies If (ALL must hold)

- Implementing a new backend service that will sit behind a load balancer.
- Adding Kubernetes liveness and readiness probes to an existing service.
- Debugging flapping services being incorrectly removed from the LB pool.
- Hardening a service so the LB accurately reflects dependency health.

## Skip If (ANY kills it)

- TCP-only services — use `tcp-check` (HAProxy) or `TCPSocket` probe (K8s).
- Stateless functions (FaaS / Lambda) — platform manages health.
- Database load balancing — use protocol-specific health checks (mysql-check, pgsql-check).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service runtime | Python / Node / Go | repo |
| Dependency list | DB / cache / queue / downstream HTTP | architecture |
| LB technology | HAProxy / Nginx / K8s / cloud | infra |
| SLO for failure detection | seconds | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-haproxy-production]] | Backend health-check syntax (`option httpchk` + `expect`). |
| [[lb-kubernetes-ingress]] | Kubernetes liveness / readiness probe semantics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: liveness-ne-readiness, deep-probe-deps, timeout-bound-probe, threshold-tuned, expect-status-match | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-handler` | sonnet | Per-language handler with bounded deps. |
| `wire-probe-config` | sonnet | LB-specific config block. |
| `tune-thresholds` | haiku | Mechanical arithmetic from SLO. |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-handlers.py` | Flask handlers for /health, /health/live, /health/ready with timeouts |
| `templates/probe-config.yaml` | Kubernetes livenessProbe + readinessProbe + startupProbe block |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-health-checks.py` | Validate the health-check artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-haproxy-production]]
- [[lb-nginx-production]]
- [[lb-kubernetes-ingress]]
- [[lb-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (runtime, dependencies, K8s vs raw LB, latency budget) to a concrete probe shape, each leaf referencing a rule from `01-core-rules.xml`.
