# Infrastructure as Code (IaC) Fundamentals

## Overview

Infrastructure as Code (IaC) applies software engineering practices to infrastructure management through declarative or imperative code definitions. This approach enables version control, testing, automation, and consistency across environments.

**Market context:** IaC market projected to reach USD 6.14 billion by 2033, growing at 22%+ CAGR (2025-2033).

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Declarative** | Define desired end-state; tool determines execution path |
| **Idempotent** | Repeated applies produce same result |
| **Immutable** | Replace rather than modify infrastructure |
| **Version controlled** | All configs in Git with full audit trail |
| **Modular** | Reusable, composable components |
| **Tested** | Unit, integration, policy tests |

## Declarative vs Imperative

| Aspect | Declarative | Imperative |
|--------|-------------|------------|
| **Definition** | What you want | How to get there |
| **Idempotency** | Built-in | Manual implementation |
| **Drift handling** | Auto-detect & correct | Manual reconciliation |
| **Learning curve** | Lower | Higher |
| **Tools** | Terraform, CloudFormation | Ansible, scripts |
| **Best for** | State management | Configuration management |

## IaC Tools Comparison

### Multi-Cloud Tools

| Tool | Language | License | Strengths | Limitations |
|------|----------|---------|-----------|-------------|
| **Terraform** | HCL | BSL | Multi-cloud, mature ecosystem, state management | BSL license concerns |
| **OpenTofu** | HCL | MPL 2.0 | Open-source, state encryption, community-driven | Smaller ecosystem |
| **Pulumi** | Python/Go/TS | Apache 2.0 | Real programming languages, loops/functions | Steeper learning curve |
| **Crossplane** | YAML | Apache 2.0 | K8s-native, kubectl integration | Requires K8s cluster |

### Cloud-Native Tools

| Tool | Cloud | Language | Best For |
|------|-------|----------|----------|
| **AWS CloudFormation** | AWS | YAML/JSON | AWS-only environments |
| **AWS CDK** | AWS | Python/TS/Java | Developers wanting programming constructs |
| **Azure Bicep** | Azure | Bicep | Azure-only environments |
| **Google Cloud Deployment Manager** | GCP | YAML/Python | GCP-only environments |

### Configuration Management

| Tool | Type | Language | Best For |
|------|------|----------|----------|
| **Ansible** | Agentless | YAML | Configuration management, orchestration |
| **Chef** | Agent-based | Ruby DSL | Complex configuration management |
| **Puppet** | Agent-based | Puppet DSL | Large-scale configuration |
| **SaltStack** | Agent/Agentless | YAML/Python | Event-driven automation |

## Tool Selection Decision Tree

```
Start
  |
  ├─ Multi-cloud? ─────────────────────────────────┐
  │     Yes                                        │
  │       │                                        │
  │       ├─ Open-source critical? ─── Yes ─→ OpenTofu
  │       │                                        │
  │       └─ No ─→ Terraform                       │
  │                                                │
  └─ Single cloud? ────────────────────────────────┤
        │                                          │
        ├─ AWS? ─────────────────────────────────┐ │
        │   │                                    │ │
        │   ├─ Developer-friendly? ─── Yes ─→ AWS CDK
        │   │                                    │ │
        │   └─ No ─→ CloudFormation              │ │
        │                                        │ │
        ├─ Azure? ─→ Azure Bicep                 │ │
        │                                        │ │
        └─ GCP? ─→ Deployment Manager            │ │
                   or Terraform                  │ │
                                                 │ │
  Kubernetes-native? ─────────────────────────────┘ │
        │                                          │
        └─ Yes ─→ Crossplane                       │
                                                   │
  Configuration management? ───────────────────────┘
        │
        └─ Yes ─→ Ansible (agentless) or Puppet/Chef (agents)
```

## GitOps Integration

### IaC + GitOps Workflow

```
Developer          Git Repository         CI/CD Pipeline         Infrastructure
    │                    │                      │                      │
    │──── Commit ───────→│                      │                      │
    │                    │───── Trigger ───────→│                      │
    │                    │                      │──── Validate ────────│
    │                    │                      │     (lint, test)     │
    │                    │                      │                      │
    │                    │                      │──── Plan ────────────│
    │                    │                      │                      │
    │←─── PR Comment ────│←──── Plan Output ────│                      │
    │     (plan diff)    │                      │                      │
    │                    │                      │                      │
    │──── Approve PR ───→│                      │                      │
    │                    │───── Merge ─────────→│                      │
    │                    │                      │──── Apply ──────────→│
    │                    │                      │                      │
    │                    │                      │──── Verify ──────────│
    │                    │                      │     (drift check)    │
```

### GitOps Tools Integration

| Tool | IaC Integration | Reconciliation |
|------|-----------------|----------------|
| **ArgoCD** | Helm, Kustomize | Continuous |
| **Flux** | Helm, Kustomize, Terraform | Continuous |
| **Atlantis** | Terraform, OpenTofu | PR-based |
| **Spacelift** | Terraform, Pulumi, CloudFormation | Policy-driven |
| **env0** | Terraform, Pulumi | Workflow-based |

## State Management

### Remote State Best Practices

| Practice | Implementation |
|----------|----------------|
| **Remote storage** | S3, GCS, Azure Blob, Terraform Cloud |
| **State locking** | DynamoDB (AWS), GCS (built-in), Azure Blob (leases) |
| **Encryption** | Enable at-rest and in-transit encryption |
| **Versioning** | Enable bucket versioning for rollback |
| **Access control** | IAM policies, least privilege |
| **Backup** | Automated snapshots, cross-region replication |

### State File Security

- Never commit state files to Git
- Use remote backends with encryption
- Implement state locking to prevent corruption
- Restrict access to state storage
- Enable audit logging for state operations

## Project Structure

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   ├── database/
│   └── storage/
├── policies/
│   ├── sentinel/
│   └── opa/
└── scripts/
    ├── bootstrap.sh
    └── validate.sh
```

## Testing Strategy

| Test Type | Tool | Purpose |
|-----------|------|---------|
| **Static analysis** | tflint, checkov | Syntax, best practices |
| **Unit tests** | Terratest, pytest | Module functionality |
| **Integration tests** | Terratest | Cross-module interaction |
| **Policy tests** | OPA, Sentinel | Compliance validation |
| **Security scanning** | tfsec, Snyk | Vulnerability detection |
| **Cost estimation** | Infracost | Budget validation |

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [OpenTofu Documentation](https://opentofu.org/docs/)
- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Crossplane Documentation](https://docs.crossplane.io/)
- [GitOps Principles](https://opengitops.dev/)

## Sources

- [Infrastructure as Code Best Practices](https://spacelift.io/blog/infrastructure-as-code)
- [IaC Tools Comparison 2026](https://spacelift.io/blog/infrastructure-as-code-tools)
- [IaC Security Best Practices](https://cycode.com/blog/8-best-practices-for-securing-infrastructure-as-code/)
- [Red Hat IaC Guide](https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac)
- [CloudOptimo IaC Guide](https://www.cloudoptimo.com/blog/infrastructure-as-code-a-complete-guide-to-modular-design-compliance-and-monitoring/)

---

*IaC Fundamentals | faion-infrastructure-engineer*
