---
slug: lb-haproxy-production
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a production HAProxy config with TLS-1.2+/1.3, stick-table rate-limiting, path-based ACL routing, keepalived VIP HA, and tuned maxconn/nbthread.
content_id: "0531eb1b31a6488c"
complexity: deep
produces: config
est_tokens: 5200
tags: [haproxy, load-balancing, tls, high-availability, infrastructure]
---
# HAProxy Production Configuration

## Summary

**One-sentence:** Generates a production HAProxy config with TLS-1.2+/1.3, stick-table rate-limiting, path-based ACL routing, keepalived VIP HA, and tuned maxconn/nbthread.

**One-paragraph:** Production HAProxy setup covers: global performance tuning (`maxconn`, `nbthread`, `cpu-map`), TLS 1.2+/1.3 with strong cipher suites, rate limiting via `stick-table` (e.g., 100 req/10s per IP) without an external state store, path-based ACL routing to separate backends, HTTP health checks with `expect` directives, and active-passive HA using `keepalived` for VIP failover.

**Ефективно для:**

- Bare-metal / VM фронт перед service fleet, де управління повне.
- Rate-limiting без Redis: stick-table в-процесі — досить для 1-2 інстансів.
- Mixed L4 (DB / Redis) + L7 (HTTP) в одному процесі через окремі frontend-блоки.
- Keepalived VIP active-passive HA для on-prem deployments.
- MetalLB + HAProxy ingress pattern для bare-metal Kubernetes.

## Applies If (ALL must hold)

- Standing up HAProxy in front of a service fleet on bare metal, VMs, or as a Kubernetes Ingress controller.
- Implementing rate limiting without an external Redis/Memcached state store.
- Routing TCP (database, Redis) alongside HTTP workloads from a single LB process.
- Setting up active-passive HA with keepalived for a VIP that survives node failure.

## Skip If (ANY kills it)

- Simple web server + LB combo — Nginx handles this with less config overhead.
- Static-content caching — Nginx has a built-in cache; HAProxy does not.
- Managed cloud environments where ALB/NLB is available — see lb-cloud-terraform.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backend list | IP:port table | service inventory |
| TLS cert + key | PEM | cert manager |
| VIP CIDR + interface | string | network |
| Rate-limit policy | req/sec per IP | product / abuse team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-technology-selection]] | Confirms HAProxy is the right tool before tuning. |
| [[lb-health-checks]] | Health-check endpoint design feeds the `option httpchk` block. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: tls12-min-cipher-suites, stick-table-rate-limit, nbthread-cpu-map, maxconn-sized, http-check-expect, keepalived-vrrp | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tune-maxconn-nbthread` | sonnet | Sizing arithmetic from RAM/CPU. |
| `write-frontend-acls` | sonnet | Routing logic per path/host. |
| `lint-config` | haiku | Mechanical `haproxy -c -f` smoke test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/haproxy.cfg` | Full production config: global + defaults + http_front + acl + backends + stick-table |
| `templates/keepalived.conf` | VRRP active-passive VIP config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-haproxy-production.py` | Validate the HAProxy artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-technology-selection]]
- [[lb-nginx-production]]
- [[lb-high-availability]]
- [[lb-health-checks]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (protocol mix, HA need, rate-limit need, capacity per node) to a concrete config shape, each leaf referencing a rule from `01-core-rules.xml`.
