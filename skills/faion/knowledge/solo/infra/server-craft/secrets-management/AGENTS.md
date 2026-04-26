# Secrets Management

## Summary

Secrets management for solo developer VPS platforms: .env file hygiene, systemd EnvironmentFile integration, 1Password CLI (op) for programmatic secret injection, pre-commit hooks to block secret commits, file permission hardening, and secret rotation procedures. Defense-in-depth across file permissions, .gitignore, and git hooks.

## Why

Secrets committed to Git or left world-readable on disk are the most common breach vector for solo developer platforms. A single master .env (chmod 600) + systemd EnvironmentFile + gitignore patterns + startup validation covers 95% of risk at minimal overhead. The 1Password op CLI enables zero-secret-on-disk workflows via op inject.

## When To Use

- Setting up a new project requiring API keys, database credentials, or JWT secrets
- Deploying a service to production where .env must be generated from a secrets manager
- Rotating a compromised or expired credential across all services
- Auditing a codebase for hardcoded secrets or improper .env handling
- Configuring systemd EnvironmentFile for a new user service

## When NOT To Use

- Compliance environments requiring HashiCorp Vault or AWS Secrets Manager with audit trails
- Short-lived ephemeral scripts that do not need persistent secrets
- Public configuration values (feature flags, log levels) that do not require protection

## Content

| File | What's inside |
|------|---------------|
| `content/01-env-patterns.xml` | .env format rules, systemd EnvironmentFile gotchas, file permission requirements |
| `content/02-prevention.xml` | .gitignore patterns, pre-commit hook for secret detection, audit commands |
| `content/03-rotation.xml` | Rotation schedule by secret type, rotation procedure, 1Password op inject workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/env.example` | .env.example with grouped placeholders for all common service credentials |
| `templates/env.tpl` | .env.tpl for op inject: 1Password {{ op://Vault/Item/field }} references |
| `templates/pre-commit-secrets.sh` | Pre-commit hook blocking Anthropic/OpenAI key patterns and PRIVATE KEY |
| `templates/validate_env.py` | Python startup validator: required vars list, fail-fast with clear message |
| `templates/gitignore-secrets` | .gitignore block covering .env, *.pem, *.key, id_*, .op/ |
