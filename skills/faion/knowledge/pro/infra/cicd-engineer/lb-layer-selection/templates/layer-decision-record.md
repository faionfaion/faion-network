<!-- purpose: ADR skeleton — LB layer (L4/L7/hybrid) + TLS strategy + rationale -->
<!-- consumes: see content/02-output-contract.xml inputs (protocol, layer, tls_strategy, features) -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml (l4-only-uniform-tcp-udp, l7-required-for-content-routing, ssl-terminates-at-l7, hybrid-l4-front-of-l7-for-anycast, no-l4-with-l7-features) -->
<!-- token-budget-impact: ~300 tokens when loaded as context -->

# Layer Decision: <service-name>

## Context

- **Service:** <service-name>
- **Protocol mix:** HTTPS, gRPC over HTTP/2
- **Content routing:** path-based (`/api`, `/static`, `/grpc`)
- **TLS:** terminate at LB (WAF + header inspection required)
- **Anycast:** no (single region for now)

## Decision

| Dimension | Choice |
|-----------|--------|
| Layer     | L7 |
| TLS       | terminate-at-lb |
| Features  | path-routing, header-routing, waf |

## Rationale

Content-based routing + WAF integration cannot be expressed at L4. Anycast is not required at this SLA tier, so a single-tier L7 LB (ALB / Ingress-Nginx) is sufficient. If we expand to multi-region with 99.99% SLA, revise this decision to hybrid (Global Accelerator → ALB).

## Consequences

- LB CPU sized for TLS termination + regex routing.
- Backend pool sees plain HTTP (TLS terminated upstream).
- WAF rule set lives at the LB, not the backend.

## Status

- [ ] Approved
- [ ] Implemented
