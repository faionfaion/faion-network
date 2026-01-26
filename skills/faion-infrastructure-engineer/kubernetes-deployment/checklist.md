# Kubernetes Deployment Checklists

**Production Readiness, Rolling Updates, Canary Deployments (2025-2026)**

---

## Deployment Checklist

### Resource Configuration

- [ ] `replicas` set appropriately (minimum 2 for HA)
- [ ] `revisionHistoryLimit` set (default: 10, recommended: 5)
- [ ] Resource `requests` defined for CPU and memory
- [ ] Resource `limits` defined for CPU and memory
- [ ] Container image uses specific tag (no `latest`)
- [ ] Image tag includes SHA or digest for immutability

### Rolling Update Strategy

- [ ] `strategy.type: RollingUpdate` configured
- [ ] `maxUnavailable` set (0 for zero-downtime)
- [ ] `maxSurge` set (1 or 25% typical)
- [ ] `minReadySeconds` configured (10-30s recommended)
- [ ] PodDisruptionBudget defined

### Health Probes

- [ ] Startup probe configured (for slow-starting apps)
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Probe endpoints return appropriate status codes
- [ ] `initialDelaySeconds` appropriate for app startup
- [ ] `periodSeconds` balanced (not too frequent)
- [ ] `failureThreshold` allows for transient failures

### Pod Configuration

- [ ] Labels follow kubernetes.io/name convention
- [ ] Annotations for Prometheus metrics (if applicable)
- [ ] `serviceAccountName` specified (not default)
- [ ] `securityContext.runAsNonRoot: true`
- [ ] `securityContext.readOnlyRootFilesystem: true`
- [ ] `securityContext.allowPrivilegeEscalation: false`
- [ ] Capabilities dropped (`drop: ALL`)

### Scheduling

- [ ] `podAntiAffinity` configured for HA
- [ ] `topologySpreadConstraints` for zone distribution
- [ ] `nodeSelector` or `nodeAffinity` if needed
- [ ] `tolerations` for tainted nodes (if applicable)

### Networking

- [ ] Service created with correct selector
- [ ] Service type appropriate (ClusterIP, LoadBalancer)
- [ ] Container ports named and documented
- [ ] NetworkPolicy defined (default deny recommended)

---

## StatefulSet Checklist

### Identity and Storage

- [ ] Headless Service created (`clusterIP: None`)
- [ ] `serviceName` matches headless service
- [ ] `volumeClaimTemplates` defined for persistent storage
- [ ] StorageClass specified (or default suitable)
- [ ] Storage size adequate with growth buffer

### Update Strategy

- [ ] `updateStrategy.type: RollingUpdate` (default)
- [ ] `updateStrategy.rollingUpdate.partition` for staged rollout
- [ ] `podManagementPolicy` appropriate (OrderedReady or Parallel)

### Pod Configuration

- [ ] `terminationGracePeriodSeconds` adequate (30-60s minimum for DBs)
- [ ] Init containers for setup if needed
- [ ] Ordered startup handled correctly
- [ ] DNS resolution tested (`<pod>.<service>.<ns>.svc.cluster.local`)

### Data Protection

- [ ] VolumeSnapshot capability enabled
- [ ] Backup strategy defined
- [ ] Restore procedure documented and tested
- [ ] PodDisruptionBudget set (minAvailable: 1 minimum)

---

## Rolling Update Checklist

### Pre-Update

- [ ] Current deployment healthy (all pods ready)
- [ ] PodDisruptionBudget configured
- [ ] HPA behavior understood (disable during update if needed)
- [ ] New image tested in staging
- [ ] Rollback plan documented
- [ ] Alert thresholds reviewed

### Update Configuration

- [ ] Zero-downtime settings (`maxUnavailable: 0`)
- [ ] Surge capacity available (`maxSurge: 1` or more)
- [ ] `minReadySeconds` set to catch early failures
- [ ] Readiness probe validates new version works

### During Update

- [ ] Monitor rollout status: `kubectl rollout status`
- [ ] Watch pod transitions: `kubectl get pods -w`
- [ ] Check error logs: `kubectl logs -f deployment/<name>`
- [ ] Verify metrics in monitoring system
- [ ] Test application functionality incrementally

### Post-Update

