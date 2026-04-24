# Terraform Checklists

**Production Readiness, Security Hardening, and Verification (2025-2026)**

---

## State Management Checklist

### Remote Backend Setup

- [ ] Remote backend configured (S3, GCS, Azure, Terraform Cloud)
- [ ] State locking enabled (DynamoDB for S3, native for GCS/TFC)
- [ ] Encryption at rest enabled (KMS, customer-managed keys)
- [ ] Encryption in transit (HTTPS only)
- [ ] Bucket versioning enabled for state recovery
- [ ] Access control configured (IAM policies, least privilege)
- [ ] Audit logging enabled (CloudTrail, Cloud Audit Logs)
- [ ] Cross-region replication (for disaster recovery)

### State Security

- [ ] No secrets stored in plain text in state
- [ ] Sensitive outputs marked with `sensitive = true`
- [ ] State file access restricted to CI/CD service accounts
- [ ] Regular state backup strategy defined
- [ ] State recovery procedure documented and tested
- [ ] No state files committed to git (.gitignore)

### State Organization

- [ ] Separate state files per environment (dev/staging/prod)
- [ ] Separate state files per component (networking/compute/db)
- [ ] Blast radius minimized (small, focused states)
- [ ] Remote state data sources used for cross-stack references
- [ ] State file naming convention defined

---

## Module Checklist

### Module Structure

- [ ] Standard file layout (main.tf, variables.tf, outputs.tf, versions.tf)
- [ ] README.md with description, inputs, outputs, examples
- [ ] examples/ directory with usage examples
- [ ] versions.tf with required_version and required_providers
- [ ] All inputs documented with descriptions
- [ ] All outputs documented with descriptions
- [ ] Validation rules on variables where appropriate

### Module Design (2025-2026)

- [ ] Single responsibility (one logical component)
- [ ] Small blast radius (limited resources per module)
- [ ] No hardcoded values (parameterize everything)
- [ ] Sensible defaults for optional variables
- [ ] Versioned with semantic versioning tags
- [ ] Published to private registry (if shared)
- [ ] Tested with terraform test or Terratest

### Module Security

- [ ] No secrets in module code
- [ ] Sensitive variables marked as sensitive
- [ ] Minimal IAM permissions documented
- [ ] Security best practices encoded (encryption, access control)
- [ ] Compliance requirements met (tagging, encryption)

---

## Workspace Checklist

### Workspace Setup

- [ ] Workspace strategy defined (CLI, directory, TFC)
- [ ] Workspace naming convention established
- [ ] Environment-specific tfvars files created
- [ ] Backend configuration per workspace (if separate)
- [ ] Variable precedence understood and documented

### Workspace Security

- [ ] Workspace access controlled per environment
- [ ] Production workspace protected (approval required)
- [ ] Workspace-specific secrets isolated
- [ ] Audit logging per workspace

### Workspace Limitations Awareness

- [ ] Understand workspaces share backend configuration
- [ ] Use separate directories for true isolation if needed
- [ ] Document workspace vs directory decision

---

## CI/CD Pipeline Checklist

### Pre-commit / PR Checks

- [ ] terraform fmt -check passes
- [ ] terraform validate passes
- [ ] tflint passes (with provider plugins)
- [ ] tfsec or Checkov security scan passes
- [ ] terraform plan runs successfully
- [ ] Plan output posted to PR for review
- [ ] Infracost estimate (optional)

### Security Scanning

- [ ] tfsec integrated in pipeline
- [ ] Checkov integrated in pipeline
- [ ] No CRITICAL/HIGH findings (or approved exceptions)
- [ ] Secret scanning for exposed credentials
- [ ] SBOM generated for modules (if using containers)

### Apply Stage

- [ ] Plan saved as artifact (`-out=tfplan`)
- [ ] Exact plan applied (not re-planned)
- [ ] Human approval required for production
- [ ] Apply output logged
- [ ] Post-apply verification (health checks, smoke tests)

### Version Control

- [ ] .terraform.lock.hcl committed
- [ ] Provider versions pinned
- [ ] Module versions pinned
- [ ] Terraform version pinned in versions.tf
- [ ] Dependabot/Renovate for controlled updates

### Rollback and Recovery

- [ ] Previous state versions available
- [ ] Rollback procedure documented
- [ ] Rollback tested in non-prod
- [ ] Break-glass procedure for emergencies

---

## Security Hardening Checklist

