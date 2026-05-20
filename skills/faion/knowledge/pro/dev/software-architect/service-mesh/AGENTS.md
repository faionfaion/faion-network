---
slug: service-mesh
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Infrastructure layer for secure, observable service-to-service communication in microservices.
content_id: "ef72df51bcd6d1cf"
tags: [microservices, service-mesh, mtls, istio, linkerd, traffic-management]
---
# Service Mesh

## Summary

**One-sentence:** Infrastructure layer for secure, observable service-to-service communication in microservices.

**One-paragraph:** Infrastructure layer for secure, observable service-to-service communication in microservices. Covers mesh selection (Istio vs Linkerd vs Cilium vs Istio Ambient), sidecar vs sidecarless architectures, mTLS configuration, traffic management patterns (canary, blue-green, circuit breaking, retries, mirroring), and 2025 performance benchmarks per mesh.

## Applies If (ALL must hold)

- 10+ microservices requiring uniform mTLS (zero-trust) between all pods
- Canary or blue-green deployments requiring fine-grained traffic splitting
- Multi-cluster communication with cross-cluster service discovery
- Compliance requirements (SOC2, HIPAA) needing encryption audit trails
- Uniform distributed tracing and RED metrics across all services

## Skip If (ANY kills it)

- Fewer than 5 services — direct HTTP/gRPC with cert-manager manual TLS is simpler
- Monolith or near-monolith — no inter-service traffic to manage
- Latency requirements under 1ms — any proxy layer adds overhead
- Team not yet comfortable with Kubernetes — master K8s basics before adding mesh complexity
- Resource-constrained environment where proxy memory per pod (20-70 MB) is prohibitive

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

- parent skill: `pro/dev/software-architect/`
