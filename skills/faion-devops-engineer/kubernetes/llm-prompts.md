# Kubernetes LLM Prompts

Effective prompts for Kubernetes tasks with LLMs.

---

## Deployment Prompts

### Create Production Deployment

```
Create a production-ready Kubernetes Deployment for [APP_NAME] with:
- Image: [IMAGE:TAG]
- Port: [PORT]
- Replicas: [N]
- Environment: [production/staging]

Requirements:
1. Security context (non-root, read-only filesystem, drop capabilities)
2. Resource requests and limits
3. Liveness, readiness, and startup probes
4. Pod anti-affinity for HA
5. ConfigMap for configuration
6. Secret references for sensitive data
```

### Review Deployment Manifest

```
Review this Kubernetes Deployment manifest for production readiness:

[PASTE MANIFEST]

Check for:
1. Security best practices (securityContext, non-root, capabilities)
2. Resource management (requests, limits, QoS class)
3. Health probes (liveness, readiness, startup)
4. High availability (replicas, anti-affinity, PDB)
5. Image security (specific tags, pull policy)

Provide specific recommendations with YAML snippets.
```

### Convert Docker Compose to Kubernetes

```
Convert this Docker Compose file to production Kubernetes manifests:

[PASTE DOCKER-COMPOSE.YAML]

Generate:
1. Deployments for each service
2. Services (ClusterIP/LoadBalancer as appropriate)
3. ConfigMaps for environment variables
4. PersistentVolumeClaims for volumes
5. NetworkPolicy for service communication

Follow 2025 best practices for security and resource management.
```

---

## Scaling Prompts

### Design HPA Strategy

```
Design an HPA strategy for [APP_NAME] with these characteristics:
- Traffic pattern: [steady/bursty/scheduled]
- Current replicas: [N]
- Peak load: [description]
- Response time SLA: [ms]

Provide:
1. HPA manifest with appropriate metrics
2. Scale-up/scale-down behavior
3. VPA recommendation (if applicable)
4. Monitoring queries to track scaling
```

### Optimize Resource Allocation

```
Analyze these Kubernetes resource metrics and recommend optimizations:

Current configuration:
- CPU request: [value], limit: [value]
- Memory request: [value], limit: [value]

Observed metrics (last 7 days):
- CPU P50: [value], P95: [value], P99: [value]
- Memory P50: [value], P95: [value], max: [value]
- Throttling percentage: [value]
- OOMKilled events: [count]

Provide:
1. Recommended resource settings
2. QoS class implications
3. HPA/VPA configuration if applicable
```

### Capacity Planning

```
Help me plan Kubernetes cluster capacity for:
- Application workloads: [list with resource requirements]
- Expected growth: [percentage per quarter]
- HA requirements: [N zones, N nodes per zone]
- Budget constraints: [if any]

Calculate:
1. Minimum node configuration
2. Recommended node pools (with instance types)
3. Autoscaler configuration
4. Cost estimate
```

---

## Security Prompts

### Security Audit

```
Perform a security audit on this Kubernetes namespace configuration:

[PASTE MANIFESTS]

Check against:
1. Pod Security Standards (restricted level)
2. Network policies (default deny, explicit allow)
3. RBAC (least privilege)
4. Secret management
5. Image security

Provide severity levels and remediation steps.
```

### Create NetworkPolicy

```
Create NetworkPolicies for this application architecture:

Services:
- frontend (receives external traffic via ingress)
- backend-api (called by frontend)
- worker (processes jobs from backend-api)
- postgres (database, called by backend-api and worker)
- redis (cache, called by backend-api)

Requirements:
1. Default deny all traffic
2. Allow only necessary communication paths
3. Allow DNS resolution
4. Document each policy purpose
```

### RBAC Configuration

```
Design RBAC configuration for these personas:
- Developers: [access requirements]
- SRE team: [access requirements]
- CI/CD service account: [access requirements]

Namespace: [NAMESPACE]

Generate:
1. ServiceAccounts
2. Roles with minimum necessary permissions
3. RoleBindings
4. Audit recommendations
```

---

## Troubleshooting Prompts

### Debug Pod Issues

```
Help me debug this Kubernetes pod issue:

Symptoms:
- Pod status: [status]
- Restarts: [count]
- Age: [duration]

kubectl describe output:
[PASTE OUTPUT]

kubectl logs output:
[PASTE OUTPUT]

Events:
[PASTE EVENTS]

Identify the root cause and provide resolution steps.
```

### Diagnose Performance

```
Diagnose performance issues in my Kubernetes deployment:

Symptoms:
- Response time increased from [X]ms to [Y]ms
- Error rate: [percentage]
- Affected services: [list]

Current metrics:
- CPU utilization: [value]
- Memory utilization: [value]
- Network latency: [value]
- Pod count: [value]

Recent changes:
[list any recent deployments or config changes]

Provide diagnostic steps and potential causes.
```

