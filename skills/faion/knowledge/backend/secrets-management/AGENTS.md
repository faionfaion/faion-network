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
| `templates/secrets-management.md.j2` | Human-readable audit trail. |
| `templates/secrets-management.md` | Human-readable audit trail. Generated from `templates/secrets-management.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/env.tpl` | Reference .env template with op:// references. |
| `templates/env.example` | Committed example file with placeholders only. |
| `templates/gitignore-secrets` | Drop-in .gitignore block for env + secrets files. |
| `templates/pre-commit-secrets.sh` | Local pre-commit hook scanning staged files for secret patterns. |
| `templates/validate_env.py` | Runtime check that required env vars are present + non-placeholder. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/secrets-management.json`

```json
{
  "artefact_id": "<plan-slug>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "secrets": [
    {
      "name": "<NAME>",
      "class": "db|api_key|jwt",
      "vault": "1Password/<vault>"
    }
  ],
  "consumers": [
    {
      "unit": "<svc>.service",
      "env_file": "/etc/<svc>.env"
    }
  ],
  "rotation_cadence_days": 90,
  "owner": "<@handle>",
  "leak_response_plan": "<one-paragraph runbook>"
}
```

### `templates/env.tpl`

```text
# .env.tpl — 1Password inject template
# Usage: op inject -i .env.tpl -o .env && chmod 600 .env
#
# Requires: op CLI + OP_SERVICE_ACCOUNT_TOKEN in environment
# Safe to commit: contains vault references, not actual secrets

# Database
DATABASE_URL={{ op://ServerVault/Database/url }}

# Redis (not a secret, literal value is fine)
REDIS_URL=redis://localhost:6379/0

# Message Broker
RABBITMQ_URL={{ op://ServerVault/RabbitMQ/url }}

# AI Keys
ANTHROPIC_API_KEY={{ op://ServerVault/Anthropic/api-key }}

# Authentication
JWT_SECRET={{ op://ServerVault/JWT/secret }}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Telegram
TELEGRAM_BOT_TOKEN={{ op://ServerVault/TelegramBot/token }}
TELEGRAM_CHAT_ID={{ op://ServerVault/TelegramBot/chat-id }}

# Application (non-secret literal values)
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
```

### `templates/env.example`

```text
# .env.example — Copy to .env and fill in real values
# Usage: cp .env.example .env && chmod 600 .env
#
# Rules: no export prefix, no $VAR expansion, no spaces around =

# ============================================================
# Database
# ============================================================
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# ============================================================
# Redis / Cache
# ============================================================
REDIS_URL=redis://localhost:6379/0

# ============================================================
# Message Broker
# ============================================================
RABBITMQ_URL=amqp://user:password@localhost:5672/vhost

# ============================================================
# AI / LLM API Keys
# ============================================================
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxx
# OPENAI_API_KEY=sk-xxxxxxxxxxxx

# ============================================================
# Authentication
# ============================================================
# Generate: openssl rand -base64 64
JWT_SECRET=replace-with-openssl-rand-base64-64-output
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# ============================================================
# Telegram
# ============================================================
TELEGRAM_BOT_TOKEN=123456:ABC-xxxxxxxxxxxx
TELEGRAM_CHAT_ID=123456789

# ============================================================
# Application
# ============================================================
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
```

### `templates/gitignore-secrets`

```text
# Secrets .gitignore block
# Add to root .gitignore of any project handling credentials

# Environment files
.env
.env.local
.env.production
.env.staging
.env.*.local
*.env

# Keep example and template files
!.env.example
!.env.tpl

# Cryptographic keys
*.pem
*.key
*.p12
*.pfx
*.crt
*.cer
id_rsa
id_ed25519
id_ecdsa
id_dsa

# 1Password CLI session
.op/

# Common credential file names
credentials.json
service-account.json
*.credentials
token.json
```

### `templates/pre-commit-secrets.sh`

```bash
# .git/hooks/pre-commit — Block commits containing secret patterns
#
# Install: cp pre-commit-secrets.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Scans staged file contents for API key patterns and private keys.
# Skips .env.example and .env.tpl (intentionally contain placeholder syntax).

PATTERNS=(
    'sk-ant-api[0-9a-zA-Z-]+'     # Anthropic API keys
    'sk-[a-zA-Z0-9]{20,}'         # OpenAI-style API keys
    'PRIVATE KEY'                   # PEM private keys
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)
FOUND=0

for FILE in $STAGED_FILES; do
    # Skip example and template files — they're supposed to reference key names
    [[ "$FILE" == *.example ]] && continue
    [[ "$FILE" == *.tpl ]] && continue
    [[ "$FILE" == *.md ]] && continue

    for PATTERN in "${PATTERNS[@]}"; do
        if git show ":$FILE" 2>/dev/null | grep -qEi "$PATTERN"; then
            echo "BLOCKED: Potential secret in $FILE (pattern: $PATTERN)"
            FOUND=1
        fi
    done
done

if [ "$FOUND" -eq 1 ]; then
    echo ""
    echo "Commit blocked. Remove secrets from staged files."
    echo "Secrets belong in .env files (not committed), not in source code."
    exit 1
fi

exit 0
```

### `templates/validate_env.py`

```python
"""Environment variable validation for service startup.

Call validate_env() at the top of your application's entry point.
The service fails fast with a clear message rather than crashing later
with a cryptic AttributeError on a missing config value.

Usage:
    from validate_env import validate_env
    env = validate_env()
    # env['DATABASE_URL'] is guaranteed to be set
"""

import os
import sys
from typing import Optional


def validate_env(
    required: Optional[list[str]] = None,
    optional: Optional[dict[str, str]] = None,
) -> dict[str, str]:
    """Validate required environment variables and apply defaults for optional ones.

    Args:
        required: Variable names that must be set and non-empty. Exits if any missing.
        optional: Variable names with default values applied if not set.

    Returns:
        Dict of all validated environment variables.
    """
    if required is None:
        required = REQUIRED
    if optional is None:
        optional = OPTIONAL

    env: dict[str, str] = {}
    missing: list[str] = []

    for var in required:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        else:
            env[var] = value

    if missing:
        print(f"FATAL: Missing required environment variables: {', '.join(missing)}")
        print("Set them in .env (EnvironmentFile) or export before starting the service.")
        sys.exit(1)

    for var, default in optional.items():
        env[var] = os.getenv(var, default)

    return env


# Customize per-service:
REQUIRED = [
    "DATABASE_URL",
    "REDIS_URL",
    "ANTHROPIC_API_KEY",
    "RABBITMQ_URL",
    "JWT_SECRET",
]

OPTIONAL = {
    "LOG_LEVEL": "INFO",
    "DEBUG": "false",
    "ENVIRONMENT": "production",
}
```
