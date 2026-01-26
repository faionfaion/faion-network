# Kubernetes Deployment LLM Prompts

**AI Prompts for Kubernetes Deployment Tasks**

---

## Deployment Generation

### Create Production Deployment

```
Create a production-ready Kubernetes Deployment for:

Context:
- Application: [NAME]
- Language/Framework: [Python/FastAPI, Node.js/Express, Go, etc.]
- Container image: [REGISTRY/IMAGE:TAG]
- Port: [PORT]
- Health endpoints: [/health/live, /health/ready]

Requirements:
1. Rolling update strategy (zero-downtime)
2. All three probes (startup, liveness, readiness)
3. Resource requests and limits
4. Security context (non-root, read-only filesystem)
5. Pod anti-affinity for HA
6. Topology spread across zones
7. ConfigMap and Secret references
8. Prometheus annotations

Environment variables needed:
- [LIST ENV VARS]

Secrets needed:
- [LIST SECRETS]

Output: Complete Deployment YAML with comments.
```

### Create Worker Deployment

```
Create a Kubernetes Deployment for a background worker:

Context:
- Application: [NAME]
- Queue system: [Celery/Sidekiq/Bull/etc.]
- Broker: [Redis/RabbitMQ]
- Container image: [IMAGE:TAG]

Requirements:
1. No HTTP ports (worker-only)
2. Exec-based health probe
3. Long termination grace period (for task completion)
4. Proper resource limits
5. Secret references for broker URL

Worker command: [COMMAND]

Output: Complete Deployment YAML.
```

### Migrate Deployment to Zero-Downtime

```
Convert this Deployment to zero-downtime rolling updates:

[PASTE EXISTING DEPLOYMENT]

Ensure:
1. maxUnavailable: 0
2. maxSurge: 1 (or appropriate)
3. minReadySeconds configured
4. All probes properly configured
5. PodDisruptionBudget created

Output:
- Updated Deployment
- PodDisruptionBudget
- Explanation of changes
```

---

## StatefulSet Generation

### Create StatefulSet for Database

```
Create a Kubernetes StatefulSet for:

Database: [PostgreSQL/MySQL/MongoDB/Redis Cluster]
Replicas: [NUMBER]
Storage size: [SIZE]
Storage class: [CLASS or default]

Requirements:
1. Headless Service
2. volumeClaimTemplates for persistent storage
3. Appropriate health probes
4. Pod anti-affinity (different nodes)
5. Ordered deployment (OrderedReady)
6. Graceful termination

Credentials via Secret: [SECRET NAME]

Output:
- Headless Service
- StatefulSet
- PodDisruptionBudget
```

### Convert Deployment to StatefulSet

```
Convert this Deployment to StatefulSet:

[PASTE DEPLOYMENT]

Reason for conversion: [WHY - e.g., need stable identity, persistent storage]

Requirements:
1. Create headless Service
2. Add volumeClaimTemplates
3. Configure serviceName
4. Set appropriate podManagementPolicy
5. Adjust termination grace period

Output:
- Headless Service
- StatefulSet
- Migration plan/notes
```

---

## Rolling Update Prompts

### Plan Rolling Update

```
Plan a rolling update for this deployment:

Current state:
[PASTE CURRENT DEPLOYMENT]

New version: [NEW IMAGE TAG]

Changes in new version:
- [LIST CHANGES]

Requirements:
1. Zero downtime
2. Ability to rollback quickly
3. Monitor specific metrics during rollout

Provide:
1. Update strategy recommendations
2. kubectl commands for update
3. Commands to monitor rollout
4. Rollback procedure
5. Key metrics to watch
```

### Debug Failed Rolling Update

```
Debug this failed rolling update:

Deployment: [NAME]
Namespace: [NAMESPACE]

kubectl rollout status output:
[PASTE OUTPUT]

kubectl describe deployment output:
[PASTE OUTPUT]

Pod events/logs:
[PASTE RELEVANT LOGS]

Provide:
1. Root cause analysis
2. Immediate fix
3. Rollback commands if needed
4. Prevention recommendations
```

### Optimize Rolling Update Speed

```
Optimize rolling update speed for this deployment:

[PASTE DEPLOYMENT]

Current rollout time: [TIME]
Target rollout time: [TARGET]
Risk tolerance: [Low/Medium/High]

Consider:
1. maxSurge/maxUnavailable tuning
2. minReadySeconds adjustment
3. Probe timing optimization
4. HPA interaction

Output:
- Optimized Deployment
- Expected improvement
- Risk assessment
```

---

## Canary Deployment Prompts

### Create Canary Setup

