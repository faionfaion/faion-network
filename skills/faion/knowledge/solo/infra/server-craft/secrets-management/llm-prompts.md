# Secrets Management LLM Prompts

## Secrets Audit

```
Audit the secrets management setup for my server project.

Context:
- Server: Ubuntu 24.04, Hetzner CX53
- Master .env location: [PATH]
- Services: [LIST OF SERVICES]
- Using systemd EnvironmentFile for secret injection

Check:
1. File permissions on all .env files (should be 600)
2. .gitignore includes .env patterns in all repos
3. No secrets committed to git history
4. No hardcoded secrets in source code (grep for API key patterns)
5. EnvironmentFile paths in systemd service files are correct
6. No secrets in Docker images or Dockerfiles
7. SSH key permissions are correct

For each issue found:
- Severity (critical/warning/info)
- Exact file and line
- Remediation command

Output format: Markdown table with findings.
```

## Secret Rotation Runbook

```
Create a secret rotation runbook for my platform.

Secrets to rotate:
- ANTHROPIC_API_KEY (Anthropic Console)
- DATABASE_URL (PostgreSQL password)
- RABBITMQ_URL (RabbitMQ password)
- JWT_SECRET (application JWT signing key)
- TELEGRAM_BOT_TOKEN (Telegram BotFather)

For each secret, provide:
1. Rotation frequency recommendation
2. Step-by-step rotation procedure
3. Which services need restart
4. Verification steps after rotation
5. Rollback procedure if new secret doesn't work

Server details:
- .env location: ~/workspace/.env
- Deploy script: bash ~/workspace/deploy/deploy.sh
- Services: nero-core, nero-channel-web, nero-channel-tg
- systemd user services
```

## Leak Detection

```
Help me check if any secrets have been leaked.

I need to:
1. Search git history across all repos for secret patterns
2. Check if .env files are tracked in any repo
3. Search application logs for leaked secret values
4. Check Docker image layers for embedded secrets
5. Verify no secrets in CI/CD configuration files

Repos to check: [LIST OR PATH]
Secret patterns to search for:
- sk-ant-api (Anthropic)
- sk- followed by 20+ chars (OpenAI)
- "PRIVATE KEY"
- Hardcoded passwords in Python/JS files

Provide exact commands to run and expected output.
If any leaks are found, provide remediation steps including git history cleanup.
```

## Generate .env Template

```
Generate a comprehensive .env.example file for my platform.

Services and their required variables:
- nero-core (Celery worker): DATABASE_URL, REDIS_URL, RABBITMQ_URL, ANTHROPIC_API_KEY
- nero-channel-web (FastAPI): DATABASE_URL, REDIS_URL, RABBITMQ_URL, JWT_SECRET
- nero-channel-tg (Telegram bot): RABBITMQ_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USER_IDS
- nero-web (React SPA): no server-side env vars

Requirements:
- Group by category (Database, Cache, Broker, AI, Auth, Telegram, App Config)
- Include comments explaining each variable
- Use placeholder values that clearly indicate format (not real values)
- Include LOG_LEVEL, DEBUG, ENVIRONMENT as non-secret config
- Note which variables are optional
- Include instructions at the top for generating secure values
```

## Migrate from Hardcoded Secrets

```
Help me migrate from hardcoded secrets to .env-based secret management.

Current state:
- Some secrets are hardcoded in Python config files
- Some are passed as command-line arguments
- Some are in a Docker Compose file
- No centralized .env file

Target state:
- Single master .env file
- systemd EnvironmentFile loads secrets
- All repos have .env in .gitignore
- .env.example documents required variables
- Startup validation fails fast on missing vars

Provide:
1. Commands to find all hardcoded secrets
2. Migration plan (step by step)
3. .env file to create
4. Code changes needed (Python config module)
5. systemd service file changes
6. .gitignore updates
7. Verification steps
```

## 1Password CLI Setup

```
Set up 1Password CLI (op) on my Ubuntu 24.04 server for automated secret management.

Requirements:
- Service account (non-interactive, no browser)
- Read-only access to a "ServerVault"
- .env.tpl template with op:// references
- op inject workflow to generate .env
- Integration with deploy scripts

Provide:
1. Installation commands for op CLI
2. Service account creation guide (1Password web console steps)
3. .env.tpl template for my services
4. op-unlock.sh script
5. Integration with systemd (how to make OP_SERVICE_ACCOUNT_TOKEN available)
6. Security considerations for storing the service account token
```
