# Terraform Basics LLM Prompts

## Project Setup

### Initialize New Terraform Project

```
Create a new Terraform project for [CLOUD_PROVIDER: AWS/GCP/Azure] with:

Project: [PROJECT_NAME]
Environment: [dev/staging/prod]
Region: [REGION]

Requirements:
- [List specific infrastructure needs]

Generate:
1. versions.tf with provider constraints
2. providers.tf with default tags
3. variables.tf with validation
4. main.tf skeleton
5. outputs.tf
6. locals.tf with common tags
7. terraform.tfvars.example
8. .gitignore

Follow Terraform best practices:
- Pin provider versions with ~>
- Use snake_case naming
- Add descriptions to all variables and outputs
- Mark sensitive values appropriately
```

### Add Remote State Backend

```
Configure remote state backend for existing Terraform project:

Cloud: [AWS S3/GCP GCS/Azure Blob/Terraform Cloud]
State bucket: [BUCKET_NAME]
Lock table: [TABLE_NAME] (if AWS)
Region: [REGION]

Generate:
1. Backend configuration block
2. State bucket resource (if creating new)
3. Lock table resource (if AWS DynamoDB)
4. IAM policy for state access

Include encryption at rest and state locking.
```

---

## Provider Configuration

### Configure Multi-Region Provider

```
Set up multi-region AWS provider configuration:

Primary region: [PRIMARY_REGION]
Secondary regions: [LIST_OF_REGIONS]

Requirements:
- Default tags on all providers
- Assume role configuration: [ROLE_ARN] (if applicable)
- Profile: [PROFILE_NAME] (if applicable)

Generate provider blocks with aliases and show example usage for cross-region resources.
```

### Configure Multi-Cloud Providers

```
Create Terraform configuration for multi-cloud deployment:

Clouds:
- AWS: region [REGION], role [ROLE_ARN]
- GCP: project [PROJECT], region [REGION]
- Azure: subscription [SUBSCRIPTION_ID]

Generate:
1. Provider requirements in terraform block
2. Provider configurations
3. Example data sources from each cloud
```

---

## Resource Creation

### Create VPC with Subnets

```
Generate Terraform code for VPC infrastructure:

Cloud: [AWS/GCP/Azure]
CIDR: [VPC_CIDR]
Availability zones: [COUNT]
Subnet types: [public, private, database]

Requirements:
- Internet gateway
- NAT gateway (single/per-AZ)
- Route tables
- Proper tagging

Use count or for_each appropriately. Follow naming convention: {project}-{env}-{resource}.
```

### Create Compute Resources

```
Generate Terraform code for [EC2/GCE/Azure VM] instances:

Count: [NUMBER]
Instance type: [TYPE]
AMI/Image: [AMI_ID or lookup criteria]
Subnet placement: [public/private]

Include:
- Security group with [PORTS]
- Key pair reference
- User data script for [BOOTSTRAP_TASK]
- EBS/disk encryption
- Proper tagging
- Lifecycle rules

Use data source for AMI lookup if not provided.
```

### Create Database Resources

```
Generate Terraform code for managed database:

Engine: [postgres/mysql/mariadb]
Version: [VERSION]
Instance class: [CLASS]
Storage: [SIZE_GB]

Security:
- Private subnet placement
- Security group (port [PORT] from app subnets only)
- Encrypted storage
- Password from [secrets manager/variable]

Backup:
- Retention: [DAYS]
- Backup window: [WINDOW]

Include subnet group and parameter group if needed.
```

### Create S3/Storage Bucket

```
Generate Terraform code for object storage:

Cloud: [AWS S3/GCP GCS/Azure Blob]
Bucket name: [NAME]

Configuration:
- Versioning: [enabled/disabled]
- Encryption: [AES256/KMS with key ARN]
- Public access: [blocked/specific policy]
- Lifecycle rules: [RULES]
- CORS: [CORS_CONFIG] (if applicable)
- Replication: [DESTINATION] (if applicable)

Include all security best practices.
```

---

## Variables and Outputs

### Design Variable Structure

```
Design input variables for Terraform module:

Module purpose: [DESCRIPTION]

Required inputs:
- [VAR1]: [TYPE] - [DESCRIPTION]
- [VAR2]: [TYPE] - [DESCRIPTION]

Optional inputs with defaults:
- [VAR3]: [TYPE] = [DEFAULT] - [DESCRIPTION]

Generate variables.tf with:
- Type constraints
- Descriptions
- Defaults where appropriate
- Validation rules
- Sensitive marking

Also generate terraform.tfvars.example.
```

### Design Output Structure

```
Design outputs for Terraform configuration:

Resources created:
- [RESOURCE_1]
- [RESOURCE_2]

Consumers of outputs:
- [Other Terraform configs/modules]
- [CI/CD pipelines]
- [Applications]

Generate outputs.tf with:
- Descriptive names (snake_case)
- Descriptions
- Sensitive marking where needed
- Grouped by resource type
```

---

## Data Sources

### Create Data Source Queries

```
Create Terraform data sources for:

1. Latest AMI for [OS_TYPE] in [REGION]
2. Available availability zones in current region
3. Current AWS account ID and region
4. Secret value from [AWS Secrets Manager/SSM Parameter Store]
5. Existing VPC by tag: [TAG_KEY]=[TAG_VALUE]

Generate data blocks with appropriate filters and show usage examples.
```

