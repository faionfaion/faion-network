# Git Server Workflow Examples

## Example 1: NERO Platform Deploy Flow

The NERO platform uses rsync-based deployment from `~/workspace/repos/` to `/srv/nero/`.

### Daily Deployment Pattern

```bash
# 1. Agent or developer makes changes
cd ~/workspace/repos/nero-core
# ... edit files ...
git add -A && git commit -m "feat: add conversation threading"

# 2. Deploy the changed service
bash ~/workspace/deploy/deploy.sh nero-core
# 09:15:23 [nero-core] === Deploying ===
# 09:15:23 [nero-core] Syncing source code...
# 09:15:24 [nero-core] Restarting service...
# 09:15:26 [nero-core] Running
# 09:15:26 [nero-core] === Done ===

# 3. Verify
curl -s http://127.0.0.1:8100/health | python3 -m json.tool
# {"status": "ok", "version": "1.3.0"}

# 4. Push to GitHub (for backup, not for deploy)
git push origin main
```

### SDK Change Flow (Multi-Repo)

When changing the shared SDK, all dependent services need redeployment:

```bash
# 1. Change SDK
cd ~/workspace/repos/nero-sdk
# ... edit models, protocols ...
git add -A && git commit -m "feat: add thread_id to MessageEnvelope"

# 2. Update dependent services to use new SDK
cd ~/workspace/repos/nero-core
# ... update code to use thread_id ...
git add -A && git commit -m "feat: use thread_id from SDK"

cd ~/workspace/repos/nero-channel-web
# ... update code ...
git add -A && git commit -m "feat: expose thread_id in API"

# 3. Deploy all (respects dependency order: SDK first)
bash ~/workspace/deploy/deploy.sh all
# Deploys: nero-sdk -> nero-core -> nero-channel-web -> nero-channel-tg -> nero-web
```

### Full Rebuild

When Python or system packages change significantly:

```bash
# Rebuild all venvs from scratch
bash ~/workspace/deploy/deploy.sh all --rebuild-venv
# 09:20:00 [nero-sdk] === Deploying ===
# 09:20:01 [nero-sdk] Syncing library...
# ...
# 09:20:30 [nero-core] Creating virtualenv...
# 09:21:15 [nero-core] Restarting service...
# 09:21:17 [nero-core] Running
# ...
# Total time: ~5 minutes for full rebuild
```

---

## Example 2: Rollback After Bad Deploy

Scenario: A new commit broke the API. Need to rollback quickly.

```bash
# 1. Notice the problem
curl http://127.0.0.1:8100/health
# {"status": "error", "message": "ImportError: ..."}

# 2. Check what was recently deployed
cd ~/workspace/repos/nero-core
git log --oneline -5
# abc1234 (HEAD -> main) feat: broken refactor
# def5678 fix: handle empty responses
# ghi9012 feat: add metrics endpoint
# jkl3456 fix: rate limiting

# 3. Rollback to previous commit
git checkout HEAD~1   # or: git checkout def5678

# 4. Redeploy
bash ~/workspace/deploy/deploy.sh nero-core

# 5. Verify fix
curl http://127.0.0.1:8100/health
# {"status": "ok"}

# 6. Return workspace to main branch
git checkout main

# 7. Fix the broken commit
# ... fix the code ...
git add -A && git commit -m "fix: correct import after refactor"

# 8. Deploy the fix
bash ~/workspace/deploy/deploy.sh nero-core
```

---

## Example 3: Worktree-Based Parallel Development

Two agents working on the same repo simultaneously.

```bash
# Agent 1: Working on auth feature (worktree)
cd ~/workspace/repos/nero-core
git worktree add ../nero-core-auth feature/auth-tokens

# Agent 1 starts working
cd ~/workspace/repos/nero-core-auth
# ... claude makes changes in this worktree ...

# Agent 2: Working on main branch (original repo)
cd ~/workspace/repos/nero-core
# ... claude makes changes here ...

# Agent 2 deploys main to test
bash ~/workspace/deploy/deploy.sh nero-core

# Agent 1 finishes, deploy from worktree to test
cd ~/workspace/repos/nero-core-auth
bash ~/workspace/deploy/deploy.sh nero-core
# Now runtime runs the auth feature code

# Agent 1 merges back
cd ~/workspace/repos/nero-core
git merge feature/auth-tokens

# Clean up
git worktree remove ../nero-core-auth
git branch -d feature/auth-tokens

# Final deploy
bash ~/workspace/deploy/deploy.sh nero-core
```

---

## Example 4: React SPA Build and Deploy

The nero-web (React SPA) requires a build step before deployment.

```bash
# 1. Make changes to frontend
cd ~/workspace/repos/nero-web
# ... edit React components ...

# 2. Build
npm install
npm run build
# dist/ directory is created with optimized static files

# 3. Deploy (syncs dist/ to runtime)
bash ~/workspace/deploy/deploy.sh nero-web
# 09:30:00 [nero-web] === Deploying ===
# 09:30:00 [nero-web] Syncing dist...
# 09:30:01 [nero-web] Restarting service...
# 09:30:03 [nero-web] Running
# 09:30:03 [nero-web] === Done ===

# 4. Verify
curl -s http://127.0.0.1:8101/ | head -5
# <!doctype html><html>...
```

### nero-web.service

```ini
[Unit]
Description=NERO Web Frontend
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/nero/nero-web
ExecStart=/usr/bin/npx serve dist -l 8101 -s
Restart=on-failure
RestartSec=5
MemoryMax=256M

[Install]
WantedBy=default.target
```

---

## Example 5: Deploy with Database Migration

When a deploy includes database schema changes.

```bash
# 1. Deploy code first (without restart)
cd ~/workspace/repos/nero-channel-web
git add -A && git commit -m "feat: add thread_id column"

# Sync code but don't restart yet
rsync -a --delete \
    --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
    ~/workspace/repos/nero-channel-web/src/ /srv/nero/nero-channel-web/src/

# 2. Run migrations
cd ~/workspace/repos/nero-infra
.venv/bin/alembic upgrade head
# INFO  [alembic.runtime.migration] Running upgrade abc -> def, add thread_id

# 3. Now restart services
systemctl --user restart nero-channel-web nero-core

# 4. Verify
curl -s http://127.0.0.1:8100/health
systemctl --user status nero-channel-web nero-core
```

### Deploy Script with Migration Support

```bash
#!/bin/bash
# deploy-with-migration.sh nero-channel-web
# Deploy with automatic migration detection

set -euo pipefail

SERVICE="$1"

# Check for pending migrations
cd ~/workspace/repos/nero-infra
PENDING=$(.venv/bin/alembic check 2>&1 || true)

if echo "$PENDING" | grep -q "New upgrade"; then
    echo "Pending migrations detected!"
    echo "Running: alembic upgrade head"
    .venv/bin/alembic upgrade head
fi

# Regular deploy
bash ~/workspace/deploy/deploy.sh "$SERVICE"
```
