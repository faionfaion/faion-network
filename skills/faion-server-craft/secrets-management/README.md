# Secrets Management

## Overview

Secrets management for solo developers running AI agent platforms on VPS. Covers environment variable hygiene, .env file patterns, systemd EnvironmentFile integration, 1Password CLI (`op`) for programmatic secret access, service accounts, secret rotation strategies, and preventing secret leaks.

**Target:** Ubuntu 24.04 VPS (Hetzner CX53) running multi-service platforms with systemd user services.

## When to Use

| Scenario | Fit |
|----------|-----|
| Setting up a new project with API keys | Essential |
| Deploying services that need database credentials | Essential |
| Rotating compromised or expired secrets | Essential |
| Auditing existing secret hygiene | Recommended |
| Migrating from hardcoded secrets to .env | Recommended |
| Setting up 1Password CLI for automation | Good |
| CI/CD pipeline secret injection | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **.env file** | Plain-text key=value file, never committed to git |
| **EnvironmentFile** | systemd directive that loads .env into service environment |
| **op CLI** | 1Password CLI for reading secrets from vault programmatically |
| **Service account** | 1Password account for non-interactive (server) access |
| **Secret rotation** | Periodic replacement of credentials to limit blast radius |
| **Least privilege** | Each service only gets the secrets it needs |
| **Defense in depth** | Multiple layers: file perms, .gitignore, pre-commit hooks |

## .env File Patterns

### Master .env

Single source of truth for all secrets on the server. Services reference it via EnvironmentFile or symlinks.

```
~/workspace/.env          # Master env (all secrets)
/srv/nero/.env            # Symlink or copy for runtime
```

### Per-Service .env

Each service gets only the variables it needs, sourced from the master file or generated during deploy.

```
/srv/nero/nero-core/.env        # Core-specific subset
/srv/nero/nero-channel-web/.env # Web channel subset
```

### .env File Format Rules

```bash
# Comments start with #
# No spaces around = sign
# Quote values with special characters
# No export prefix (systemd EnvironmentFile does not support it)

DATABASE_URL=postgresql://nero:secretpass@localhost:5432/nero
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxx
JWT_SECRET=a-long-random-string-here
RABBITMQ_URL=amqp://nero:rabbitpass@localhost:5672/nero

# Feature flags (not secrets, but convenient here)
LOG_LEVEL=INFO
DEBUG=false
```

## systemd EnvironmentFile Integration

### How It Works

systemd's `EnvironmentFile=` directive reads key=value pairs and injects them as environment variables into the service process.

```ini
[Service]
EnvironmentFile=/srv/nero/.env
EnvironmentFile=-/srv/nero/nero-core/.env   # Optional (- prefix)
ExecStart=/srv/nero/nero-core/.venv/bin/celery -A nero_core worker
```

### Important Rules

| Rule | Detail |
|------|--------|
| No `export` prefix | `EnvironmentFile` does not parse `export KEY=val` |
| No variable expansion | `$VAR` is not expanded, use literal values |
| `-` prefix = optional | `EnvironmentFile=-/path` won't fail if file missing |
| File permissions | Must be readable by the user running the service |
| Reload required | `systemctl --user daemon-reload` after changing EnvironmentFile path |

## 1Password CLI (op)

### Installation

```bash
# Ubuntu/Debian
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
  sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/amd64 stable main" | \
  sudo tee /etc/apt/sources.list.d/1password-cli.list
sudo apt update && sudo apt install -y 1password-cli
```

### Service Account (Non-Interactive)

For servers that need to read secrets without human interaction:

1. Create a service account in 1Password web console
2. Grant it read access to the specific vault
3. Set the token as an environment variable

```bash
# In ~/.bashrc or system environment
export OP_SERVICE_ACCOUNT_TOKEN="ops_xxxxxxxxxxxx"

# Read a secret
op read "op://ServerVault/NERO/ANTHROPIC_API_KEY"

# Inject into .env
op inject -i .env.tpl -o .env
```

