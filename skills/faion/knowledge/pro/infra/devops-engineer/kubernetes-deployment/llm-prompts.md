# LLM Prompts for Kubernetes Deployments

## Strategy Selection

### Choose Deployment Strategy

```
I need to deploy a [TYPE] application with the following requirements:
- Traffic: [REQUESTS_PER_SECOND] RPS
- Availability SLA: [PERCENTAGE]%
- Rollback requirement: [INSTANT/GRADUAL/ACCEPTABLE_DOWNTIME]
- Team experience: [BEGINNER/INTERMEDIATE/ADVANCED]
- Existing tools: [K8S_NATIVE/ARGO_ROLLOUTS/SERVICE_MESH]

Recommend the most appropriate deployment strategy and explain why.
Consider: rolling update, blue-green, canary, or recreate.
```

### Migration from Rolling to Canary

```
We currently use native Kubernetes rolling updates for our [APP_NAME] application.
Current setup:
- Replicas: [NUMBER]
- maxUnavailable: [VALUE]
- maxSurge: [VALUE]
- No automated analysis

We want to migrate to Argo Rollouts canary deployments.

Create a migration plan that:
1. Minimizes risk during transition
2. Preserves existing monitoring
3. Introduces gradual traffic shifting
4. Adds Prometheus-based analysis

Provide the complete Rollout YAML configuration.
```

---

## Configuration Generation

### Generate Rolling Update Deployment

```
Create a Kubernetes Deployment manifest for:
- App name: [APP_NAME]
- Namespace: [NAMESPACE]
- Image: [REGISTRY]/[IMAGE]:[TAG]
- Port: [PORT]
- Replicas: [NUMBER]
- Resource requests: CPU [VALUE], Memory [VALUE]
- Resource limits: CPU [VALUE], Memory [VALUE]
- Health check endpoint: [PATH]

Requirements:
- Zero-downtime rolling updates
- Pod anti-affinity for HA
- Security best practices (non-root, read-only filesystem)
- Prometheus metrics annotations

Include: Deployment, Service, HPA, PDB
```

### Generate Blue-Green Rollout

```
Create an Argo Rollouts Blue-Green deployment for:
- App name: [APP_NAME]
- Namespace: [NAMESPACE]
- Image: [REGISTRY]/[IMAGE]:[TAG]
- Active service: [SERVICE_NAME]-active
- Preview service: [SERVICE_NAME]-preview

Requirements:
- Manual promotion (autoPromotionEnabled: false)
- 30 second scale down delay
- Pre-promotion smoke test analysis
- Post-promotion success rate analysis

Include: Rollout, Services, AnalysisTemplates
```

### Generate Canary Rollout with Istio

```
Create an Argo Rollouts Canary deployment with Istio traffic management:
- App name: [APP_NAME]
- Namespace: [NAMESPACE]
- Image: [REGISTRY]/[IMAGE]:[TAG]
- Host: [DOMAIN]

Canary steps:
1. 5% traffic for 2 minutes
2. 10% traffic for 5 minutes (start analysis)
3. 25% traffic for 10 minutes
4. 50% traffic for 10 minutes
5. 75% traffic for 5 minutes
6. 100% promotion

Analysis requirements:
- Success rate >= 99%
- P99 latency < 500ms
- Error count < 10 per 5 minutes

Include: Rollout, Services, VirtualService, AnalysisTemplate
```

---

## Troubleshooting

### Diagnose Failed Rollout

```
My Argo Rollouts canary deployment is stuck. Here's the status:

```
kubectl argo rollouts get rollout [NAME] -n [NAMESPACE]
[PASTE_OUTPUT]
```

Analysis run status:
```
kubectl get analysisrun -n [NAMESPACE]
[PASTE_OUTPUT]
```

Recent events:
```
kubectl get events -n [NAMESPACE] --sort-by='.lastTimestamp'
[PASTE_OUTPUT]
```

Diagnose the issue and provide:
1. Root cause
2. Immediate fix
3. Prevention measures
```

### Debug Pod Health Check Failures

```
Pods are failing readiness checks after deployment:

Pod status:
```
kubectl describe pod [POD_NAME] -n [NAMESPACE]
[PASTE_OUTPUT]
```

Pod logs:
```
kubectl logs [POD_NAME] -n [NAMESPACE]
[PASTE_OUTPUT]
```

Current probe configuration:
```yaml
[PASTE_PROBE_CONFIG]
```

Analyze the issue and suggest:
1. Root cause
2. Probe configuration fixes
3. Application-side fixes if needed
```

### Rollback Investigation

```
We had to rollback deployment of [APP_NAME] due to increased errors.

Before rollback metrics:
- Error rate: [VALUE]%
- P99 latency: [VALUE]ms
- Affected endpoints: [LIST]

After rollback metrics:
- Error rate: [VALUE]%
- P99 latency: [VALUE]ms

Deployment diff:
```
kubectl diff -f new-deployment.yaml
[PASTE_OUTPUT]
```

Help me:
1. Identify what caused the regression
2. Create an analysis template to catch this in future
3. Suggest safe testing approach before re-deployment
```

---

## Analysis Templates

