# Terraform State LLM Prompts

AI-assisted prompts for Terraform state management tasks.

## Remote Backend Setup

### Configure S3 Backend

```
I need to configure an S3 backend for Terraform state with the following requirements:

Environment: [dev/staging/prod]
AWS Account: [account_id]
Region: [us-east-1]
Company Name: [company]
Component: [networking/compute/database]

Requirements:
- State locking with DynamoDB
- KMS encryption
- Cross-account access: [yes/no]
- State bucket already exists: [yes/no]

Please provide:
1. Backend configuration block
2. Required IAM policy
3. DynamoDB table configuration (if needed)
4. S3 bucket configuration (if needed)
```

### Migrate Local to Remote State

```
I need to migrate Terraform state from local to remote backend.

Current state: Local file (terraform.tfstate)
Target backend: [S3/GCS/Azure/TFC]
Backend details: [bucket/container name, region]

Please provide:
1. Backend configuration to add
2. Step-by-step migration commands
3. Verification steps
4. Rollback procedure if something goes wrong
```

## State Operations

### Import Existing Resources

```
I need to import existing infrastructure into Terraform state.

Resources to import:
- [Resource type]: [Resource ID]
- [Resource type]: [Resource ID]

Terraform version: [1.5+ / older]
Preferred method: [import blocks / CLI import]

Please provide:
1. Terraform configuration for each resource
2. Import blocks or import commands
3. Steps to verify successful import
4. How to generate configuration if unknown
```

### Refactor State Structure

```
I need to refactor my Terraform state structure.

Current structure:
[Describe current resource names/modules]

Target structure:
[Describe desired resource names/modules]

Changes needed:
- Rename: [old_name] -> [new_name]
- Move to module: [resource] -> module.[name]
- Split module: module.[old] -> module.[new1], module.[new2]

Please provide:
1. Moved blocks for each change
2. State commands as fallback
3. Verification steps
4. Order of operations to avoid issues
```

### Remove Resources from State

```
I need to remove resources from Terraform state without destroying them.

Resources to remove:
- [resource_address]
- [resource_address]

Reason: [moving to different state / manual management / etc.]

Please provide:
1. State rm commands for each resource
2. Backup commands to run first
3. Verification that resources still exist in cloud
4. Steps to re-import if needed later
```

## Troubleshooting

### State Lock Issues

```
I'm experiencing state lock issues with Terraform.

Error message:
[paste error message]

Backend type: [S3/GCS/Azure/TFC]
Lock mechanism: [DynamoDB/native]

Please help me:
1. Understand why the lock is held
2. Verify if another operation is running
3. Safely unlock if needed
4. Prevent this in the future
```

### State Corruption Recovery

```
My Terraform state appears corrupted or inconsistent.

Symptoms:
[describe what's happening]

Backend: [S3/GCS/Azure/TFC]
Versioning enabled: [yes/no]
Last known good state: [time/version]

Please provide:
1. How to diagnose the corruption
2. Steps to recover from backup
3. How to reconcile state with actual infrastructure
4. Prevention measures
```

### State Drift Detection

```
I need to detect and handle drift between Terraform state and actual infrastructure.

Environment: [env]
Components: [list of components]
Suspected drift: [what you think changed]

Please help me:
1. Detect all drift in the state
2. Generate a report of differences
3. Decide how to handle each drift (update state vs. update infrastructure)
4. Implement the chosen approach
```

## Security

### Audit State for Secrets

```
I need to audit my Terraform state for sensitive data exposure.

State location: [backend details]
Concerns: [passwords, API keys, certificates, etc.]

Please help me:
1. Identify sensitive data in state
2. Understand how it got there
3. Mitigate current exposure
4. Prevent future sensitive data in state
```

### Secure State Access

```
I need to implement secure access controls for Terraform state.

Cloud provider: [AWS/GCP/Azure]
Current access: [describe current setup]
Requirements:
- Least privilege access
- Audit logging
- Cross-account access: [yes/no]
- CI/CD access: [yes/no]

Please provide:
1. IAM policy/role configuration
2. Bucket/storage access policies
3. Audit logging configuration
4. CI/CD authentication setup (OIDC preferred)
```

## Multi-Environment

### Design State Structure

```
I need to design a state structure for multiple environments.

Environments: [dev, staging, prod]
Components: [networking, compute, database, etc.]
Teams: [describe team structure]
Blast radius concerns: [describe isolation needs]

Options to consider:
- Workspaces vs. separate backends
- Monorepo vs. multi-repo
- Shared vs. isolated state

Please recommend:
1. State structure diagram
2. Backend configuration for each environment
3. Access control strategy
4. Cross-environment data sharing approach
```

### Share Data Between States

```
I need to share data between separate Terraform states.

Source state: [env/component]
Data to share: [vpc_id, subnet_ids, etc.]
Target state: [env/component]

Please provide:
1. Outputs to add in source configuration
2. Remote state data source in target
3. Alternative approaches (SSM Parameter Store, etc.)
4. Security considerations
```

## CI/CD Integration

### Setup GitHub Actions for State

```
I need to configure GitHub Actions for Terraform with proper state management.

Cloud provider: [AWS/GCP/Azure]
Backend: [S3/GCS/Azure/TFC]
Workflow needs:
- Plan on PR
- Apply on merge to main
- State locking
- OIDC authentication

Please provide:
1. Complete GitHub Actions workflow
2. OIDC trust relationship configuration
3. IAM role/policy for GitHub Actions
4. Environment variables and secrets needed
```

### Implement State Locking in Pipelines

```
I'm experiencing state locking issues in CI/CD pipelines.

CI system: [GitHub Actions/GitLab CI/Jenkins]
Backend: [S3/GCS/Azure/TFC]
Issue: [concurrent runs, stuck locks, timeouts]

Please help me:
1. Implement proper concurrency controls
2. Configure appropriate lock timeouts
3. Handle lock failures gracefully
4. Monitor lock status
```

## Migration

### Migrate Between Backends

```
I need to migrate Terraform state between backends.

Source backend: [type and details]
Target backend: [type and details]
State size: [small/medium/large]
Downtime tolerance: [none/minimal/acceptable]

Please provide:
1. Pre-migration checklist
2. Step-by-step migration procedure
3. Validation steps
4. Rollback procedure
5. Post-migration cleanup
```

### Consolidate Multiple States

```
I need to consolidate multiple Terraform states into one.

Current states:
- [state1]: [resources]
- [state2]: [resources]
- [state3]: [resources]

Target: Single state with proper module structure

Please provide:
1. Target module structure
2. State move operations for each resource
3. Order of operations
4. Verification at each step
```

---

*Terraform State LLM Prompts | Part of terraform-state methodology*
