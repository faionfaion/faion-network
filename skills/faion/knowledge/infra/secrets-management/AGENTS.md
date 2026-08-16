# Secrets Management

## Summary

**One-sentence:** Secrets management spec: eliminate static credentials, use cloud identity (IRSA / Workload Identity / OIDC), short-lived dynamic credentials, 30-day rotation, ESO for Kubernetes injection.

**One-paragraph:** Secrets management in 2025-2026 means eliminating static, long-lived credentials. Apps authenticate via cloud identity (IRSA on EKS, Workload Identity on GKE, OIDC for CI/CD) and receive short-lived dynamic credentials from a secrets backend (Vault, AWS Secrets Manager, GCP Secret Manager). Kubernetes integration uses External Secrets Operator (ESO) as the bridge. Rotation is automated on a 30-day or shorter cycle. Static keys in env vars, repo files, or CI variables are the primary breach vector and must be eradicated.

**Ефективно для:**

- Eliminate static AWS/GCP/Vault keys в CI/CD через OIDC trust.
- Kubernetes pod secrets через ESO замість kubectl create secret.
- Automated rotation на 30-денному циклі без app downtime.
- Audit trail для secret access (хто, коли, який secret).

## Applies If (ALL must hold)

- Application needs database credentials, API keys, or TLS certificates at runtime
- Kubernetes workloads require secrets without storing them as native K8s Secrets in plain base64
- CI/CD pipelines must authenticate to cloud providers without stored access keys
- Compliance requires secret rotation, audit logging, and access control (SOC2, HIPAA, PCI-DSS)

## Skip If (ANY kills it)

- Development-only local environment — .env files are acceptable
- Secrets that are truly public (public API keys, non-sensitive config) — use ConfigMaps
- Single-cloud project where cloud-native secrets service covers all use cases — Vault is unnecessary overhead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cloud account with identity provider (AWS IAM / GCP IAM / Azure AD) | IAM policies | platform team |
| Secrets backend (Vault / AWS Secrets Manager / GCP Secret Manager) | credentials + backend URL | platform team |
| Kubernetes cluster (for ESO use case) | kubeconfig + namespace | platform team |
| GitHub / GitLab project (for OIDC CI/CD) | repo settings + admin rights | DevOps lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[external-secrets-operator-recipe]] | ESO setup pattern for Kubernetes injection |
| [[ssl-tls-setup]] | TLS for secrets-in-transit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_secrets` | haiku | Listing existing credentials is mechanical |
| `policy_design` | sonnet | Least-privilege policy synthesis |
| `backend_choice` | opus | Cross-cloud + compliance tradeoff judgment |

## Templates

| File | Purpose |
|------|---------|
| `templates/eso-secret-store.yaml` | Eso secret store template |
| `templates/prompt-audit.txt` | Prompt audit template |
| `templates/vault-policy.hcl` | Vault policy template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-secrets-management.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[external-secrets-operator-recipe]]
- [[ssl-tls-setup]]
- [[security-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/eso-secret-store.yaml`

```yaml
# External Secrets Operator: SecretStore + ExternalSecret patterns
# Supports AWS SSM, GCP Secret Manager, HashiCorp Vault, Azure Key Vault

---
# AWS SSM Parameter Store via IRSA
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-ssm
  namespace: production
spec:
  provider:
    aws:
      service: ParameterStore
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa  # has IRSA annotation
---
# GCP Secret Manager via Workload Identity
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: gcp-secretmanager
  namespace: production
spec:
  provider:
    gcpsm:
      projectID: my-gcp-project
      auth:
        workloadIdentity:
          clusterLocation: us-central1
          clusterName: my-cluster
          clusterProjectID: my-gcp-project
          serviceAccountRef:
            name: external-secrets-sa
---
# HashiCorp Vault via Kubernetes auth
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault
  namespace: production
spec:
  provider:
    vault:
      server: https://vault.internal.example.com
      path: secret
      version: v2
      auth:
        kubernetes:
          mountPath: kubernetes
          role: production-app
          serviceAccountRef:
            name: vault-auth-sa
---
# ExternalSecret: pull multiple keys from SSM into one K8s Secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-ssm
    kind: SecretStore
  target:
    name: app-secrets           # K8s Secret name to create
    creationPolicy: Owner       # ESO owns lifecycle; delete ExternalSecret → delete Secret
    template:
      engineVersion: v2
      data:
        DATABASE_URL: "{{ .db_password | b64dec }}"  # transform if needed
  data:
    - secretKey: db-password        # key in K8s Secret
      remoteRef:
        key: /production/app/db-password
    - secretKey: api-key
      remoteRef:
        key: /production/app/api-key
  dataFrom:
    - extract:
        key: /production/app/config  # pulls all sub-keys as flat map
---
# ClusterSecretStore for cross-namespace access (use sparingly)
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-cluster
spec:
  provider:
    vault:
      server: https://vault.internal.example.com
      path: secret
      version: v2
      auth:
        kubernetes:
          mountPath: kubernetes
          role: cluster-reader
          serviceAccountRef:
            name: eso-cluster-sa
            namespace: external-secrets
```

### `templates/prompt-audit.txt`

