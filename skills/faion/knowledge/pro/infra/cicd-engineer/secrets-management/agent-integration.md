# Agent Integration — Secrets Management

## When to use
- Any system with database creds, API keys, signing keys, OAuth tokens, TLS certs, webhook secrets — i.e. all production systems.
- CI/CD pipelines that need cloud creds (AWS / GCP / Azure) — replace long-lived access keys with OIDC + STS / Workload Identity.
- Kubernetes workloads that need to consume secrets from a central store (Vault, AWS SM, Azure KV) — External Secrets Operator (ESO) is the standard glue.
- GitOps repos where config (including secrets) must live in Git — SOPS + KMS provider, or sealed-secrets, never plaintext.
- Multi-environment systems where dev/stage/prod secrets must be cleanly partitioned and audited.

## When NOT to use
- A solo dev laptop project that hits a free-tier API — `.env` + 1Password CLI is enough; full Vault is overkill.
- "Storing" config that is not actually secret (feature flags, public URLs). Conflating config and secrets makes both worse.
- As a key-value store for hot data — secrets backends are throttled and audit-logged; agents misuse them as Redis and hit rate limits.

## Where it fails / limitations
- **Plaintext secrets in Git.** The single most common breach vector. `git-secrets`, `gitleaks`, `trufflehog` pre-commit + push checks are non-negotiable.
- **Static credentials with no rotation.** A leaked AWS access key from 3 years ago still works. Force short-lived (≤1h) tokens via OIDC / Vault dynamic secrets.
- **`.env` files committed.** Even `.env.example` accidentally containing real values happens monthly. Add `.env*` to `.gitignore` and a pre-commit secret scan.
- **K8s `Secret` objects are base64-encoded, not encrypted.** Default etcd encryption is off in many clusters. Enable encryption-at-rest + use ESO + RBAC.
- **SOPS key sprawl.** Team uses age + AWS KMS + GCP KMS + PGP for one repo; rotation requires touching every secret file. Pick one provider per repo.
- **ESO permission scope.** Agents grant ESO controller wildcard read on Vault — one compromised cluster reads every secret. Scope per-namespace via ServiceAccount + Vault role binding.
- **Vault auto-unseal** misconfigured → cluster restart reveals "vault is sealed", outage. Always use cloud KMS auto-unseal in production.
- **Vault token TTLs too long.** "30-day token" defeats the purpose. Default to ≤1h with renewal; force re-auth on workload restart.
- **Secret rotation breaks consumers.** Rotation rotates the secret but the app caches the old one in memory. Need graceful reload (SIGHUP, periodic refresh, or sidecar like vault-agent).
- **CI logs leak secrets.** Even with masking, `set -x`, `curl -v`, error stack traces print env vars. Disable verbose modes; mask in log shipping pipeline.
- **OIDC audience misconfig.** Agents copy a workflow that uses `aud: sts.amazonaws.com` against a Vault role expecting `aud: vault.example.com` — auth silently uses default and grants more than intended.

## Agentic workflow
Treat secrets as a typed resource with a lifecycle. Have one agent inventory every secret in scope (name, type, owner, rotation policy, consumers) BEFORE generating IaC or code. A second agent generates the secret-store config (Vault policies / AWS SM resource policies / ESO `ExternalSecret` CRs / SOPS files) using the inventory. A reviewer agent runs `gitleaks detect`, `trivy fs`, and a custom diff that flags any plaintext secret hitting Git. For runtime, prefer workload identity → cloud STS → short-lived creds; never pass long-lived keys via env. Agents must never call the secret store API directly from application code at request time — that's an outage waiting to happen; use a sidecar or init container that materializes secrets to memory/tmpfs.

### Recommended subagents
- `password-scrubber-agent` — first pass on every diff; blocks the commit if anything looks like a credential.
- `faion-sdd-executor-agent` — quality gate must require a `gitleaks` clean run plus an inventory diff.
- A custom `secret-rotation-planner` (Sonnet) — given an inventory, emits a rotation calendar (which secrets, what cadence, what consumers, what reload strategy).
- A custom `eso-policy-auditor` — diffs proposed `ExternalSecret` + `SecretStore` CRs against current cluster RBAC and flags over-broad reads.

