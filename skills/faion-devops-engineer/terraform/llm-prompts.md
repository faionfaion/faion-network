# Terraform LLM Prompts

Prompts for generating, reviewing, and troubleshooting Terraform code.

---

## Code Generation Prompts

### Generate Module

```
Generate a Terraform module for [RESOURCE_TYPE] with the following requirements:

Context:
- Cloud provider: [AWS/GCP/Azure]
- Terraform version: >= 1.6.0
- Provider version: ~> 5.0

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Include:
1. main.tf with all resources
2. variables.tf with descriptions and validations
3. outputs.tf with descriptions
4. versions.tf with provider constraints
5. README.md with usage example

Follow HashiCorp standard module structure.
Use snake_case for all names.
Add appropriate tags to all resources.
Include lifecycle rules where appropriate.
```

### Generate Infrastructure

```
Generate Terraform configuration for a [APPLICATION_TYPE] application:

Architecture:
- Environment: [dev/staging/prod]
- Region: [REGION]
- Components: [VPC, ECS, RDS, S3, etc.]

Requirements:
- [Requirement 1]
- [Requirement 2]

Constraints:
- Must follow security best practices
- Use remote state with S3 backend
- Include proper tagging strategy
- No hardcoded values

Output structure:
- environments/[env]/main.tf
- environments/[env]/variables.tf
- environments/[env]/outputs.tf
- environments/[env]/backend.tf
- modules/[component]/
```

### Generate Security Group

```
Generate Terraform aws_security_group for:

Service: [SERVICE_NAME]
Purpose: [PURPOSE]
VPC: Reference from variable

Ingress rules:
- [Port X from CIDR/SG for PURPOSE]
- [Port Y from CIDR/SG for PURPOSE]

Egress rules:
- [Specify or use default allow all]

Include:
- Descriptions for all rules
- Proper naming convention
- Tags with Name, Environment, ManagedBy
```

### Generate IAM Role

```
Generate Terraform IAM role and policy for:

Service: [SERVICE_NAME] (e.g., ECS task, Lambda, EC2)
Purpose: [PURPOSE]

Required permissions:
- [Action 1 on Resource 1]
- [Action 2 on Resource 2]

Constraints:
- Follow least privilege principle
- Add conditions where possible
- Use aws_iam_policy_document for policy
- Include trust policy for service
```

---

## Code Review Prompts

### Security Review

```
Review this Terraform code for security issues:

```hcl
[PASTE TERRAFORM CODE]
```

Check for:
1. Hardcoded secrets or credentials
2. Overly permissive IAM policies
3. Insecure network configurations (0.0.0.0/0)
4. Unencrypted resources
5. Missing access logging
6. Public exposure of resources
7. Missing deletion protection

For each issue found:
- Describe the risk
- Provide the fix
- Rate severity (High/Medium/Low)
```

### Best Practices Review

```
Review this Terraform code for best practices:

```hcl
[PASTE TERRAFORM CODE]
```

Check for:
1. Code organization and structure
2. Naming conventions
3. Variable usage and validations
4. Resource dependencies
5. Use of data sources
6. Tagging strategy
7. Lifecycle rules
8. State management considerations

Provide specific recommendations for improvement.
```

### Module Review

```
Review this Terraform module:

```hcl
[PASTE MODULE CODE]
```

Evaluate:
1. Does it follow HashiCorp standard structure?
2. Are inputs well-documented with descriptions?
3. Are outputs comprehensive?
4. Is the module focused (single responsibility)?
5. Are there appropriate validations?
6. Is it reusable across environments?
7. Are there any hardcoded values?

Suggest improvements for production readiness.
```

---

## Troubleshooting Prompts

### Debug Error

```
Help me debug this Terraform error:

Error message:
```
[PASTE ERROR MESSAGE]
```

Relevant code:
```hcl
[PASTE RELEVANT CODE]
```

Context:
- Terraform version: [VERSION]
- Provider version: [VERSION]
- Last successful apply: [WHEN]
- Recent changes: [WHAT CHANGED]

Provide:
1. Root cause analysis
2. Step-by-step fix
3. Prevention tips
```

### State Issue

```
Help me resolve this Terraform state issue:

Problem: [DESCRIBE THE ISSUE]
- Resource in state but not in config
- Resource in config but not in state
- State drift detected
- State locked
- Other: [DESCRIBE]

Current state output:
```
[PASTE terraform state list OR terraform state show OUTPUT]
```

Provide:
1. Diagnosis of the issue
2. Safe resolution steps
3. Commands to run (with explanations)
4. Backup/recovery recommendations
```

