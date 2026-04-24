# Terraform LLM Prompts

## Module Development Prompts

### Create New Module

```
Create a Terraform module for [RESOURCE_TYPE] with the following requirements:

Context:
- Cloud provider: [AWS/GCP/Azure]
- Terraform version: 1.10+
- Module purpose: [DESCRIPTION]

Requirements:
1. Standard module structure (main.tf, variables.tf, outputs.tf, versions.tf)
2. All variables with descriptions and validation where appropriate
3. All resources with at least one output
4. Proper tagging with project_name and environment
5. README.md with usage example

Resources to create:
- [LIST RESOURCES]

Variables needed:
- project_name (required)
- environment (required, validated: dev/staging/prod)
- [OTHER VARIABLES]

Outputs needed:
- [LIST OUTPUTS]
```

### Refactor Existing Module

```
Refactor this Terraform module following best practices:

Current code:
[PASTE CODE]

Issues to address:
1. Add variable validation blocks
2. Add proper descriptions to all variables and outputs
3. Use locals for computed values
4. Add lifecycle rules where appropriate
5. Follow naming conventions: ${var.project_name}-${var.environment}-resource

Output:
- Refactored main.tf
- Updated variables.tf with validation
- Updated outputs.tf with descriptions
```

### Module Composition Design

```
Design a module composition strategy for:

Infrastructure components:
- [LIST COMPONENTS: VPC, EKS, RDS, etc.]

Requirements:
- Environments: dev, staging, prod
- Reusable across multiple projects
- Minimal blast radius per module
- Clear dependency graph

Provide:
1. Module directory structure
2. Root module composition example
3. Dependency flow diagram
4. Variable passing strategy
```

---

## State Management Prompts

### Configure Remote Backend

```
Create Terraform backend configuration for:

Cloud provider: [AWS/GCP/Azure]
Requirements:
- State encryption at rest
- State locking enabled
- Versioning enabled
- Environment: [ENVIRONMENT]
- Region: [REGION]

Include:
1. Backend configuration in backend.tf
2. Bootstrap script to create backend resources
3. IAM permissions needed for Terraform
```

### State Migration

```
Create a state migration plan for:

Current state: [LOCAL/S3/GCS/TERRAFORM_CLOUD]
Target state: [S3/GCS/TERRAFORM_CLOUD]

Existing resources:
[LIST OR DESCRIBE]

Provide:
1. Pre-migration checklist
2. Backend configuration files (before/after)
3. Migration commands
4. Verification steps
5. Rollback procedure
```

### Import Existing Resources

```
Create Terraform import strategy for:

Existing resources to import:
[LIST RESOURCES WITH IDs]

Requirements:
- Minimal disruption
- State consistency
- Proper resource addressing

Provide:
1. Resource definitions to add to .tf files
2. Import commands for each resource
3. Verification plan (terraform plan should show no changes)
```

---

## Testing Prompts

### Create Unit Tests

```
Create Terraform tests for this module:

Module code:
[PASTE main.tf, variables.tf, outputs.tf]

Test requirements:
1. Validate all variable constraints
2. Test default values
3. Test required outputs exist
4. Test resource counts for different configs

Use Terraform native testing (.tftest.hcl) with:
- command = plan for unit tests
- Meaningful assertion messages
- Multiple run blocks for different scenarios
```

### Create Integration Tests

```
Create integration tests for this module:

Module: [MODULE_NAME]
Purpose: [DESCRIPTION]

Test scenarios:
1. [SCENARIO 1]
2. [SCENARIO 2]
3. [SCENARIO 3]

Requirements:
- Use real resources (command = apply)
- Clean up after tests
- Test actual resource attributes
- Verify cross-resource dependencies
```

### Create Test with Mocking

```
Create mocked tests for this module to avoid creating real resources:

Module code:
[PASTE CODE]

Mock requirements:
- Mock all AWS/GCP/Azure resources
- Provide realistic mock values
- Test logic without cloud API calls

Use mock_provider blocks with mock_resource definitions.
```

---

## CI/CD Prompts

### Create GitHub Actions Workflow

```
Create a GitHub Actions workflow for Terraform with:

Repository structure:
infrastructure/
├── environments/{dev,staging,prod}/
├── modules/
└── tests/

Requirements:
1. Format check (terraform fmt)
2. Validation (terraform validate)
3. Module tests (terraform test)
4. Plan on PR with comment
5. Apply on merge to main (prod requires approval)

Include:
- OIDC authentication to AWS/GCP
- Proper job dependencies
- Artifact caching
- Secure secret handling
```

