# Terraform Basics Checklist

## Project Setup

- [ ] Create standard file structure (versions.tf, providers.tf, variables.tf, main.tf, outputs.tf)
- [ ] Define Terraform version constraint (`required_version = ">= 1.5.0"`)
- [ ] Configure required providers with version constraints
- [ ] Set up remote backend for state storage
- [ ] Add `.terraform/` and `*.tfstate*` to `.gitignore`
- [ ] Check in `.terraform.lock.hcl` for provider version consistency
- [ ] Configure pre-commit hooks for `terraform fmt` and `terraform validate`

## Provider Configuration

- [ ] Pin provider versions with pessimistic constraint (`~> 5.0`)
- [ ] Configure default tags (ManagedBy, Project, Environment)
- [ ] Set up provider aliases for multi-region deployments
- [ ] Use environment variables or assume roles for credentials (never hardcode)
- [ ] Document provider authentication requirements

## Variables

- [ ] Add description to all variables
- [ ] Specify type constraints (string, number, bool, list, map, object)
- [ ] Set sensible defaults where appropriate
- [ ] Mark sensitive variables with `sensitive = true`
- [ ] Add validation blocks for input validation
- [ ] Create `terraform.tfvars.example` with sample values
- [ ] Never commit actual `terraform.tfvars` with secrets

## Resources

- [ ] Use consistent naming convention: `{project}-{env}-{resource}-{index}`
- [ ] Apply common tags via locals
- [ ] Use `for_each` over `count` when resources need unique identifiers
- [ ] Add explicit `depends_on` only when implicit dependencies are insufficient
- [ ] Configure lifecycle rules (prevent_destroy for critical resources)
- [ ] Add pre/postconditions for validation
- [ ] Avoid provisioners (use cloud-init, user data instead)

## Data Sources

- [ ] Use data sources for dynamic lookups (AMIs, AZs, account info)
- [ ] Add filters to narrow results
- [ ] Handle empty results gracefully
- [ ] Prefer data sources over hardcoded values

## Outputs

- [ ] Export all values needed by other configurations
- [ ] Add descriptions to outputs
- [ ] Mark sensitive outputs with `sensitive = true`
- [ ] Use consistent naming (snake_case, descriptive)

## State Management

- [ ] Configure remote backend (S3+DynamoDB, GCS, Terraform Cloud)
- [ ] Enable state locking
- [ ] Enable encryption at rest
- [ ] Set up state file backup
- [ ] Document state recovery procedures

## Security

- [ ] Never store secrets in code or state
- [ ] Use secret managers (AWS Secrets Manager, HashiCorp Vault)
- [ ] Enable encryption for storage resources
- [ ] Restrict network access (no 0.0.0.0/0 unless required)
- [ ] Apply least privilege IAM policies
- [ ] Review security groups for overly permissive rules

## Code Quality

- [ ] Run `terraform fmt -recursive` before committing
- [ ] Run `terraform validate` to check syntax
- [ ] Generate and review plan before apply
- [ ] Use consistent indentation (2 spaces)
- [ ] Group related resources in logical files
- [ ] Add comments for non-obvious configurations

## Testing

- [ ] Validate configuration with `terraform validate`
- [ ] Review plan output carefully
- [ ] Test in non-production environment first
- [ ] Use Terratest for automated testing
- [ ] Check for drift regularly

## CI/CD Integration

- [ ] Run `terraform fmt -check` in CI
- [ ] Run `terraform validate` in CI
- [ ] Generate plan on pull requests
- [ ] Require plan review before apply
- [ ] Store plan artifacts
- [ ] Apply only from CI (not local machines)

## Documentation

- [ ] Document module inputs and outputs
- [ ] Add README with usage examples
- [ ] Document provider requirements
- [ ] Keep architecture diagrams updated
- [ ] Document state backend configuration

---

*Terraform Basics Checklist | Part of faion-infrastructure-engineer skill*
