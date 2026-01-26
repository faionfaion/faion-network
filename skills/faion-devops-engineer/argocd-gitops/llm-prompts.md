# ArgoCD LLM Prompts

Prompts for generating ArgoCD configurations and solving common tasks.

## Application Generation

### Generate Application Manifest

```
Create an ArgoCD Application manifest with:
- Name: {app_name}
- Source repository: {repo_url}
- Path: {manifest_path}
- Target revision: {branch_or_tag}
- Destination cluster: {cluster_url_or_default}
- Destination namespace: {namespace}
- Sync policy: {manual|automated}
- Self-heal: {true|false}
- Prune: {true|false}
- Notifications: {slack_channel}

Include appropriate sync options and retry configuration for {environment}.
```

### Generate Helm Application

```
Create an ArgoCD Application for Helm chart:
- Chart: {chart_name} from {helm_repo_url}
- Version: {chart_version}
- Release name: {release_name}
- Namespace: {namespace}
- Values to override:
  {key1}: {value1}
  {key2}: {value2}

Include production-ready sync policy with appropriate retry logic.
```

## ApplicationSet Generation

### Multi-Environment ApplicationSet

```
Create an ArgoCD ApplicationSet that deploys {app_name} to multiple environments:
- Environments: {staging, production}
- Repository: {repo_url}
- Kustomize overlays path pattern: apps/{app_name}/overlays/{env}

Configure:
- Staging: automated sync with prune and self-heal
- Production: manual sync with self-heal only
- Appropriate namespace per environment
```

### Multi-Cluster ApplicationSet

```
Create an ArgoCD ApplicationSet for multi-cluster deployment:
- Application: {app_name}
- Target clusters: all clusters with label env={environment}
- Source: {repo_url}, path: {path}
- Tool: {Helm|Kustomize}

Pass cluster name to application for configuration purposes.
```

### PR Preview ApplicationSet

```
Create an ArgoCD ApplicationSet for PR preview environments:
- GitHub org: {org_name}
- Repository: {repo_name}
- Require label: {label_name}
- Image pattern: {registry}/{image}:pr-{number}
- Preview namespace pattern: preview-{number}

Include automatic cleanup when PR is closed.
```

## AppProject Generation

### Team Project

```
Create an ArgoCD AppProject for team {team_name}:
- Allowed source repos: https://github.com/{org}/{team_name}-*
- Allowed namespaces: {team_name}-*
- Allowed cluster resources: Namespace, Ingress
- Roles:
  - developer: get, sync applications
  - admin: full access
- OIDC groups for role mapping:
  - developers: {team_name}-developers
  - admins: {team_name}-admins
```

### Production Project with Sync Windows

```
Create an ArgoCD AppProject for production workloads:
- Name: {project_name}
- Source repos: {repo_patterns}
- Destinations: production namespace only
- Sync windows:
  - Allow: business hours {timezone}
  - Deny: weekends
  - Deny: maintenance window {schedule}

Include strict RBAC with approval workflow hints.
```

## Migration and Conversion

### Convert Deployment to ArgoCD

```
I have an existing Kubernetes deployment managed by {current_tool}:
{existing_manifest}

Convert this to ArgoCD-managed GitOps:
1. Create appropriate Kustomize base structure
2. Generate ArgoCD Application manifest
3. Recommend repository structure
4. Include sync waves if dependencies exist
```

### Migrate from Helm to ArgoCD+Helm

```
I'm using Helm directly for deployments:
- Chart: {chart_name}
- Values file: {values_content}

Create ArgoCD Application to manage this Helm release with:
- Same values preserved
- Automated sync for {environment}
- Notifications to {channel}
```

## Troubleshooting

### Debug Sync Issues

```
ArgoCD sync is failing with error:
{error_message}

Application details:
- Name: {app_name}
- Source: {repo_url}, path: {path}
- Sync status: {status}

Diagnose the issue and provide:
1. Root cause analysis
2. Recommended fix
3. Prevention strategy
```

### Optimize Sync Performance

```
ArgoCD sync is slow for application {app_name}:
- Number of resources: {count}
- Sync time: {duration}
- Controller replicas: {count}

Recommend optimizations:
1. Sync options to enable
2. Controller tuning
3. Repository structure improvements
```

### Resolve Drift Detection

```
ArgoCD keeps showing drift for:
{resource_type}/{resource_name}

Changing fields:
{field_paths}

Provide ignoreDifferences configuration to handle:
1. Controller-managed fields
2. Defaulted fields
3. Dynamic/timestamp fields
```

## Configuration Generation

### Generate Notifications

```
Configure ArgoCD notifications for:
- Service: {Slack|Teams|Email}
- Credentials: {token_secret_name}
- Triggers:
  - Sync succeeded
  - Sync failed
  - Health degraded
- Message format: Include app name, environment, revision

Generate notification configuration for ArgoCD.
```

### Generate RBAC

```
Generate ArgoCD RBAC configuration:
- Project: {project_name}
- Roles:
  - {role_name}: {permissions}
- OIDC group mappings: {group_to_role}

Include both AppProject policies and global policies if needed.
```

### Generate Sync Waves

```
I have these Kubernetes resources with dependencies:
{resource_list_with_dependencies}

Generate sync wave annotations to ensure proper ordering:
1. CRDs and Namespaces first
2. ConfigMaps and Secrets before Deployments
3. Deployments before Services
4. Services before Ingress
```

## Multi-Cluster Setup

### Add Cluster

```
Generate instructions and manifests to add cluster to ArgoCD:
- Cluster name: {name}
- API server: {url}
- Authentication: {ServiceAccount|OIDC|Kubeconfig}
- Labels: {key=value pairs}

Include:
1. CLI command
2. Declarative Secret manifest
3. RBAC requirements on target cluster
```

### Hub-and-Spoke Architecture

```
Design ArgoCD multi-cluster architecture:
- Management cluster: {management_cluster}
- Workload clusters: {cluster_list}
- Separation: {by_region|by_environment|by_team}

Provide:
1. Recommended architecture
2. ApplicationSet configuration
3. Network requirements
4. Scaling considerations
```

## Progressive Delivery

### Canary with Argo Rollouts

```
Create Argo Rollouts configuration for canary deployment:
- Application: {app_name}
- Canary steps: {weight_percentage_steps}
- Analysis: query Prometheus for {metric}
- Success threshold: {threshold}
- Traffic routing: {nginx|istio|alb}

Include ArgoCD Application to manage the Rollout.
```

### Blue-Green Deployment

```
Configure blue-green deployment with Argo Rollouts:
- Application: {app_name}
- Promotion: {automatic|manual}
- Analysis metrics: {metrics}
- Rollback trigger: {condition}

Include service configuration for traffic switching.
```

## Repository Structure

### Design GitOps Repository

```
Design GitOps repository structure for:
- Applications: {app_list}
- Environments: {env_list}
- Tool: {Kustomize|Helm}
- Teams: {team_structure}

Provide:
1. Directory structure
2. Kustomization files
3. ArgoCD Application/ApplicationSet configuration
4. Branching strategy recommendation
```

### Monorepo vs Multi-Repo

```
Evaluate repository strategy for ArgoCD GitOps:
- Number of applications: {count}
- Team structure: {structure}
- Deployment frequency: {frequency}
- Compliance requirements: {requirements}

Recommend:
1. Monorepo vs multi-repo
2. Repository layout
3. Access control strategy
4. CI/CD integration approach
```

## Security

### Secure Secrets

```
Configure secure secrets management for ArgoCD:
- Secrets backend: {Vault|AWS Secrets Manager|External Secrets}
- Applications needing secrets: {app_list}
- Rotation requirements: {frequency}

Provide:
1. External Secrets Operator configuration
2. SecretStore/ClusterSecretStore
3. ExternalSecret for each application
4. ArgoCD Application to manage ESO
```

### Harden ArgoCD

```
Generate security hardening configuration for ArgoCD:
- Authentication: {OIDC provider}
- Network policy: {enabled|disabled}
- RBAC: principle of least privilege
- Audit logging: {enabled}

Provide:
1. Helm values for security settings
2. Network policies
3. RBAC policies
4. Audit configuration
```

## Prompt Templates with Variables

### Quick Application

```
Generate ArgoCD Application:
name={name} repo={repo} path={path} ns={namespace} env={staging|production}
```

### Quick ApplicationSet

```
Generate ArgoCD ApplicationSet:
type={matrix|git|cluster|pr} apps={app_list} envs={env_list} repo={repo}
```

### Quick Project

```
Generate ArgoCD AppProject:
team={team} repos={repo_patterns} namespaces={ns_patterns} roles={role_list}
```
