# Kubernetes Basics LLM Prompts

## Troubleshooting Prompts

### Pod Not Starting

```
I have a Kubernetes pod that won't start. Here's the output of `kubectl describe pod <name>`:

[PASTE DESCRIBE OUTPUT]

And here's the pod YAML:

[PASTE POD YAML]

Please:
1. Identify the root cause from the events and status
2. Explain what's happening
3. Provide specific commands or YAML fixes
4. Suggest preventive measures
```

### CrashLoopBackOff

```
My pod is in CrashLoopBackOff. Here's the information:

Pod describe:
[PASTE DESCRIBE OUTPUT]

Container logs (kubectl logs --previous):
[PASTE LOGS]

Please diagnose:
1. Why is the container crashing?
2. What are possible fixes?
3. How should I configure probes to handle this?
```

### Service Not Reaching Pods

```
My Kubernetes service isn't reaching the pods. Here's my setup:

Service YAML:
[PASTE SERVICE YAML]

Deployment YAML:
[PASTE DEPLOYMENT YAML]

kubectl get endpoints output:
[PASTE ENDPOINTS]

Please:
1. Check if selector labels match
2. Verify port configuration
3. Identify networking issues
4. Provide corrected YAML if needed
```

### Resource Exhaustion

```
My pods are being evicted or OOMKilled. Current state:

kubectl top nodes:
[PASTE OUTPUT]

kubectl top pods:
[PASTE OUTPUT]

kubectl describe node:
[PASTE RELEVANT SECTIONS]

Pod resource configuration:
[PASTE RESOURCES SECTION]

Please:
1. Analyze resource usage vs limits
2. Recommend appropriate resource values
3. Suggest HPA configuration if applicable
4. Identify if cluster needs scaling
```

## Generation Prompts

### Generate Deployment

```
Generate a production-ready Kubernetes Deployment for:

Application: [NAME]
Image: [IMAGE:TAG]
Port: [PORT]
Environment: [dev/staging/production]

Requirements:
- Replicas: [NUMBER]
- CPU: [REQUEST]/[LIMIT]
- Memory: [REQUEST]/[LIMIT]
- Health endpoint: [PATH]
- Environment variables: [LIST]
- ConfigMap: [NAME] (if applicable)
- Secrets: [NAME] (if applicable)

Include:
- Resource requests and limits
- Liveness and readiness probes
- Security context (non-root, read-only fs)
- Rolling update strategy
- Pod anti-affinity for HA
```

### Generate Service

```
Generate a Kubernetes Service for:

Application: [NAME]
Type: [ClusterIP/NodePort/LoadBalancer]
Port mapping: [SERVICE_PORT] -> [TARGET_PORT]
Protocol: [TCP/UDP]

Additional requirements:
- [Any specific annotations for cloud provider]
- [Session affinity if needed]
```

### Generate Namespace Setup

```
Generate a complete namespace setup for environment: [NAME]

Include:
1. Namespace with labels
2. ResourceQuota with:
   - CPU: [TOTAL_REQUESTS]/[TOTAL_LIMITS]
   - Memory: [TOTAL_REQUESTS]/[TOTAL_LIMITS]
   - Max pods: [NUMBER]
3. LimitRange with:
   - Default CPU: [REQUEST]/[LIMIT]
   - Default memory: [REQUEST]/[LIMIT]
4. Default NetworkPolicy (deny all ingress, allow DNS egress)
```

### Generate HPA

```
Generate a Horizontal Pod Autoscaler for:

Deployment: [NAME]
Min replicas: [NUMBER]
Max replicas: [NUMBER]

Scaling metrics:
- CPU target: [PERCENTAGE]%
- Memory target: [PERCENTAGE]%
- [Custom metrics if any]

Behavior:
- Scale up: [AGGRESSIVE/MODERATE/CONSERVATIVE]
- Scale down: [AGGRESSIVE/MODERATE/CONSERVATIVE]
- Stabilization window: [SECONDS]
```