### Network Troubleshooting

```
Help me troubleshoot network connectivity in Kubernetes:

Issue: Service A cannot reach Service B

Environment:
- Both in namespace: [NAMESPACE]
- Service A selector: [labels]
- Service B selector: [labels]
- Service B port: [port]

What I've tried:
[list attempts]

NetworkPolicies:
[PASTE POLICIES]

Provide step-by-step diagnostic commands and analysis.
```

---

## Migration Prompts

### Migrate to Kubernetes

```
Create a migration plan from [current infrastructure] to Kubernetes:

Current setup:
- [describe VMs/services/databases]
- Traffic: [patterns]
- Dependencies: [external services]

Requirements:
1. Zero-downtime migration
2. Rollback capability
3. [other requirements]

Provide:
1. Phase-by-phase migration plan
2. Kubernetes manifests for each service
3. Traffic cutover strategy
4. Verification checklist
```

### Upgrade Kubernetes Version

```
Create an upgrade plan from Kubernetes [CURRENT_VERSION] to [TARGET_VERSION]:

Cluster:
- Provider: [EKS/GKE/AKS/self-managed]
- Node count: [N]
- Critical workloads: [list]

Provide:
1. Pre-upgrade checklist
2. API deprecation analysis
3. Upgrade procedure (control plane, nodes)
4. Rollback plan
5. Post-upgrade validation
```

---

## GitOps Prompts

### ArgoCD Application

```
Create ArgoCD Application manifests for:

Repository: [GIT_URL]
Path: [MANIFEST_PATH]
Target cluster: [CLUSTER]
Target namespace: [NAMESPACE]

Requirements:
1. Automated sync with pruning
2. Health checks
3. Sync waves for dependencies
4. Notification on sync failure
```

### Kustomize Structure

```
Design a Kustomize structure for deploying [APP_NAME] to multiple environments:

Environments:
- dev (namespace: dev, replicas: 1, debug logging)
- staging (namespace: staging, replicas: 2, real database)
- production (namespace: prod, replicas: 3, HA, monitoring)

Generate:
1. Base manifests
2. Overlays for each environment
3. kustomization.yaml files
4. Usage instructions
```

---

## Cost Optimization Prompts

### Analyze Costs

```
Analyze Kubernetes costs and recommend optimizations:

Current state:
- Nodes: [count, instance types]
- Total CPU allocated: [value]
- Total memory allocated: [value]
- CPU utilization: [percentage]
- Memory utilization: [percentage]
- Monthly cost: [estimate]

Workload patterns:
- [describe peak/off-peak patterns]

Provide:
1. Right-sizing recommendations
2. Spot/preemptible instance opportunities
3. Bin packing improvements
4. Reserved instance recommendations
5. Estimated savings
```

### Resource Right-Sizing

```
Analyze these workloads and recommend right-sizing:

[LIST DEPLOYMENTS WITH:]
- Name
- Current replicas
- CPU request/limit
- Memory request/limit
- Actual CPU usage (avg, P95)
- Actual memory usage (avg, max)

Provide:
1. Recommended resource settings for each
2. Expected QoS class
3. Risk assessment
4. Implementation priority
```

---

## Prompt Engineering Tips

### Context Setting

```
You are a Kubernetes expert helping with [TASK_TYPE].
Environment: [PROVIDER] Kubernetes [VERSION]
Constraints: [list any constraints]
Output format: [YAML/step-by-step/analysis]
```

### Request Validation

```
Before implementing, validate this Kubernetes configuration:

[PASTE CONFIG]

Check:
1. Syntax correctness
2. Best practice compliance
3. Security implications
4. Resource requirements
5. Dependencies

Return validation result and any corrections needed.
```

### Iterative Refinement

```
Current Kubernetes manifest:
[PASTE CURRENT]

Issues/requirements not met:
1. [issue 1]
2. [issue 2]

Update the manifest to address these issues while maintaining:
- [constraint 1]
- [constraint 2]
```

---

## Quick Reference

| Task | Key Prompt Elements |
|------|---------------------|
| Create resources | App name, image, ports, replicas, environment |
| Review/audit | Paste manifest, specify check criteria |
| Troubleshoot | Symptoms, describe output, logs, events |
| Optimize | Current metrics, target metrics, constraints |
| Migrate | Current state, target state, requirements |
| Scale | Traffic patterns, SLAs, current config |
| Secure | Namespace, services, communication paths |

---

## Sources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [14 Kubernetes Best Practices 2025](https://komodor.com/learn/14-kubernetes-best-practices-you-must-know-in-2025/)
- [Kubernetes Best Practices: Optimize, Secure, Scale](https://kodekloud.com/blog/kubernetes-best-practices-2025/)
