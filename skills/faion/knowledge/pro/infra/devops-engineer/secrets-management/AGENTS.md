# Secrets Management

## Summary

Secrets management in 2025-2026 means eliminating static, long-lived credentials: apps authenticate via cloud identity (IRSA, Workload Identity, OIDC) and receive short-lived dynamic credentials from a secrets backend. Kubernetes integration uses External Secrets Operator (ESO) as the standard bridge between any backend and pod-level secret injection. Rotation must be automated on a 30-day or shorter cycle.

## Why

Static secrets stored in environment variables or Kubernetes native Secrets (base64, not encrypted at rest by default) are the most common breach vector. Dynamic secrets from Vault's database engine issue credentials that expire in minutes — a compromised secret becomes useless before an attacker can act. OIDC-based auth for CI/CD (GitHub Actions, GitLab CI) eliminates long-lived service account keys entirely.

## When To Use

- Application needs database credentials, API keys, or TLS certificates at runtime
- Kubernetes workloads require secrets without storing them as native K8s Secrets in plain base64
- CI/CD pipelines must authenticate to cloud providers without stored access keys
- Compliance requires secret rotation, audit logging, and access control (SOC2, HIPAA, PCI-DSS)

## When NOT To Use

- Development-only local environment — `.env` files are acceptable; do not add Vault overhead
- Secrets that are truly public (public API keys, non-sensitive config values) — use ConfigMaps, not secrets backends
- Single-cloud project where the cloud provider's native secrets service (AWS Secrets Manager, GCP Secret Manager) covers all use cases — adding Vault is unnecessary operational overhead

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Secret lifecycle, tool selection matrix, dynamic vs static secrets, JIT access patterns |
| `content/02-kubernetes.xml` | External Secrets Operator setup, Vault Secrets Operator, IRSA/Workload Identity auth patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/eso-secret-store.yaml` | ESO ClusterSecretStore + ExternalSecret for AWS Secrets Manager |
| `templates/vault-policy.hcl` | Vault policy template with least-privilege path scoping |
| `templates/prompt-audit.txt` | LLM prompt for auditing secrets posture |
