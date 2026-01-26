# LLM Prompts for Kubernetes Resource Management

Prompts for analyzing, optimizing, and configuring Kubernetes resources.

---

## Resource Analysis

### Analyze Current Resource Usage

```
Analyze the following Kubernetes resource configuration and provide recommendations:

[PASTE DEPLOYMENT/POD YAML HERE]

Consider:
1. Are requests/limits appropriately sized?
2. What QoS class will this pod receive?
3. Are there any potential issues (OOM risk, CPU throttling)?
4. Suggest optimized values based on workload type.

Workload type: [web service / background worker / batch job / database]
Expected traffic pattern: [steady / bursty / variable]
```

### Calculate Namespace Resource Requirements

```
Help me calculate ResourceQuota values for a namespace with:

- Number of pods: [X]
- Average CPU request per pod: [Y]m
- Average memory request per pod: [Z]Mi
- Peak multiplier for limits: [1.5-3x]
- Headroom percentage: [15-20%]

Provide:
1. Recommended ResourceQuota values
2. Matching LimitRange defaults
3. Rationale for each value
```

### Review Multi-Container Pod Resources

```
Review this multi-container pod specification for resource allocation:

[PASTE POD YAML HERE]

Check:
1. Total pod resources vs individual container resources
2. Sidecar containers sizing (should be minimal)
3. Init container resources (can be higher temporarily)
4. Overall QoS class determination
5. Potential resource contention between containers
```

---

## Configuration Generation

### Generate LimitRange

```
Generate a LimitRange for a [development/staging/production] namespace with:

Environment: [dev/staging/production]
Team size: [small/medium/large]
Workload types: [web services, workers, databases, etc.]

Requirements:
- Prevent resource hogging by single containers
- Ensure minimum resources for stability
- Set sensible defaults for forgetful developers
- Allow burst for variable workloads

Output: Complete LimitRange YAML with comments explaining each value.
```

### Generate ResourceQuota

```
Generate a ResourceQuota for namespace: [NAMESPACE_NAME]

Team characteristics:
- Team size: [X developers]
- Number of services: [Y]
- Expected pod count: [Z]
- Storage needs: [minimal/moderate/high]

Constraints:
- Total cluster capacity: [CPU cores, Memory]
- Number of teams sharing cluster: [N]
- Fair share percentage: [X%]

Output: Complete ResourceQuota YAML with justification for each limit.
```

### Generate Complete Namespace Setup

```
Generate a complete namespace setup for team: [TEAM_NAME]

Environment: [production/staging/development]
Tier: [tier1-small/tier2-medium/tier3-large]

Include:
1. Namespace with appropriate labels
2. LimitRange with defaults and bounds
3. ResourceQuota for compute and objects
4. Default NetworkPolicy (deny-all with exceptions)
5. PriorityClass usage recommendations

Output: All YAML manifests with explanatory comments.
```

---

## Troubleshooting

### Diagnose OOMKilled Pods

```
A pod is being OOMKilled repeatedly. Help diagnose:

Current configuration:
[PASTE POD YAML WITH RESOURCES]

Observed metrics:
- Memory usage before kill: [X]Mi
- Memory limit: [Y]Mi
- JVM heap (if applicable): [Z]

Questions:
1. Is the memory limit too low?
2. What's a safe memory limit for this workload?
3. Should I adjust JVM settings?
4. How to set up alerts to catch this earlier?
```

### Diagnose CPU Throttling

```
A pod is experiencing CPU throttling. Help optimize:

Current configuration:
[PASTE POD YAML WITH RESOURCES]

Observed metrics:
- CPU usage: [X]m average, [Y]m peak
- CPU limit: [Z]m
- Throttled periods: [N per minute]

Questions:
1. Is the CPU limit too restrictive?
2. Should I increase limit or remove it?
3. How does this affect QoS class?
4. What's the performance vs cost tradeoff?
```

### Diagnose Scheduling Failures

```
Pods are failing to schedule with "Insufficient resources". Help troubleshoot:

Error message:
[PASTE SCHEDULER ERROR]

Cluster info:
- Node count: [X]
- Node capacity: [CPU, Memory per node]
- Current utilization: [Y%]

Pod requirements:
[PASTE POD RESOURCE SPEC]

Questions:
1. Are requests too high?
2. Should I adjust node sizing?
3. Is cluster autoscaler needed?
4. How to optimize bin-packing?
```

---

## Optimization

### Right-Size Resources