```text
You are a secrets management security auditor. Audit the system described below and identify all violations, risks, and remediation steps.

Context:
- System description: {{SYSTEM_DESCRIPTION}}
- Current secret storage: {{SECRET_STORAGE_METHOD}}
- CI/CD platform: {{CICD_PLATFORM}}
- Kubernetes in use: {{YES_NO}}
- Cloud provider: {{CLOUD_PROVIDER}}

Audit checklist — for each item mark: PASS / FAIL / N/A and explain why.

SECTION 1: Secret Discovery
1. Are there any hardcoded credentials in source code? (scan .env files committed, tokens in YAML, connection strings in code)
2. Are secrets stored in CI/CD platform variables (non-OIDC)? Which ones could be replaced with OIDC/WIF?
3. Are there long-lived service account keys (AWS access keys, GCP SA JSON keys, Azure client secrets)?
4. Are secrets shared across environments (same credential in dev and production)?
5. Are secrets stored in Kubernetes etcd without encryption at rest?

SECTION 2: Access Control
6. Does every secret follow least-privilege (application reads only its own secrets)?
7. Are there wildcard policies (e.g., "read all secrets")?
8. Is there a defined secret owner for each secret? Who rotates it?
9. Are break-glass/admin credentials stored separately and access-logged?
10. Are there orphaned secrets with no known owner/application?

SECTION 3: Rotation
11. Are all static credentials rotated at least every 90 days?
12. Are database credentials dynamic (Vault database secrets engine, RDS IAM auth)?
13. Is there automated rotation for API keys to third-party services?
14. After any team member offboarding, are shared credentials rotated immediately?

SECTION 4: Transport & Storage
15. Are secrets transmitted only over TLS 1.2+?
16. Are secrets logged anywhere (application logs, CI/CD output, monitoring systems)?
17. Are secrets encrypted at rest (KMS-managed, not application-level only)?
18. Are backups of secret stores also encrypted and access-controlled?

SECTION 5: Kubernetes-specific (skip if N/A)
19. Is External Secrets Operator or Secrets Store CSI Driver in use (not manual kubectl create secret)?
20. Are Kubernetes Secrets base64-decoded values ever logged or exposed in env vars printouts?
21. Is etcd encryption at rest configured?
22. Are Pods running with `envFrom: secretRef` (exposes all keys) vs specific `env.valueFrom.secretKeyRef`?

SECTION 6: CI/CD-specific
23. Is OIDC/WIF used for cloud provider auth (no static keys in CI)?
24. Are secret values masked in CI logs?
25. Are pull request pipelines prevented from accessing production secrets?
26. Is there a secret scanning step in the pipeline (detect-secrets, trufflehog, gitleaks)?

For each FAIL, provide:
- Risk level: Critical / High / Medium / Low
- Remediation: Specific action with the recommended tool/service
- Priority: immediate / next sprint / next quarter

Final summary: overall secret hygiene score (A/B/C/D/F) with top 5 critical actions.
```

### `templates/vault-policy.hcl`

```hcl
# HashiCorp Vault policy templates
# Apply with: vault policy write <name> <file.hcl>

# ---
# Application policy: read-only access to own path
# ---
# vault policy write app-production production-app.hcl
path "secret/data/production/{{identity.entity.aliases.auth_kubernetes_XXX.metadata.service_account_namespace}}/{{identity.entity.aliases.auth_kubernetes_XXX.metadata.service_account_name}}/*" {
  capabilities = ["read"]
}

# Simpler static path for a named application
path "secret/data/production/myapp/*" {
  capabilities = ["read"]
}

# Allow listing (needed for UI and some apps to enumerate paths)
path "secret/metadata/production/myapp/*" {
  capabilities = ["list", "read"]
}

# ---
# CI/CD policy: write secrets during deploy, read during run
# ---
# vault policy write cicd-deploy cicd-deploy.hcl
path "secret/data/production/*" {
  capabilities = ["create", "update"]
  # Restrict to specific fields if needed:
  # allowed_parameters = {
  #   "data" = []
  # }
}

path "secret/data/staging/*" {
  capabilities = ["create", "update", "read", "delete"]
}

# Allow CI to rotate its own token
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# ---
# Admin policy: full control over KV engine (break-glass only)
# ---
# vault policy write kv-admin kv-admin.hcl
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list", "patch"]
}

# Allow managing policies themselves
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# ---
# Dynamic database credentials policy
# ---
path "database/creds/production-readonly" {
  capabilities = ["read"]
}

path "database/creds/production-readwrite" {
  capabilities = ["read"]
}

# Allow lease renewal (so apps can extend dynamic creds)
path "sys/leases/renew" {
  capabilities = ["update"]
}

# ---
# PKI: request TLS certificates
# ---
path "pki/issue/internal-services" {
  capabilities = ["create", "update"]
  allowed_parameters = {
    "common_name" = ["*.internal.example.com", "*.svc.cluster.local"]
    "ttl"         = ["24h", "72h"]
  }
}

path "pki/cert/ca" {
  capabilities = ["read"]
}

# ---
# Kubernetes auth role (configure, not a policy file, but shown for reference)
# ---
# vault write auth/kubernetes/role/production-app \
#   bound_service_account_names=myapp \
#   bound_service_account_namespaces=production \
#   policies=app-production \
#   ttl=1h \
#   max_ttl=4h
```
