# GitOps LLM Prompts

## Analysis Prompts

### Assess Current Deployment State

```
Analyze my current deployment process and recommend a GitOps adoption strategy.

Current state:
- Deployment method: [CI/CD push / manual / scripts]
- Infrastructure: [Kubernetes / VMs / serverless]
- Team size: [number]
- Number of environments: [dev/staging/prod]
- Current tools: [Jenkins / GitHub Actions / etc.]

Please provide:
1. Gap analysis between current state and GitOps
2. Recommended GitOps tool (ArgoCD vs Flux) with reasoning
3. Repository structure recommendation
4. Migration phases
5. Risk assessment
```

### Push vs Pull Decision

```
Help me decide between push-based and pull-based GitOps for my organization.

Context:
- Security requirements: [strict / moderate / basic]
- Compliance needs: [SOC2 / HIPAA / PCI-DSS / none]
- Multi-cluster: [yes / no, how many clusters]
- Team experience with Kubernetes: [expert / intermediate / beginner]
- Existing CI/CD: [describe current pipeline]

Provide a recommendation with:
1. Recommended approach (push/pull/hybrid)
2. Security implications
3. Operational complexity comparison
4. Migration effort estimate
```

### Repository Structure Design

```
Design a GitOps repository structure for my project.

Requirements:
- Number of applications: [count]
- Environments: [list: dev, staging, prod, etc.]
- Teams: [number and names]
- Multi-tenant: [yes / no]
- Shared infrastructure: [yes / no]

Please provide:
1. Recommended repository structure (monorepo vs polyrepo)
2. Directory layout with explanations
3. Kustomize vs Helm recommendation
4. Environment promotion strategy
5. RBAC considerations
```

## Implementation Prompts

### ArgoCD Setup

```
Generate ArgoCD configuration for my Kubernetes cluster.

Requirements:
- Cluster: [name and context]
- Git repository: [URL]
- Applications to deploy: [list with paths]
- Environments: [dev, staging, prod]
- SSO provider: [Okta / Azure AD / Google / none]
- Multi-cluster: [yes / no]

Generate:
1. ArgoCD installation command with appropriate settings
2. AppProject definition for team isolation
3. Application definitions for each app
4. RBAC configuration
5. Repository credentials secret
```

### Flux Setup

```
Generate Flux CD configuration for my cluster.

Requirements:
- Cluster: [name]
- Git repository: [URL]
- Branch: [main / master]
- Applications: [list]
- Helm charts needed: [yes / no, which charts]
- Image automation: [yes / no]

Generate:
1. Flux bootstrap command
2. GitRepository source definition
3. Kustomization definitions
4. HelmRelease definitions (if needed)
5. Image automation config (if needed)
```

### Environment Promotion

```
Design an environment promotion workflow for GitOps.

Context:
- Environments: [list in order]
- Approval requirements: [describe per environment]
- Automation level: [fully automated / semi-automated / manual]
- Rollback requirements: [describe]

Generate:
1. Promotion workflow diagram
2. PR-based promotion configuration
3. Automated promotion script (if applicable)
4. Rollback procedure
5. Notification setup
```

## Troubleshooting Prompts

### Sync Issues

```
Help troubleshoot ArgoCD/Flux sync issues.

Symptoms:
- Error message: [paste error]
- Application status: [OutOfSync / Degraded / Unknown]
- Last successful sync: [when]
- Recent changes: [describe]

Provide:
1. Likely root cause
2. Diagnostic commands to run
3. Resolution steps
4. Prevention measures
```

### Drift Detection

```
My GitOps setup is detecting drift but I don't understand why.

Context:
- Tool: [ArgoCD / Flux]
- Resources showing drift: [list]
- Drift details: [describe what's different]
- Self-heal enabled: [yes / no]

Help me:
1. Understand why drift is occurring
2. Determine if this is expected (generated fields, etc.)
3. Configure ignore rules if appropriate
4. Set up proper drift handling
```

