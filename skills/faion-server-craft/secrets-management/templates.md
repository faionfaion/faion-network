# Secrets Management Templates

## .env.example Template

Copy-paste template for documenting required environment variables without actual secrets.

```bash
# .env.example - Copy to .env and fill in real values
# chmod 600 .env after creating

# ============================================================
# Database
# ============================================================
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# ============================================================
# Redis
# ============================================================
REDIS_URL=redis://localhost:6379/0

# ============================================================
# Message Broker
# ============================================================
RABBITMQ_URL=amqp://user:password@localhost:5672/vhost

# ============================================================
# AI/LLM API Keys
# ============================================================
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxx
# OPENAI_API_KEY=sk-xxxxxxxxxxxx

# ============================================================
# Authentication
# ============================================================
JWT_SECRET=generate-with-openssl-rand-base64-64
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# ============================================================
# Application
# ============================================================
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production

# ============================================================
# External Services (optional)
# ============================================================
# TELEGRAM_BOT_TOKEN=123456:ABC-xxxxxxxxxxxx
# SENTRY_DSN=https://key@sentry.io/project
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=user@gmail.com
# SMTP_PASSWORD=app-password
```

## .env.tpl Template (1Password inject)

Template for generating .env from 1Password vault using `op inject`.

```bash
# .env.tpl - 1Password template
# Usage: op inject -i .env.tpl -o .env && chmod 600 .env

# Database
DATABASE_URL={{ op://ServerVault/Database/url }}

# Redis
REDIS_URL=redis://localhost:6379/0

# Message Broker
RABBITMQ_URL={{ op://ServerVault/RabbitMQ/url }}

# AI Keys
ANTHROPIC_API_KEY={{ op://ServerVault/Anthropic/api-key }}

# Authentication
JWT_SECRET={{ op://ServerVault/JWT/secret }}

# Telegram
TELEGRAM_BOT_TOKEN={{ op://ServerVault/TelegramBot/token }}

# Application (not secrets, literal values)
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
```

## op-unlock.sh Script

Script to generate .env from 1Password on server login.

```bash
#!/bin/bash
# op-unlock.sh - Generate .env from 1Password
# Usage: bash op-unlock.sh [env-template] [output-file]
set -euo pipefail

TEMPLATE="${1:-$HOME/workspace/.env.tpl}"
OUTPUT="${2:-$HOME/workspace/.env}"

# Check 1Password CLI
if ! command -v op &>/dev/null; then
    echo "ERROR: 1Password CLI (op) not installed"
    exit 1
fi

# Check service account token
if [ -z "${OP_SERVICE_ACCOUNT_TOKEN:-}" ]; then
    echo "ERROR: OP_SERVICE_ACCOUNT_TOKEN not set"
    echo "Set it in ~/.bashrc or export it before running this script"
    exit 1
fi

# Check template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

# Generate .env
echo "Generating $OUTPUT from $TEMPLATE..."
op inject -i "$TEMPLATE" -o "$OUTPUT"
chmod 600 "$OUTPUT"

echo "Done. Generated $OUTPUT ($(wc -l < "$OUTPUT") lines)"
echo "Remember to restart services after updating .env"
```

## EnvironmentFile systemd Pattern

Template for systemd service with EnvironmentFile.

```ini
# ~/.config/systemd/user/myservice.service
[Unit]
Description=My Service
After=network.target

[Service]
Type=simple

# Load environment from .env file
# Required file (service fails if missing):
EnvironmentFile=/srv/myproject/.env

# Optional override file (no error if missing, note the - prefix):
EnvironmentFile=-/srv/myproject/.env.local

# Working directory
WorkingDirectory=/srv/myproject/src

# Start command
ExecStart=/srv/myproject/.venv/bin/python -m myservice

# Restart policy
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5

[Install]
WantedBy=default.target
```

## Pre-Commit Hook: Secret Detection

