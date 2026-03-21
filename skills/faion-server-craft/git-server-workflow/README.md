# Git Server Workflow

Git-based deployment patterns for single-server platforms. Covers workspace/runtime separation, rsync-based deploy scripts, worktrees for parallel agents, CI-less deploy patterns, git-based rollback, and post-receive hooks.

## Overview

For solo developer VPS platforms, deploying from Git without CI/CD pipelines is fast and simple. The pattern separates workspace (where you develop) from runtime (where services execute).

| Concept | Description |
|---------|-------------|
| **Workspace** | Git repos, source code, development tools (`~/workspace/repos/`) |
| **Runtime** | Deployed code, venvs, running services (`/srv/nero/`) |
| **Deploy script** | rsync from workspace to runtime + service restart |
| **Rollback** | git checkout previous commit + redeploy |

## Why Workspace/Runtime Separation

| Aspect | Single Directory | Workspace + Runtime |
|--------|-----------------|---------------------|
| Git operations | Affect running services | Isolated from services |
| Branch switching | Can break running app | No impact on runtime |
| Dependency install | Blocks running app | Separate venv per location |
| Agent changes | Can crash production | Deploy when ready |
| Disk layout | Everything mixed | Clean separation |
| Permissions | Need write access to runtime | Runtime can be read-only |

## Directory Layout

```
~/workspace/                    # Development workspace
  repos/                        # Git repositories
    nero-sdk/                   #   Shared library
    nero-core/                  #   Celery worker (source)
    nero-channel-web/           #   FastAPI API (source)
    nero-channel-tg/            #   Telegram bot (source)
    nero-web/                   #   React SPA (source)
    nero-infra/                 #   Docker Compose + migrations
  deploy/
    deploy.sh                   # Master deploy script
  .env                          # Master env file (shared)

/srv/nero/                      # Runtime (services run from here)
  nero-core/                    #   Deployed code + .venv
    src/                        #     Synced source code
    .venv/                      #     Production virtualenv
    requirements.txt
  nero-channel-web/             #   Deployed code + .venv
    src/
    .venv/
  nero-channel-tg/              #   Deployed code + .venv
  nero-web/                     #   Built static files
    dist/
  nero-infra/                   #   Docker Compose files
```

## Deploy Flow

```
Developer/Agent makes changes in ~/workspace/repos/nero-core/
    |
    v
Runs: bash ~/workspace/deploy/deploy.sh nero-core
    |
    v
deploy.sh:
  1. rsync src/ -> /srv/nero/nero-core/src/
  2. rsync requirements.txt -> /srv/nero/nero-core/
  3. pip install -r requirements.txt (if changed)
  4. systemctl --user restart nero-core
  5. Verify service is running
  6. Done
```

## rsync-Based Deploy

### Why rsync

| Method | Speed | Reliability | Incremental | Simple |
|--------|-------|-------------|-------------|--------|
| rsync | Fast | High | Yes (only changed files) | Yes |
| cp -r | Slow | Medium | No (copies everything) | Yes |
| git clone | Slow | High | No (full clone) | No |
| Docker build | Very slow | High | Partial | Complex |
| symlink switch | Instant | High | N/A | Medium |

### rsync Flags

```bash
rsync -a --delete \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='.mypy_cache' \
    --exclude='.ruff_cache' \
    --exclude='node_modules' \
    "$SOURCE/" "$DEST/"
```

| Flag | Purpose |
|------|---------|
| `-a` | Archive mode (recursive, preserves permissions, timestamps) |
| `--delete` | Remove files in dest that don't exist in source |
| `--exclude` | Skip directories/files that shouldn't be deployed |

## Git-Based Rollback

### Quick Rollback

```bash
# In workspace repo
cd ~/workspace/repos/nero-core

# Check recent commits
git log --oneline -10

# Rollback to previous commit
git checkout HEAD~1

# Redeploy
bash ~/workspace/deploy/deploy.sh nero-core

# Return to latest
git checkout main
```

### Tagged Releases

```bash
# Tag a known-good state
git tag -a v1.2.3 -m "Working state before auth refactor"

# Deploy a specific tag
git checkout v1.2.3
bash ~/workspace/deploy/deploy.sh nero-core

# Return to main
git checkout main
```

### Commit-Based Rollback

```bash
# Deploy specific commit
git checkout abc1234
bash ~/workspace/deploy/deploy.sh nero-core
git checkout main  # Return HEAD to main
```

## Post-Receive Hooks (Push-to-Deploy)