```
Help right-size resources based on observed metrics:

Application: [APP_NAME]
Current configuration:
[PASTE CURRENT RESOURCES]

Observed metrics (last 7 days):
- CPU: P50=[X]m, P95=[Y]m, P99=[Z]m, Max=[W]m
- Memory: P50=[A]Mi, P95=[B]Mi, P99=[C]Mi, Max=[D]Mi

Requirements:
- QoS class desired: [Guaranteed/Burstable]
- Cost priority: [minimize cost / balance / maximize performance]
- Stability priority: [high / medium / low]

Output:
1. Recommended requests and limits
2. Rationale for each value
3. Expected savings or performance impact
```

### Multi-Tenant Cluster Optimization

```
Optimize resource allocation across a multi-tenant cluster:

Cluster capacity:
- Total CPU: [X] cores
- Total Memory: [Y] Gi
- Node count: [Z]

Tenants:
1. Team A: [workload description, current usage, priority]
2. Team B: [workload description, current usage, priority]
3. Team C: [workload description, current usage, priority]

Goals:
- Fair resource distribution
- Prevent noisy neighbor issues
- Allow burst when cluster has capacity
- Enable chargeback reporting

Output:
1. ResourceQuota per namespace
2. LimitRange per namespace
3. PriorityClass recommendations
4. Monitoring/alerting suggestions
```

### Cost Optimization

```
Optimize Kubernetes resource costs:

Current state:
- Total cluster spend: $[X]/month
- Average CPU utilization: [Y]%
- Average memory utilization: [Z]%

Namespaces with high waste:
[LIST NAMESPACES WITH UTILIZATION]

Constraints:
- Cannot impact production stability
- Some workloads need burst capacity
- Must maintain QoS=Guaranteed for critical services

Output:
1. Specific right-sizing recommendations
2. Candidates for VPA
3. Candidates for HPA
4. Expected cost savings
5. Risk assessment
```

---

## Best Practices Review

### Review Deployment Best Practices

```
Review this deployment for resource management best practices:

[PASTE DEPLOYMENT YAML]

Check against:
1. Resource requests and limits present
2. Appropriate QoS class for workload type
3. Memory/CPU ratio sensible for workload
4. Probes configured (affect resource availability)
5. Pod disruption budget (related to resource planning)
6. Anti-affinity rules (spread resource load)

Output: Scorecard with pass/fail for each check and recommendations.
```

### Audit Namespace Configuration

```
Audit this namespace configuration:

LimitRange:
[PASTE LIMITRANGE YAML]

ResourceQuota:
[PASTE RESOURCEQUOTA YAML]

Check:
1. LimitRange defaults align with quota capacity
2. Max limits don't exceed quota
3. Defaults won't cause immediate quota exhaustion
4. Storage limits match actual needs
5. Object counts are reasonable

Output: Audit report with findings and remediation steps.
```

---

## Migration & Planning

### Plan Resource Migration

```
Help plan resource configuration migration:

Current state (Cluster A):
[DESCRIBE CURRENT SETUP]

Target state (Cluster B):
[DESCRIBE TARGET CLUSTER]

Migration requirements:
- Zero downtime required: [yes/no]
- Budget constraints: [description]
- Timeline: [description]

Output:
1. Resource mapping from old to new
2. LimitRange/ResourceQuota for new cluster
3. Migration steps with validation checkpoints
4. Rollback plan
```

### Capacity Planning

```
Help with capacity planning for new workloads:

New workloads to deploy:
1. [Service A]: [expected resource needs]
2. [Service B]: [expected resource needs]
3. [Service C]: [expected resource needs]

Current cluster:
- Available capacity: [CPU, Memory]
- Current namespaces and quotas: [list]

Questions:
1. Can current cluster handle new workloads?
2. What quota changes needed?
3. Node scaling recommendations?
4. Cost projection?
```

---

## Prompt Tips

### Effective Prompting

1. **Include actual YAML** - Paste real configurations, not descriptions
2. **Provide metrics** - Include P50/P95/P99 values when available
3. **Specify constraints** - Cost, stability, compliance requirements
4. **Define workload type** - Different patterns need different approaches
5. **State environment** - Dev/staging/prod have different needs

### Common Variables to Include

| Variable | Why Important |
|----------|---------------|
| Workload type | Determines resource patterns |
| Traffic pattern | Affects burst requirements |
| Environment | Dev needs less than prod |
| Team size | Affects quota sizing |
| SLA requirements | Affects QoS class choice |
| Budget constraints | Affects optimization strategy |

---

*k8s-resources/llm-prompts.md | LLM Prompts for Resource Analysis*
