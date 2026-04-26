# Agent Integration — Secrets Management

## When to use
- Setting up a new project that requires API keys, database credentials, or JWT secrets
- Deploying a service to production where the .env must be generated from a secrets manager
- Rotating a compromised or expired credential across all services
- Auditing an existing codebase for hardcoded secrets or improper .env handling
- Configuring systemd EnvironmentFile for a new user service

## When NOT to use
- Secrets that belong in a secrets manager with audit trails (HashiCorp Vault, AWS Secrets Manager) for compliance environments — this methodology covers the solo/VPS pattern, not enterprise compliance
- Short-lived ephemeral scripts that don't need persistent secrets
- Public configuration values (feature flags, log levels) that don't require protection

## Where it fails / limitations
- `.env` files are plaintext at rest — if the server is compromised, all secrets in the file are exposed simultaneously
- `EnvironmentFile` in systemd does not support variable expansion (`$OTHER_VAR` references don't work within the file)
- `op inject` requires active 1Password session or service account token — fails silently if token is expired
- `git-secrets` pre-commit hook only prevents future commits; does not scan existing history
- Per-service `.env` copied from master means rotating one secret requires updating all copies — easy to miss one
- Shell history leaks secrets if you `echo $ANTHROPIC_API_KEY` or use secrets directly in shell commands
- Secrets in Docker build args appear in image layers — `docker history` reveals them; never use build args for runtime secrets

## Agentic workflow
An agent can safely manage secrets by never reading secret values directly but instead using `op read` to inject them at the point of use, or by generating an `.env` from a template using `op inject`. The recommended pattern for agents is: read the `.env.tpl` template, call `op inject` to generate the live `.env`, set permissions, and restart the affected service. The agent should never log, echo, or include secret values in its own output.

### Recommended subagents
- `faion-sdd-executor-agent` — inject secrets during deployment tasks (`.env.tpl` → `op inject` → `.env`)
- `nero-sdd-executor-agent` — NERO service secret rotation and validation

### Prompt pattern
```
Generate a fresh .env for the faion-net-be service:
1. Run: op inject -i ~/workspace/projects/faion-net/faion-net-be/.env.tpl -o /srv/faion-net-be/.env
2. Set permissions: chmod 600 /srv/faion-net-be/.env
3. Verify required variables are present (do NOT print their values):
   for var in DATABASE_URL REDIS_URL ANTHROPIC_API_KEY JWT_SECRET; do
     grep -q "^$var=" /srv/faion-net-be/.env && echo "OK $var" || echo "MISSING $var"
   done
4. Reload systemd: systemctl --user daemon-reload && systemctl --user restart faion-net-api
Output: list of OK/MISSING checks + service restart status
```

```
Rotate the ANTHROPIC_API_KEY:
1. Read new key from 1Password: op read "op://Faion/NERO/anthropic-api-key"
2. Update ~/workspace/.env: sed -i "s/^ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=<new-key>/" ~/workspace/.env
   (Do NOT output the key value in your response)
3. Restart affected services: systemctl --user restart nero-core nero-channel-web nero-channel-tg
4. Verify services are active after 5 seconds
5. Confirm rotation complete
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `op` | 1Password CLI for reading/injecting secrets | [1password.com/downloads/command-line](https://1password.com/downloads/command-line/) |
| `git-secrets` | Pre-commit hook to block secret commits | [github.com/awslabs/git-secrets](https://github.com/awslabs/git-secrets) |
| `truffleHog` | Scan git history for leaked secrets | [github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) |
| `detect-secrets` | Yelp tool for secret detection in code | `pip install detect-secrets` |
| `age` | Modern file encryption (alternative to gpg) | `apt install age` |
| `gpg` | File/value encryption | `apt install gnupg` |
| `chmod` | Set file permissions on .env | Built-in |
| `systemctl` | Reload services after .env changes | Built-in systemd |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| 1Password CLI (`op`) | SaaS + OSS CLI | Yes — service account token | `op inject` generates .env from template; supports CI/CD |
| HashiCorp Vault | OSS | Yes (HTTP API) | Enterprise-grade; overkill for solo but scriptable |
| AWS Secrets Manager | SaaS | Yes (AWS CLI + SDK) | Good if already on AWS; per-secret cost |
| Doppler | SaaS | Yes (CLI + API) | Designed for dev teams; generous free tier |
| Infisical | OSS/SaaS | Yes (CLI + API) | Open-source Doppler alternative |
| Bitwarden Secrets | SaaS | Yes (CLI) | `bws` CLI; good free tier |
| direnv + `.envrc` | OSS | Partial | Per-directory env injection; not suitable for systemd services |

## Templates & scripts
See `templates.md` for full `.env.tpl` template pattern.

Inline: secret validation function for service startup (≤20 lines):
```bash
#!/bin/bash
# validate-env.sh — fail fast if required secrets are missing
# Source this in service entrypoints or deploy scripts

validate_env() {
    local missing=()
    for var in "$@"; do
        if [ -z "${!var:-}" ]; then
            missing+=("$var")
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        echo "FATAL: Missing required env vars: ${missing[*]}" >&2
        exit 1
    fi
    echo "ENV: all required variables present (${#@} checked)"
}

# Usage:
# source validate-env.sh
# validate_env DATABASE_URL REDIS_URL ANTHROPIC_API_KEY JWT_SECRET
```

## Best practices
- Use `EnvironmentFile=-/path/.env` (with `-` prefix) for optional env files; services don't fail if the file is missing during first setup
- Never put `export` prefix in systemd EnvironmentFile — it causes parse errors
- `chmod 600` all `.env` files immediately after creation; the default `umask` on most systems creates 644
- Audit shell history after any manual secret handling: `history | grep -i key` and clear if needed (`history -d <line>`)
- Keep a `.env.tpl` (template with 1Password references) in the repo; keep the generated `.env` in `.gitignore`
- For secret rotation, update the 1Password vault entry first, then re-inject via `op inject` — this is the single source of truth
- Run `truffleHog git file://./` before first push of any new repo to catch accidentally committed secrets

## AI-agent gotchas
- Agent must NEVER log, print, or include secret values in its own output or reasoning — treat all `.env` values as opaque after injection
- `op inject` requires `OP_SERVICE_ACCOUNT_TOKEN` env var or active interactive session; agent must check this before calling
- `sed -i` in-place on `.env` to rotate a key can corrupt the file if disk is full or write is interrupted — always backup first
- Agent reading `.env` with `source .env` in bash will execute any shell commands embedded in the file — dangerous if file is from untrusted source; use `grep "^KEY="` instead
- Service restart after `.env` change requires `systemctl --user daemon-reload` first if the EnvironmentFile path changed
- `op read` outputs the secret followed by a newline — strip with `tr -d '\n'` when assigning to a variable to avoid trailing newline in credentials

## References
- [1Password CLI documentation](https://developer.1password.com/docs/cli/)
- [systemd EnvironmentFile](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#EnvironmentFile=)
- [git-secrets — AWS Labs](https://github.com/awslabs/git-secrets)
- [TruffleHog — secret scanning](https://github.com/trufflesecurity/trufflehog)
- [OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