### Multi-Cluster Issues

```
Troubleshoot multi-cluster GitOps deployment issues.

Setup:
- Management cluster: [describe]
- Target clusters: [list]
- GitOps tool: [ArgoCD / Flux]
- Issue: [describe problem]

Provide:
1. Connectivity verification steps
2. RBAC/permissions check
3. Network policy considerations
4. Resolution steps
```

## Migration Prompts

### Migrate from CI/CD Push to GitOps

```
Create a migration plan from push-based CI/CD to GitOps.

Current state:
- CI/CD tool: [Jenkins / GitHub Actions / GitLab CI]
- Deployment method: [kubectl apply / helm upgrade / scripts]
- Number of applications: [count]
- Environments: [list]

Target state:
- GitOps tool: [ArgoCD / Flux]
- Repository structure: [monorepo / polyrepo]

Generate:
1. Phased migration plan
2. Parallel running strategy
3. Cutover checklist
4. Rollback plan
5. Success criteria
```

### Migrate ArgoCD to Flux (or vice versa)

```
Create a migration plan from [ArgoCD / Flux] to [Flux / ArgoCD].

Current setup:
- Current tool: [ArgoCD / Flux]
- Number of applications: [count]
- Custom configurations: [describe]
- Integrations: [SSO, notifications, etc.]

Reason for migration: [explain]

Generate:
1. Feature mapping between tools
2. Configuration translation guide
3. Migration steps
4. Testing strategy
5. Rollback procedure
```

## Security Prompts

### Secrets Management Setup

```
Design a secrets management strategy for GitOps.

Requirements:
- Secret types: [database creds / API keys / certificates]
- Compliance requirements: [list]
- Cloud provider: [AWS / GCP / Azure / on-prem]
- Rotation requirements: [automatic / manual, frequency]

Recommend:
1. Secret management solution (SOPS / Sealed Secrets / External Secrets)
2. Integration with GitOps workflow
3. Key management strategy
4. Rotation procedure
5. Audit logging setup
```

### GitOps Security Audit

```
Perform a security audit of my GitOps setup.

Current configuration:
- GitOps tool: [ArgoCD / Flux]
- Repository access: [describe]
- RBAC: [describe]
- Network policies: [yes / no]
- Secrets management: [describe]

Analyze:
1. Attack surface assessment
2. Credential exposure risks
3. RBAC gaps
4. Network security issues
5. Recommended remediations prioritized by severity
```

## Advanced Prompts

### Progressive Delivery Setup

```
Design a progressive delivery strategy with GitOps.

Requirements:
- Deployment strategy: [canary / blue-green / rolling]
- Traffic management: [Istio / Nginx / Linkerd / other]
- Metrics for analysis: [list]
- Rollback criteria: [describe]

Generate:
1. Tool selection (Flagger / Argo Rollouts)
2. Canary/rollout configuration
3. Analysis template
4. Integration with GitOps workflow
5. Alert configuration
```

### Multi-Tenancy Design

```
Design a multi-tenant GitOps architecture.

Requirements:
- Tenant isolation level: [namespace / cluster]
- Number of tenants: [count]
- Shared resources: [list]
- Self-service requirements: [describe]

Generate:
1. Tenant isolation strategy
2. RBAC model
3. Resource quota templates
4. Network policy templates
5. Tenant onboarding automation
```

### Disaster Recovery

```
Design a disaster recovery plan for GitOps infrastructure.

Setup:
- GitOps tool: [ArgoCD / Flux]
- Number of clusters: [count]
- Critical applications: [list]
- RTO requirement: [time]
- RPO requirement: [time]

Generate:
1. Backup strategy for GitOps state
2. Repository redundancy plan
3. Cluster recovery procedure
4. Application recovery order
5. DR testing schedule
```

---

*GitOps LLM Prompts | faion-cicd-engineer*