### Create GitLab CI Pipeline

```
Create a GitLab CI pipeline for Terraform with:

[SAME STRUCTURE AS ABOVE]

Use:
- gitlab-terraform image
- Terraform state in GitLab-managed backend OR S3/GCS
- Environment-specific deployments
- MR comments with plan output
```

### Drift Detection Workflow

```
Create a scheduled workflow for Terraform drift detection:

Requirements:
1. Run daily at [TIME]
2. Check all environments
3. Alert on drift via [SLACK/EMAIL/GITHUB_ISSUE]
4. Store drift reports

Include:
- Terraform plan with -detailed-exitcode
- Parsing of plan output
- Notification payload formatting
```

---

## Security Prompts

### Security Audit

```
Audit this Terraform configuration for security issues:

[PASTE CODE]

Check for:
1. Hardcoded secrets or credentials
2. Overly permissive IAM policies
3. Missing encryption configurations
4. Public access to private resources
5. Missing deletion protection on critical resources
6. Security groups with 0.0.0.0/0

Provide:
- List of issues with severity
- Remediation for each issue
- Updated code with fixes
```

### Create Least-Privilege IAM

```
Create least-privilege IAM policy for Terraform to manage:

Resources:
[LIST RESOURCES TO MANAGE]

Operations:
- Create
- Update
- Delete
- Read

Provide:
- IAM policy JSON
- Trust policy for CI/CD role assumption
- Explanation of each permission
```

### Secrets Management Integration

```
Integrate secrets management into this Terraform config:

Current code with hardcoded secrets:
[PASTE CODE]

Secrets manager: [AWS_SECRETS_MANAGER/HASHICORP_VAULT/GCP_SECRET_MANAGER]

Requirements:
- Remove all hardcoded secrets
- Use data sources to fetch secrets
- Handle secret rotation
- Document secret creation process
```

---

## Troubleshooting Prompts

### Debug Apply Error

```
Debug this Terraform error:

Error message:
[PASTE ERROR]

Context:
- Provider: [AWS/GCP/Azure]
- Resource type: [RESOURCE]
- Action: [CREATE/UPDATE/DELETE]

Current configuration:
[PASTE RELEVANT CONFIG]

Provide:
1. Root cause analysis
2. Fix options (ranked by preference)
3. Prevention strategy
```

### Fix State Issues

```
Help fix this Terraform state issue:

Symptoms:
[DESCRIBE ISSUE]

Current state:
terraform state list output:
[PASTE OUTPUT]

Expected vs actual:
[DESCRIBE DISCREPANCY]

Provide:
1. Diagnosis
2. Recovery commands
3. Verification steps
```

### Resolve Dependency Cycle

```
Resolve this dependency cycle in Terraform:

Error:
[PASTE CYCLE ERROR]

Resources involved:
[PASTE RESOURCE CONFIGS]

Provide:
1. Explanation of the cycle
2. Refactoring options
3. Recommended solution with code
```

---

## Migration Prompts

### CloudFormation to Terraform

```
Convert this CloudFormation template to Terraform:

CloudFormation template:
[PASTE YAML/JSON]

Requirements:
- Follow Terraform best practices
- Use modules where appropriate
- Parameterize environment-specific values
- Include state import commands for existing resources
```

### Terraform Version Upgrade

```
Upgrade this Terraform configuration:

Current version: [VERSION]
Target version: [VERSION]

Current code:
[PASTE CODE]

Provide:
1. Breaking changes to address
2. Deprecated features to update
3. New features to adopt
4. Updated code
5. Testing plan
```

### Provider Version Upgrade

```
Upgrade provider version in this configuration:

Provider: [PROVIDER_NAME]
Current version: [VERSION]
Target version: [VERSION]

Current code:
[PASTE CODE]

Provide:
1. Breaking changes to address
2. Deprecated resources/attributes
3. Updated code
4. Testing plan
```

---

## Documentation Prompts

### Generate Module Documentation

```
Generate comprehensive documentation for this Terraform module:

Module code:
[PASTE ALL MODULE FILES]

Include:
1. Overview and purpose
2. Architecture diagram (Mermaid)
3. Requirements table
4. Inputs table with defaults
5. Outputs table
6. Usage examples (basic and advanced)
7. Common issues and solutions
```

### Create Runbook

```
Create an operational runbook for this Terraform infrastructure:

Infrastructure overview:
[DESCRIBE]

Include:
1. Common operations (scale, update, rotate secrets)
2. Troubleshooting guide
3. Disaster recovery procedures
4. Monitoring and alerting setup
5. Maintenance windows and procedures
```
