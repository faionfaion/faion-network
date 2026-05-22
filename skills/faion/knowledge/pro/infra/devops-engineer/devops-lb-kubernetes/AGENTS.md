---
slug: devops-lb-kubernetes
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes provides a layered load balancing model: Service (kube-proxy, L4) distributes traffic across pods; Ingress (Nginx, Traefik, AWS ALB Controller) handles L7 routing, TLS, and host/path rules.
content_id: "6344b16be4a65a0f"
tags: [kubernetes, load-balancing, ingress, traefik, aws-alb]
---
# Kubernetes Load Balancing: Services, Ingress, and Probes

## Summary

**One-sentence:** Kubernetes provides a layered load balancing model: Service (kube-proxy, L4) distributes traffic across pods; Ingress (Nginx, Traefik, AWS ALB Controller) handles L7 routing, TLS, and host/path rules.

**One-paragraph:** Kubernetes provides a layered load balancing model: Service (kube-proxy, L4) distributes traffic across pods; Ingress (Nginx, Traefik, AWS ALB Controller) handles L7 routing, TLS, and host/path rules. Readiness probes gate traffic admission during rolling deployments; liveness probes trigger pod restarts on deadlocks.

## Applies If (ALL must hold)

- All Kubernetes-hosted services that need stable network access — Services are mandatory, not optional.
- Multiple HTTP services behind a single external IP — use Ingress to avoid provisioning one cloud LB per service.
- Rolling deployments — readiness probes ensure new pods receive traffic only after they are ready.
- Cloud-specific routing (AWS ALB with WAF, GCP NEG) via cloud controller annotations.

## Skip If (ANY kills it)

- Non-HTTP services (raw TCP, UDP, gRPC without HTTP/2 Ingress support) — use Service type LoadBalancer with NLB annotations instead of Ingress.
- Do not use NodePort in production for external traffic — port range 30000-32767 is not firewall-friendly and bypasses Ingress.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/devops-engineer/`