### Dependency Issue

```
Help me resolve this Terraform dependency issue:

Error message:
```
[PASTE ERROR]
```

Resources involved:
```hcl
[PASTE RELEVANT RESOURCES]
```

Problem type:
- Circular dependency
- Missing dependency
- Incorrect depends_on
- Ordering issue

Provide:
1. Explanation of the dependency problem
2. Refactored code to fix it
3. Best practices for managing dependencies
```

---

## Migration Prompts

### Migrate to Modules

```
Help me refactor this Terraform code into modules:

Current code:
```hcl
[PASTE CURRENT CODE]
```

Requirements:
- Create reusable modules
- Support multiple environments
- Maintain state compatibility
- Follow HashiCorp conventions

Provide:
1. Module structure recommendation
2. Refactored module code
3. Root module calling the modules
4. State migration commands (if needed)
```

### Import Resources

```
Help me import existing AWS resources into Terraform:

Resources to import:
- [Resource Type 1]: [Resource ID/ARN]
- [Resource Type 2]: [Resource ID/ARN]

Provide:
1. Terraform resource blocks to create
2. Import commands to run
3. Post-import verification steps
4. Tips for handling drift
```

### Upgrade Provider

```
Help me upgrade Terraform AWS provider from [OLD_VERSION] to [NEW_VERSION]:

Current configuration:
```hcl
[PASTE RELEVANT CONFIG]
```

Resources affected:
- [LIST KEY RESOURCES]

Provide:
1. Breaking changes to address
2. Deprecated resources/attributes to update
3. New features to leverage
4. Upgrade steps and testing approach
```

---

## Optimization Prompts

### Cost Optimization

```
Review this Terraform configuration for cost optimization:

```hcl
[PASTE TERRAFORM CODE]
```

Environment: [dev/staging/prod]
Monthly budget: [AMOUNT]

Analyze:
1. Right-sizing opportunities
2. Reserved capacity recommendations
3. Storage optimization
4. Network cost reduction
5. Unused resource identification

Provide estimated savings for each recommendation.
```

### Performance Optimization

```
Review this Terraform configuration for performance:

```hcl
[PASTE TERRAFORM CODE]
```

Current issues:
- [DESCRIBE PERFORMANCE ISSUES]

Check:
1. Instance types and sizing
2. Storage IOPS and throughput
3. Network bandwidth
4. Caching opportunities
5. Multi-AZ and load balancing
6. Auto-scaling configuration

Provide optimized configuration.
```

### Code Optimization

```
Optimize this Terraform code for maintainability:

```hcl
[PASTE TERRAFORM CODE]
```

Goals:
- Reduce duplication
- Improve readability
- Add reusability
- Simplify complexity

Provide:
1. Refactored code using for_each, dynamic blocks, locals
2. Explanation of changes
3. Before/after comparison
```

---

## Documentation Prompts

### Generate Documentation

```
Generate documentation for this Terraform module:

```hcl
[PASTE MODULE CODE]
```

Include:
1. README.md with:
   - Description
   - Usage example
   - Requirements table
   - Inputs table (from variables.tf)
   - Outputs table (from outputs.tf)
   - Resources created
2. CHANGELOG template
3. CONTRIBUTING guidelines
```

### Generate ADR

```
Generate an Architecture Decision Record for this Terraform decision:

Decision: [DESCRIBE THE DECISION]
Context: [DESCRIBE THE CONTEXT]
Alternatives considered:
- [Alternative 1]
- [Alternative 2]

Include:
1. Title
2. Status
3. Context
4. Decision
5. Consequences
6. Alternatives considered with pros/cons
```

---

## Template Prompts

### Generate tfvars Template

```
Generate terraform.tfvars.example for this configuration:

```hcl
[PASTE variables.tf]
```

Include:
1. All required variables with example values
2. Optional variables commented out
3. Comments explaining each variable
4. Environment-specific examples (dev/prod)
```

### Generate CI/CD Pipeline

```
Generate CI/CD pipeline for Terraform:

Platform: [GitHub Actions/GitLab CI/Jenkins]
Cloud: [AWS/GCP/Azure]
Environments: [dev, staging, prod]

Requirements:
- Format and validate on PR
- Security scanning (tfsec, checkov)
- Plan on PR with output comment
- Apply on merge to main
- Environment-specific approvals
- OIDC authentication (no long-lived credentials)

Provide complete pipeline configuration.
```
