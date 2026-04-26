# IaC Patterns Checklist

## Module Design

### Structure
- [ ] Single responsibility - module does one thing well
- [ ] Clear naming convention (`{provider}_{resource}` or `{purpose}`)
- [ ] Standard file layout (main.tf, variables.tf, outputs.tf, versions.tf)
- [ ] README.md with usage examples
- [ ] CHANGELOG.md for version history
- [ ] examples/ directory with working configurations

### Variables
- [ ] All variables have descriptions
- [ ] Sensible defaults where appropriate
- [ ] Validation rules for complex inputs
- [ ] Type constraints defined
- [ ] Sensitive variables marked as `sensitive = true`
- [ ] No hardcoded environment-specific values

### Outputs
- [ ] All outputs have descriptions
- [ ] Minimal but sufficient outputs exposed
- [ ] Sensitive outputs marked appropriately
- [ ] Output names follow consistent pattern

### Documentation
- [ ] Module purpose clearly stated
- [ ] All inputs documented
- [ ] All outputs documented
- [ ] Usage examples provided
- [ ] Requirements/dependencies listed

## DRY Principles

### Code Reuse
- [ ] No copy-pasted resource blocks
- [ ] Common patterns extracted to modules
- [ ] Locals used for computed values
- [ ] for_each/count for similar resources
- [ ] Dynamic blocks for repeated nested structures

### Configuration
- [ ] Environment differences parameterized
- [ ] Common tags defined in locals
- [ ] Naming conventions use prefix/suffix variables
- [ ] Region/account agnostic where possible

### Module Versioning
- [ ] Semantic versioning used (vMAJOR.MINOR.PATCH)
- [ ] Version constraints in module calls
- [ ] Breaking changes bump major version
- [ ] Migration guide for major versions

## Composition Patterns

### Module Composition
- [ ] Dependencies passed as inputs (not hardcoded)
- [ ] Data sources used for existing resources
- [ ] Module outputs chain to dependent modules
- [ ] Clear separation between base/core/app modules

### Wrapper Modules
- [ ] Org-specific defaults enforced
- [ ] Security policies embedded
- [ ] Compliance requirements baked in
- [ ] Simplified interface for consumers

### Facade Pattern
- [ ] Complex orchestration hidden
- [ ] Simple API exposed
- [ ] Multiple modules coordinated internally
- [ ] Sensible defaults reduce required inputs

## Testing

### Static Analysis
- [ ] `terraform fmt` applied
- [ ] `terraform validate` passes
- [ ] `tflint` configured and passes
- [ ] `checkov`/`tfsec` security scanning
- [ ] No provider credentials in code

### Unit Testing (terraform test)
- [ ] Test files in tests/ directory
- [ ] Input validation tested
- [ ] Output contracts verified
- [ ] Mock providers for unit tests
- [ ] Plan-only tests for quick feedback

### Integration Testing
- [ ] Dedicated test environment
- [ ] Resources actually deployed
- [ ] Functionality validated
- [ ] Resources cleaned up after test
- [ ] Tests run in CI pipeline

### Policy Testing
- [ ] OPA/Conftest policies defined
- [ ] Security policies enforced
- [ ] Cost policies applied
- [ ] Naming conventions validated
- [ ] Tag requirements checked

## State Management

### Remote State
- [ ] Backend configured (S3, GCS, Azure Blob)
- [ ] State locking enabled (DynamoDB, etc.)
- [ ] Encryption at rest enabled
- [ ] Access controls configured
- [ ] State file never committed to git

### State Isolation
- [ ] Separate state per environment
- [ ] Separate state per component (where appropriate)
- [ ] Remote state data sources for dependencies
- [ ] State file naming convention consistent

### State Operations
- [ ] `terraform state` commands documented
- [ ] Import procedures documented
- [ ] State migration plan for refactors
- [ ] Backup before destructive operations

## CI/CD Integration

### Pipeline Steps
- [ ] Format check (terraform fmt -check)
- [ ] Validate (terraform validate)
- [ ] Lint (tflint)
- [ ] Security scan (checkov/tfsec)
- [ ] Plan on PR
- [ ] Apply on merge (with approval gates)

### Security
- [ ] Credentials from vault/secrets manager
- [ ] No secrets in state (use data sources)
- [ ] OIDC for cloud authentication
- [ ] Least privilege for pipeline service account
- [ ] Audit logging enabled

### Workflows
- [ ] PR requires plan output
- [ ] Plan reviewed before apply
- [ ] Apply only from main/protected branch
- [ ] Drift detection scheduled
- [ ] Automated formatting PRs

## Production Readiness

### Reliability
- [ ] Multi-AZ/region where appropriate
- [ ] Backup/recovery tested
- [ ] Disaster recovery plan documented
- [ ] Health checks configured

### Security
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Network segmentation
- [ ] IAM least privilege
- [ ] Security groups/firewall rules minimized

### Observability
- [ ] Logging enabled
- [ ] Metrics exposed
- [ ] Alerting configured
- [ ] Cost monitoring enabled

### Compliance
- [ ] Required tags applied
- [ ] Naming conventions followed
- [ ] Region restrictions respected
- [ ] Data residency requirements met

---

*IaC Patterns Checklist | faion-infrastructure-engineer*
