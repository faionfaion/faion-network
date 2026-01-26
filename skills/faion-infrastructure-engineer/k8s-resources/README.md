---
name: faion-k8s-resources
user-invocable: false
description: "Kubernetes resource management: requests, limits, QoS, LimitRanges, ResourceQuotas"
---

# Kubernetes Resource Management

**Resource requests/limits, QoS classes, LimitRanges, and ResourceQuotas**

---

## Overview

Kubernetes resource management ensures workloads get the resources they need while preventing any single workload from monopolizing cluster resources. According to 2025 benchmarks, 99.94% of clusters are over-provisioned with average CPU utilization at just 10%.

### Core Concepts

| Concept | Scope | Purpose |
|---------|-------|---------|
| **Requests** | Container | Scheduler uses to place pods; minimum guaranteed resources |
| **Limits** | Container | Maximum resources; kubelet enforces |
| **QoS Classes** | Pod | Eviction priority during resource pressure |
| **LimitRange** | Namespace | Default/min/max for individual containers |
| **ResourceQuota** | Namespace | Aggregate limits for all resources |

---

## Resource Requests and Limits

### How They Work

```
Requests → Scheduler decision (which node)
Limits   → Runtime enforcement (kubelet)
```

| Field | Effect | Default |
|-------|--------|---------|
| `requests.cpu` | Guaranteed CPU shares | None (BestEffort) |
| `requests.memory` | Guaranteed memory | None (BestEffort) |
| `limits.cpu` | CPU throttling ceiling | None (unlimited) |
| `limits.memory` | OOMKill threshold | None (unlimited) |

### CPU Units

| Value | Meaning |
|-------|---------|
| `1` | 1 vCPU/core |
| `500m` | 0.5 vCPU (millicores) |
| `100m` | 0.1 vCPU |

### Memory Units

| Value | Meaning |
|-------|---------|
| `128Mi` | 128 mebibytes |
| `1Gi` | 1 gibibyte |
| `256M` | 256 megabytes (decimal) |

---

## Quality of Service (QoS) Classes

Kubernetes assigns QoS class based on requests/limits configuration:

| QoS Class | Condition | Eviction Priority |
|-----------|-----------|-------------------|
| **Guaranteed** | requests = limits (all containers) | Last (highest priority) |
| **Burstable** | requests < limits (any container) | Middle |
| **BestEffort** | No requests/limits | First (lowest priority) |

### When to Use Each

| Use Case | QoS Class | Configuration |
|----------|-----------|---------------|
| Critical services (DB, API) | Guaranteed | requests = limits |
| Standard workloads | Burstable | requests < limits |
| Batch jobs, dev workloads | BestEffort | No resources |

---

## LimitRange

Enforces resource constraints at **container/pod level** within a namespace.

### Capabilities

- Set **default** requests/limits for containers without explicit values
- Set **min/max** bounds for resources
- Set **defaultRequest** (different from default limit)
- Enforce **request/limit ratios**

### Common Use Cases

| Scenario | LimitRange Feature |
|----------|-------------------|
| Prevent huge containers | `max` limits |
| Ensure baseline resources | `min` requests |
| Auto-apply sensible defaults | `default`, `defaultRequest` |
| Prevent overcommit | `maxLimitRequestRatio` |

---

## ResourceQuota

Enforces resource constraints at **namespace level** (aggregate totals).

### Quotable Resources

| Category | Resources |
|----------|-----------|
| Compute | `requests.cpu`, `limits.cpu`, `requests.memory`, `limits.memory` |
| Storage | `requests.storage`, `persistentvolumeclaims` |
| Objects | `pods`, `services`, `secrets`, `configmaps`, `deployments` |

### Quota Scopes

| Scope | Matches |
|-------|---------|
| `Terminating` | Pods with activeDeadlineSeconds |
| `NotTerminating` | Pods without activeDeadlineSeconds |
| `BestEffort` | BestEffort QoS pods |
| `NotBestEffort` | Guaranteed/Burstable pods |
| `PriorityClass` | Pods with specific priority |

---

## Combined Strategy

Best practice: Use **both** LimitRange and ResourceQuota together.

```
LimitRange → Per-container governance (defaults + bounds)
     +
ResourceQuota → Namespace-wide caps (aggregate limits)
     =
Complete resource management
```

### Defense in Depth

1. **LimitRange** prevents individual containers from being too large/small
2. **ResourceQuota** prevents namespace from consuming too many cluster resources
3. **PriorityClass** ensures critical workloads survive eviction
4. **VPA/HPA** automates right-sizing over time

---

## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Real-world YAML examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for resource analysis |

---

## References

- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)
- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Mastering Kubernetes Resource Management 2025](https://aokumo.io/blog/kubernetes-resource-management-2025/)
- [Kubernetes Resource Requests & Limits Best Practices](https://medium.com/@bavicnative/resource-requests-limits-best-practices-in-kubernetes-3d2ed90d6f17)
- [PerfectScale: Kubernetes Resource Quotas & Limit Ranges](https://www.perfectscale.io/blog/kubernetes-resource-quotas-limit-ranges)

---

*k8s-resources | Resource Management Reference*