### Code Security

- [ ] No hardcoded secrets in any .tf files
- [ ] No secrets in terraform.tfvars (use env vars or vault)
- [ ] Sensitive variables marked `sensitive = true`
- [ ] Sensitive outputs marked `sensitive = true`
- [ ] No curl | bash or similar in provisioners
- [ ] Checksums verified for external resources

### Provider Security

- [ ] Provider versions pinned with constraints
- [ ] Official/verified providers only
- [ ] Provider credentials via environment variables
- [ ] No credentials in .tf files or tfvars
- [ ] Assume role used for cross-account (AWS)

### Infrastructure Security

- [ ] Encryption enabled on all storage (S3, RDS, etc.)
- [ ] Network security groups restrictive
- [ ] No 0.0.0.0/0 in security groups (unless intentional)
- [ ] IAM roles follow least privilege
- [ ] Public access blocked by default
- [ ] Logging enabled on all resources
- [ ] Tagging policy enforced

### Policy as Code

- [ ] Sentinel policies (Terraform Cloud/Enterprise)
- [ ] OPA/Conftest policies (open source)
- [ ] Policies enforced in CI/CD
- [ ] Policy exceptions documented and approved

---

## Production Deployment Checklist

### Pre-deployment

- [ ] terraform plan reviewed by team
- [ ] No unexpected destroys or replacements
- [ ] Cost impact assessed (Infracost)
- [ ] Change management ticket created
- [ ] Rollback plan documented
- [ ] Maintenance window scheduled (if needed)

### Deployment

- [ ] Apply from saved plan artifact
- [ ] Apply runs in isolated environment
- [ ] Credentials rotated after deploy (if exposed)
- [ ] Deployment logged and auditable
- [ ] Team notified of deployment

### Post-deployment

- [ ] Health checks pass
- [ ] Smoke tests pass
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Post-mortem if issues occurred

---

## Code Quality Checklist

### Formatting and Style

- [ ] terraform fmt applied
- [ ] Consistent naming conventions
- [ ] Variables in alphabetical order
- [ ] Outputs in alphabetical order
- [ ] Resources grouped logically
- [ ] Comments for complex logic

### Documentation

- [ ] README.md in root and each module
- [ ] terraform-docs generated
- [ ] Architecture diagrams updated
- [ ] Runbook for common operations
- [ ] ADR for significant decisions

### Testing

- [ ] terraform validate passes
- [ ] terraform plan -detailed-exitcode in CI
- [ ] terraform test (native tests) if available
- [ ] Terratest for integration testing
- [ ] Drift detection scheduled

---

## Compliance Checklist

### Tagging

- [ ] All resources tagged
- [ ] Required tags: Environment, Project, Owner, ManagedBy
- [ ] Cost allocation tags applied
- [ ] Tagging policy enforced via policy-as-code

### Audit and Logging

- [ ] CloudTrail enabled (AWS)
- [ ] Cloud Audit Logs enabled (GCP)
- [ ] Activity Log enabled (Azure)
- [ ] State access logged
- [ ] Terraform apply logged

### Regulatory

- [ ] Encryption requirements met
- [ ] Data residency requirements met
- [ ] Access control requirements met
- [ ] Retention policies configured
- [ ] Compliance validated (SOC2, PCI, HIPAA)

---

## Quick Verification Commands

```bash
# Format check
terraform fmt -check -recursive -diff

# Validate
terraform validate

# Lint
tflint --init
tflint

# Security scan
tfsec .
checkov -d .

# Plan (detailed exit code: 0=no changes, 1=error, 2=changes)
terraform plan -detailed-exitcode

# List resources
terraform state list

# Show resource details
terraform state show aws_instance.web

# Verify provider versions
terraform providers

# Generate docs
terraform-docs markdown table . > README.md

# Cost estimate
infracost breakdown --path .

# Graph
terraform graph | dot -Tpng > graph.png
```

---

## Compliance Mapping

| Standard | Key Requirements |
|----------|------------------|
| **CIS Benchmarks** | Encryption, access control, logging |
| **SOC 2** | Change management, audit logs, access control |
| **PCI-DSS** | Encryption, network segmentation, logging |
| **HIPAA** | Encryption, access control, audit trails |
| **GDPR** | Data residency, encryption, access logs |
| **FedRAMP** | All of the above + government-specific |

---

*Terraform Checklists | faion-infrastructure-engineer*
