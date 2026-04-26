# Secrets Management Checklist

## Initial Setup

- [ ] Create master .env file with all required variables
- [ ] Set file permissions: `chmod 600 ~/.env` or equivalent
- [ ] Create .env.example with placeholder values (no real secrets)
- [ ] Add .env and secret patterns to .gitignore
- [ ] Verify .gitignore is committed and working (`git status` shows no .env)

## Environment Variable Hygiene

- [ ] No `export` prefix in .env (systemd EnvironmentFile does not support it)
- [ ] No variable expansion ($VAR) in .env (use literal values)
- [ ] All values with special characters are quoted
- [ ] No trailing spaces after values
- [ ] Comments explain non-obvious variables
- [ ] Naming follows `SERVICE_VARIABLE` convention

## systemd Integration

- [ ] EnvironmentFile directive points to correct .env path
- [ ] Optional .env files use `-` prefix: `EnvironmentFile=-/path`
- [ ] `systemctl --user daemon-reload` after changing EnvironmentFile paths
- [ ] Service starts successfully with environment variables loaded
- [ ] Verify variables are available: `systemctl --user show nero-core -p Environment`

## Git Protection

- [ ] .gitignore includes: `.env`, `.env.*`, `*.pem`, `*.key`, `id_rsa`, `id_ed25519`
- [ ] .gitignore excludes: `!.env.example`, `!.env.tpl`
- [ ] Pre-commit hook installed (git-secrets or similar)
- [ ] Custom patterns added for Anthropic keys (`sk-ant-api...`)
- [ ] Custom patterns added for OpenAI keys (`sk-...`)
- [ ] Custom patterns added for private keys (`PRIVATE KEY`)
- [ ] Test: try committing a file with a secret pattern (should be blocked)

## File Permissions

- [ ] .env files: `600` (owner read/write only)
- [ ] SSH directory: `700`
- [ ] SSH private keys: `600`
- [ ] SSH public keys: `644`
- [ ] SSH authorized_keys: `600`
- [ ] SSL certificate keys: `600`

## Service Startup Validation

- [ ] Each service validates required environment variables at startup
- [ ] Missing variables cause immediate exit with clear error message
- [ ] No secrets logged during startup (even at DEBUG level)
- [ ] Startup logs confirm which .env file was loaded (path only, not contents)

## 1Password CLI (Optional)

- [ ] `op` CLI installed and working
- [ ] Service account created in 1Password web console
- [ ] Service account token stored securely (OP_SERVICE_ACCOUNT_TOKEN)
- [ ] Vault access restricted to needed items only
- [ ] .env.tpl template created with `{{ op://Vault/Item/Field }}` references
- [ ] `op inject` generates .env from template successfully
- [ ] Generated .env has correct permissions (600)

## Secret Rotation

- [ ] Rotation schedule documented per secret type
- [ ] API keys: rotation procedure documented
- [ ] Database passwords: ALTER USER procedure documented
- [ ] JWT secrets: key rotation procedure documented
- [ ] Rotation tested: new secret works, old secret revoked
- [ ] All affected services restarted after rotation

## Audit

- [ ] No secrets in git history: `git log -p | grep -i "api.key\|password\|secret"` returns nothing sensitive
- [ ] No secrets in Docker images: `docker history` and Dockerfile review
- [ ] No secrets in shell history: `~/.bash_history` reviewed
- [ ] No secrets in log files: grep application logs for secret patterns
- [ ] No secrets in error messages or stack traces
- [ ] File permissions reviewed on all .env files across the system

## Emergency: Secret Leaked

- [ ] Identify which secret(s) were exposed
- [ ] Rotate affected secret immediately
- [ ] Update .env on all servers
- [ ] Restart affected services
- [ ] Revoke old secret at provider (API dashboard)
- [ ] Check for unauthorized usage during exposure window
- [ ] Review git history: if committed, use `git filter-repo` to remove
- [ ] Add prevention measure (pre-commit hook, etc.)
- [ ] Document incident and update procedures
