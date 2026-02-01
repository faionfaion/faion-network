# Secrets Management

Securely storing, accessing, and rotating sensitive information like passwords, API keys, certificates, and encryption keys.

## Overview

Modern secrets management (2025-2026) has shifted from static, long-lived credentials to dynamic, Just-In-Time (JIT) access. The standard is to eliminate local secrets entirely, injecting them at runtime via identity-based authentication.

## When to Use

- Managing application credentials
- Storing API keys and tokens
- Handling database passwords
- Managing TLS certificates
- Implementing zero-trust security
- Meeting compliance requirements (SOC2, HIPAA, PCI-DSS)

## Key Concepts

### Secret Types

| Category | Examples |
|----------|----------|
| Credentials | Database passwords, SSH keys, API keys |
| Certificates | TLS/CA certs, client certs, code signing keys |
| Tokens | OAuth tokens, JWT secrets, webhook secrets |
| Encryption Keys | DEKs, KEKs, HMAC keys |

### Secret Lifecycle

```
Creation → Storage → Access → Rotation → Revocation
    |          |        |         |           |
    |          |        |         |           └── Audit, cleanup
    |          |        |         └── Automated (30 days typical)
    |          |        └── RBAC, audit logging
    |          └── Encrypted at rest
    └── Secure generation
```

### 2025-2026 Best Practices

1. **Dynamic secrets** - Short-lived, JIT credentials instead of static secrets
2. **Identity-based access** - Apps authenticate via cloud identity (IAM, K8s SA)
3. **External Secrets Operator** - Standard for Kubernetes integration
4. **Automatic rotation** - 30-day rotation cycles minimum
5. **Zero local secrets** - Inject at runtime, never store locally

## Tool Selection Guide

| Tool | Best For | Limitations |
|------|----------|-------------|
| **HashiCorp Vault** | Multi-cloud, regulated industries, complex dynamic secrets | Operational overhead |
| **AWS Secrets Manager** | AWS-native workloads, managed service | AWS lock-in, limited cross-cloud |
| **External Secrets Operator** | Kubernetes clusters, any backend | Requires K8s |
| **SOPS** | GitOps, encrypted files in repos | Manual rotation |

### Decision Tree

```
Multi-cloud or hybrid?
├── YES → HashiCorp Vault
└── NO → AWS-only?
         ├── YES → AWS Secrets Manager
         └── NO → GCP/Azure native solutions

Kubernetes workloads?
├── YES → External Secrets Operator + backend
└── NO → Direct SDK integration

Need dynamic database credentials?
├── YES → Vault Database Secrets Engine
└── NO → Static secrets with rotation
```

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples and configurations |
| [templates.md](templates.md) | Ready-to-use templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for secrets tasks |

## Related

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [External Secrets Operator](https://external-secrets.io/)
- [SOPS](https://github.com/getsops/sops)
- [Vault Secrets Operator](https://developer.hashicorp.com/vault/tutorials/kubernetes-introduction/vault-secrets-operator)

## Sources (2025-2026 Research)

- [Secrets Management in 2026: Vault, AWS Secrets Manager, and Beyond](https://www.javacodegeeks.com/2025/12/secrets-management-in-2026-vault-aws-secrets-manager-and-beyond-a-developers-guide.html)
- [What Is Secrets Management? Best Practices for 2026](https://www.strongdm.com/blog/secrets-management)
- [Kubernetes Secrets Management in 2025](https://infisical.com/blog/kubernetes-secrets-management-2025)
- [HashiCorp Vault Kubernetes: The Definitive Guide](https://www.plural.sh/blog/hashicorp-vault-kubernetes-guide/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |
