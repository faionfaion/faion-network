---
slug: load-balancing-concepts
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Picks LB layer (L4/L7), algorithm, health-check + session-persistence policy, and HA topology for a given service.
content_id: "f2f2dc1132c7a19e"
complexity: medium
produces: decision-record
est_tokens: 4400
tags: [load-balancing, high-availability, networking, infrastructure, health-checks]
---

# Load Balancing Concepts

## Summary

**One-sentence:** Picks LB layer (L4/L7), algorithm, health-check + session-persistence policy, and HA topology for a given service.

**One-paragraph:** Selecting a load balancer is not picking a vendor — it's picking the OSI layer (L4 vs L7), the algorithm (static vs dynamic), the health-check shape (TCP vs HTTP /health), the session-persistence strategy (externalised state vs sticky), and the HA topology (active-passive vs multi-region GSLB). Wrong layer or wrong stickiness cascades into latency, uneven backend utilisation, lost sessions on failover, or single-points-of-failure that defeat the whole point of fronting with an LB. This methodology produces a decision record: chosen layer, algorithm, health-check parameters, persistence strategy, HA pattern, and the rationale tying each decision to an observable input.

**Ефективно для:**

- Horizontal scaling: множинні backend-инстанси за одним endpoint, треба розподіл трафіку.
- HA-вимоги (99.9%+): треба усунути SPOF на LB і backend рівнях.
- API-gateway сценарії (L7): content-routing, SSL termination, header manipulation.
- Stateful workloads (WebSocket / cart sessions): рішення sticky vs externalised state.
- Multi-region failover: GSLB шар + регіональні LB-пары.

## Applies If (ALL must hold)

- Service has ≥2 backend instances (or is on the path to becoming horizontally scaled).
- An availability target ≥99.9% is in the contract or roadmap.
- Backend traffic profile (RPS, connection longevity, payload shape) can be characterised.

## Skip If (ANY kills it)

- Single-server dev / staging env where the LB overhead is not justified.
- Internal-only tool with <10 RPS and no HA SLA — front it with DNS round-robin instead.
- Stateful monolith that cannot be refactored AND cannot tolerate sticky-session loss on failover — pause and rearchitect first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Traffic profile | JSON / spec doc | load test or production metrics (RPS, p95 latency, concurrent connections) |
| Availability target | SLO numeric (e.g. 99.95) | service contract / SLO doc |
| Protocol set | list (HTTP, HTTPS, TCP, UDP, gRPC, WebSocket) | service catalogue |
| Session model | stateless | session-in-cookie | session-server-side | sticky-required | application architecture review |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[nginx-configuration]] | If chosen LB is nginx, the config syntax is owned there |
| [[backup-strategies]] | Backend redundancy and DR posture interact with LB topology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: layer-choice, algorithm-choice, health-check-shape, session-externalisation, ha-no-spof, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision-record + valid / invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: tcp-only-check, sticky-without-fallback, single-lb-spof, l7-when-l4-fits | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: profile → layer → algorithm → health-checks → persistence → HA topology | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on protocol + statefulness + availability target → rule | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-traffic-profile` | haiku | Mechanical bucketing of (rps, payload, longevity) — no judgment. |
| `pick-layer-and-algorithm` | sonnet | Decision-tree application with reasoning about why a branch fits. |
| `write-decision-record` | sonnet | Lightweight prose for the rationale block. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lb-decision-record.md` | Markdown skeleton for the decision record (sections + rationale prompts) |
| `templates/lb-decision-record.json` | JSON template for the decision-record artefact (validator target) |
| `templates/_smoke-test.json` | Minimum filled artefact used by validate-load-balancing-concepts.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-load-balancing-concepts.py` | Validate the decision-record artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[nginx-configuration]]
- [[backup-strategies]]
- [[ssl-tls-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it whenever you have to defend the L4-vs-L7 choice, the algorithm choice, or the sticky-vs-externalised choice in a design review.