```
Create a canary deployment setup for:

Application: [NAME]
Current version: [VERSION]
Canary version: [NEW VERSION]
Traffic split: [INITIAL %] to canary

Infrastructure:
- Ingress controller: [nginx/traefik/etc.]
- Service mesh: [none/Istio/Linkerd]

Requirements:
1. Separate stable and canary deployments
2. Traffic splitting mechanism
3. Easy progression (10% -> 30% -> 50% -> 100%)
4. Quick rollback capability

Output:
- Stable Deployment
- Canary Deployment
- Services
- Ingress/Traffic routing config
- Commands for progression
```

### Create Argo Rollouts Canary

```
Create an Argo Rollouts canary configuration:

Application: [NAME]
Namespace: [NAMESPACE]
Container image: [IMAGE:TAG]

Canary strategy:
- Steps: 10% -> 30% -> 50% -> 80% -> 100%
- Pause between steps: [DURATION]
- Auto-promotion: [yes/no]

Analysis requirements:
- Success rate threshold: [%]
- Latency P99 threshold: [ms]
- Custom metrics: [LIST]

Prometheus endpoint: [URL]

Output:
- Rollout manifest
- AnalysisTemplate
- Services (stable and canary)
- Instructions
```

### Debug Canary Issues

```
Debug this canary deployment issue:

Setup:
[DESCRIBE SETUP - deployments, services, ingress]

Problem:
[DESCRIBE ISSUE - traffic not splitting, metrics wrong, etc.]

Relevant configs:
[PASTE CONFIGS]

Provide:
1. Diagnostic commands
2. Root cause analysis
3. Fix
4. Verification steps
```

---

## Health Probe Prompts

### Design Health Probes

```
Design health probes for this application:

Application type: [API/Worker/Database/etc.]
Framework: [FastAPI/Express/Spring/etc.]
Startup time: [APPROXIMATE]
Dependencies: [Database, Redis, external APIs, etc.]

Health endpoints available:
- [LIST ENDPOINTS AND WHAT THEY CHECK]

Requirements:
1. Startup probe (prevent premature traffic/restarts)
2. Liveness probe (detect hung processes)
3. Readiness probe (check dependencies)
4. Appropriate timing to avoid false positives

Output:
- Probe configurations
- Recommended endpoint implementations
- Timing justification
```

### Fix Probe Issues

```
Fix health probe issues for this deployment:

Problem: [DESCRIBE - pods restarting, not receiving traffic, etc.]

Current probes:
[PASTE PROBE CONFIG]

Pod logs:
[PASTE RELEVANT LOGS]

kubectl describe pod output:
[PASTE OUTPUT]

Provide:
1. Root cause
2. Fixed probe configuration
3. Timing recommendations
4. Testing approach
```

---

## Autoscaling Prompts

### Create HPA Configuration

```
Create an HPA configuration for:

Deployment: [NAME]
Current replicas: [NUMBER]

Scaling requirements:
- Min replicas: [NUMBER]
- Max replicas: [NUMBER]
- Scale up trigger: [CPU %, memory %, custom metric]
- Scale down behavior: [conservative/aggressive]

Traffic pattern:
- [DESCRIBE - steady, spiky, time-based]

Provide:
- HPA manifest (autoscaling/v2)
- Behavior configuration
- Recommendations for limits/requests
```

### Debug HPA Not Scaling

```
Debug why HPA is not scaling:

HPA status:
[kubectl get hpa OUTPUT]

HPA describe:
[kubectl describe hpa OUTPUT]

Current metrics:
[kubectl top pods OUTPUT]

Metrics server status:
[kubectl get pods -n kube-system | grep metrics-server]

Provide:
1. Diagnosis
2. Fix
3. Verification commands
```

---

## Security Prompts

### Security Audit Deployment

```
Perform a security audit on this Deployment:

[PASTE DEPLOYMENT]

Check for:
1. Running as root
2. Privileged containers
3. Excessive capabilities
4. Missing security context
5. Secrets in environment (vs secretKeyRef)
6. Missing network policies
7. Missing resource limits

Compliance: [CIS Benchmark / Pod Security Standards]

Output:
- Risk assessment
- Issues found with severity
- Hardened Deployment
- NetworkPolicy recommendation
```

### Create NetworkPolicy

```
Create NetworkPolicies for this application:

Architecture:
- Frontend: [DEPLOYMENT NAME]
- API: [DEPLOYMENT NAME]
- Workers: [DEPLOYMENT NAME]
- Database: [STATEFULSET NAME]
- Cache: [DEPLOYMENT NAME]

Traffic flow:
- Internet -> Frontend (ports 80, 443)
- Frontend -> API (port 8000)
- API -> Database (port 5432)
- API -> Cache (port 6379)
- Workers -> Database (port 5432)
- Workers -> Cache (port 6379)

Namespace: [NAMESPACE]
Ingress namespace: [INGRESS NAMESPACE]

Output: NetworkPolicies for each component with default deny.
```

