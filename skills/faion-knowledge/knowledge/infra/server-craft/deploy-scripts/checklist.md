# Create Deployment Pipeline Checklist

## Prerequisites

- [ ] Workspace/runtime separation defined (source dir, runtime dir)
- [ ] .env file exists with all required secrets
- [ ] systemd service files created for all services
- [ ] Services can start manually: `systemctl --user start <service>`

## Deploy Script Structure

- [ ] Create deploy directory: `mkdir -p ~/workspace/deploy/`
- [ ] Create main deploy script: `deploy.sh`
- [ ] Create service registry (map of service names to types)
- [ ] Support single service deploy: `deploy.sh nero-core`
- [ ] Support full deploy: `deploy.sh all`
- [ ] Support venv rebuild: `deploy.sh all --rebuild-venv`
- [ ] Make script executable: `chmod +x deploy.sh`

## Pre-Deploy Checks

- [ ] Validate .env file exists
- [ ] Check disk space (minimum 1GB free)
- [ ] Verify systemd user session available
- [ ] Verify runtime directory exists
- [ ] Verify source directory exists
- [ ] Check for required tools (rsync, python3, pip)

## Code Sync (rsync)

- [ ] rsync from workspace to runtime
- [ ] Exclude .git/ directory
- [ ] Exclude __pycache__/ directories
- [ ] Exclude .venv/ directory (managed separately)
- [ ] Exclude .env files (managed separately)
- [ ] Exclude node_modules/ (if applicable)
- [ ] Use `--delete` to remove old files
- [ ] Test rsync with `--dry-run` first

## Virtualenv Management

- [ ] Create venv if not exists
- [ ] Rebuild venv when `--rebuild-venv` flag passed
- [ ] Upgrade pip before installing dependencies
- [ ] Install project with `pip install -e .` (editable)
- [ ] Handle requirements.txt if it exists
- [ ] Verify imports work: `python -c "import <module>"`

## Dependency Order

- [ ] Define deploy order for all services
- [ ] Libraries (nero-sdk) deployed first
- [ ] Infrastructure (docker-compose) before application services
- [ ] Backend before frontend (if frontend depends on API)
- [ ] Document which services need redeployment when a dependency changes

## Service Restart

- [ ] `systemctl --user restart <service>`
- [ ] Wait for service to start (2-5 seconds)
- [ ] Check service is active: `systemctl --user is-active <service>`
- [ ] Check for startup errors: `journalctl --user -u <service> --since "1 min ago"`

## Post-Deploy Validation

- [ ] HTTP health check (for API services): `curl -sf http://127.0.0.1:<port>/health`
- [ ] Service is-active check (for non-HTTP services)
- [ ] No error logs in journal
- [ ] All dependent services still healthy

## Rollback

- [ ] Git-based rollback procedure documented
- [ ] Know how to: `cd repo && git checkout HEAD~1 && bash deploy.sh <service>`
- [ ] Optional: pre-deploy snapshot of runtime directory
- [ ] Optional: rollback.sh script that automates the above
- [ ] Rollback tested: deploy, break, rollback, verify

## Deploy Hooks (Optional)

- [ ] Pre-deploy hook: backup, validation
- [ ] Post-sync hook: run database migrations
- [ ] Post-restart hook: verify health, send notification
- [ ] Hook scripts are in service repo: `deploy-hooks/`

## Environment Validation

- [ ] .env symlink created in runtime directory
- [ ] Required environment variables present
- [ ] Database connection works
- [ ] Redis connection works
- [ ] RabbitMQ connection works (if applicable)
- [ ] External API keys valid (basic validation)

## Testing the Pipeline

- [ ] Full deploy from scratch: `deploy.sh all --rebuild-venv`
- [ ] Single service deploy: `deploy.sh nero-core`
- [ ] Deploy with no changes (idempotent)
- [ ] Deploy with code changes
- [ ] Deploy with dependency changes
- [ ] Rollback and redeploy
- [ ] Pre-deploy check failure handling

## Documentation

- [ ] Deploy procedure documented (which commands, what order)
- [ ] Rollback procedure documented
- [ ] Service dependency map documented
- [ ] Port allocations documented
- [ ] Known issues and workarounds documented
