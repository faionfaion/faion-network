---
slug: lb-kubernetes-ingress
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Kubernetes Ingress requires: controller deployment with 3+ replicas, PodDisruptionBudget (minAvailable: 2), pod anti-affinity to prevent co-location, topology spread constraints across AZs, explicit resource requests/limits (TLS and regex are CPU-bound), and per-Ingress annotations for TLS redirect, rate limiting, CORS, body size, and timeouts.
content_id: "6264ae834cf559c6"
tags: [kubernetes, ingress, load-balancing, gateway-api, infrastructure]
---
# Kubernetes Ingress Configuration

## Summary

**One-sentence:** Kubernetes Ingress requires: controller deployment with 3+ replicas, PodDisruptionBudget (minAvailable: 2), pod anti-affinity to prevent co-location, topology spread constraints across AZs, explicit resource requests/limits (TLS and regex are CPU-bound), and per-Ingress annotations for TLS redirect, rate limiting, CORS, body size, and timeouts.

**One-paragraph:** Kubernetes Ingress requires: controller deployment with 3+ replicas, PodDisruptionBudget (minAvailable: 2), pod anti-affinity to prevent co-location, topology spread constraints across AZs, explicit resource requests/limits (TLS and regex are CPU-bound), and per-Ingress annotations for TLS redirect, rate limiting, CORS, body size, and timeouts. Use separate Ingress controllers per traffic class (public/internal/admin).

## Applies If (ALL must hold)

- Deploying Kubernetes Ingress controller (Nginx-Ingress, Traefik, HAProxy Ingress, Envoy Gateway) and tuning health checks, TLS, and replicas.
- Migrating legacy Nginx configs to a Gateway API plus Envoy-based stack.
- Setting up separate Ingress controllers per traffic class (public, internal, admin).
- Bare-metal K8s clusters where MetalLB provides LoadBalancer Services for the Ingress controller.

## Skip If (ANY kills it)

- Managed cloud clusters where the cloud-native LB (ALB Ingress Controller on EKS, GKE Ingress) integrates better with the cloud network fabric.
- Service mesh routing between internal services — use Istio VirtualService or Linkerd SMI instead of Ingress.
- TCP/UDP load balancing — Ingress API only handles HTTP(S); use a LoadBalancer Service or HAProxy at L4.

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

- parent skill: `pro/infra/cicd-engineer/`
