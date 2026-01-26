# IaC Implementation Checklist

## Project Setup

- [ ] Version control repository initialized
- [ ] `.gitignore` configured (state files, secrets, .terraform/)
- [ ] Pre-commit hooks installed (formatting, linting)
- [ ] CI/CD pipeline configured
- [ ] Remote backend configured with encryption
- [ ] State locking mechanism enabled

## Code Organization

- [ ] Environment separation (dev/staging/prod)
- [ ] Module structure defined
- [ ] Naming conventions documented
- [ ] Tagging strategy implemented
- [ ] Variable validation rules defined
- [ ] Output values documented

## Security

- [ ] No hardcoded credentials in code
- [ ] Secrets management solution integrated (Vault, AWS Secrets Manager)
- [ ] State file encryption enabled
- [ ] Access control policies defined
- [ ] Security scanning in CI/CD (tfsec, checkov)
- [ ] Least privilege IAM policies
- [ ] Audit logging enabled

## Testing

- [ ] Static analysis configured (tflint)
- [ ] Policy tests defined (OPA/Sentinel)
- [ ] Unit tests for modules (Terratest)
- [ ] Integration test environment
- [ ] Cost estimation integrated (Infracost)
- [ ] Drift detection scheduled

## Documentation

- [ ] Module README files
- [ ] Variable descriptions complete
- [ ] Architecture diagrams updated
- [ ] Runbook for common operations
- [ ] Disaster recovery procedures

## GitOps Integration

- [ ] PR-based workflow enforced
- [ ] Plan output in PR comments
- [ ] Required approvals configured
- [ ] Branch protection rules
- [ ] Merge triggers apply
- [ ] Continuous reconciliation (if applicable)

## Operational Readiness

- [ ] Monitoring for infrastructure changes
- [ ] Alerting for drift detection
- [ ] Backup strategy for state files
- [ ] Rollback procedures documented
- [ ] On-call runbooks prepared

## Compliance

- [ ] Required tags enforced
- [ ] Resource naming validated
- [ ] Region restrictions applied
- [ ] Instance type allowlists
- [ ] Network security policies
- [ ] Data residency requirements

---

*IaC Checklist | faion-infrastructure-engineer*