```bash
#!/bin/bash
# .git/hooks/pre-commit (or use git-secrets)
# Prevents committing files containing secret patterns

PATTERNS=(
    'sk-ant-api[0-9a-zA-Z-]+'       # Anthropic API keys
    'sk-[a-zA-Z0-9]{20,}'           # OpenAI API keys
    'PRIVATE KEY'                     # Private keys
    'password\s*=\s*[^$]'           # Hardcoded passwords
    'secret\s*=\s*[^${}]'           # Hardcoded secrets
    'token\s*=\s*[^${}]'            # Hardcoded tokens
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
FOUND=0

for FILE in $STAGED_FILES; do
    # Skip binary files and .env.example
    [[ "$FILE" == *.example ]] && continue
    [[ "$FILE" == *.tpl ]] && continue

    for PATTERN in "${PATTERNS[@]}"; do
        if git show ":$FILE" 2>/dev/null | grep -qEi "$PATTERN"; then
            echo "BLOCKED: Potential secret found in $FILE (pattern: $PATTERN)"
            FOUND=1
        fi
    done
done

if [ "$FOUND" -eq 1 ]; then
    echo ""
    echo "Commit blocked. Remove secrets from staged files."
    echo "Use .env files for secrets, not source code."
    exit 1
fi

exit 0
```

## .gitignore Template for Secrets

```gitignore
# ============================================================
# Environment files (secrets)
# ============================================================
.env
.env.local
.env.production
.env.staging
.env.*.local
*.env

# Keep example/template files
!.env.example
!.env.tpl

# ============================================================
# Cryptographic keys
# ============================================================
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

# ============================================================
# 1Password
# ============================================================
.op/

# ============================================================
# Credential files
# ============================================================
credentials.json
service-account.json
*.credentials
token.json
```

## Startup Validation Template (Python)

```python
"""Environment variable validation module.

Usage:
    from config import validate_env
    validate_env()  # Call at application startup
"""

import os
import sys
from typing import Optional


def validate_env(
    required: Optional[list[str]] = None,
    optional: Optional[dict[str, str]] = None,
) -> dict[str, str]:
    """Validate required environment variables and set defaults for optional ones.

    Args:
        required: List of required variable names. Exits if any are missing.
        optional: Dict of optional variable names with default values.

    Returns:
        Dict of all validated environment variables.
    """
    if required is None:
        required = []
    if optional is None:
        optional = {}

    env = {}
    missing = []

    # Check required variables
    for var in required:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        else:
            env[var] = value

    if missing:
        print(f"FATAL: Missing required environment variables: {', '.join(missing)}")
        print("Set them in .env or export them before starting the service.")
        sys.exit(1)

    # Set defaults for optional variables
    for var, default in optional.items():
        env[var] = os.getenv(var, default)

    return env


# Example usage for NERO platform
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

## Secret Rotation Runbook Template

```markdown
# Secret Rotation: [SECRET_NAME]

## Details
- **Secret:** [e.g., ANTHROPIC_API_KEY]
- **Provider:** [e.g., Anthropic Console]
- **Rotation frequency:** [e.g., 90 days]
- **Last rotated:** [date]
- **Affected services:** [list of services]

## Procedure

1. **Generate new secret**
   - Go to [provider dashboard URL]
   - Generate new key/password
   - Copy new value (DO NOT close the page yet)

2. **Update secret storage**
   - Update in 1Password vault: `op item edit "ItemName" "field=NEW_VALUE"`
   - OR update .env directly: `nano ~/workspace/.env`

3. **Deploy new secret**
   - If using op inject: `bash op-unlock.sh`
   - If direct edit: secret is already in .env

4. **Restart services**
   ```bash
   systemctl --user restart nero-core
   systemctl --user restart nero-channel-web
   systemctl --user restart nero-channel-tg
   ```

5. **Verify**
   - Check service health: `curl http://127.0.0.1:8100/health`
   - Check logs: `journalctl --user -u nero-core --since "2 min ago"`

6. **Revoke old secret**
   - Go to [provider dashboard URL]
   - Delete/revoke the old key

7. **Document**
   - Update "Last rotated" date above
   - Note any issues encountered
```
