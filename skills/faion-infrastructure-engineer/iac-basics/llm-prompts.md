# IaC LLM Prompts

## Infrastructure Design

### Multi-Cloud Architecture Design

```
Design infrastructure for [APPLICATION TYPE] with the following requirements:

**Functional Requirements:**
- [List functional requirements]

**Non-Functional Requirements:**
- Availability: [e.g., 99.9%]
- Regions: [e.g., EU, US]
- Scale: [e.g., 10K requests/sec]
- Compliance: [e.g., GDPR, SOC2]

**Constraints:**
- Budget: [e.g., $X/month]
- Team expertise: [e.g., AWS experience]
- Timeline: [e.g., 3 months]

**Output Requirements:**
1. Architecture diagram (text-based)
2. Component list with cloud services
3. Terraform module structure
4. Cost estimation breakdown
5. Security considerations
6. Disaster recovery approach
```

### IaC Tool Selection

```
Help me select the right IaC tool for:

**Project Context:**
- Cloud providers: [AWS only / multi-cloud / hybrid]
- Team size: [X engineers]
- Team experience: [Terraform / programming languages / K8s]
- Existing tooling: [current tools]

**Requirements:**
- [ ] Multi-cloud support
- [ ] State encryption
- [ ] Policy enforcement
- [ ] Cost management
- [ ] GitOps integration
- [ ] Programming language support

**Evaluate:**
1. Terraform vs OpenTofu
2. Pulumi (if team prefers programming)
3. Crossplane (if K8s-native)
4. Cloud-native options

Provide comparison table and recommendation with reasoning.
```

## Terraform Development

### Module Development

```
Create a Terraform module for [RESOURCE TYPE]:

**Requirements:**
- Cloud provider: [AWS/GCP/Azure]
- Resource type: [e.g., VPC, EKS cluster, RDS]
- Environment support: dev/staging/prod
- Security: [encryption, IAM, network isolation]

**Module should include:**
1. main.tf - resource definitions
2. variables.tf - with validation rules
3. outputs.tf - useful outputs for consuming modules
4. versions.tf - provider version constraints
5. README.md - documentation with examples

**Patterns to follow:**
- Use for_each over count where appropriate
- Implement dynamic blocks for flexible configuration
- Add lifecycle rules for critical resources
- Include default tags
- Handle sensitive outputs appropriately
```

### State Migration

```
Help me migrate Terraform state:

**Current State:**
- Backend: [S3/local/Terraform Cloud]
- Resources: [number of resources]
- Workspaces: [list workspaces]

**Target State:**
- Backend: [new backend]
- State structure: [single/split by environment]

**Requirements:**
1. Zero downtime migration plan
2. Rollback procedure
3. State verification steps
4. Team coordination checklist
```

### Import Existing Resources

```
Generate Terraform import commands for:

**Resources to import:**
- [Resource type]: [Resource identifier]
- [Resource type]: [Resource identifier]

**Requirements:**
1. Import command for each resource
2. Corresponding resource block skeleton
3. Data source alternative if import not suitable
4. Verification steps post-import
5. State manipulation if needed (mv, rm)
```

## Security & Compliance

### Security Scanning Configuration

```
Set up IaC security scanning for:

**Repository:**
- IaC tool: [Terraform/Pulumi/CloudFormation]
- CI/CD: [GitHub Actions/GitLab CI/Jenkins]
- Cloud: [AWS/GCP/Azure]

**Required checks:**
- [ ] Secret detection
- [ ] Misconfiguration detection
- [ ] Compliance policy checks
- [ ] Cost estimation

**Tools to configure:**
1. tfsec or checkov for security
2. OPA/Sentinel for policy
3. Infracost for cost
4. Pre-commit hooks

Provide complete CI/CD configuration.
```

### Policy as Code

```
Create OPA/Rego policies for:

**Policy Requirements:**
1. Required tags: [Environment, Project, Team, CostCenter]
2. Allowed instance types: [t3.*, m5.*, c5.*]
3. Encryption required: [S3, RDS, EBS]
4. Network restrictions: [no 0.0.0.0/0 ingress on SSH/RDP]
5. Region restrictions: [eu-central-1, eu-west-1]

**Output:**
1. Individual policy files
2. Test cases for each policy
3. CI/CD integration configuration
4. Documentation for developers
```

## GitOps Integration

### Atlantis Setup

