# Secrets Management

## Summary

Secrets management securely stores, accesses, and rotates credentials, API keys, certificates, and encryption keys. Modern practice (2025–2026) favors dynamic short-lived credentials over static long-lived ones, and identity-based access ("who is asking") over shared secret keys. The recommended Kubernetes pattern is External Secrets Operator (ESO) syncing from a central backend (Vault or AWS Secrets Manager), with SOPS for GitOps-encrypted configs. Never store secrets in environment variables committed to Git, build-time injection, or application logs.

## Why

Static, long-lived credentials are the root cause of most cloud breaches. Dynamic secrets (Vault database engine, AWS IAM temporary credentials) expire with the workload, so a leaked credential is useless within minutes. Workload identity federation (K8s ServiceAccount → OIDC → cloud IAM) eliminates stored credentials entirely in modern cloud environments.

## When To Use

- Designing secrets access for a new service or Kubernetes workload
- Migrating from hardcoded credentials or `.env` files to a secrets manager
- Setting up GitOps with encrypted secrets in Git (SOPS + FluxCD or ArgoCD)
- Choosing between Vault, AWS Secrets Manager, SOPS, and ESO for a project
- Implementing credential rotation (database passwords, API tokens, TLS certificates)

## When NOT To Use

- Local development with non-sensitive dummy credentials — use `.env` files with `.gitignore`; overhead of Vault/ESO is not justified
- Read-only public configuration (non-sensitive feature flags) — use ConfigMaps or plain environment variables
- Prototypes with no production deployment path

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Secret lifecycle, tool comparison (Vault/AWS SM/SOPS/ESO), five architecture patterns |
| `content/02-rules.xml` | Storage rules (encrypt at rest, HA), access rules (short-lived creds, no secrets in logs), rotation rules |
| `content/03-examples.xml` | Vault Kubernetes auth, ESO ExternalSecret, SOPS encryption workflow, AWS Secrets Manager rotation |

## Templates

| File | Purpose |
|------|---------|
| `templates/external-secret.yaml` | ESO ExternalSecret manifest syncing from Vault or AWS SM to K8s Secret |
| `templates/sops-config.yaml` | .sops.yaml with path_regex for per-environment KMS key routing |
| `templates/vault-policy.hcl` | Vault least-privilege policy for a Kubernetes workload |
