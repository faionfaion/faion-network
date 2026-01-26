# Terraform LLM Prompts

**AI Prompts for Terraform Infrastructure Tasks (2025-2026)**

---

## State Management Prompts

### Configure Remote Backend

```
Configure a Terraform remote backend with:

Cloud Provider: [AWS S3 / GCP GCS / Azure Blob / Terraform Cloud]
Environment: [dev / staging / prod]
Project: [PROJECT_NAME]
Region: [REGION]

Requirements:
1. State encryption at rest (KMS/customer-managed key)
2. State locking (DynamoDB for AWS / native for others)
3. Bucket versioning for recovery
4. Access restricted to CI/CD and admins
5. Separate state per environment

Provide:
- backend.tf configuration
- Supporting resources (lock table, bucket, IAM)
- Migration commands from local state
```

### State Migration

```
Help migrate Terraform state:

Current Backend: [local / s3 / other]
Target Backend: [s3 / gcs / terraform-cloud]

Current state location: [PATH_OR_BUCKET]
Target state location: [NEW_BUCKET/KEY]

Provide:
1. Pre-migration checklist
2. Backup commands
3. Migration steps
4. Verification commands
5. Rollback procedure
```

### Split Monolithic State

```
Split this monolithic Terraform state into multiple states:

Current Structure:
[DESCRIBE OR PASTE CURRENT STRUCTURE]

Desired State Separation:
- networking (VPC, subnets, security groups)
- compute (EC2, ASG, ALB)
- database (RDS, ElastiCache)
- [OTHER]

Provide:
1. State split strategy
2. terraform state mv commands
3. Remote state data sources for cross-references
4. Updated module structure
5. Migration runbook
```

---

## Module Development Prompts

### Create Reusable Module

```
Create a reusable Terraform module for:

Component: [VPC / RDS / EKS / Lambda / S3 / etc.]
Cloud: [AWS / GCP / Azure]
Use Case: [DESCRIPTION]

Requirements:
1. Standard module structure (main.tf, variables.tf, outputs.tf, versions.tf)
2. Comprehensive variable validation
3. Sensible defaults for optional variables
4. All outputs documented
5. README with usage example
6. Support for multiple environments (dev/staging/prod)

Best Practices (2025-2026):
- Pin provider versions with constraints
- Mark sensitive outputs
- Include security defaults (encryption, access control)
- Add lifecycle rules where appropriate

Provide:
- Complete module files
- Usage example
- README.md with inputs/outputs table
```

### Refactor Existing Code to Modules

```
Refactor this Terraform code into reusable modules:

Current Code:
[PASTE TERRAFORM CODE]

Goals:
- DRY principle (no repetition)
- Reusable across environments
- Clear separation of concerns

Provide:
1. Module structure proposal
2. Refactored main.tf using modules
3. Module definitions
4. moved blocks for state migration
5. Before/after comparison
```

### Module Testing Strategy

```
Create a testing strategy for this Terraform module:

Module: [MODULE_NAME]
Purpose: [DESCRIPTION]

Testing Levels Needed:
1. Static validation (terraform validate)
2. Linting (tflint)
3. Security scanning (tfsec/Checkov)
4. Unit tests (terraform test)
5. Integration tests (Terratest)

Provide:
- .tftest.hcl file with test cases
- Terratest Go code (if applicable)
- CI/CD pipeline integration
- Test data/fixtures
```

---

## Workspace and Environment Prompts

### Multi-Environment Setup

```
Design a multi-environment Terraform setup for:

Environments: development, staging, production
Components: [networking, compute, database, etc.]

Requirements:
1. Strong isolation between environments
2. Shared modules
3. Environment-specific configurations
4. Different AWS accounts per environment (optional)
5. CI/CD integration

Strategy Options:
A. Workspaces (simple, shared backend)
B. Directory per environment (isolated backends)
C. Terragrunt (DRY, hierarchical)

Recommend the best approach and provide:
1. Directory structure
2. Configuration files
3. Environment-specific tfvars
4. CI/CD workflow
```

### Workspace Migration

```
Migrate from workspaces to directory-based environments:

Current Setup:
- Using terraform.workspace for environment
- Single backend with workspace-prefixed keys
- [OTHER DETAILS]

Target Setup:
- Separate directory per environment
- Separate backend per environment
- Shared modules

Provide:
1. Migration strategy
2. State migration commands
3. New directory structure
4. Updated CI/CD pipeline
5. Rollback procedure
```