### Create Custom Analysis Template

```
Create a Prometheus AnalysisTemplate for:
- Metric: [METRIC_NAME]
- Query type: [COUNTER/GAUGE/HISTOGRAM]
- Success condition: [THRESHOLD_DESCRIPTION]
- Failure limit: [NUMBER]
- Check interval: [DURATION]

Additional requirements:
- [CUSTOM_REQUIREMENT_1]
- [CUSTOM_REQUIREMENT_2]

Prometheus endpoint: [URL]
Service label: [LABEL_NAME]
```

### Multi-Metric Analysis

```
Create a comprehensive AnalysisTemplate that checks:
1. Success rate (HTTP 2xx / total) >= [THRESHOLD]%
2. Error rate (HTTP 5xx / total) < [THRESHOLD]%
3. P95 latency < [VALUE]ms
4. P99 latency < [VALUE]ms
5. Request throughput within [MIN]-[MAX] RPS

All metrics should use [PROMETHEUS/DATADOG/NEWRELIC].
Failure on any metric should abort the rollout.
```

---

## Optimization

### Resource Right-Sizing

```
Analyze these resource metrics for [APP_NAME]:

CPU usage over 7 days:
- P50: [VALUE]
- P95: [VALUE]
- P99: [VALUE]
- Max: [VALUE]

Memory usage over 7 days:
- P50: [VALUE]
- P95: [VALUE]
- P99: [VALUE]
- Max: [VALUE]

Current configuration:
- Requests: CPU [VALUE], Memory [VALUE]
- Limits: CPU [VALUE], Memory [VALUE]

Recommend optimal resource configuration considering:
- Cost efficiency
- Burst handling
- OOM prevention
- CPU throttling prevention
```

### HPA Tuning

```
Current HPA configuration:
```yaml
[PASTE_HPA_CONFIG]
```

Observed behavior:
- Scale-up events: [DESCRIPTION]
- Scale-down events: [DESCRIPTION]
- Traffic pattern: [STEADY/SPIKY/GRADUAL]
- Current issues: [DESCRIPTION]

Recommend HPA tuning for:
1. Faster response to traffic spikes
2. Gradual scale-down to prevent thrashing
3. Custom metrics if needed
```

---

## Migration Scenarios

### Migrate from Helm to Argo Rollouts

```
Current Helm deployment template:
```yaml
[PASTE_HELM_TEMPLATE]
```

Current values.yaml:
```yaml
[PASTE_VALUES]
```

Convert to Argo Rollouts with:
- Strategy: [BLUE_GREEN/CANARY]
- Traffic management: [ISTIO/NGINX/NONE]
- Analysis integration: [YES/NO]

Maintain compatibility with existing:
- ConfigMaps
- Secrets
- Services
- Ingress
```

### Migrate from Docker Compose to Kubernetes

```
Docker Compose file:
```yaml
[PASTE_DOCKER_COMPOSE]
```

Convert to Kubernetes manifests with:
- Namespace: [NAME]
- Deployment strategy: [STRATEGY]
- Ingress controller: [NGINX/TRAEFIK]
- SSL: [CERT_MANAGER/MANUAL]

Include all necessary resources:
- Deployments
- Services
- ConfigMaps
- Secrets (placeholder values)
- PVC if needed
- Ingress
- NetworkPolicies
```

---

## Best Practices Review

### Review Deployment Configuration

```
Review this Kubernetes Deployment for production readiness:

```yaml
[PASTE_DEPLOYMENT_YAML]
```

Check for:
1. Security best practices
2. Resource configuration
3. Health check configuration
4. High availability setup
5. Observability
6. Rolling update configuration

Provide:
- Issues found (critical/warning/info)
- Recommended fixes
- Improved YAML configuration
```

### Review Argo Rollouts Configuration

```
Review this Argo Rollouts configuration:

```yaml
[PASTE_ROLLOUT_YAML]
```

AnalysisTemplate:
```yaml
[PASTE_ANALYSIS_TEMPLATE]
```

Evaluate:
1. Step progression (traffic percentages, durations)
2. Analysis coverage and thresholds
3. Rollback conditions
4. Resource efficiency
5. Integration with traffic management

Provide recommendations for improvement.
```

---

## Emergency Procedures

### Emergency Rollback Procedure

```
Generate an emergency rollback procedure for:
- Application: [APP_NAME]
- Namespace: [NAMESPACE]
- Deployment type: [NATIVE_K8S/ARGO_ROLLOUTS]
- Traffic management: [ISTIO/NGINX/NONE]

Include:
1. Immediate rollback commands
2. Verification steps
3. Communication template
4. Post-incident checklist
5. Root cause investigation guide
```

### Incident Response Runbook

```
Create an incident response runbook for deployment failures:

Environment:
- Cluster: [NAME]
- Monitoring: [PROMETHEUS/DATADOG]
- Alerting: [ALERTMANAGER/PAGERDUTY]
- Deployment tool: [ARGO_ROLLOUTS/NATIVE]

Include sections for:
1. Alert triage
2. Impact assessment
3. Immediate mitigation
4. Rollback decision tree
5. Communication templates
6. Post-incident tasks
```
