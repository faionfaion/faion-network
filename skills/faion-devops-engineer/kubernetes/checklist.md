# Kubernetes Production Checklist

Comprehensive checklist for production-ready Kubernetes deployments (2025-2026).

---

## Pre-Deployment Checklist

### Container Image

- [ ] Use specific image tags (never `latest` in production)
- [ ] Images signed with Sigstore/Cosign
- [ ] Base images from trusted registries
- [ ] Multi-stage builds for minimal image size
- [ ] No secrets baked into images
- [ ] Vulnerability scanning in CI pipeline
- [ ] Image pull secrets configured

### Resource Configuration

- [ ] CPU/memory requests defined
- [ ] CPU/memory limits defined
- [ ] Requests based on actual usage metrics
- [ ] Avoid over-provisioning (monitor utilization)
- [ ] QoS class appropriate for workload
- [ ] Resource quotas per namespace
- [ ] LimitRange configured

### Health Probes

- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Startup probe for slow-starting apps
- [ ] Appropriate timeouts and thresholds
- [ ] Probes test actual functionality
- [ ] initialDelaySeconds accounts for startup time

### Security

- [ ] `runAsNonRoot: true`
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] `capabilities.drop: ["ALL"]`
- [ ] Pod Security Standards enforced
- [ ] Network policies defined
- [ ] Secrets in external secret manager
- [ ] RBAC with least privilege
- [ ] Service account per workload

### High Availability

- [ ] Multiple replicas (min 2 for HA)
- [ ] PodDisruptionBudget defined
- [ ] Pod anti-affinity rules
- [ ] Topology spread constraints
- [ ] HPA configured
- [ ] Resource headroom for scaling

---

## Deployment Strategy Checklist

### Rolling Update (Default)

- [ ] maxSurge configured (recommended: 25%)
- [ ] maxUnavailable configured (recommended: 25%)
- [ ] Readiness probe validates new pods
- [ ] Rollback strategy tested
- [ ] `kubectl rollout status` in CI

### Blue/Green Deployment

- [ ] Service mesh or ingress configured
- [ ] Traffic switching mechanism ready
- [ ] Both environments can run simultaneously
- [ ] Rollback is instant switch
- [ ] Database migrations backward-compatible

### Canary Deployment

- [ ] Argo Rollouts or Flagger installed
- [ ] Traffic splitting configured
- [ ] Metrics for success criteria defined
- [ ] Automatic rollback on failure
- [ ] Progressive percentage increase

---

## Resource Management Checklist

### CPU

- [ ] Requests set to P95 usage
- [ ] Limits 2-3x requests (or omitted)
- [ ] Avoid CPU throttling
- [ ] Monitor CPU throttle metrics

### Memory

- [ ] Requests set to typical usage
- [ ] Limits set to maximum expected
- [ ] OOMKilled alerts configured
- [ ] Memory leak monitoring

### Autoscaling

- [ ] HPA metrics appropriate for workload
- [ ] VPA recommendations reviewed
- [ ] Cluster autoscaler enabled
- [ ] Scale-down delay configured
- [ ] Pod scaling limits set

### Cost Optimization

- [ ] Right-size node types
- [ ] Spot/preemptible instances for non-critical
- [ ] Reserved instances for steady workloads
- [ ] Idle resource detection
- [ ] Namespace-level cost attribution

---

## Security Checklist

### Pod Security

- [ ] Pod Security Standards: Restricted
- [ ] Seccomp profiles applied
- [ ] AppArmor/SELinux enabled
- [ ] No privileged containers
- [ ] Host namespaces disabled

### Network Security

- [ ] Default deny NetworkPolicy
- [ ] Ingress rules explicit
- [ ] Egress rules explicit
- [ ] Service mesh mTLS (optional)
- [ ] External traffic encrypted

### Secrets Management

- [ ] Secrets encrypted at rest
- [ ] External secret manager (Vault, AWS SM)
- [ ] No secrets in ConfigMaps
- [ ] Secret rotation automated
- [ ] Audit logging for secret access

### Image Security

- [ ] Images signed and verified
- [ ] Admission controller validates signatures
- [ ] CVE scanning in pipeline
- [ ] No high/critical vulnerabilities
- [ ] Image pull from private registry

### Access Control

- [ ] RBAC per namespace
- [ ] Service accounts non-default
- [ ] No cluster-admin for apps
- [ ] Audit logging enabled
- [ ] Regular access reviews

---

## Observability Checklist

### Logging

- [ ] Structured logging (JSON)
- [ ] Logs aggregated (ELK, Loki)
- [ ] Log retention policy
- [ ] PII/secrets not logged
- [ ] Correlation IDs in logs

### Metrics

- [ ] Prometheus scraping enabled
- [ ] Application metrics exposed
- [ ] RED metrics (Rate, Errors, Duration)
- [ ] USE metrics (Utilization, Saturation, Errors)
- [ ] Custom dashboards in Grafana

### Tracing

- [ ] Distributed tracing enabled
- [ ] Trace context propagation
- [ ] Sampling strategy defined
- [ ] Integration with logging

### Alerting

- [ ] SLO-based alerts
- [ ] PagerDuty/Opsgenie integration
- [ ] Runbooks linked to alerts
- [ ] Alert fatigue prevention
- [ ] Escalation policies

---

## Operational Checklist

### GitOps

- [ ] ArgoCD or Flux deployed
- [ ] Git as single source of truth
- [ ] Automatic sync enabled
- [ ] Drift detection alerts
- [ ] Pull request workflows

### Backup & DR

- [ ] PV backup strategy (Velero)
- [ ] etcd backup automated
- [ ] DR runbook documented
- [ ] Recovery tested quarterly
- [ ] RTO/RPO defined

### Upgrades

- [ ] Node upgrade strategy (rolling)
- [ ] Control plane upgrade tested
- [ ] API deprecation monitoring
- [ ] Helm chart version pins
- [ ] Upgrade runbook documented

---

## Namespace Checklist

- [ ] Resource quotas defined
- [ ] LimitRange configured
- [ ] NetworkPolicy default deny
- [ ] RBAC per namespace
- [ ] Labels for cost attribution
- [ ] Pod Security Standards enforced

---

## Quick Validation Commands

```bash
# Check pod security
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.spec.containers[*].securityContext}{"\n"}{end}'

# Check resource requests/limits
kubectl get pods -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[0].resources.requests.cpu,\
CPU_LIM:.spec.containers[0].resources.limits.cpu,\
MEM_REQ:.spec.containers[0].resources.requests.memory,\
MEM_LIM:.spec.containers[0].resources.limits.memory

# Check HPA status
kubectl get hpa -A

# Check PDB
kubectl get pdb -A

# Check network policies
kubectl get networkpolicies -A

# Validate deployment readiness
kubectl rollout status deployment/<name> -n <namespace>
```

---

## Sources

- [Kubernetes Production Best Practices](https://learnkube.com/production-best-practices)
- [Kubernetes Security Checklist 2025](https://atmosly.com/blog/kubernetes-security-checklist-50-best-practices-2025-part-ii)
- [21 K8s Deployment Best Practices](https://devtron.ai/blog/kubernetes-deployment-best-practices/)
- [Managing Kubernetes 2025: 7 Pillars](https://scaleops.com/blog/the-complete-guide-to-kubernetes-management-in-2025-7-pillars-for-production-scale/)
