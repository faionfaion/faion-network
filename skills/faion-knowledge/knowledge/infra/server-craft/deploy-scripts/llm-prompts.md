# Deploy Scripts LLM Prompts

## Create Deployment Pipeline

```
Create a deployment pipeline for my multi-service platform.

Architecture:
- Source code: [WORKSPACE_PATH, e.g., ~/workspace/repos/]
- Runtime: [RUNTIME_PATH, e.g., /srv/nero/]
- Services: [LIST with types, e.g.:
  - nero-sdk: Python library (no service)
  - nero-core: Python Celery workers (systemd)
  - nero-channel-web: Python FastAPI (systemd)
  - nero-web: React SPA static files (systemd + serve)
  - nero-infra: Docker Compose (PostgreSQL, Redis, RabbitMQ)
]
- .env location: [PATH]
- Python version: [VERSION]

Requirements:
- Deploy single service: deploy.sh <service>
- Deploy all: deploy.sh all
- Rebuild virtualenvs: deploy.sh all --rebuild-venv
- Dependency-aware deploy order
- Pre-deploy validation
- Post-deploy health check
- Rollback support

Provide:
1. deploy.sh (main script, production quality)
2. rollback.sh
3. pre-deploy-check.sh
4. status.sh (show all service status)
5. systemd service file templates
6. Example deploy run output
```

## Deploy Troubleshooting

```
My deployment failed. Help me diagnose and fix.

What happened:
[DESCRIBE, e.g., "deploy.sh nero-core failed, service won't start"]

Error output:
[PASTE DEPLOY OUTPUT AND/OR JOURNAL LOGS]

Server details:
- Ubuntu 24.04
- Python [VERSION]
- Service type: [systemd/docker/static]
- Deploy method: [rsync + pip install / docker compose / etc.]

Please:
1. Diagnose the root cause from the error output
2. Provide fix commands
3. How to verify the fix
4. How to prevent this type of failure
5. If the fix requires rolling back, provide rollback steps
```

## Zero-Downtime Deploy

```
Help me implement zero-downtime deployment for my web service.

Service: [NAME]
Type: [FastAPI with uvicorn / Django with gunicorn / etc.]
Current deploy: [DESCRIBE, e.g., "restart service, ~5s downtime"]
Load balancer: [nginx / none]

Constraints:
- Solo developer, single server
- Must maintain WebSocket connections if possible
- Database migrations may be needed

Options to evaluate:
1. systemctl reload (SIGHUP) for graceful restart
2. Blue-green with port switching
3. Rolling restart with multiple workers
4. Socket-based handoff

For the recommended approach:
- Step-by-step implementation
- nginx configuration changes (if needed)
- systemd service file changes
- Deploy script changes
- Testing procedure
- What if it goes wrong (quick fallback)
```

## Rollback Procedures

```
Help me create rollback procedures for my platform.

Services: [LIST]
Deploy method: rsync from git repo to runtime directory
Version control: git (all services in separate repos)

Rollback scenarios:
1. Bad code deployed (service crashes)
2. Bad migration (database schema broken)
3. Bad dependency update (pip install breaks)
4. Configuration change broke things

For each scenario, provide:
- How to detect the problem
- Immediate actions (stop the bleeding)
- Rollback steps
- Verification after rollback
- How to prevent recurrence

Also provide:
- rollback.sh script
- Pre-deploy snapshot strategy
- Database rollback procedure (Alembic downgrade)
```

## CI/CD Automation

```
Help me automate deployments from GitHub push to production.

Current workflow (manual):
1. Push code to GitHub
2. SSH to server
3. git pull in workspace repo
4. Run deploy.sh

Desired workflow:
- Push to main branch triggers deploy
- GitHub Actions or webhook-based
- No GitHub runners needed (server pulls)

Constraints:
- Single VPS (no separate CI/CD server)
- Don't want to expose SSH to GitHub Actions
- Want to keep it simple (solo developer)

Options to evaluate:
1. GitHub webhook + listener on server
2. GitHub Actions with SSH deploy
3. Cron-based git pull + auto-deploy
4. Simple webhook endpoint on the server

For the recommended approach:
- Complete setup guide
- Security considerations
- How to handle failures
- How to skip deploy (commit message flag)
- Notification on deploy success/failure
```

## Deploy Script for New Project

```
Create a deploy script for a new project I'm adding to my server.

Project: [NAME]
Type: [FastAPI / Next.js / Django / etc.]
Source: [SOURCE_PATH]
Runtime: [RUNTIME_PATH]
Port: [PORT]
Database: [yes/no, shared PostgreSQL]
Needs venv: [yes/no]

Requirements:
- Sync code from source to runtime
- Create/manage virtualenv (if Python)
- Install dependencies
- Run migrations (if applicable)
- Restart systemd service
- Health check after deploy

Existing infrastructure:
- Master .env at [PATH]
- Deploy scripts at [PATH]
- systemd user services

Provide:
1. Deploy script for this specific project
2. systemd service file
3. How to integrate with existing deploy.sh (if applicable)
4. First-time setup vs subsequent deploys
```
