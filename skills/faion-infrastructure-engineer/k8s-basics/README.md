# Kubernetes Basics

**Core kubectl operations, pods, services, namespaces, and fundamental concepts**

## Overview

Kubernetes (K8s) is the bedrock of modern container orchestration. This methodology covers essential concepts for running containers at scale with reliability and efficiency.

**Version Requirements:**
- Kubernetes: 1.29+ (prefer 1.31+)
- kubectl: Match cluster version
- Helm: 3.14+
- Kustomize: Built into kubectl 1.14+

## Core Concepts

### Architecture Components

| Component | Role |
|-----------|------|
| **Control Plane** | Manages cluster state (API server, scheduler, controller manager, etcd) |
| **Worker Nodes** | Run containerized workloads |
| **kubelet** | Node agent ensuring containers run in Pods |
| **kube-proxy** | Network proxy for Service implementation |

### Workload Resources

| Resource | Short | Purpose |
|----------|-------|---------|
| Pod | po | Smallest deployable unit, runs containers |
| Deployment | deploy | Manages ReplicaSets, declarative updates |
| ReplicaSet | rs | Ensures specified number of pod replicas |
| StatefulSet | sts | Manages stateful applications |
| DaemonSet | ds | Runs pod on every node |
| Job | - | One-time task execution |
| CronJob | cj | Scheduled task execution |

### Service & Networking

| Resource | Short | Purpose |
|----------|-------|---------|
| Service | svc | Stable network endpoint for pods |
| Ingress | ing | HTTP/HTTPS routing, load balancing |
| NetworkPolicy | netpol | Pod network traffic rules |
| Endpoints | ep | IP addresses backing a Service |

### Configuration & Storage

| Resource | Short | Purpose |
|----------|-------|---------|
| ConfigMap | cm | Non-sensitive configuration data |
| Secret | - | Sensitive data (credentials, keys) |
| PersistentVolumeClaim | pvc | Request for storage |
| PersistentVolume | pv | Cluster storage resource |

### Cluster Organization

| Resource | Short | Purpose |
|----------|-------|---------|
| Namespace | ns | Virtual cluster partitioning |
| ResourceQuota | quota | Resource limits per namespace |
| LimitRange | limits | Default resource constraints |
| Node | no | Worker machine in cluster |

## Best Practices (2025-2026)

### Resource Management

1. **Always set resource requests and limits** - Prevents resource starvation
2. **Use Vertical Pod Autoscaler (VPA)** - Automated right-sizing
3. **Implement namespace quotas** - Fair resource allocation
4. **Monitor actual usage vs requests** - Avoid overprovisioning

### Security

1. **Run as non-root** - Principle of least privilege
2. **Read-only root filesystem** - Prevent runtime modifications
3. **Drop all capabilities** - Minimize attack surface
4. **Use network policies** - Restrict pod-to-pod traffic
5. **Scan container images** - Prevent vulnerable deployments

### Reliability

1. **Configure health probes** - Liveness, readiness, startup
2. **Use Pod Disruption Budgets** - Ensure availability during maintenance
3. **Implement graceful shutdown** - Handle SIGTERM properly
4. **Set appropriate replica counts** - Minimum 2 for production

### Configuration

1. **Use declarative YAML** - Version control all manifests
2. **Separate config from code** - ConfigMaps and Secrets
3. **Use Kustomize or Helm** - Environment-specific overlays
4. **Validate manifests** - Use admission controllers, policy tools

## Files in This Methodology

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment and operational checklists |
| [examples.md](examples.md) | kubectl commands and common operations |
| [templates.md](templates.md) | YAML manifests for pods, services, deployments |
| [llm-prompts.md](llm-prompts.md) | Prompts for K8s troubleshooting and generation |

## Quick kubectl Reference

```bash
# Context and namespace
kubectl config current-context
kubectl config set-context --current --namespace=<ns>

# Resource operations
kubectl get <resource> -o wide          # List with details
kubectl describe <resource> <name>      # Detailed info
kubectl apply -f manifest.yaml          # Apply configuration
kubectl delete -f manifest.yaml         # Delete resources

# Debugging
kubectl logs <pod> [-c container]       # View logs
kubectl exec -it <pod> -- /bin/sh       # Shell access
kubectl port-forward <pod> 8080:80      # Local access
```

## Related Methodologies

| Methodology | Focus |
|-------------|-------|
| [kubernetes-deployment/](../kubernetes-deployment/) | Advanced deployments, strategies |
| [helm-basics/](../helm-basics/) | Helm charts and templating |
| [k8s-resources](../k8s-resources.md) | Resource management deep-dive |

## Sources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices (Komodor)](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)
- [Kubernetes Configuration Good Practices](https://kubernetes.io/blog/2025/11/25/configuration-good-practices/)
- [CNCF Kubernetes Resources 2026](https://www.cncf.io/blog/2026/01/19/top-28-kubernetes-resources-for-2026-learn-and-stay-up-to-date/)
- [Kubernetes Production Best Practices](https://learnkube.com/production-best-practices)
- [KodeKloud K8s Best Practices 2025](https://kodekloud.com/blog/kubernetes-best-practices-2025/)

---

*faion-infrastructure-engineer/k8s-basics | Kubernetes fundamentals*
