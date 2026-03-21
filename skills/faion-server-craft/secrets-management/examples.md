# Secrets Management Examples

## Example 1: NERO Platform Master .env

The NERO platform uses a single master .env file at `~/workspace/.env` that is shared across all services via symlinks and systemd EnvironmentFile.

### Master .env Structure

```bash
# ~/workspace/.env
# Generated from 1Password or manually maintained
# chmod 600 ~/workspace/.env

# ============================================================
# Database (shared PostgreSQL in Docker)
# ============================================================
DATABASE_URL=postgresql://nero:PG_STRONG_PASS_HERE@localhost:5432/nero

# ============================================================
# Redis (shared, Docker)
# ============================================================
REDIS_URL=redis://localhost:6379/0

# ============================================================
# RabbitMQ (Docker)
# ============================================================
RABBITMQ_URL=amqp://nero:RMQ_STRONG_PASS_HERE@localhost:5672/nero
RABBITMQ_MANAGEMENT_URL=http://nero:RMQ_STRONG_PASS_HERE@localhost:15672

# ============================================================
# Anthropic (Claude API - main AI provider)
# ============================================================
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================================
# Authentication
# ============================================================
JWT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# ============================================================
# Telegram Bot
# ============================================================
TELEGRAM_BOT_TOKEN=1234567890:ABCDefGhIjKlMnOpQrStUvWxYz
TELEGRAM_ALLOWED_USER_IDS=123456789

# ============================================================
# Application Config (non-secret but convenient here)
# ============================================================
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
CELERY_CONCURRENCY=4
```

### How Services Access Secrets

```ini
# ~/.config/systemd/user/nero-core.service
[Service]
EnvironmentFile=/srv/nero/.env
# /srv/nero/.env is a symlink to ~/workspace/.env
```

```bash
# During deploy, create symlink:
ln -sf ~/workspace/.env /srv/nero/.env
```

### .env.example for the Repository

```bash
# .env.example - Copy to ~/workspace/.env and fill in values
# chmod 600 ~/workspace/.env

DATABASE_URL=postgresql://nero:changeme@localhost:5432/nero
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://nero:changeme@localhost:5672/nero
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
JWT_SECRET=generate-with-openssl-rand-base64-64
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_ALLOWED_USER_IDS=your-telegram-user-id
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
CELERY_CONCURRENCY=4
```

## Example 2: 1Password Service Account Integration

Setting up 1Password CLI on the NERO server for automated secret management.

### Setup

```bash
# 1. Install op CLI
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
  sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/amd64 stable main" | \
  sudo tee /etc/apt/sources.list.d/1password-cli.list
sudo apt update && sudo apt install -y 1password-cli

# 2. Create service account in 1Password web console:
#    - Settings > Service Accounts > New Service Account
#    - Name: "nero-server"
#    - Grant read access to "ServerVault"
#    - Copy the token

# 3. Store token (add to ~/.bashrc or systemd environment)
echo 'export OP_SERVICE_ACCOUNT_TOKEN="ops_xxxxxxxxxxxxxxxxxxxx"' >> ~/.bashrc
source ~/.bashrc

# 4. Verify
op whoami
```

### Create .env Template

```bash
# ~/workspace/.env.tpl
DATABASE_URL={{ op://ServerVault/NERO-Database/connection-url }}
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL={{ op://ServerVault/NERO-RabbitMQ/connection-url }}
ANTHROPIC_API_KEY={{ op://ServerVault/Anthropic/api-key }}
JWT_SECRET={{ op://ServerVault/NERO-JWT/secret }}
TELEGRAM_BOT_TOKEN={{ op://ServerVault/NERO-TelegramBot/token }}
TELEGRAM_ALLOWED_USER_IDS={{ op://ServerVault/NERO-TelegramBot/allowed-users }}
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
CELERY_CONCURRENCY=4
```

### Generate .env

```bash
# Generate .env from 1Password
op inject -i ~/workspace/.env.tpl -o ~/workspace/.env
chmod 600 ~/workspace/.env

# Verify (count lines, don't print values)
wc -l ~/workspace/.env
# Should show ~12 lines
```

### Automate Rotation

```bash
# Rotate Anthropic key:
# 1. Generate new key at console.anthropic.com
# 2. Update in 1Password: op item edit "Anthropic" "api-key=sk-ant-api03-NEW-KEY"
# 3. Regenerate .env: op inject -i ~/workspace/.env.tpl -o ~/workspace/.env && chmod 600 ~/workspace/.env
# 4. Restart services: bash ~/workspace/deploy/deploy.sh all
```

## Example 3: Secrets Audit on NERO Server

Running a comprehensive secrets audit to find leaks.

### Audit Script

