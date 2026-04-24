# GitOps LLM Prompts

Prompts for generating GitOps configurations and solving common tasks.

## Model Selection

### Evaluate Push vs Pull Model

```
Evaluate GitOps model for my organization:
- Team size: {team_size}
- Number of applications: {app_count}
- Number of clusters: {cluster_count}
- Existing CI/CD: {Jenkins|GitHub Actions|GitLab|CircleCI|none}
- Security requirements: {high|medium|standard}
- Compliance needs: {SOC2|HIPAA|PCI-DSS|none}
- Deployment frequency: {continuous|daily|weekly}

Recommend:
1. Push, Pull, or Hybrid model with justification
2. Specific tools to use
3. Migration path from current state
4. Key success metrics to track
```

### Compare GitOps Tools

```
Compare GitOps tools for my requirements:
- Primary use case: {app_deployment|infrastructure|both}
- Kubernetes experience: {beginner|intermediate|advanced}
- Multi-cluster: {yes|no}, count: {cluster_count}
- Progressive delivery needed: {canary|blue-green|none}
- Team preference: {GUI|CLI|GitOps-native}

Compare:
- ArgoCD
- Flux CD
- Kargo
- GitLab GitOps

Provide recommendation with pros/cons for each.
```

## Repository Design

### Design GitOps Repository

```
Design GitOps repository structure for:
- Applications: {app_list}
- Environments: {dev, staging, production}
- Teams: {team_structure}
- Tool: {Kustomize|Helm|both}
- Multi-cluster: {yes|no}

Provide:
1. Complete directory structure
2. Kustomization/Helm files
3. Environment promotion strategy
4. Access control recommendations
5. Branch protection rules
```

### Monorepo vs Multi-Repo Strategy

```
Evaluate repository strategy for GitOps:
- Number of applications: {count}
- Number of teams: {count}
- Team autonomy level: {high|medium|low}
- Deployment frequency: {frequency}
- Compliance requirements: {requirements}
- Change approval process: {description}

Recommend:
1. Monorepo vs multi-repo with justification
2. Repository layout
3. CODEOWNERS configuration
4. CI/CD integration approach
5. Scaling considerations
```

## Application Configuration

### Generate ArgoCD Application

```
Create ArgoCD Application manifest:
- Name: {app_name}
- Source repository: {repo_url}
- Path: {manifest_path}
- Target revision: {branch_or_tag}
- Destination namespace: {namespace}
- Environment: {dev|staging|production}
- Sync policy: {manual|automated}
- Self-heal: {true|false}
- Prune: {true|false}
- Notifications: {slack_channel|none}

Include appropriate sync options and retry configuration.
```

### Generate Flux Kustomization

```
Create Flux Kustomization for:
- Application: {app_name}
- GitRepository: {git_repo_name}
- Path: {path}
- Target namespace: {namespace}
- Interval: {sync_interval}
- Health checks: {deployment_names}
- Dependencies: {other_kustomizations}
- Prune: {true|false}

Include postBuild substitutions if needed.
```

### Convert to GitOps

```
I have an existing Kubernetes deployment managed by {current_method}:
{existing_manifest_or_helm_command}

Convert to GitOps with:
- Tool: {ArgoCD|Flux}
- Repository: {repo_url}
- Environment structure: {single|multi-env}

Provide:
1. Repository structure
2. Kustomize base/overlay files
3. GitOps Application/Kustomization manifest
4. Migration steps
5. Rollback plan
```

## Multi-Environment Deployment

### Multi-Environment ApplicationSet

```
Create ApplicationSet for multi-environment deployment:
- Application: {app_name}
- Environments: {staging, production}
- Repository: {repo_url}
- Kustomize overlays path: apps/{app}/overlays/{env}
- Cluster: {single|multi-cluster}

Configure:
- Staging: automated sync with prune and self-heal
- Production: manual sync with self-heal only
- Appropriate notifications per environment
```

### Environment Promotion Strategy

