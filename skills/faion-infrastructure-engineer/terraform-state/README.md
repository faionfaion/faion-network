# Terraform State Management

Technical reference for Terraform state: remote backends, state operations, locking, import, and data sources.

## Overview

Terraform state is the source of truth for your infrastructure. It maps real-world resources to your configuration, tracks metadata, and improves performance for large infrastructures.

## Key Concepts

| Concept | Description |
|---------|-------------|
| State File | JSON file containing resource mappings and metadata |
| Remote Backend | Shared storage for team collaboration |
| State Locking | Prevents concurrent state modifications |
| State Encryption | Protects sensitive data at rest |
| State Versioning | Enables rollback and recovery |

## Remote Backend Options

| Backend | Provider | Locking | Encryption | Best For |
|---------|----------|---------|------------|----------|
| S3 + DynamoDB | AWS | Native | SSE-S3/KMS | AWS-centric teams |
| GCS | GCP | Native | Default | GCP-centric teams |
| Azure Blob | Azure | Native | Default | Azure-centric teams |
| Terraform Cloud | HashiCorp | Native | Default | Multi-cloud, enterprise |
| PostgreSQL | Any | Native | TLS | Self-hosted |
| Consul | HashiCorp | Native | Optional | Service mesh users |

## State Operations Quick Reference

| Operation | Command | Use Case |
|-----------|---------|----------|
| List resources | `terraform state list` | View managed resources |
| Show resource | `terraform state show <addr>` | Inspect resource details |
| Move resource | `terraform state mv <src> <dst>` | Rename/refactor |
| Remove from state | `terraform state rm <addr>` | Unmanage resource |
| Import resource | `terraform import <addr> <id>` | Bring existing resource |
| Pull state | `terraform state pull` | Download remote state |
| Push state | `terraform state push` | Upload local state |
| Replace provider | `terraform state replace-provider` | Provider migration |

## Best Practices Summary

1. **Always use remote state** for team environments
2. **Enable state locking** to prevent corruption
3. **Enable encryption** for security compliance
4. **Enable versioning** for disaster recovery
5. **Never commit state to git** (contains secrets)
6. **Separate state by environment** (dev/staging/prod)
7. **Use workspaces or separate backends** for isolation
8. **Backup before manual operations**
9. **Split large configurations** for performance

## 2025-2026 Updates

- **Terraform Cloud Free Tier** ends March 31, 2026 - plan migration to paid tiers or alternative backends
- **Import blocks** (Terraform 1.5+) preferred over `terraform import` CLI
- **State encryption** now available in open-source Terraform 1.7+
- **Moved blocks** for safer refactoring without state commands

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-flight and operational checklists |
| [examples.md](examples.md) | Backend configurations and operations |
| [templates.md](templates.md) | Copy-paste ready configurations |
| [llm-prompts.md](llm-prompts.md) | AI-assisted state management |

## Sources

- [Terraform State Documentation](https://developer.hashicorp.com/terraform/language/state)
- [Remote State](https://developer.hashicorp.com/terraform/language/state/remote)
- [State Locking](https://developer.hashicorp.com/terraform/language/state/locking)
- [Spacelift - Terraform State Best Practices](https://spacelift.io/blog/terraform-state)
- [Scalr - State Files Best Practices](https://scalr.com/learning-center/terraform-state-files-best-practices/)
- [AWS DevOps Blog - Terraform State in CI/CD](https://aws.amazon.com/blogs/devops/best-practices-for-managing-terraform-state-files-in-aws-ci-cd-pipeline/)

---

*Terraform State Management Reference | Part of faion-infrastructure-engineer skill*
