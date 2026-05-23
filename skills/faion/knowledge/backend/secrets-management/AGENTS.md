# Secrets Management

## Summary

**One-sentence:** Generates an env-file + systemd EnvironmentFile + 1Password integration plan for a solo VPS — defense-in-depth across file perms, .gitignore, and pre-commit hooks.

**One-paragraph:** Solo secrets management is .env file hygiene + systemd EnvironmentFile wiring + 1Password CLI (`op`) for programmatic injection + a pre-commit hook to block accidental commits. The output is a SecretsPlan declaring which files exist where, which systemd units consume which file, which secret rotates on what cadence, and a named owner per secret class.

**Ефективно для:**

- Solo VPS where systemd services need DB / API credentials.
- Bootstrapping a fresh project that must not leak secrets into git history.
- Rotation drills after a known leak — every consumer of the old secret must be tracked.
- Hardening an existing repo with a leaked-secret pre-commit guard.

## Applies If (ALL must hold)

- A new project requires API keys, DB credentials, or JWT secrets.
- Deploying a service to production where .env must be generated from a secrets manager.
- Rotating a compromised or expired credential across all services.
- Auditing a codebase for hardcoded secrets or improper .env handling.

## Skip If (ANY kills it)

- Compliance environments requiring HashiCorp Vault / AWS Secrets Manager with audit trails.
- Short-lived ephemeral scripts with no persistent secrets.
- Public configuration values (feature flags, log levels) that need no protection.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Secret inventory | list of {name, class, owner} | operator scan |
| 1Password vault access | op CLI session | operator credentials |
| List of systemd units consuming secrets | service file paths | /etc/systemd |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| systemd-user-services | EnvironmentFile= directive lives in service units we own. |
| ssh-hardening | 1Password CLI session lives behind hardened SSH access. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-no-secrets-in-git, r2-systemd-env-file, r3-file-perms-600, r4-named-rotation-owner, r5-rotation-on-leak | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Secrets Management artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: env-checked-into-git, env-readable-by-other, secret-rotation-skipped, op-token-in-bashrc | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-leaked-secrets` | sonnet | Pattern match + entropy scan on repo history. |
| `draft-secrets-plan` | sonnet | Per-service mapping with stakes. |
| `render-env-tpl` | haiku | Mechanical template fill from inventory. |

## Templates

| File | Purpose |
|------|---------|
| `templates/secrets-management.json` | SecretsPlan JSON skeleton (inventory + consumers + rotation). |
| `templates/secrets-management.md` | Human-readable audit trail. |
| `templates/env.tpl` | Reference .env template with op:// references. |
| `templates/env.example` | Committed example file with placeholders only. |
| `templates/gitignore-secrets` | Drop-in .gitignore block for env + secrets files. |
| `templates/pre-commit-secrets.sh` | Local pre-commit hook scanning staged files for secret patterns. |
| `templates/validate_env.py` | Runtime check that required env vars are present + non-placeholder. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-secrets-management.py` | Validate SecretsPlan JSON against the output-contract schema. | Pre-deploy + post-rotation. |

## Related

- [[systemd-user-services]]
- [[ssh-hardening]]
- [[server-init-bootstrap]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