---

## CI/CD Integration Prompts

### Create CI/CD Pipeline

```
Create a Terraform CI/CD pipeline for:

Platform: [GitHub Actions / GitLab CI / Azure DevOps / Jenkins]
Cloud: [AWS / GCP / Azure]
Environments: [dev / staging / prod]

Pipeline Stages:
1. Lint (tflint, terraform fmt)
2. Security scan (tfsec, Checkov)
3. Plan
4. Manual approval (for prod)
5. Apply
6. Drift detection (scheduled)

Requirements:
- OIDC authentication (no long-lived credentials)
- Plan output in PR comments
- Separate workflows per environment
- Cost estimation (Infracost)
- Fail on HIGH/CRITICAL security findings

Provide:
- Complete pipeline file(s)
- Required secrets/variables
- Branch protection rules
- OIDC setup instructions
```

### Atlantis Configuration

```
Configure Atlantis for Terraform PR automation:

Repository: [REPO_URL]
Projects:
- [PROJECT_1]: terraform/environments/dev
- [PROJECT_2]: terraform/environments/prod

Requirements:
1. Autoplan on file changes
2. Require approval before apply
3. Lock files during operations
4. Custom workflows for security scanning
5. Policy checks

Provide:
- atlantis.yaml configuration
- Server setup instructions
- GitHub/GitLab integration
- Custom workflow definitions
```

### Drift Detection

```
Set up Terraform drift detection:

Platform: [GitHub Actions / GitLab CI / AWS Lambda]
Environments: [LIST]
Schedule: [daily / weekly]

Requirements:
1. Run terraform plan on schedule
2. Alert on detected drift (Slack/email/PagerDuty)
3. Store plan outputs for review
4. Automatic remediation (optional)

Provide:
1. Scheduled pipeline configuration
2. Alerting integration
3. Remediation strategy
4. Dashboard/reporting setup
```

---

## Security Prompts

### Security Audit

```
Perform a security audit on this Terraform configuration:

[PASTE TERRAFORM CODE]

Check for:
1. Hardcoded secrets
2. Overly permissive IAM policies
3. Public access to resources
4. Missing encryption
5. Security group issues (0.0.0.0/0)
6. Missing logging/monitoring
7. Non-compliant configurations

Provide:
- Risk assessment (Critical/High/Medium/Low)
- Specific findings with line numbers
- Remediation steps
- Hardened configuration
- tfsec/Checkov rules to enforce
```

### Implement Policy as Code

```
Implement policy-as-code for Terraform:

Platform: [Sentinel / OPA/Conftest / Checkov custom]
Policies Needed:
1. All S3 buckets must have encryption
2. No security groups with 0.0.0.0/0 ingress
3. All resources must have required tags
4. Instance types limited to approved list
5. [OTHER POLICIES]

Provide:
1. Policy files (Sentinel or Rego)
2. CI/CD integration
3. Enforcement configuration
4. Exception handling process
```

### Secrets Management

```
Implement secrets management for Terraform:

Current Problem: [DESCRIBE - e.g., secrets in tfvars]
Secret Types: [database passwords, API keys, certificates]
Cloud: [AWS / GCP / Azure]

Options to Evaluate:
A. AWS Secrets Manager / Parameter Store
B. HashiCorp Vault
C. Environment variables in CI/CD
D. SOPS encrypted files

Provide:
1. Recommended approach
2. Implementation code
3. CI/CD integration
4. Rotation strategy
5. Access control setup
```

---

## Troubleshooting Prompts

### Debug State Issues

```
Debug this Terraform state issue:

Error:
[PASTE ERROR MESSAGE]

Context:
- Last successful operation: [DESCRIBE]
- Recent changes: [DESCRIBE]
- Backend: [s3/gcs/local]

Current State:
[PASTE terraform state list OR relevant state output]

Provide:
1. Root cause analysis
2. Resolution steps
3. Commands to fix
4. Prevention measures
```

### Resource Import

```
Import existing infrastructure into Terraform:

Resources to Import:
- [RESOURCE_TYPE]: [RESOURCE_ID]
- [EXAMPLE]: aws_instance: i-1234567890abcdef0
- [EXAMPLE]: aws_vpc: vpc-12345678

Provide:
1. import blocks (Terraform 1.5+)
2. Resource configurations to add
3. Import commands (legacy method)
4. State verification
5. Post-import cleanup
```

### Resolve Conflicts