### op inject Pattern

Template file (`.env.tpl`) references 1Password items:

```bash
DATABASE_URL={{ op://ServerVault/NERO-DB/url }}
ANTHROPIC_API_KEY={{ op://ServerVault/NERO/anthropic-api-key }}
JWT_SECRET={{ op://ServerVault/NERO/jwt-secret }}
```

Then generate the actual .env:

```bash
op inject -i ~/workspace/.env.tpl -o ~/workspace/.env
chmod 600 ~/workspace/.env
```

## Secret Rotation

### Rotation Strategy

| Secret Type | Rotation Frequency | Method |
|-------------|-------------------|--------|
| API keys (Anthropic, OpenAI) | 90 days or on compromise | Regenerate in provider dashboard |
| Database passwords | 180 days | ALTER USER, update .env, restart |
| JWT signing keys | 90 days | Generate new key, update .env |
| SSH keys | Annually | ssh-keygen, update authorized_keys |
| RabbitMQ passwords | 180 days | rabbitmqctl, update .env |

### Rotation Procedure

1. Generate new secret value
2. Update in 1Password vault (if using op)
3. Update .env file on server
4. Restart affected services
5. Verify services are healthy
6. Revoke old secret (if applicable)

## Prevention: Never Commit Secrets

### .gitignore Patterns

```gitignore
# Environment files
.env
.env.local
.env.production
.env.*.local
*.env

# Keep examples
!.env.example
!.env.tpl

# Key files
*.pem
*.key
*.p12
*.pfx
id_rsa
id_ed25519

# 1Password
.op/

# OS-specific
.DS_Store
Thumbs.db
```

### Pre-Commit Hook (git-secrets)

```bash
# Install git-secrets
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets && sudo make install

# Configure for repo
cd ~/workspace/repos/nero-core
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'sk-ant-api[0-9a-zA-Z-]+'    # Anthropic keys
git secrets --add 'sk-[a-zA-Z0-9]{48}'          # OpenAI keys
git secrets --add 'PRIVATE KEY'                   # Private keys
```

### File Permissions

```bash
# .env files: owner read/write only
chmod 600 ~/workspace/.env
chmod 600 /srv/nero/.env

# SSH keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
```

## Environment Variable Hygiene

### Naming Conventions

| Pattern | Example | Usage |
|---------|---------|-------|
| `SERVICE_VARIABLE` | `NERO_CORE_LOG_LEVEL` | Service-specific config |
| `PROVIDER_KEY` | `ANTHROPIC_API_KEY` | Third-party API credentials |
| `DB_*` | `DATABASE_URL` | Database connection |
| `REDIS_*` | `REDIS_URL` | Cache/broker connection |

### Validation at Startup

Every service should validate required environment variables at startup and fail fast with clear error messages:

```python
import os
import sys

REQUIRED_VARS = [
    "DATABASE_URL",
    "REDIS_URL",
    "ANTHROPIC_API_KEY",
    "RABBITMQ_URL",
]

missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    print(f"FATAL: Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)
```

## Threat Model

| Threat | Mitigation |
|--------|-----------|
| Secret committed to git | .gitignore, pre-commit hooks, git-secrets |
| Secret in shell history | Use `op read` piped directly, avoid echo |
| Secret in logs | Never log secret values, mask in output |
| File permission too open | chmod 600 on all .env files |
| Secret in Docker image | Use EnvironmentFile, never COPY .env in Dockerfile |
| Compromised API key | Rotation procedure, monitoring for unusual usage |
| Server compromise | Limit blast radius with per-service secrets |

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [server-init-bootstrap](../server-init-bootstrap/) | Initial secret setup during bootstrap |
| [deploy-scripts](../deploy-scripts/) | Secret injection during deployment |
| [dotfiles-management](../dotfiles-management/) | What NOT to put in dotfiles |
| [multi-project-hosting](../multi-project-hosting/) | Per-project secret isolation |