For automated deployment when pushing to a bare repo on the server.

### Setup Bare Repository

```bash
# Create bare repo on server
mkdir -p /srv/git/nero-core.git
cd /srv/git/nero-core.git
git init --bare

# Create post-receive hook
cat > hooks/post-receive << 'HOOK'
#!/bin/bash
# Deploy on push to main branch

set -euo pipefail

while read oldrev newrev refname; do
    BRANCH=$(git rev-parse --symbolic --abbrev-ref "$refname" 2>/dev/null || echo "")

    if [ "$BRANCH" = "main" ]; then
        echo "=== Deploying nero-core (main branch) ==="

        # Checkout to workspace
        GIT_WORK_TREE=/home/nero/workspace/repos/nero-core git checkout -f main

        # Run deploy
        bash /home/nero/workspace/deploy/deploy.sh nero-core

        echo "=== Deploy complete ==="
    fi
done
HOOK
chmod +x hooks/post-receive
```

### Add Remote on Dev Machine

```bash
# On local dev machine
cd nero-core
git remote add deploy nero@server:/srv/git/nero-core.git

# Push to deploy
git push deploy main
```

## Worktrees for Parallel Agents

Git worktrees allow multiple checkouts of the same repository, enabling parallel agent work.

```bash
# Main repo (workspace)
~/workspace/repos/nero-core/          # main branch

# Worktrees for parallel work
~/workspace/repos/nero-core-feature/  # feature branch worktree
~/workspace/repos/nero-core-hotfix/   # hotfix branch worktree
```

### Worktree Commands

```bash
# Create worktree for feature branch
cd ~/workspace/repos/nero-core
git worktree add ../nero-core-feature feature/new-api

# List all worktrees
git worktree list
# /home/nero/workspace/repos/nero-core          abc1234 [main]
# /home/nero/workspace/repos/nero-core-feature  def5678 [feature/new-api]

# Remove worktree
git worktree remove ../nero-core-feature

# Prune stale entries
git worktree prune
```

### Worktree Deploy

```bash
# Deploy from a worktree (same deploy script works)
cd ~/workspace/repos/nero-core-feature
bash ~/workspace/deploy/deploy.sh nero-core

# Or deploy from main repo
cd ~/workspace/repos/nero-core
bash ~/workspace/deploy/deploy.sh nero-core
```

## Dependency Management

### Detect Changed Requirements

```bash
# Compare deployed vs workspace requirements
diff -q ~/workspace/repos/nero-core/requirements.txt /srv/nero/nero-core/requirements.txt

# Install only if changed
if ! diff -q "$WORKSPACE/requirements.txt" "$RUNTIME/requirements.txt" &>/dev/null; then
    echo "Requirements changed, installing..."
    "$RUNTIME/.venv/bin/pip" install -q -r "$WORKSPACE/requirements.txt"
fi
```

### Venv Rebuild

```bash
# Full venv rebuild (for major dependency changes)
rm -rf /srv/nero/nero-core/.venv
python3 -m venv /srv/nero/nero-core/.venv
/srv/nero/nero-core/.venv/bin/pip install -r /srv/nero/nero-core/requirements.txt

# Install SDK in editable mode (if using local SDK)
/srv/nero/nero-core/.venv/bin/pip install -e /srv/nero/nero-sdk
```

## Multi-Repo Deploy

When deploying a platform with multiple repos that share a common SDK:

```bash
# Deploy order matters: SDK first, then dependents
bash ~/workspace/deploy/deploy.sh nero-sdk
bash ~/workspace/deploy/deploy.sh nero-core
bash ~/workspace/deploy/deploy.sh nero-channel-web
bash ~/workspace/deploy/deploy.sh nero-channel-tg
bash ~/workspace/deploy/deploy.sh nero-web

# Or deploy all at once
bash ~/workspace/deploy/deploy.sh all
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Service won't start after deploy | Import error, missing dependency | Check logs, pip install |
| Old code still running | Service not restarted | Verify systemctl restart ran |
| rsync deletes too much | Missing --exclude for important dirs | Add excludes |
| Permission denied on deploy | Wrong ownership in /srv/nero | `chown -R nero: /srv/nero` |
| Stale .pyc files | Python caching old compiled files | Delete `__pycache__` dirs |
| Venv broken after OS upgrade | Python version mismatch | Rebuild venv |

## Related Methodologies

- `systemd-user-services/` -- services that get restarted after deploy
- `deploy-scripts/` -- detailed deploy script patterns
- `agent-dev-tuning/` -- worktree patterns for agents
