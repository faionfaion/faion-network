# Deploy Scripts

## Summary

Bash-based deploy orchestrator for workspace/runtime separation: rsync source to runtime, manage Python virtualenvs with `pip install -e .`, restart systemd user services, and validate with a health check. A single `deploy.sh <service|all> [--rebuild-venv]` script handles the full lifecycle. Pre-deploy checks guard against missing env files or low disk space. Post-deploy health checks catch failures before they reach users.

## Why

Ad-hoc deployment (ssh in, git pull, restart) is error-prone and leaves no audit trail. A structured script enforces consistent deploy order (SDK before dependents), detects dependency changes, validates before and after, and provides a reproducible rollback path. The `--rebuild-venv` flag handles Python upgrades without manual steps.

## When To Use

- Adding or changing a service on a VPS using the workspace/runtime separation pattern
- Setting up initial deploy pipeline for a multi-service Python/Node platform
- Needing rollback capability (`rollback.sh service HEAD~1`)
- Post-deploy health validation before declaring success

## When NOT To Use

- Docker-only deployments (use `docker compose up --pull` instead)
- CI/CD-managed deployments (GitHub Actions, GitLab CI) — the script is for manual/agent-triggered deploys
- Monorepos where workspace and runtime are the same directory

## Content

| File | What's inside |
|------|---------------|
| `content/01-deploy-flow.xml` | Deploy lifecycle: pre-checks, rsync patterns, venv management, restart and validation, hook system |
| `content/02-examples.xml` | NERO platform deploy output examples, rollback scenario, migration hook, pre-deploy validation output |

## Templates

| File | Purpose |
|------|---------|
| `templates/deploy.sh` | Full deploy orchestrator: service registry, pre-checks, rsync, venv, restart, health check |
| `templates/rollback.sh` | Git-based rollback: checkout previous commit, redeploy, print undo command |
| `templates/pre-deploy-check.sh` | Standalone pre-deploy validation: env file, disk space, git status, backing services |
| `templates/status.sh` | Show all service status, Docker containers, health endpoints, resource usage |