### Prompt pattern
```
Inventory secrets for <project>. Output Markdown table: name, type (cred/cert/token/key), backend (vault/aws-sm/sops/eso), owner, rotation_period, consumers[], reload_strategy (sighup/restart/sidecar/runtime-fetch), failure_mode_if_unavailable.
Then emit IaC (Terraform / Helm) creating only the missing entries. Do NOT touch secrets that already exist; emit "OUT OF SCOPE" for those.
Forbid: hardcoded values, long-lived cloud access keys, K8s Secret without ESO source-of-truth, SOPS without explicit kms_key/age recipient, Vault tokens with TTL > 1h.
```

```
Pre-commit gate: run `gitleaks detect --no-git -v` AND `trufflehog filesystem .` AND a custom check that fails if any file under `secrets/` lacks SOPS sops metadata. Emit JSON {findings: [{file, rule, line, redacted_match, severity}]}. Reject merge if any high/critical finding.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vault` | HashiCorp Vault CLI: read/write secrets, manage policies, transit/PKI | https://developer.hashicorp.com/vault/docs/commands |
| `aws secretsmanager` / `aws kms` | AWS Secrets Manager + KMS | https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/ |
| `gcloud secrets` | GCP Secret Manager | https://cloud.google.com/sdk/gcloud/reference/secrets |
| `az keyvault` | Azure Key Vault | https://learn.microsoft.com/cli/azure/keyvault |
| `sops` | Encrypt YAML/JSON files in Git with KMS/age/PGP | https://github.com/getsops/sops |
| `age` | Modern file encryption — pair with SOPS | https://github.com/FiloSottile/age |
| `gitleaks` | Pre-commit + CI secret scan | https://github.com/gitleaks/gitleaks |
| `trufflehog` | Deeper entropy + verifier-based scan; can verify creds are live | https://github.com/trufflesecurity/trufflehog |
| `kubeseal` (Sealed Secrets) | Encrypt K8s Secrets in Git with cluster public key | https://github.com/bitnami-labs/sealed-secrets |
| `external-secrets` (kubectl plugin) | Manage ESO `ExternalSecret` CRs | https://external-secrets.io |
| `vault-agent` | Sidecar/init container that fetches secrets, renders templates | https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent |
| `op` (1Password CLI) | Local dev secret access via 1Password | https://developer.1password.com/docs/cli |
| `doppler` / `infisical` CLIs | SaaS secrets backends with CI/CLI integration | https://docs.doppler.com · https://infisical.com/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| HashiCorp Vault | OSS / Enterprise | Yes | Gold standard for dynamic secrets, PKI, transit; agents need policy discipline. |
| AWS Secrets Manager | SaaS | Yes | Tight IAM integration; cost grows per secret + per call — watch out for hot loops. |
| AWS Parameter Store (SSM) | SaaS | Yes | Cheaper alternative for non-rotated config; SecureString = KMS-encrypted. |
| GCP Secret Manager | SaaS | Yes | Versioned secrets; Workload Identity Federation for GH/GL CI. |
| Azure Key Vault | SaaS | Yes | Managed Identity auth; soft-delete + purge protection are mandatory. |
| External Secrets Operator | OSS | Yes | K8s standard; supports Vault, AWS SM, GCP SM, Azure KV, 1Password, Doppler, Infisical. |
| Sealed Secrets (Bitnami) | OSS | Yes | Encrypt-in-Git with cluster public key — simpler than ESO, less powerful. |
| SOPS + Mozilla SOPS | OSS | Yes | GitOps-native; FluxCD has built-in decryption. |
| Doppler / Infisical / 1Password Secrets Automation | SaaS | Yes | Modern devex — UI + CLI + SDK; team-friendly but adds a vendor. |
| GitLab/GitHub OIDC | SaaS | Yes | Replace long-lived cloud keys with short-lived STS tokens. |
| `cert-manager` | OSS | Yes | TLS cert issuance + rotation in K8s; pair with Vault PKI or Let's Encrypt. |

## Templates & scripts
See `templates.md` and `examples.md`. Pre-commit gate covering 90% of leaks (≤30 lines):

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/awslabs/git-secrets
    rev: 1.3.0
    hooks:
      - id: git-secrets
        args: [--scan]
  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks-docker
        files: \.(env|yaml|yml|json|tf|tfvars|properties)$
  - repo: local
    hooks:
      - id: forbid-plaintext-env
        name: Block plaintext .env files
        entry: bash -c 'if git diff --cached --name-only | grep -E "^\.env$|^\.env\..*"; then echo "Refusing to commit raw .env"; exit 1; fi'
        language: system
        pass_filenames: false