- [ ] All pods in Running state
- [ ] All pods pass readiness checks
- [ ] Application metrics normal
- [ ] Error rates within threshold
- [ ] Old ReplicaSet scaled to 0
- [ ] Document version in changelog

### Rollback Procedure

```bash
# Check rollout history
kubectl rollout history deployment/<name>

# Rollback to previous version
kubectl rollout undo deployment/<name>

# Rollback to specific revision
kubectl rollout undo deployment/<name> --to-revision=<N>

# Monitor rollback
kubectl rollout status deployment/<name>
```

---

## Canary Deployment Checklist

### Pre-Canary Setup

- [ ] Baseline deployment stable (production)
- [ ] Canary deployment manifest prepared
- [ ] Traffic splitting mechanism chosen:
  - [ ] Ingress annotations (nginx, traefik)
  - [ ] Service mesh (Istio, Linkerd)
  - [ ] Argo Rollouts / Flagger
- [ ] Metrics for analysis defined (latency, error rate, custom)
- [ ] Success criteria documented
- [ ] Rollback triggers defined

### Canary Configuration

- [ ] Separate Deployment for canary version
- [ ] Same labels except version identifier
- [ ] Same Service selector matches both versions
- [ ] Initial traffic weight (5-10% recommended)
- [ ] Promotion schedule defined (10% -> 30% -> 50% -> 100%)

### Analysis Metrics (2025-2026)

| Metric | Threshold | Source |
|--------|-----------|--------|
| Error rate | < baseline + 1% | Prometheus |
| P99 latency | < baseline + 10% | Prometheus |
| Success rate | > 99% | Prometheus |
| Custom business metric | Define per app | Application |

### Canary Progression

- [ ] Stage 1: 5-10% traffic, 5-10 min analysis
- [ ] Stage 2: 25-30% traffic, 10-15 min analysis
- [ ] Stage 3: 50% traffic, 15-30 min analysis
- [ ] Stage 4: 100% promotion (or rollback)

### Post-Canary

- [ ] Old deployment scaled down
- [ ] Canary promoted to stable
- [ ] Metrics documented
- [ ] Lessons learned recorded

---

## Argo Rollouts Checklist (2025-2026)

### Setup

- [ ] Argo Rollouts controller installed
- [ ] AnalysisTemplate defined
- [ ] Prometheus/Datadog integration configured
- [ ] Ingress/Service mesh configured for traffic

### Rollout Configuration

- [ ] Strategy: canary or blueGreen
- [ ] Steps defined with weight and pauses
- [ ] Analysis at each step
- [ ] Anti-affinity for stable/canary

### Analysis Template

- [ ] Metrics provider configured
- [ ] Query returns success/failure correctly
- [ ] successCondition defined
- [ ] failureLimit appropriate
- [ ] interval and count balanced

### Monitoring

- [ ] Argo Rollouts dashboard accessible
- [ ] `kubectl argo rollouts get rollout <name> -w`
- [ ] Alerts on rollout failures
- [ ] Slack/Teams notifications configured

---

## PodDisruptionBudget Checklist

### Configuration

- [ ] PDB created for every production Deployment/StatefulSet
- [ ] `minAvailable` OR `maxUnavailable` set (not both)
- [ ] Selector matches target pods
- [ ] Value allows for rolling updates

### Guidelines

| Replicas | minAvailable | maxUnavailable | Notes |
|----------|--------------|----------------|-------|
| 2 | 1 | 1 | Minimum HA |
| 3 | 2 | 1 | Standard HA |
| 5+ | N-1 or 80% | 1 or 20% | Large deployments |

### Verification

```bash
# Check PDB status
kubectl get pdb

# Describe PDB
kubectl describe pdb <name>

# Verify during drain
kubectl drain <node> --dry-run
```

---

## HorizontalPodAutoscaler Checklist

### Configuration

- [ ] `minReplicas` set (>= 2 for HA)
- [ ] `maxReplicas` set with cluster capacity in mind
- [ ] Target metrics defined (CPU, memory, custom)
- [ ] `scaleTargetRef` points to correct Deployment

### Behavior (2025-2026)

- [ ] `behavior.scaleDown.stabilizationWindowSeconds` set (300s default)
- [ ] `behavior.scaleUp.stabilizationWindowSeconds` set (0 for fast scale-up)
- [ ] Scale-down policies prevent aggressive reduction
- [ ] Scale-up policies allow rapid response