```
Design environment promotion strategy:
- Environments: {env_list}
- Promotion method: {manual|automated|semi-automated}
- Approval requirements: {description}
- Rollback strategy: {description}

Using: {Kargo|ArgoCD|Flux}

Provide:
1. Promotion workflow
2. Configuration files
3. Approval gates
4. Rollback procedure
5. Notification setup
```

## Multi-Cluster Deployment

### Multi-Cluster ApplicationSet

```
Create ApplicationSet for multi-cluster deployment:
- Application: {app_name}
- Clusters: all with label {label_key}={label_value}
- Source: {repo_url}, path: {path}
- Tool: {Helm|Kustomize}
- Per-cluster configuration: {cluster_name, region, etc.}

Include cluster-specific values substitution.
```

### Hub-and-Spoke Architecture

```
Design multi-cluster GitOps architecture:
- Management cluster: {management_cluster}
- Workload clusters: {cluster_list}
- Cluster grouping: {by_region|by_environment|by_team}
- Applications to deploy: {app_list}

Provide:
1. Architecture diagram (text)
2. ArgoCD/Flux configuration
3. ApplicationSet for cluster management
4. Network requirements
5. Scaling considerations
6. Failover strategy
```

## Progressive Delivery

### Canary Deployment

```
Create canary deployment configuration:
- Application: {app_name}
- Namespace: {namespace}
- Canary steps: {5%, 20%, 50%, 80%, 100%}
- Pause duration between steps: {duration}
- Success metric: {metric_name} with threshold {threshold}
- Traffic routing: {nginx|istio|alb}
- Prometheus address: {address}

Using: {Argo Rollouts|Flagger}

Include analysis template and rollback configuration.
```

### Blue-Green Deployment

```
Create blue-green deployment configuration:
- Application: {app_name}
- Namespace: {namespace}
- Promotion: {automatic|manual}
- Pre-promotion analysis: {metrics}
- Scale down delay: {seconds}

Using: {Argo Rollouts|Flagger}

Include services configuration for traffic switching.
```

### Progressive Delivery Strategy Selection

```
Recommend progressive delivery strategy:
- Application type: {stateless|stateful}
- Traffic volume: {low|medium|high}
- Rollback time requirement: {seconds}
- Testing capability: {automated|manual}
- Risk tolerance: {low|medium|high}

Compare canary vs blue-green vs A/B testing for this use case.
Provide implementation recommendation.
```

## Drift Detection and Remediation

### Configure Drift Detection

```
Configure drift detection and remediation:
- Tool: {ArgoCD|Flux}
- Application: {app_name}
- Fields to ignore: {list_of_fields}
- Self-heal: {enabled|disabled}
- Alert on drift: {yes|no}
- Alert channel: {slack_channel}

Provide:
1. ignoreDifferences/ignore configuration
2. Self-heal settings
3. Alert configuration
4. Monitoring queries
```

### Resolve Persistent Drift

```
ArgoCD keeps showing drift for:
{resource_type}/{resource_name}

Changing fields:
{field_paths}

Possible causes:
- Controller-managed fields (HPA, etc.)
- Defaulted fields by admission webhooks
- Timestamp/generation fields

Provide ignoreDifferences configuration to resolve.
```

## Security

### Secrets Management Setup

```
Configure secrets management for GitOps:
- Secrets backend: {Vault|AWS Secrets Manager|GCP Secret Manager|Azure Key Vault}
- Applications: {app_list}
- Rotation requirement: {frequency}
- Cross-namespace access: {yes|no}

Provide:
1. External Secrets Operator setup
2. SecretStore/ClusterSecretStore configuration
3. ExternalSecret for each application
4. GitOps Application to manage ESO
5. Rotation strategy
```

### Harden GitOps Installation

```
Generate security hardening for {ArgoCD|Flux}:
- Authentication: {OIDC_provider}
- RBAC model: {role_list}
- Network policy: {enabled|disabled}
- Audit logging: {enabled|disabled}
- Webhook signature verification: {enabled|disabled}

Provide:
1. Helm values for security settings
2. RBAC policies
3. Network policies
4. Audit configuration
5. Compliance checklist
```

