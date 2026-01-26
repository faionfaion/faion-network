# Terraform State Checklists

## Remote Backend Setup Checklist

### Pre-Configuration

- [ ] Identify team collaboration requirements
- [ ] Choose appropriate backend (S3, GCS, Azure, TFC)
- [ ] Determine environment isolation strategy (workspaces vs separate backends)
- [ ] Plan state file naming convention (`{env}/{component}/terraform.tfstate`)
- [ ] Define access control requirements (IAM policies/roles)

### Backend Infrastructure (AWS S3 Example)

- [ ] Create S3 bucket with unique name
- [ ] Enable bucket versioning
- [ ] Enable server-side encryption (SSE-S3 or SSE-KMS)
- [ ] Block all public access
- [ ] Create DynamoDB table for state locking
- [ ] Configure IAM policy with least privilege
- [ ] Test backend access from CI/CD environment

### Backend Configuration

- [ ] Add backend block to Terraform configuration
- [ ] Configure encryption settings
- [ ] Configure locking mechanism
- [ ] Run `terraform init` to initialize backend
- [ ] Verify state migration (if migrating from local)
- [ ] Test state operations from multiple machines

## State Security Checklist

### Encryption

- [ ] Enable encryption at rest on storage backend
- [ ] Use KMS/customer-managed keys for sensitive workloads
- [ ] Enable TLS for state transfer (default in most backends)
- [ ] Verify encryption is active (`aws s3api get-bucket-encryption`)

### Access Control

- [ ] Implement least-privilege IAM policies
- [ ] Use role assumption for cross-account access
- [ ] Restrict state bucket access to Terraform roles only
- [ ] Enable access logging on state bucket
- [ ] Review access policies quarterly

### Sensitive Data

- [ ] Mark sensitive outputs with `sensitive = true`
- [ ] Use external secret managers (Vault, AWS Secrets Manager)
- [ ] Never store secrets directly in state
- [ ] Audit state for accidentally committed secrets
- [ ] Use `terraform show -json | jq` to inspect sensitive values

## State Operations Checklist

### Before Any State Operation

- [ ] Backup current state (`terraform state pull > backup.tfstate`)
- [ ] Verify backup is valid (`terraform show backup.tfstate`)
- [ ] Communicate with team (prevent concurrent operations)
- [ ] Acquire state lock (automatic with remote backends)

### After State Operation

- [ ] Run `terraform plan` to verify no unexpected changes
- [ ] Verify resource count matches expectations
- [ ] Check for drift (`terraform plan` shows no changes)
- [ ] Document operation in change log

## Import Existing Resources Checklist

### Pre-Import

- [ ] Identify all resources to import
- [ ] Gather resource IDs from cloud console/CLI
- [ ] Write Terraform configuration for each resource
- [ ] Create import blocks (Terraform 1.5+) or prepare import commands

### Import Process

- [ ] Run `terraform plan` with import blocks
- [ ] Review planned import operations
- [ ] Apply import (`terraform apply`)
- [ ] Verify imported resources match configuration
- [ ] Run `terraform plan` again (should show no changes)

### Post-Import

- [ ] Review state for completeness
- [ ] Update configuration to match actual resource settings
- [ ] Add missing arguments discovered during import
- [ ] Document any manual adjustments

## State Migration Checklist

### Local to Remote Migration

- [ ] Configure new remote backend block
- [ ] Run `terraform init -migrate-state`
- [ ] Confirm migration prompt
- [ ] Verify state in remote backend
- [ ] Delete local state file after verification
- [ ] Update `.gitignore` to exclude `*.tfstate*`

### Backend to Backend Migration

- [ ] Backup current state from source backend
- [ ] Update backend configuration to target
- [ ] Run `terraform init -migrate-state`
- [ ] Verify state in target backend
- [ ] Test `terraform plan` shows no changes
- [ ] Remove state from source backend (optional)

## Disaster Recovery Checklist

### Backup Strategy

- [ ] Enable versioning on state storage
- [ ] Configure lifecycle policy for version retention
- [ ] Document state file locations for all environments
- [ ] Test state recovery procedure quarterly

### Recovery Procedure

- [ ] Identify last known good state version
- [ ] Download state version (`aws s3api get-object --version-id`)
- [ ] Verify state integrity
- [ ] Push recovered state (`terraform state push`)
- [ ] Run `terraform plan` to verify consistency
- [ ] Document incident and recovery steps

## CI/CD Integration Checklist

### Pipeline Setup

- [ ] Configure backend credentials (OIDC preferred over static keys)
- [ ] Set `TF_IN_AUTOMATION=true` environment variable
- [ ] Implement plan/apply separation (review before apply)
- [ ] Configure state locking timeout appropriately
- [ ] Add plan output as PR comment

### Security

- [ ] Use OIDC for cloud provider authentication
- [ ] Never store backend credentials in code
- [ ] Rotate service account keys regularly
- [ ] Audit pipeline access to state

---

*Terraform State Checklists | Part of terraform-state methodology*
