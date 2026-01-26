# Kubernetes Resource Management Checklist

## Pre-Implementation

- [ ] Profile workloads under realistic load
- [ ] Review Prometheus/Grafana metrics for baseline usage
- [ ] Identify critical vs non-critical workloads
- [ ] Document current resource consumption patterns
- [ ] Plan namespace structure for multi-tenancy

---

## Resource Requests/Limits

### Setting Values

- [ ] **Never leave resources blank** (results in BestEffort QoS)
- [ ] Set requests based on observed P50 usage
- [ ] Set limits based on observed P99 usage + headroom
- [ ] Use VPA in recommendation mode before locking values
- [ ] Test under load before finalizing

### CPU Guidelines

- [ ] Start with requests = observed average
- [ ] Set limits 2-3x requests for variable workloads
- [ ] For steady workloads, requests = limits (Guaranteed)
- [ ] Avoid limits too tight (causes throttling)

### Memory Guidelines

- [ ] Set requests = working set size
- [ ] Set limits = max heap/buffer + overhead
- [ ] For JVM: limits = Xmx + metaspace + stack + buffers
- [ ] Test OOM scenarios in staging

---

## QoS Classes

### Guaranteed (Critical Services)

- [ ] `requests.cpu` = `limits.cpu`
- [ ] `requests.memory` = `limits.memory`
- [ ] All containers in pod must have equal requests/limits
- [ ] Apply to: databases, critical APIs, stateful services

### Burstable (Standard Workloads)

- [ ] Set both requests and limits
- [ ] `requests < limits` for burst capacity
- [ ] Apply to: web servers, background workers

### BestEffort (Low Priority)

- [ ] Acceptable only for truly disposable workloads
- [ ] Will be evicted first under pressure
- [ ] Apply to: batch jobs, dev environments

---

## LimitRange Configuration

### Namespace Setup

- [ ] Create LimitRange for every namespace
- [ ] Set sensible defaults for containers without resources
- [ ] Define min/max bounds to prevent extremes
- [ ] Set defaultRequest lower than default limit

### Recommended Values

- [ ] `default.cpu`: 500m - 1000m
- [ ] `default.memory`: 256Mi - 512Mi
- [ ] `defaultRequest.cpu`: 100m - 250m
- [ ] `defaultRequest.memory`: 128Mi - 256Mi
- [ ] `max.cpu`: 4 - 8 (prevent single-container monopoly)
- [ ] `max.memory`: 8Gi - 16Gi

### Validation

- [ ] Test pod creation without explicit resources
- [ ] Verify defaults are applied
- [ ] Test rejection of oversized containers
- [ ] Document LimitRange for team

---

## ResourceQuota Configuration

### Namespace Quotas

- [ ] Create ResourceQuota for every namespace
- [ ] Start generous, tune based on actual usage
- [ ] Set both requests and limits quotas
- [ ] Include object count quotas

### Multi-Tenancy

- [ ] Assign quotas proportional to team needs
- [ ] Reserve headroom for burst (15-20%)
- [ ] Implement chargeback via labels
- [ ] Monitor quota utilization

### Object Limits

- [ ] `pods`: Prevent pod explosion
- [ ] `services`: Control service proliferation
- [ ] `persistentvolumeclaims`: Limit storage claims
- [ ] `secrets`, `configmaps`: Prevent sprawl

---

## Monitoring & Observability

### Prometheus Metrics

- [ ] `container_cpu_usage_seconds_total`
- [ ] `container_memory_usage_bytes`
- [ ] `container_memory_working_set_bytes`
- [ ] `kube_pod_container_resource_requests`
- [ ] `kube_pod_container_resource_limits`
- [ ] `kube_resourcequota`

### Alerts

- [ ] CPU throttling (`container_cpu_cfs_throttled_seconds_total`)
- [ ] Memory near limit (>80%)
- [ ] Quota exhaustion (>90%)
- [ ] OOMKill events
- [ ] Pod evictions

### Dashboards

- [ ] Resource utilization vs requests/limits
- [ ] QoS class distribution
- [ ] Quota usage per namespace
- [ ] Right-sizing recommendations (Goldilocks)

---

## Tools

### Right-Sizing

- [ ] **Goldilocks** - VPA recommendations dashboard
- [ ] **Kubecost** - Cost allocation and optimization
- [ ] **CAST AI** - Automated optimization
- [ ] **PerfectScale** - Resource recommendations

### Enforcement

- [ ] **OPA Gatekeeper** - Policy enforcement
- [ ] **Kyverno** - Kubernetes native policies
- [ ] **Admission webhooks** - Custom validation

---

## Anti-Patterns to Avoid

- [ ] Do NOT leave requests/limits blank in production
- [ ] Do NOT set limits without requests
- [ ] Do NOT set limits lower than requests
- [ ] Do NOT use identical quotas for all namespaces
- [ ] Do NOT ignore CPU throttling metrics
- [ ] Do NOT skip load testing before setting limits

---

## Review Cadence

| Review | Frequency |
|--------|-----------|
| Resource utilization | Weekly |
| Quota adjustments | Monthly |
| LimitRange defaults | Quarterly |
| Full audit | Semi-annually |

---

*k8s-resources/checklist.md | Implementation Checklist*