## Migration Prompts

### Docker Compose to Kubernetes

```
Convert this Docker Compose file to Kubernetes manifests:

[PASTE DOCKER-COMPOSE.YML]

Requirements:
- Generate separate files for each resource type
- Use ConfigMaps for environment variables
- Use Secrets for sensitive data
- Include appropriate Services
- Add resource limits
- Configure health checks
```

### Update Manifest for Production

```
Update this Kubernetes manifest for production readiness:

[PASTE CURRENT YAML]

Add/improve:
1. Resource requests and limits
2. Security context
3. Health probes (liveness, readiness, startup)
4. Pod disruption budget
5. Anti-affinity rules
6. Appropriate annotations
```

## Analysis Prompts

### Security Audit

```
Audit this Kubernetes manifest for security issues:

[PASTE YAML]

Check for:
1. Running as root
2. Privileged containers
3. Writable root filesystem
4. Missing capabilities drop
5. Host namespace sharing
6. Missing network policies
7. Secrets in environment variables
8. Missing resource limits

Provide:
- List of issues by severity
- Specific fixes for each issue
- Corrected YAML
```

### Resource Optimization

```
Analyze these Kubernetes resource configurations:

Current deployment:
[PASTE DEPLOYMENT YAML]

Metrics (kubectl top pods over time):
[PASTE METRICS]

HPA events (if any):
[PASTE HPA DESCRIBE]

Provide:
1. Are resources over/under provisioned?
2. Recommended request/limit values
3. HPA configuration suggestions
4. Cost optimization recommendations
```

### High Availability Review

```
Review this Kubernetes setup for high availability:

Deployment:
[PASTE YAML]

Service:
[PASTE YAML]

Current pod distribution:
[kubectl get pods -o wide OUTPUT]

Analyze:
1. Replica count adequacy
2. Pod anti-affinity configuration
3. Topology spread constraints
4. Pod disruption budget
5. Multi-zone distribution
6. Single points of failure

Provide HA-improved configuration.
```

## Learning Prompts

### Explain Concept

```
Explain Kubernetes [CONCEPT] in detail:

Cover:
1. What it is and why it exists
2. How it works internally
3. Common use cases
4. Best practices
5. Common pitfalls
6. Example YAML with annotations
7. Related concepts

Concept: [pods/services/deployments/namespaces/configmaps/secrets/etc.]
```

### Compare Options

```
Compare these Kubernetes options for [USE CASE]:

Options:
1. [OPTION 1]
2. [OPTION 2]
3. [OPTION 3]

Compare:
- Use cases for each
- Pros and cons
- Performance implications
- Complexity
- When to use which

Use case context: [DESCRIBE YOUR SITUATION]
```

### Debug Strategy

```
Teach me how to debug [KUBERNETES ISSUE]:

Issue type: [pod not starting/networking/performance/etc.]

Provide:
1. Diagnostic commands in order
2. What to look for in output
3. Common causes and solutions
4. Decision tree for troubleshooting
5. Prevention strategies
```

## Quick Fix Prompts

### Fix YAML Error

```
Fix this Kubernetes YAML that's failing validation:

[PASTE YAML]

Error message:
[PASTE ERROR]

Provide corrected YAML with explanation of the issue.
```

### Scale Recommendation

```
Based on this workload pattern, recommend scaling configuration:

Current setup:
- Replicas: [NUMBER]
- CPU request/limit: [VALUES]
- Memory request/limit: [VALUES]

Traffic pattern:
[DESCRIBE: steady/bursty/time-based/etc.]

Peak load characteristics:
[DESCRIBE]

Recommend:
1. Static replica count or HPA
2. If HPA: min/max/metrics/behavior
3. Resource adjustment if needed
4. VPA consideration
```

---

*k8s-basics/llm-prompts.md | Prompts for K8s troubleshooting and generation*