### External Data Integration

```
Create data source to fetch external data:

Source: [API endpoint/script/file]
Data needed: [DESCRIPTION]
Format: [JSON/text]

Generate:
1. http or external data source
2. Locals to parse the response
3. Example usage in resources
```

---

## Code Review and Refactoring

### Review Terraform Configuration

```
Review this Terraform configuration for:

[PASTE_TERRAFORM_CODE]

Check for:
1. Security issues (hardcoded secrets, overly permissive access)
2. Best practices violations
3. Missing lifecycle rules
4. Improper resource dependencies
5. Naming convention issues
6. Missing tags
7. Hardcoded values that should be variables
8. Missing outputs
9. State management concerns

Provide specific recommendations with code examples.
```

### Refactor to Use for_each

```
Refactor this Terraform code from count to for_each:

[PASTE_TERRAFORM_CODE]

Current issues:
- [Describe issues with current approach]

Requirements:
- Stable resource addresses
- Meaningful resource keys
- Handle the conversion safely

Provide refactored code and migration steps.
```

### Convert to Module

```
Convert this Terraform configuration into a reusable module:

[PASTE_TERRAFORM_CODE]

Module requirements:
- Name: [MODULE_NAME]
- Purpose: [DESCRIPTION]
- Consumers: [WHO_WILL_USE]

Generate:
1. Module file structure
2. variables.tf with all inputs
3. main.tf with resources
4. outputs.tf
5. README.md with usage example
6. Example calling code
```

---

## Troubleshooting

### Debug Terraform Error

```
Help debug this Terraform error:

Error message:
[PASTE_ERROR]

Configuration:
[PASTE_RELEVANT_CODE]

Context:
- Operation: [init/plan/apply/destroy]
- Provider version: [VERSION]
- Terraform version: [VERSION]

Explain:
1. What the error means
2. Common causes
3. Solution steps
4. Prevention strategies
```

### Fix State Issues

```
Help resolve Terraform state issue:

Problem: [DESCRIPTION]
- Resource: [RESOURCE_ADDRESS]
- Actual state: [WHAT_EXISTS]
- Terraform state: [WHAT_TF_THINKS]

Options to consider:
1. terraform import
2. terraform state rm
3. terraform state mv
4. Manual state file edit (last resort)

Provide safest resolution approach with exact commands.
```

### Plan Analysis

```
Analyze this Terraform plan output:

[PASTE_PLAN_OUTPUT]

Identify:
1. Resources being created/modified/destroyed
2. Potential issues or unexpected changes
3. Resources with force replacement
4. Sensitive data exposure risks
5. Cost implications (if applicable)

Recommend:
- Whether this plan is safe to apply
- Any changes needed before apply
- Resources to watch carefully
```

---

## CI/CD Integration

### Generate CI/CD Pipeline

```
Generate [GitHub Actions/GitLab CI/Azure DevOps] pipeline for Terraform:

Workflow:
1. On PR: format check, validate, plan
2. On merge to main: apply to [staging]
3. Manual approval for [prod]

Requirements:
- State backend: [TYPE]
- Credentials: [SECRET_NAMES]
- Working directory: [PATH]
- Terraform version: [VERSION]

Include:
- Plan output as PR comment
- Artifact storage for plans
- Manual approval gates
- Rollback strategy
```

### Pre-commit Hooks

```
Generate pre-commit configuration for Terraform:

Checks needed:
- terraform fmt
- terraform validate
- tflint
- tfsec/checkov
- terraform-docs

Generate:
1. .pre-commit-config.yaml
2. .tflint.hcl
3. Installation instructions
```

---

## Security

### Security Audit

```
Perform security audit on Terraform configuration:

[PASTE_TERRAFORM_CODE]

Check for:
1. Hardcoded credentials or secrets
2. Overly permissive IAM policies
3. Public access to private resources
4. Missing encryption (at rest and in transit)
5. Overly permissive security groups
6. Missing logging and monitoring
7. Non-compliant resource configurations

Provide:
- Severity rating for each finding
- Remediation code
- Compliance framework references (CIS, SOC2, etc.)
```

### Generate Secure Configuration

```
Generate security-hardened Terraform configuration for:

Resource: [RESOURCE_TYPE]
Compliance: [CIS/SOC2/HIPAA/PCI-DSS]

Requirements:
- Encryption at rest
- Encryption in transit
- Least privilege access
- Logging enabled
- Monitoring configured

Include all security controls with explanatory comments.
```

---

## Quick Reference Prompts

### Syntax Help

```
Show Terraform syntax for [TOPIC]:
- [Dynamic blocks/for_each/count/conditionals/functions]

Include:
- Basic syntax
- Common use cases
- Edge cases to watch for
- Examples
```

### Function Usage

```
Explain Terraform function: [FUNCTION_NAME]

Include:
- Syntax
- Parameters
- Return type
- 3 practical examples
- Common mistakes
```

### Provider Resource Reference

```
Show complete Terraform reference for:

Provider: [PROVIDER]
Resource: [RESOURCE_TYPE]

Include:
- All arguments (required and optional)
- Attributes exported
- Common configurations
- Best practices
- Example code
```

---

*Terraform Basics LLM Prompts | Part of faion-infrastructure-engineer skill*
