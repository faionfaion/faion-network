# Container Orchestration

## Summary

Kubernetes architecture patterns, pod design, deployment strategies, autoscaling, persistent storage, RBAC, and security best practices for production workloads. Covers the sidecar/ambassador/adapter/init-container pod patterns, rolling/blue-green/canary deployment strategies, HPA/KEDA/VPA autoscaling, and 2025 security standards (distroless images, eBPF runtime security, External Secrets Operator).

## Why

Kubernetes declarative model (desired state reconciliation) enables self-healing, horizontal scaling, and zero-downtime deployments — but misconfigured resource requests cause OOM kills and poor scheduling, missing liveness/readiness probes cause traffic to reach broken pods, and over-privileged service accounts create security blast radius. Each pattern addresses a specific operational failure mode.

## When To Use

- Deploying a new service to a Kubernetes cluster (select pod pattern, set probes, set resource limits)
- Choosing a deployment strategy for a high-risk release (canary vs blue-green)
- Configuring autoscaling for queue-backed or event-driven workloads (KEDA)
- Hardening a Kubernetes workload: RBAC, network policies, pod security standards
- Migrating Docker Compose to Kubernetes manifests

## When NOT To Use

- Single-VM or bare-metal deployment without container runtime — use systemd/supervisor instead
- Serverless function with sub-second invocation pattern — K8s cold-start overhead is not justified
- Development environment where Docker Compose is sufficient — K8s adds operational overhead with no benefit
- Stateful workloads requiring POSIX file locking across nodes — ReadWriteMany volumes add complexity

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture-and-pod-patterns.xml` | Control plane / worker node components, resource hierarchy, sidecar/ambassador/adapter/init-container patterns with use cases |
| `content/02-deployments-and-autoscaling.xml` | Rolling update parameters, blue-green vs canary trade-offs, HPA vs KEDA vs VPA selection, QoS classes, resource quota |
| `content/03-security-and-storage.xml` | RBAC least-privilege, network policies, pod security standards, 2025 security practices (distroless, eBPF, External Secrets), storage access modes, CSI best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/deployment.yaml` | Production Deployment with liveness/readiness/startup probes, resource limits, non-root security context |
| `templates/hpa.yaml` | HPA with CPU + custom metric (requests_per_second) targets |
| `templates/keda-scaledobject.yaml` | KEDA ScaledObject for Kafka consumer lag scaling with scale-to-zero |
