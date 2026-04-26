# Git Server Workflow

## Summary

Workspace/runtime separation pattern for solo VPS deployments: source code lives in `~/workspace/repos/`, services run from `/srv/project/`. Deploy with rsync (not `git pull` to runtime). Rollback by checking out a previous commit in the workspace repo and redeploying. Git worktrees enable parallel agent work on the same repository without branch conflicts.

## Why

Running `git pull` in the runtime directory mixes git operations with a running service — branch switches can break live processes, and uncommitted changes interfere with pulls. rsync copies only changed files in milliseconds, keeping the runtime clean and reproducible. The workspace/runtime split also makes rollback trivial: the workspace is a full git history; the runtime is just synced source.

## When To Use

- Solo VPS with multiple services (Python/Node apps + shared SDK)
- Need to deploy from workspace to server without CI/CD
- Need quick rollback (`git checkout HEAD~1 && deploy.sh service`)
- Running multiple parallel Claude Code agents on the same repo (worktrees)
- Push-to-deploy via post-receive hook on a bare server repo

## When NOT To Use

- Multi-server deployments — rsync from one machine to many is unwieldy; use Ansible or Capistrano
- When the team uses Docker for the application (use image tags + `docker compose up` instead)
- Monorepos where workspace and runtime are the same directory (no separation needed)

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Workspace/runtime directory layout, rsync flags, dependency detection, deploy order for multi-repo |
| `content/02-rollback-worktrees.xml` | Git-based rollback procedure, tagged releases, worktree commands for parallel agents, post-receive hook pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/deploy.sh` | Master deploy script: rsync + venv + systemd restart, supports `all` and `--rebuild-venv` |
| `templates/rollback.sh` | Rollback a service to a previous commit or tag and redeploy |
| `templates/post-receive` | Bare repo post-receive hook for push-to-deploy on main branch |
