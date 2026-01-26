---
id: secrets-management
name: "Secrets Management"
domain: OPS
skill: faion-cicd-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01-26"
---

# Secrets Management

## Overview

Secrets management involves securely storing, accessing, and rotating sensitive information like passwords, API keys, certificates, and encryption keys. Modern secrets management (2025-2026) has shifted from static, long-lived credentials to dynamic, short-lived Just-In-Time (JIT) access with identity-based authentication.

**Key 2025-2026 Trends:**
- Dynamic secrets over static credentials
- Identity-based access ("Who is asking?" vs "What is the secret?")
- Workload identity federation (no stored credentials)
- External Secrets Operator as K8s standard
- GitOps-native encryption with SOPS

## When to Use

| Scenario | Recommended Tool |
|----------|------------------|
| Multi-cloud enterprise, regulated industries | HashiCorp Vault |
| AWS-only, zero operational overhead | AWS Secrets Manager |
| GitOps workflows, encrypted configs in Git | SOPS |
| Kubernetes workloads with external backends | External Secrets Operator |
| Hybrid: central store + K8s + dev/CI | Vault/ASM + ESO + SOPS |

## Secret Types

| Category | Examples |
|----------|----------|
| Credentials | Database passwords, service accounts, SSH keys, API keys |
| Certificates | TLS certs, CA certs, client certs, code signing keys |
| Tokens | OAuth tokens, JWT secrets, session secrets, webhooks |
| Encryption Keys | DEKs, KEKs, HMAC keys |

## Secret Lifecycle

```
Creation → Storage → Access → Rotation → Revocation
    │          │        │         │           │
    │          │        │         │           └── Audit, cleanup
    │          │        │         └── Automated (30 days typical)
    │          │        └── RBAC, audit logging, identity-based
    │          └── Encrypted at rest, HA deployment
    └── Secure generation, short-lived preferred
```

## Tool Comparison (2025-2026)

| Feature | Vault | AWS SM | SOPS | ESO |
|---------|-------|--------|------|-----|
| Dynamic Secrets | Yes | Limited | No | Via backend |
| Auto Rotation | Yes | Yes | Manual | Via backend |
| Multi-cloud | Yes | No | Yes | Yes |
| K8s Native | Operator | Indirect | FluxCD | Yes |
| Complexity | High | Low | Low | Medium |
| Cost | Self-hosted | Per secret/call | Free | Free |

## Architecture Patterns

### Pattern 1: AWS-Native

```
Application → AWS SDK → AWS Secrets Manager
                              ↓
                        Rotation Lambda
```

### Pattern 2: Multi-Cloud with Vault

```
Application → Vault Agent → HashiCorp Vault
                                  ↓
                           Dynamic Secrets
                           (DB, AWS, PKI)
```

### Pattern 3: GitOps with SOPS

```
Git Repo → SOPS Encrypted Files → FluxCD/ArgoCD → K8s Secrets
                    ↓
              AWS KMS / GCP KMS
```

### Pattern 4: K8s with External Secrets Operator

```
ExternalSecret CR → ESO Controller → Backend (Vault/ASM/GCP)
        ↓
K8s Secret (auto-synced)
```

### Pattern 5: Hybrid (Recommended 2026)

```
Central Store (Vault/ASM/Infisical)
        ↓
   ESO for K8s Production
        ↓
   SOPS for GitOps Configs
        ↓
   Doppler for Dev/CI
```

## Best Practices (2025-2026)

### Storage
1. Encrypt at rest - Never store secrets in plaintext
2. HA deployment - 3-5 node Raft cluster across AZs
3. Access control - Principle of least privilege
4. Audit logging - Track all access
5. Backup encryption keys - Separate from secrets

### Access
1. Short-lived credentials - Expire with workload
2. Identity-based auth - IAM roles, workload identity
3. No secrets in code - Environment or secret store
4. No secrets in logs - Mask sensitive data
5. Runtime injection - Not build time

### Rotation
1. Automate rotation - 30 days typical
2. Grace periods - Support old+new during transition
3. Test rotation - Verify before production
4. Incident response - Rapid rotation on breach

### Development
1. Different secrets per env - Dev, staging, prod
2. Mock secrets in tests - Don't use real secrets
3. Secret scanning - Pre-commit hooks, CI checks
4. Documentation - Where secrets come from

## Files in This Methodology

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples for all tools |
| [templates.md](templates.md) | Ready-to-use configurations |
| [llm-prompts.md](llm-prompts.md) | AI prompts for secrets tasks |

## Sources

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)
- [External Secrets Operator](https://external-secrets.io/)
- [SOPS GitHub](https://github.com/getsops/sops)
- [Secrets Management Best Practices 2026](https://www.strongdm.com/blog/secrets-management)
- [Vault vs AWS Secrets Manager](https://infisical.com/blog/aws-secrets-manager-vs-hashicorp-vault)
- [ESO Security Best Practices](https://external-secrets.io/latest/guides/security-best-practices/)

---

*Secrets Management Methodology v2.0.0 | Updated 2026-01-26*