```
Configure Atlantis for Terraform GitOps:

**Environment:**
- Git platform: [GitHub/GitLab/Bitbucket]
- Cloud: [AWS/GCP/Azure]
- Terraform version: [X.X.X]
- Repository structure: [monorepo/multi-repo]

**Requirements:**
1. atlantis.yaml configuration
2. Repository settings (webhooks, branch protection)
3. Server deployment (K8s/Docker/VM)
4. AWS IAM role for Atlantis
5. Security best practices
6. Team workflow documentation
```

### ArgoCD Infrastructure

```
Set up ArgoCD for infrastructure GitOps:

**Scenario:**
- Kubernetes cluster: [EKS/GKE/AKS]
- Infrastructure tools: [Helm/Kustomize/Crossplane]
- Environments: [dev/staging/prod]

**Configure:**
1. ArgoCD installation (Helm chart)
2. Application manifests for infrastructure
3. ApplicationSet for environment promotion
4. RBAC configuration
5. Notification setup (Slack/Teams)
6. Sync policies and health checks
```

## Troubleshooting

### State Issues

```
Help troubleshoot Terraform state issue:

**Symptoms:**
[Describe the error message or unexpected behavior]

**Context:**
- Terraform version: [X.X.X]
- Backend: [S3/GCS/Terraform Cloud]
- Last successful operation: [plan/apply/destroy]
- Recent changes: [describe any recent changes]

**Error Output:**
```
[Paste error message]
```

**Provide:**
1. Root cause analysis
2. Step-by-step resolution
3. Prevention measures
4. Related documentation
```

### Drift Detection

```
Set up drift detection for infrastructure:

**Infrastructure:**
- IaC tool: [Terraform/Pulumi]
- Resources: [approximately X resources]
- Environments: [list environments]

**Requirements:**
1. Automated drift detection schedule
2. Notification on drift (Slack/email)
3. Drift report generation
4. Auto-remediation options
5. False positive handling

**Provide:**
1. Detection script/workflow
2. CI/CD integration
3. Alert configuration
4. Remediation runbook
```

## Cost Optimization

### Infrastructure Cost Analysis

```
Analyze and optimize infrastructure costs:

**Current State:**
- Monthly cost: $[X]
- Cloud provider: [AWS/GCP/Azure]
- Main cost drivers: [compute/storage/networking]

**Optimization Areas:**
1. Right-sizing compute resources
2. Reserved instances vs on-demand
3. Storage tiering
4. Network optimization
5. Unused resource cleanup

**Output:**
1. Cost breakdown analysis
2. Optimization recommendations with savings estimate
3. Terraform changes for each recommendation
4. Implementation priority
5. Monitoring setup for ongoing optimization
```

### Infracost Integration

```
Set up Infracost for PR cost estimation:

**CI/CD Platform:** [GitHub Actions/GitLab CI]
**Terraform Structure:** [monorepo/multi-repo]
**Environments:** [list environments]

**Requirements:**
1. Cost diff on every PR
2. Cost thresholds with warnings
3. Monthly cost trending
4. Team notifications

**Provide:**
1. CI/CD workflow configuration
2. Infracost configuration file
3. Cost policy rules
4. Dashboard setup
```

## Migration & Modernization

### Cloud Migration Planning

```
Plan infrastructure migration:

**Source:**
- Platform: [on-prem/other cloud]
- Components: [list major components]
- Data volume: [X TB]
- Dependencies: [external integrations]

**Target:**
- Cloud: [AWS/GCP/Azure]
- Architecture: [lift-shift/refactor/rebuild]
- Timeline: [X months]

**Requirements:**
1. Migration strategy by component
2. Terraform modules for target infrastructure
3. Data migration approach
4. Cutover plan with rollback
5. Testing and validation
6. Cost comparison
```

### Terraform Upgrade

```
Plan Terraform version upgrade:

**Current Version:** [X.X.X]
**Target Version:** [Y.Y.Y]

**Codebase:**
- Number of modules: [X]
- Lines of HCL: [approximately X]
- Provider versions: [list major providers]

**Requirements:**
1. Breaking changes analysis
2. Deprecated feature list
3. Code migration steps
4. Testing strategy
5. Rollback plan
6. Team training needs
```

## Disaster Recovery

### DR Infrastructure

```
Design disaster recovery infrastructure:

**Primary Region:** [e.g., eu-central-1]
**DR Region:** [e.g., eu-west-1]

**RPO:** [e.g., 1 hour]
**RTO:** [e.g., 4 hours]

**Components:**
- [List critical components]

**Requirements:**
1. DR architecture design
2. Terraform modules for DR resources
3. Replication configuration
4. Failover automation
5. Failback procedure
6. Testing runbook
7. Cost estimation for DR
```

---

*IaC LLM Prompts | faion-infrastructure-engineer*
