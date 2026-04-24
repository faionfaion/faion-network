# Kubernetes Basics Checklist

## Pre-Deployment Checklist

### Container Image

- [ ] Image tagged with specific version (not `latest`)
- [ ] Image pulled from trusted registry
- [ ] Image vulnerability scan completed
- [ ] Multi-stage build for smaller image size
- [ ] Non-root user configured in Dockerfile

### Pod Specification

- [ ] Resource requests defined (CPU, memory)
- [ ] Resource limits defined (CPU, memory)
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Startup probe for slow-starting apps
- [ ] Security context set (runAsNonRoot, readOnlyRootFilesystem)
- [ ] Capabilities dropped (drop: ALL)

### Deployment Configuration

- [ ] Replicas set appropriately (minimum 2 for production)
- [ ] Update strategy defined (RollingUpdate recommended)
- [ ] maxSurge and maxUnavailable configured
- [ ] Labels applied for service selection
- [ ] Annotations for monitoring/observability

### Service Configuration

- [ ] Correct service type selected (ClusterIP/NodePort/LoadBalancer)
- [ ] Port and targetPort correctly mapped
- [ ] Selector matches pod labels
- [ ] Service account configured if needed

### Namespace Organization

- [ ] Namespace created and documented
- [ ] ResourceQuota applied to namespace
- [ ] LimitRange set for default resources
- [ ] Network policies defined

### Configuration Management

- [ ] Sensitive data stored in Secrets (not ConfigMaps)
- [ ] ConfigMaps used for non-sensitive config
- [ ] Environment variables properly referenced
- [ ] Volume mounts configured correctly

## Operational Checklist

### Daily Operations

- [ ] Check pod status across namespaces
- [ ] Review recent events for warnings
- [ ] Monitor resource utilization
- [ ] Verify service endpoints are healthy

### Debugging Issues

- [ ] Check pod events: `kubectl describe pod <name>`
- [ ] Review container logs: `kubectl logs <pod>`
- [ ] Verify resource availability on nodes
- [ ] Check network policies blocking traffic
- [ ] Validate service selector matches pods
- [ ] Test DNS resolution in cluster

### Common Issue Resolution

| Symptom | Check |
|---------|-------|
| ImagePullBackOff | Registry auth, image name/tag |
| CrashLoopBackOff | Logs, resource limits, startup probe |
| Pending | Node resources, node selector, PVC |
| ContainerCreating | PVC, ConfigMap, Secret availability |
| OOMKilled | Increase memory limits |
| Evicted | Node disk/memory pressure |

### Scaling Operations

- [ ] Verify HPA metrics are available
- [ ] Check cluster autoscaler logs
- [ ] Monitor pod distribution across nodes
- [ ] Validate PodDisruptionBudget settings

### Security Audit

- [ ] No privileged containers
- [ ] No host network/PID/IPC sharing
- [ ] Secrets not exposed in environment variables (prefer volume mounts)
- [ ] RBAC configured with least privilege
- [ ] Network policies restrict unnecessary traffic
- [ ] Pod security admission enforced

## Rollout Checklist

### Before Rollout

- [ ] Changes tested in staging/dev
- [ ] Manifests version controlled
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured
- [ ] PodDisruptionBudget in place

### During Rollout

- [ ] Monitor rollout status: `kubectl rollout status`
- [ ] Watch for pod failures
- [ ] Verify readiness probes pass
- [ ] Check application metrics/logs

### After Rollout

- [ ] All pods running and ready
- [ ] Service endpoints updated
- [ ] Application responding correctly
- [ ] No increase in error rates
- [ ] Document deployment in changelog

## Namespace Setup Checklist

```yaml
# Minimum namespace configuration
Namespace:
  - [ ] Created with meaningful name
  - [ ] Labels for organization (team, environment)

ResourceQuota:
  - [ ] CPU requests/limits
  - [ ] Memory requests/limits
  - [ ] Pod count limit
  - [ ] PVC count limit

LimitRange:
  - [ ] Default CPU request/limit
  - [ ] Default memory request/limit
  - [ ] Min/max constraints

NetworkPolicy:
  - [ ] Default deny ingress (optional but recommended)
  - [ ] Allow required traffic explicitly
```

## Quick Validation Commands

```bash
# Cluster health
kubectl cluster-info
kubectl get nodes
kubectl get componentstatuses

# Namespace resources
kubectl get all -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Pod health
kubectl get pods -o wide
kubectl top pods
kubectl describe pod <name>

# Service validation
kubectl get endpoints <service>
kubectl run curl --rm -it --image=curlimages/curl -- curl http://<service>:<port>
```

---

*k8s-basics/checklist.md | Deployment and operational verification*
