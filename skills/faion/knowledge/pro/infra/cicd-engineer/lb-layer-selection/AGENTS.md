---
slug: lb-layer-selection
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a layered LB topology decision (L4 vs L7 vs hybrid L4-front-of-L7) consistent with traffic profile, content routing, and TLS strategy.
content_id: "3873656382041061"
complexity: medium
produces: decision-record
est_tokens: 4600
tags: [load-balancing, networking, l4, l7, infrastructure]
---
# Load Balancer Layer Selection: L4 vs L7

## Summary

**One-sentence:** Generates a layered LB topology decision (L4 vs L7 vs hybrid L4-front-of-L7) consistent with traffic profile, content routing, and TLS strategy.

**One-paragraph:** Choosing between L4 (transport layer) and L7 (application layer) load balancing is the first architectural decision when deploying a load balancer. L4 routes TCP/UDP by IP and port with minimal CPU cost; L7 routes by HTTP headers, URL, cookies, and content — enabling SSL termination, path routing, and header manipulation at the cost of more resources. Modern stacks often use both layers together (NLB / HAProxy L4 front-end + Ingress / Envoy L7 layer behind). The output of this methodology is a decision record naming the layer + a TLS strategy (terminate / pass-through / re-encrypt).

**Ефективно для:**

- New infra design: пояснений вибір L4 / L7 / hybrid у ADR.
- Architecture review: відхилити пропозицію "L4 for performance + path routing" (суперечність).
- DB/Redis/gaming = L4. Web/API з path routing + TLS termination + WAF = L7.
- Multi-layer: NLB / HAProxy L4 → Ingress / Envoy L7 для anycast + content routing.
- SSL strategy alignment: termination at LB / pass-through / re-encryption — узгоджено з layer.

## Applies If (ALL must hold)

- Choosing or reviewing a load balancer type at the start of an infrastructure design.
- Traffic profile is purely TCP/UDP (gaming, streaming, DB proxies) — L4 is sufficient.
- Content-based routing, SSL termination at the LB, or HTTP header manipulation is needed — L7 is required.
- A/B testing, canary deployments, or API-gateway functionality is in scope — L7 is required.
- Architecture review catches an agent proposing L4 but listing L7 features — reject inconsistency.

## Skip If (ANY kills it)

- Vendor / tool selection — see lb-haproxy-production / lb-nginx-production / lb-cloud-terraform.
- TLS cipher-suite decisions — see ssl-tls-setup.
- Service-mesh internal routing (mTLS, sidecar / sidecarless) — different concern.
- DB read-replica routing — use DB-specific guidance.
- API gateway features (auth, quotas, transforms) — a gateway is more than a load balancer.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Traffic protocol mix | list (HTTP / gRPC / TCP / UDP) | architecture |
| Content-routing needs | path / header / cookie rules | product |
| TLS strategy | terminate / pass-through / re-encrypt | security |
| Performance target | rps + connections / sec | load test |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-technology-selection]] | The layer decision feeds the product / tool decision next. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: l4-only-uniform-tcp-udp, l7-required-for-content-routing, ssl-terminates-at-l7, hybrid-l4-front-of-l7-for-anycast, no-l4-with-l7-features | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision-record + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `analyze-traffic` | sonnet | Protocol + routing-feature analysis. |
| `emit-decision` | sonnet | Structured decision-record. |
| `lint-contradictions` | haiku | Mechanical check for "L4 + L7 features" mixed. |

## Templates

| File | Purpose |
|------|---------|
| `templates/layer-decision-record.md` | ADR skeleton: traffic profile → layer → TLS strategy → rationale |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-layer-selection.py` | Validate the layer decision-record JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-algorithms]]
- [[lb-health-checks]]
- [[lb-session-persistence]]
- [[lb-high-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (protocol, content routing, TLS strategy, anycast need) to a concrete layer choice, each leaf referencing a rule from `01-core-rules.xml`.