```
Resolve this Terraform state conflict:

Error:
[PASTE ERROR - e.g., "Error acquiring state lock"]

Context:
- Multiple users/pipelines running simultaneously
- Backend: [s3 + dynamodb / gcs / terraform cloud]
- Lock ID: [IF AVAILABLE]

Provide:
1. Immediate resolution (unlock if safe)
2. Investigation steps
3. Prevention strategy
4. Pipeline configuration to prevent future conflicts
```

---

## Migration Prompts

### Cloud Migration

```
Plan Terraform migration between clouds:

Source: [AWS / GCP / Azure / On-prem]
Target: [AWS / GCP / Azure]

Components:
- [LIST RESOURCES TO MIGRATE]

Requirements:
1. Minimal downtime
2. Data migration strategy
3. DNS/networking transition
4. Rollback capability

Provide:
1. Migration plan phases
2. Terraform code for target cloud
3. Data migration steps
4. Cutover procedure
5. Rollback plan
```

### Terraform Version Upgrade

```
Plan Terraform version upgrade:

Current Version: [VERSION]
Target Version: [VERSION]

Codebase Size: [NUMBER] of .tf files
Providers: [LIST PROVIDERS AND VERSIONS]

Provide:
1. Breaking changes between versions
2. Code modifications needed
3. Provider version updates
4. Testing strategy
5. Rollback procedure
6. Team communication plan
```

### Provider Upgrade

```
Upgrade Terraform provider:

Provider: [aws / google / azurerm / kubernetes]
Current Version: [VERSION]
Target Version: [VERSION]

Provide:
1. Breaking changes in new version
2. Deprecated resources/attributes
3. Code modifications needed
4. State migration (if required)
5. Testing checklist
```

---

## Architecture Prompts

### Design Infrastructure

```
Design Terraform infrastructure for:

Application: [DESCRIPTION]
Requirements:
- High availability
- Multi-AZ / Multi-region
- Auto-scaling
- [OTHER REQUIREMENTS]

Cloud: [AWS / GCP / Azure]
Environments: [dev / staging / prod]

Provide:
1. Architecture diagram description
2. Terraform module structure
3. Component breakdown
4. State organization
5. CI/CD pipeline design
6. Cost estimation approach
```

### Disaster Recovery

```
Implement DR strategy in Terraform:

Application: [DESCRIPTION]
Current Region: [PRIMARY_REGION]
DR Region: [DR_REGION]

RTO: [RECOVERY_TIME_OBJECTIVE]
RPO: [RECOVERY_POINT_OBJECTIVE]

Provide:
1. DR architecture
2. Terraform code for DR resources
3. Data replication setup
4. Failover procedure
5. Testing strategy
6. Runbook
```

---

## Quick Task Prompts

### Generate Module Documentation

```
Generate documentation for this Terraform module:

[PASTE MODULE CODE]

Generate:
- README.md with terraform-docs format
- Usage examples
- Inputs table
- Outputs table
- Requirements table
```

### Create Variable Validation

```
Add validation to these Terraform variables:

[PASTE VARIABLES.TF]

Validations Needed:
- CIDR format validation
- Environment name (dev/staging/prod)
- Instance type (t3.micro, t3.small, etc.)
- Port numbers (1-65535)
- Email format
- [OTHER]

Provide updated variables.tf with validation blocks.
```

### Optimize Configuration

```
Optimize this Terraform configuration:

[PASTE TERRAFORM CODE]

Optimize for:
1. Reduced code duplication
2. Better variable usage
3. Improved readability
4. Performance (fewer API calls)
5. Cost (if applicable)

Provide:
- Optimized code
- Explanation of changes
- Before/after comparison
```

---

## Prompt Template Variables

Use these placeholders in prompts:

| Variable | Description |
|----------|-------------|
| `[CLOUD]` | AWS, GCP, Azure |
| `[REGION]` | Cloud region (us-east-1, etc.) |
| `[ENVIRONMENT]` | dev, staging, prod |
| `[PROJECT_NAME]` | Project identifier |
| `[RESOURCE_TYPE]` | Terraform resource type |
| `[RESOURCE_ID]` | Cloud resource identifier |
| `[VERSION]` | Terraform or provider version |
| `[COMPONENT]` | Infrastructure component |
| `[DESCRIPTION]` | Detailed description |
| `[PASTE ...]` | Insert relevant code/output |

---

*Terraform LLM Prompts | faion-infrastructure-engineer*