```bash
#!/bin/bash
# audit-secrets.sh - Find potential secret leaks
echo "=== Secrets Audit: $(date) ==="
ISSUES=0

echo ""
echo "--- 1. Checking .env file permissions ---"
for envfile in ~/workspace/.env /srv/nero/.env /srv/nero/*/.env; do
    if [ -f "$envfile" ]; then
        PERMS=$(stat -c '%a' "$envfile")
        if [ "$PERMS" != "600" ]; then
            echo "  ISSUE: $envfile has permissions $PERMS (should be 600)"
            ((ISSUES++))
        else
            echo "  OK: $envfile (600)"
        fi
    fi
done

echo ""
echo "--- 2. Checking git repos for secrets ---"
for repo in ~/workspace/repos/nero-*; do
    if [ -d "$repo/.git" ]; then
        REPO_NAME=$(basename "$repo")
        # Check if .env is tracked
        if git -C "$repo" ls-files --error-unmatch .env 2>/dev/null; then
            echo "  ISSUE: $REPO_NAME has .env tracked in git!"
            ((ISSUES++))
        fi
        # Check .gitignore includes .env
        if [ -f "$repo/.gitignore" ] && grep -q "\.env" "$repo/.gitignore"; then
            echo "  OK: $REPO_NAME .gitignore includes .env"
        else
            echo "  WARN: $REPO_NAME .gitignore may not exclude .env"
        fi
    fi
done

echo ""
echo "--- 3. Checking for hardcoded secrets in code ---"
PATTERNS=("sk-ant-api" "sk-[a-zA-Z0-9]{20}" "PRIVATE KEY" "password\s*=\s*['\"][^'\"]+['\"]")
for repo in ~/workspace/repos/nero-*; do
    REPO_NAME=$(basename "$repo")
    for pattern in "${PATTERNS[@]}"; do
        MATCHES=$(grep -rl "$pattern" "$repo" \
            --include="*.py" --include="*.js" --include="*.ts" \
            --exclude-dir=".git" --exclude-dir="node_modules" \
            --exclude-dir=".venv" 2>/dev/null | head -5)
        if [ -n "$MATCHES" ]; then
            echo "  ISSUE: $REPO_NAME may contain secrets matching '$pattern':"
            echo "$MATCHES" | sed 's/^/    /'
            ((ISSUES++))
        fi
    done
done

echo ""
echo "--- 4. Checking SSH key permissions ---"
for keyfile in ~/.ssh/id_*; do
    if [ -f "$keyfile" ] && [[ "$keyfile" != *.pub ]]; then
        PERMS=$(stat -c '%a' "$keyfile")
        if [ "$PERMS" != "600" ]; then
            echo "  ISSUE: $keyfile has permissions $PERMS (should be 600)"
            ((ISSUES++))
        else
            echo "  OK: $keyfile (600)"
        fi
    fi
done

echo ""
echo "=== Audit complete: $ISSUES issues found ==="
```

### Audit Output (Clean Server)

```
=== Secrets Audit: 2026-03-21 ===

--- 1. Checking .env file permissions ---
  OK: /home/nero/workspace/.env (600)
  OK: /srv/nero/.env (600)

--- 2. Checking git repos for secrets ---
  OK: nero-sdk .gitignore includes .env
  OK: nero-core .gitignore includes .env
  OK: nero-channel-web .gitignore includes .env
  OK: nero-channel-tg .gitignore includes .env
  OK: nero-web .gitignore includes .env
  OK: nero-infra .gitignore includes .env

--- 3. Checking for hardcoded secrets in code ---

--- 4. Checking SSH key permissions ---
  OK: /home/nero/.ssh/id_ed25519 (600)

=== Audit complete: 0 issues found ===
```

## Example 4: Per-Service Environment Validation

NERO Core validates all required environment variables at startup.

```python
# nero_core/config.py
import os
import sys

REQUIRED = {
    "DATABASE_URL": "PostgreSQL connection string",
    "REDIS_URL": "Redis connection string",
    "RABBITMQ_URL": "RabbitMQ AMQP connection string",
    "ANTHROPIC_API_KEY": "Anthropic API key for Claude",
}

OPTIONAL = {
    "LOG_LEVEL": ("INFO", "Logging level"),
    "CELERY_CONCURRENCY": ("4", "Number of Celery worker processes"),
    "ENVIRONMENT": ("production", "Environment name"),
}

def validate():
    """Validate environment variables at startup. Exit if any required vars are missing."""
    missing = []
    for var, desc in REQUIRED.items():
        if not os.getenv(var):
            missing.append(f"  {var}: {desc}")

    if missing:
        print("FATAL: Missing required environment variables:")
        for m in missing:
            print(m)
        print("\nSet them in .env or export before starting.")
        sys.exit(1)

    # Set defaults for optional vars
    for var, (default, _desc) in OPTIONAL.items():
        if not os.getenv(var):
            os.environ[var] = default

    # Log startup (without revealing secret values)
    env = os.getenv("ENVIRONMENT", "unknown")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    print(f"Config validated: env={env}, log_level={log_level}, "
          f"db=***@{os.getenv('DATABASE_URL', '').split('@')[-1]}")
```

Startup output:
```
Config validated: env=production, log_level=INFO, db=***@localhost:5432/nero
```
