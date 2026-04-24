# Git Server Workflow Checklist

## Workspace Setup

- [ ] Create workspace directory structure: `~/workspace/repos/`
- [ ] Clone all repositories into `~/workspace/repos/`
- [ ] Set up master .env file: `~/workspace/.env` (chmod 600)
- [ ] Create deploy scripts directory: `~/workspace/deploy/`
- [ ] Verify git is configured (user.name, user.email)

## Runtime Setup

- [ ] Create runtime directory: `/srv/nero/` (or `/srv/project/`)
- [ ] Set ownership: `sudo chown -R $USER: /srv/nero/`
- [ ] Create subdirectory for each service
- [ ] Create Python venvs for each Python service
- [ ] Install dependencies in each venv
- [ ] Symlink or copy .env to runtime (or use EnvironmentFile in systemd)

## Deploy Script

### Core Functionality

- [ ] Script accepts service name as argument
- [ ] Script accepts "all" to deploy everything
- [ ] rsync source code from workspace to runtime
- [ ] Exclude unnecessary files (.git, .venv, __pycache__, node_modules)
- [ ] rsync requirements/package files
- [ ] Detect dependency changes and install only when needed
- [ ] Restart service via systemctl --user
- [ ] Wait and verify service started successfully
- [ ] Log deploy results

### Options

- [ ] `--rebuild-venv` flag for full venv recreation
- [ ] `--dry-run` flag to show what would change
- [ ] `--no-restart` flag to sync without restarting
- [ ] Deploy order respects dependencies (SDK first)

### Error Handling

- [ ] Script exits on error (`set -euo pipefail`)
- [ ] Reports which step failed
- [ ] Shows last few log lines on service start failure
- [ ] Returns non-zero exit code on failure

## Deploy Verification

- [ ] Test deploy single service: `deploy.sh nero-core`
- [ ] Test deploy all services: `deploy.sh all`
- [ ] Test deploy with venv rebuild: `deploy.sh nero-core --rebuild-venv`
- [ ] Verify service runs after deploy
- [ ] Verify code changes are reflected in runtime
- [ ] Verify excluded files are not in runtime

## Git Workflow

### Branching

- [ ] main branch is always deployable
- [ ] Feature branches for development
- [ ] Worktrees for parallel agent work (optional)

### Tagging

- [ ] Tag releases before major changes
- [ ] Use semantic versioning (v1.2.3)
- [ ] Test rollback to a tag works

### Rollback

- [ ] Document rollback procedure
- [ ] Test: `git checkout HEAD~1 && deploy.sh service`
- [ ] Test: `git checkout v1.x.x && deploy.sh service`
- [ ] Verify rollback restores previous behavior

## Post-Receive Hook (Optional)

- [ ] Create bare repo on server: `/srv/git/repo.git`
- [ ] Create post-receive hook script
- [ ] Make hook executable
- [ ] Add deploy remote on dev machine
- [ ] Test: `git push deploy main` triggers deployment
- [ ] Verify only main branch triggers deploy (not feature branches)

## Worktrees (Optional)

- [ ] Test worktree creation: `git worktree add ../repo-feature feature/name`
- [ ] Test deploying from worktree
- [ ] Test worktree removal: `git worktree remove ../repo-feature`
- [ ] Set up worktree cleanup schedule
- [ ] Document worktree workflow

## Multi-Repo Coordination

- [ ] Define deploy order (dependencies first)
- [ ] SDK deploys before dependent services
- [ ] Test deploying SDK change propagates correctly
- [ ] Document dependency relationships
- [ ] Test rollback scenario across multiple repos

## Maintenance

- [ ] Regularly pull from origin in workspace repos
- [ ] Prune old branches: `git remote prune origin`
- [ ] Clean up stale worktrees: `git worktree prune`
- [ ] Review and update deploy script as services change
- [ ] Monitor runtime disk usage (old venvs, logs)
