# Kubernetes Reference

Production-grade Kubernetes operations, deployment strategies, and best practices for 2025-2026.

## Overview

| Aspect | Coverage |
|--------|----------|
| Versions | Kubernetes 1.28+ (prefer 1.31+), kubectl, Helm 3.14+ |
| Focus | Deployments, Services, Scaling, Security, Resource Management |
| Tools | kubectl, Helm, Kustomize, ArgoCD, Karpenter |

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Production readiness checklist |
| [examples.md](examples.md) | Code examples and patterns |
| [templates.md](templates.md) | Ready-to-use YAML templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for K8s tasks |

## Quick Reference

### Resource Types

| Resource | Short | Description |
|----------|-------|-------------|
| pods | po | Running containers |
| deployments | deploy | Manages ReplicaSets |
| services | svc | Network endpoints |
| configmaps | cm | Configuration data |
| secrets | - | Sensitive data |
| ingress | ing | HTTP routing |
| persistentvolumeclaims | pvc | Storage claims |
| namespaces | ns | Cluster partitions |
| nodes | no | Cluster nodes |
| replicasets | rs | Pod replicas |
| daemonsets | ds | Node-level pods |
| statefulsets | sts | Stateful apps |
| jobs | - | One-time tasks |
| cronjobs | cj | Scheduled tasks |
| horizontalpodautoscalers | hpa | Auto-scaling |
| verticalpodautoscalers | vpa | Resource tuning |
| poddisruptionbudgets | pdb | Availability guarantees |
| networkpolicies | netpol | Traffic control |

### Deployment Strategies

| Strategy | Use Case | Zero Downtime |
|----------|----------|---------------|
| Rolling Update | Default, gradual replacement | Yes |
| Recreate | Stateful apps, breaking changes | No |
| Blue/Green | Full environment switch | Yes |
| Canary | Risk mitigation, testing | Yes |
| A/B Testing | Feature experiments | Yes |

### Scaling Methods

| Method | Description | Best For |
|--------|-------------|----------|
| HPA | Horizontal Pod Autoscaler | Request-based workloads |
| VPA | Vertical Pod Autoscaler | Resource optimization |
| Cluster Autoscaler | Node scaling | Capacity management |
| Karpenter | Pod-aware node provisioning | Dynamic clusters |
| KEDA | Event-driven autoscaling | Queue/event workloads |

## Key Concepts

### Resource Management

```yaml
resources:
  requests:           # Guaranteed resources (scheduling)
    memory: "256Mi"
    cpu: "250m"
  limits:             # Maximum allowed (throttling/OOM)
    memory: "512Mi"
    cpu: "500m"
```

**2025 Insight:** 99.94% of clusters are over-provisioned. Average CPU utilization is only 10%, memory ~23%.

### Health Probes

| Probe | Purpose | Action on Failure |
|-------|---------|-------------------|
| Liveness | Is container alive? | Restart container |
| Readiness | Is container ready? | Remove from service |
| Startup | Is container starting? | Wait before other probes |

### Security Context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

## Tool Selection

| Tool | Use Case |
|------|----------|
| kubectl | Direct cluster interaction |
| Helm | Package management, templating |
| Kustomize | Configuration overlays |
| ArgoCD/Flux | GitOps deployments |
| Karpenter | Dynamic node provisioning |
| KEDA | Event-driven scaling |

## Sources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [14 Kubernetes Best Practices 2025](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)
- [Kubernetes Best Practices 2025: Optimize, Secure, Scale](https://kodekloud.com/blog/kubernetes-best-practices-2025/)
- [Kubernetes Security 2025-2026](https://www.cncf.io/blog/2025/12/15/kubernetes-security-2025-stable-features-and-2026-preview/)
- [CNCF: Top 5 Hard-Earned Lessons](https://www.cncf.io/blog/2025/11/18/top-5-hard-earned-lessons-from-the-experts-on-managing-kubernetes/)
- [Kubernetes Autoscaling 2025](https://www.sedai.io/blog/kubernetes-autoscaling)
- [Kubernetes Cost Optimization 2025-26](https://sedai.io/blog/a-guide-to-kubernetes-capacity-planning-and-optimization)