```

```hcl
# Vault policy: agents must scope tightly per workload
path "kv/data/app/billing/*" { capabilities = ["read"] }
path "database/creds/billing-readonly" { capabilities = ["read"] }
path "transit/encrypt/billing" { capabilities = ["update"] }
path "transit/decrypt/billing" { capabilities = ["update"] }
# DENY everything else by default — Vault is allow-list.
```

## Best practices
- One backend per environment + one path namespace per workload. `kv/data/<env>/<service>/<key>`. Cross-env access never granted.
- Short-lived dynamic creds wherever the backend supports it: DB creds, AWS STS, K8s SA tokens. Static secrets are an anti-pattern; treat them as legacy debt.
- Enable encryption-at-rest on K8s etcd. Without it, `kubectl get secret -o yaml` from a compromised etcd snapshot is plaintext.
- Vault: TLS to clients, KMS auto-unseal, Raft 3-5 nodes across AZs, daily snapshot to encrypted bucket, audit log to a separate sink.
- AWS SM: enable rotation via Lambda for DB creds; use resource policies + IAM with `aws:PrincipalTag` conditions; never wildcard `secretsmanager:GetSecretValue`.
- ESO: one `SecretStore`/`ClusterSecretStore` per backend, one ServiceAccount per namespace, scoped Vault role per SA — JWT auth via projected SA token.
- SOPS: one creation rule per directory tree; rotate KMS keys yearly; never mix age + PGP recipients in the same file.
- Mask aggressively in logs; ship logs through a redactor before they hit external SIEM. Test masking by piping a known token through.
- Document the rotation playbook for every secret type. Untested rotation = no rotation.
- Secret-zero problem (where do you store the credential to talk to the secret store?): Workload Identity / IMDSv2 / projected SA tokens — never a static bootstrap key on disk.

## AI-agent gotchas
- Agents pick env vars (`AWS_ACCESS_KEY_ID`) over IAM roles because tutorials use them. Ban env-var creds in prod and force `assume_role_with_web_identity` patterns.
- LLMs occasionally synthesize plausible-looking dummy secrets (`sk_test_4eC39H...`) into examples that DO match real Stripe test keys; pre-commit scanners flag them as criticals. Train the agent to use `<REPLACE_ME>` placeholders.
- `kubectl get secret -o yaml | tee secret.yaml` to "back up" a secret — agents commit it. ESO + Git source of truth makes this obsolete; ban manual `Secret` YAML in repos.
- Caching: agents fetch a secret once at boot then keep using it for weeks; rotation breaks them silently. Add a TTL'd refresh or use `vault-agent` template rendering.
- Vault policy by negation: agents write `path "*" { capabilities = ["read"] }` plus a DENY for one prefix. Vault evaluates broad allow first; the DENY is brittle. Always allow-list specific paths.
- Multi-cloud OIDC trust: agents enable both GitHub and GitLab OIDC providers on the same role with `*` audience. One side compromised → both compromised. Bind aud + sub claims tightly.
- Human-in-loop checkpoints (mandatory): creating a new secret backend, granting a new policy/role, rotating a root signing key, changing audit-log destination. These are credential-equivalent operations.
- Build-time vs runtime secrets: agents bake API keys into Docker images (`ARG SECRET_KEY` then `ENV SECRET_KEY=$ARG`). The image holds it forever. Use BuildKit `--mount=type=secret`.
- ESO `creationPolicy: Owner` then `kubectl delete externalsecret` deletes the underlying Secret + cascades to consumers. Agents test this in prod and cause outages.

## References
- HashiCorp Vault docs — https://developer.hashicorp.com/vault/docs
- AWS Secrets Manager — https://docs.aws.amazon.com/secretsmanager/
- External Secrets Operator — https://external-secrets.io
- SOPS — https://github.com/getsops/sops
- Sealed Secrets — https://github.com/bitnami-labs/sealed-secrets
- gitleaks — https://github.com/gitleaks/gitleaks
- OWASP Secrets Management Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- 12-factor: III. Config — https://12factor.net/config
- GitHub OIDC — https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- GitLab ID tokens — https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html
