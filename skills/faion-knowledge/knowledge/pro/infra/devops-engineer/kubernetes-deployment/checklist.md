# Kubernetes Deployment Checklists

## Pre-Deployment Checklist

### Image Preparation

- [ ] Image tagged with specific version (NOT `latest`)
- [ ] Image scanned for vulnerabilities
- [ ] Image pushed to registry
- [ ] Image pull secrets configured

### Configuration Validation

- [ ] Resource requests and limits defined
- [ ] Environment variables set correctly
- [ ] ConfigMaps and Secrets created
- [ ] Volume mounts configured
- [ ] Service account created with minimal permissions

### Health Checks

- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Startup probe configured (for slow-starting apps)
- [ ] Probe endpoints implemented in application

### Networking

- [ ] Service created and configured
- [ ] Ingress rules defined
- [ ] Network policies applied
- [ ] TLS certificates provisioned

### Scaling Configuration

- [ ] Replica count appropriate for load
- [ ] HPA configured with appropriate metrics
- [ ] Pod Disruption Budget defined
- [ ] Anti-affinity rules set for HA

### Rollout Strategy

- [ ] Deployment strategy selected (Rolling/Blue-Green/Canary)
- [ ] maxUnavailable and maxSurge configured
- [ ] Rollback plan documented
- [ ] Feature flags ready (if applicable)

---

## Rolling Update Checklist

### Before Deployment

- [ ] Current deployment healthy (`kubectl rollout status`)
- [ ] Rollback command prepared
- [ ] Monitoring dashboards open
- [ ] Team notified of deployment window

### Configuration

- [ ] `maxUnavailable: 1` (conservative)
- [ ] `maxSurge: 2-3` (moderate)
- [ ] `revisionHistoryLimit: 5` (for rollbacks)
- [ ] Readiness probe with appropriate thresholds

### During Deployment

- [ ] Monitor pod status transitions
- [ ] Watch for CrashLoopBackOff
- [ ] Check application logs for errors
- [ ] Verify metrics (latency, error rate)

### After Deployment

- [ ] All pods running and ready
- [ ] No increase in error rates
- [ ] Response times within SLA
- [ ] Smoke tests passing

---

## Blue-Green Checklist

### Infrastructure Setup

- [ ] Two identical environments prepared
- [ ] Active service pointing to blue
- [ ] Preview service pointing to green
- [ ] Sufficient resources for 2x capacity

### Deployment Process

- [ ] Green environment deployed
- [ ] Green pods healthy and ready
- [ ] Preview service traffic verified
- [ ] Smoke tests on preview passed
- [ ] Integration tests on preview passed

### Traffic Switch

- [ ] Monitoring alerts configured
- [ ] Rollback command prepared: `kubectl argo rollouts undo`
- [ ] Active service switched to green
- [ ] User traffic verified on new version
- [ ] Old (blue) pods scaled down after validation

### Post-Switch

- [ ] Error rates stable
- [ ] Latency within thresholds
- [ ] No customer complaints
- [ ] Blue environment terminated after scaleDownDelay

---

## Canary Checklist

### Pre-Canary

- [ ] Baseline metrics captured
- [ ] Analysis template configured
- [ ] Success/failure thresholds defined
- [ ] Traffic management configured (Istio/NGINX)

### Canary Steps

| Step | Traffic % | Duration | Validation |
|------|-----------|----------|------------|
| 1 | 5% | 5 min | Basic health |
| 2 | 25% | 10 min | Error rate < 1% |
| 3 | 50% | 15 min | Latency p99 < 500ms |
| 4 | 75% | 10 min | Full analysis |
| 5 | 100% | - | Promotion complete |

### During Canary

- [ ] Canary pods receiving traffic
- [ ] Analysis metrics being collected
- [ ] Error rate below threshold
- [ ] Latency within acceptable range
- [ ] No failed analysis runs

### Promotion/Rollback

- [ ] Manual promotion: `kubectl argo rollouts promote <name>`
- [ ] Abort if needed: `kubectl argo rollouts abort <name>`
- [ ] Verify full traffic on new version
- [ ] Old ReplicaSet scaled to zero

---

## Argo Rollouts Setup Checklist

### Installation

- [ ] Argo Rollouts controller installed
- [ ] CRDs applied to cluster
- [ ] kubectl-argo-rollouts plugin installed
- [ ] Dashboard accessible (optional)

### Integration

- [ ] Traffic management provider configured
  - [ ] Istio VirtualService
  - [ ] NGINX Ingress annotations
  - [ ] AWS ALB annotations
- [ ] Metrics provider configured
  - [ ] Prometheus
  - [ ] Datadog
  - [ ] New Relic

### Analysis Configuration

- [ ] AnalysisTemplate created
- [ ] Success condition defined
- [ ] Failure limit set
- [ ] Metric queries validated

---

## Rollback Checklist

### Immediate Actions

- [ ] Identify issue severity
- [ ] Notify team of rollback decision
- [ ] Execute rollback command

### Native Kubernetes Rollback

```bash
# Check rollout history
kubectl rollout history deployment/<name>

# Rollback to previous version
kubectl rollout undo deployment/<name>

# Rollback to specific revision
kubectl rollout undo deployment/<name> --to-revision=<N>
```

### Argo Rollouts Rollback

```bash
# Abort current rollout
kubectl argo rollouts abort <name>

# Undo to previous version
kubectl argo rollouts undo <name>

# Retry aborted rollout
kubectl argo rollouts retry <name>
```

### Post-Rollback

- [ ] Verify old version serving traffic
- [ ] Confirm error rates normalized
- [ ] Document incident
- [ ] Root cause analysis scheduled
- [ ] Fix deployed in next iteration

---

## Production Readiness Checklist

### Security

- [ ] Pods running as non-root
- [ ] Read-only root filesystem
- [ ] Capabilities dropped
- [ ] Network policies restricting traffic
- [ ] Secrets encrypted at rest

### Observability

- [ ] Prometheus metrics exposed
- [ ] Structured logging implemented
- [ ] Distributed tracing enabled
- [ ] Alerts configured for key metrics

### Resilience

- [ ] Pod anti-affinity configured
- [ ] Topology spread constraints set
- [ ] Pod Disruption Budget defined
- [ ] Graceful shutdown implemented

### Documentation

- [ ] Runbook for common issues
- [ ] Architecture diagram updated
- [ ] On-call rotation aware
- [ ] Escalation path defined