## Troubleshooting

### Debug Sync Issues

```
GitOps sync is failing:
- Tool: {ArgoCD|Flux}
- Application: {app_name}
- Error: {error_message}
- Source: {repo_url}, path: {path}
- Sync status: {status}

Diagnose:
1. Root cause analysis
2. Recommended fix
3. Prevention strategy
4. Monitoring to add
```

### Optimize Sync Performance

```
GitOps sync is slow:
- Tool: {ArgoCD|Flux}
- Application: {app_name}
- Number of resources: {count}
- Current sync time: {duration}
- Controller replicas: {count}

Recommend:
1. Sync options to enable
2. Controller tuning parameters
3. Repository structure improvements
4. Caching configuration
```

### Debug Progressive Delivery

```
Progressive delivery is stuck/failing:
- Tool: {Argo Rollouts|Flagger}
- Application: {app_name}
- Current step: {step}
- Analysis result: {result}
- Metrics query: {query}

Diagnose and provide:
1. Root cause
2. Fix for current deployment
3. Configuration improvements
4. Better analysis metrics
```

## CI/CD Integration

### GitHub Actions Integration

```
Create GitHub Actions workflow for GitOps:
- Application: {app_name}
- Source repo: {source_repo}
- GitOps repo: {gitops_repo}
- Registry: {container_registry}
- Trigger: {on_push|on_tag|on_release}

Workflow should:
1. Build and push container image
2. Update manifest in GitOps repo
3. Wait for sync (optional)
4. Notify on completion
```

### GitLab CI Integration

```
Create GitLab CI pipeline for GitOps:
- Application: {app_name}
- GitOps repo: {gitops_repo}
- Registry: {container_registry}
- Branch strategy: {trunk|gitflow}

Pipeline should:
1. Build and push container image
2. Update manifest in GitOps repo
3. Trigger ArgoCD/Flux sync
4. Verify deployment health
```

## Quick Prompts

### Quick ArgoCD Application

```
Generate ArgoCD Application:
name={name} repo={repo} path={path} ns={namespace} env={staging|production}
```

### Quick Flux Kustomization

```
Generate Flux Kustomization:
name={name} gitrepo={gitrepo} path={path} ns={namespace} interval={interval}
```

### Quick ApplicationSet

```
Generate ApplicationSet:
type={matrix|git|cluster|pr} apps={app_list} envs={env_list} repo={repo}
```

### Quick Canary Rollout

```
Generate Argo Rollouts Canary:
name={name} steps={5,20,50,100} pause={5m} metric={success_rate} threshold={0.95}
```

### Quick Repository Structure

```
Generate GitOps repository structure:
apps={app_list} envs={env_list} tool={kustomize|helm} clusters={single|multi}
```

## Comparison and Migration

### Migrate from Helm to GitOps

```
Migrate Helm deployment to GitOps:
- Current Helm command: helm install {release} {chart} -f {values}
- Target tool: {ArgoCD|Flux}
- Environment: {env_list}

Provide:
1. Repository structure
2. GitOps Application/HelmRelease
3. Migration steps (zero-downtime)
4. Validation checklist
```

### Migrate from ArgoCD to Flux (or vice versa)

```
Migrate from {ArgoCD|Flux} to {Flux|ArgoCD}:
- Current configuration: {paste_current_config}
- Applications: {app_list}
- Requirements: {specific_requirements}

Provide:
1. Equivalent configuration in target tool
2. Migration strategy
3. Rollback plan
4. Feature gaps to address
```

### Compare Push vs Pull Security

```
Compare security posture:
- Current: {push|pull|hybrid}
- Proposed: {push|pull|hybrid}
- Threat model concerns: {list}

Analyze:
1. Credential exposure risks
2. Audit trail capabilities
3. Blast radius of compromise
4. Compliance implications
5. Recommended security controls
```