### Apply Pod Security Standards

```
Update this namespace and deployments for Pod Security Standards:

Current namespace:
[PASTE NAMESPACE YAML]

Deployments:
[PASTE DEPLOYMENTS]

Target PSS level: [baseline/restricted]

Provide:
1. Updated namespace with PSS labels
2. Updated deployments to comply
3. List of changes required
4. Potential issues/exceptions
```

---

## Troubleshooting Prompts

### Debug Deployment Issues

```
Debug deployment issues:

Deployment: [NAME]
Namespace: [NAMESPACE]

Symptoms:
[DESCRIBE - pods not starting, crashlooping, etc.]

kubectl get pods output:
[PASTE OUTPUT]

kubectl describe pod output:
[PASTE OUTPUT]

Pod logs:
[PASTE LOGS]

Events:
[PASTE EVENTS]

Provide:
1. Root cause analysis
2. Immediate fix
3. Long-term prevention
```

### Debug Service Connectivity

```
Debug service connectivity issue:

Problem: [Pod A cannot reach Service B]

Service:
[PASTE SERVICE YAML]

Deployment behind service:
[PASTE DEPLOYMENT]

Test pod configuration:
[PASTE TEST POD OR DESCRIBE SOURCE]

Commands already tried:
[LIST COMMANDS AND RESULTS]

Provide:
1. Additional diagnostic commands
2. Likely root cause
3. Fix
4. Verification steps
```

### Debug Resource Issues

```
Debug resource issues for this deployment:

Symptoms:
[DESCRIBE - OOMKilled, CPU throttling, pending pods]

Current resource config:
[PASTE RESOURCES SECTION]

kubectl top pods output:
[PASTE OUTPUT]

Node resources:
[kubectl describe node OUTPUT]

Provide:
1. Analysis of resource usage
2. Recommended resource adjustments
3. HPA recommendations if applicable
4. Node scaling recommendations if applicable
```

---

## Migration Prompts

### Migrate from Docker Compose

```
Migrate this Docker Compose setup to Kubernetes:

[PASTE DOCKER COMPOSE]

Target environment:
- Kubernetes version: [VERSION]
- Ingress controller: [nginx/traefik]
- Storage class: [CLASS]
- Registry: [REGISTRY URL]

Requirements:
1. Production-ready manifests
2. ConfigMaps and Secrets separated
3. Persistent storage for stateful services
4. Health checks
5. Resource limits

Output:
- All Kubernetes manifests
- Kustomize structure (optional)
- Migration checklist
- Notes on differences
```

### Migrate to GitOps

```
Convert these Kubernetes manifests for GitOps:

Current manifests:
[PASTE OR DESCRIBE]

GitOps tool: [Argo CD / Flux]
Git repository structure: [monorepo / separate repos]
Environments: [dev, staging, production]

Requirements:
1. Kustomize overlays per environment
2. Image automation
3. Secrets management approach
4. Sync policies

Output:
- Directory structure
- Kustomization files
- GitOps configuration
- Workflow recommendations
```

---

## Quick Task Prompts

### Generate PodDisruptionBudget

```
Generate a PodDisruptionBudget for:

Deployment: [NAME]
Replicas: [NUMBER]
Availability requirement: [e.g., always at least 2 pods]

Output: PDB manifest with explanation.
```

### Generate Resource Recommendations

```
Recommend resources for this workload:

Application type: [API/Worker/DB/Cache]
Expected traffic: [REQUESTS/SEC or CONCURRENT USERS]
Memory footprint: [OBSERVED or ESTIMATED]
CPU profile: [CPU-bound/IO-bound/mixed]

Output:
- requests and limits
- Justification
- HPA thresholds if applicable
```

### Create Rollback Runbook

```
Create a rollback runbook for:

Application: [NAME]
Deployment type: [Deployment/StatefulSet/Argo Rollout]
Environment: [NAMESPACE]

Include:
1. Pre-rollback checks
2. Rollback commands
3. Verification steps
4. Communication template
5. Post-rollback actions
```

---

## Prompt Variables Reference

| Variable | Description |
|----------|-------------|
| `[NAME]` | Application/resource name |
| `[NAMESPACE]` | Kubernetes namespace |
| `[VERSION]` | Image version/tag |
| `[REGISTRY]` | Container registry URL |
| `[PORT]` | Container port |
| `[REPLICAS]` | Number of replicas |
| `[SIZE]` | Storage size (e.g., 50Gi) |
| `[CLASS]` | StorageClass name |
| `[DURATION]` | Time duration (e.g., 5m, 1h) |
| `[%]` | Percentage value |

---

*Kubernetes Deployment LLM Prompts | faion-infrastructure-engineer*