### Metrics

| Metric Type | Use Case | Configuration |
|-------------|----------|---------------|
| CPU | General compute | 70% utilization target |
| Memory | Memory-bound apps | 80% utilization target |
| Custom | Request rate, queue depth | Application-specific |
| External | Cloud metrics | Datadog, CloudWatch |

### Verification

```bash
# Check HPA status
kubectl get hpa

# Describe HPA with events
kubectl describe hpa <name>

# Check current metrics
kubectl top pods -l app=<name>
```

---

## Security Checklist (2025-2026)

### Pod Security Standards

- [ ] Namespace labeled with PSS level:
  - [ ] `pod-security.kubernetes.io/enforce: restricted`
  - [ ] `pod-security.kubernetes.io/warn: restricted`
  - [ ] `pod-security.kubernetes.io/audit: restricted`

### Container Security

- [ ] `runAsNonRoot: true`
- [ ] `runAsUser` specified (UID 1000+)
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] `capabilities.drop: ["ALL"]`
- [ ] Only necessary capabilities added

### Service Account

- [ ] Dedicated ServiceAccount (not default)
- [ ] `automountServiceAccountToken: false` if not needed
- [ ] RBAC Role/RoleBinding with minimal permissions

### Secrets Management

- [ ] Secrets not hardcoded in manifests
- [ ] External secrets operator or vault used
- [ ] Secrets rotated regularly
- [ ] Environment variables from secretKeyRef

### Network Security

- [ ] NetworkPolicy denies all by default
- [ ] Explicit ingress rules for required traffic
- [ ] Explicit egress rules (DNS, required services)
- [ ] mTLS enabled (service mesh)

---

## Pre-Production Checklist

### Configuration Validation

- [ ] `kubectl apply --dry-run=server` passes
- [ ] Kyverno/OPA policies pass
- [ ] Polaris audit passes with score > 80%
- [ ] YAML linted (kubeconform, kubeval)

### Resource Verification

- [ ] Namespace exists
- [ ] ConfigMaps created
- [ ] Secrets created (via proper channel)
- [ ] PersistentVolumeClaims bound
- [ ] ServiceAccount exists

### Testing

- [ ] Application starts correctly in staging
- [ ] Health probes respond correctly
- [ ] Integration tests pass
- [ ] Load test completed
- [ ] Chaos engineering tests pass (optional)

### Monitoring

- [ ] Metrics endpoint exposed
- [ ] ServiceMonitor/PodMonitor created
- [ ] Dashboards configured
- [ ] Alerts defined
- [ ] Runbooks documented

---

## Rollback Checklist

### When to Rollback

- [ ] Error rate exceeds threshold (>1% increase)
- [ ] Latency exceeds threshold (>10% P99 increase)
- [ ] Crash loop detected
- [ ] Critical functionality broken
- [ ] Security vulnerability discovered

### Rollback Procedure

```bash
# 1. Check current status
kubectl rollout status deployment/<name>

# 2. View revision history
kubectl rollout history deployment/<name>

# 3. Execute rollback
kubectl rollout undo deployment/<name>

# 4. Monitor rollback
kubectl rollout status deployment/<name>

# 5. Verify pods
kubectl get pods -l app=<name>

# 6. Test application
curl https://app.example.com/health
```

### Post-Rollback

- [ ] Incident documented
- [ ] Root cause analysis started
- [ ] Stakeholders notified
- [ ] Fix branch created
- [ ] Additional tests added

---

## Quick Verification Commands

```bash
# Deployment status
kubectl get deployment <name> -o wide
kubectl describe deployment <name>

# Pod status
kubectl get pods -l app=<name> -o wide
kubectl describe pod <pod-name>

# Rollout status
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>

# Resource usage
kubectl top pods -l app=<name>

# Logs
kubectl logs -l app=<name> --tail=100
kubectl logs -l app=<name> -f

# Events
kubectl get events --sort-by='.lastTimestamp' | grep <name>

# HPA status
kubectl get hpa <name>
kubectl describe hpa <name>

# PDB status
kubectl get pdb
kubectl describe pdb <name>

# Network policy
kubectl get networkpolicy -n <namespace>

# Service endpoints
kubectl get endpoints <service-name>
```

---

*Kubernetes Deployment Checklists | faion-infrastructure-engineer*
