# Service Mesh

## Summary

Infrastructure layer for secure, observable service-to-service communication in microservices. Covers mesh selection (Istio vs Linkerd vs Cilium vs Istio Ambient), sidecar vs sidecarless architectures, mTLS configuration, traffic management patterns (canary, blue-green, circuit breaking, retries, mirroring), and 2025 performance benchmarks per mesh.

## Why

Without a service mesh, each service team must implement mTLS, retries, circuit breaking, and distributed tracing independently — leading to inconsistency and gaps. A mesh provides these uniformly via the proxy layer without application code changes. The 2025 shift to sidecarless (Ambient, Cilium eBPF) reduces latency overhead from ~166% to under 8% compared to traditional Envoy sidecars.

## When To Use

- 10+ microservices requiring uniform mTLS (zero-trust) between all pods
- Canary or blue-green deployments requiring fine-grained traffic splitting
- Multi-cluster communication with cross-cluster service discovery
- Compliance requirements (SOC2, HIPAA) needing encryption audit trails
- Uniform distributed tracing and RED metrics across all services

## When NOT To Use

- Fewer than 5 services — direct HTTP/gRPC with cert-manager manual TLS is simpler
- Monolith or near-monolith — no inter-service traffic to manage
- Latency requirements under 1ms — any proxy layer adds overhead
- Team not yet comfortable with Kubernetes — master K8s basics before adding mesh complexity
- Resource-constrained environment where proxy memory per pod (20-70 MB) is prohibitive

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture-and-selection.xml` | Sidecar vs per-node vs eBPF data plane, 2025 performance benchmarks, Istio vs Linkerd vs Cilium feature comparison, decision framework |
| `content/02-mtls-and-traffic-management.xml` | mTLS permissive-to-strict migration, SPIFFE identity, certificate rotation best practices, traffic patterns (canary/blue-green/mirroring/circuit-breaking/retries/timeouts) |

## Templates

| File | Purpose |
|------|---------|
| `templates/istio-virtualservice.yaml` | VirtualService + DestinationRule for canary traffic splitting with header-based routing |
| `templates/linkerd-trafficsplit.yaml` | Linkerd SMI TrafficSplit for weighted canary |
