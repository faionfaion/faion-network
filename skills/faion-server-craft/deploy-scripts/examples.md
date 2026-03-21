# Deploy Scripts Examples

## Example 1: NERO Deploy Flow

Complete deployment of the NERO platform from workspace to runtime.

### Architecture

```
Source:  ~/workspace/repos/nero-core/      # Git repo, development
Deploy:  rsync + pip install
Runtime: /srv/nero/nero-core/              # systemd runs from here
```

### Single Service Deploy

```bash
$ bash ~/workspace/deploy/deploy.sh nero-core
============================================================
Deploy: nero-core
============================================================
Pre-deploy checks passed
=== Deploying nero-core (systemd) ===
  Synced: /home/nero/workspace/repos/nero-core -> /srv/nero/nero-core/src
  Dependencies installed
  Service nero-core: ACTIVE

============================================================
Deploy complete
============================================================
```

### Full Stack Deploy

```bash
$ bash ~/workspace/deploy/deploy.sh all
============================================================
Deploy: all
============================================================
Pre-deploy checks passed
=== Deploying nero-sdk (library) ===
  Synced: /home/nero/workspace/repos/nero-sdk -> /srv/nero/nero-sdk/src
  Library synced (no service to restart)

=== Deploying nero-infra (docker) ===
  Synced: /home/nero/workspace/repos/nero-infra -> /srv/nero/nero-infra/src
  Docker services started

=== Deploying nero-core (systemd) ===
  Synced: /home/nero/workspace/repos/nero-core -> /srv/nero/nero-core/src
  Dependencies installed
  Service nero-core: ACTIVE

=== Deploying nero-channel-web (systemd) ===
  Synced: /home/nero/workspace/repos/nero-channel-web -> /srv/nero/nero-channel-web/src
  Dependencies installed
  Service nero-channel-web: ACTIVE

=== Deploying nero-channel-tg (systemd) ===
  Synced: /home/nero/workspace/repos/nero-channel-tg -> /srv/nero/nero-channel-tg/src
  Dependencies installed
  Service nero-channel-tg: ACTIVE

=== Deploying nero-web (static) ===
  Static files synced
  Service nero-web: ACTIVE

============================================================
Deploy complete
============================================================
```

### Rebuild All Virtualenvs

After a Python version upgrade or dependency conflict:

```bash
$ bash ~/workspace/deploy/deploy.sh all --rebuild-venv
============================================================
Deploy: all (rebuild venv)
============================================================
Pre-deploy checks passed
=== Deploying nero-sdk (library) ===
  Synced: ...

=== Deploying nero-core (systemd) ===
  Synced: ...
  Creating virtualenv...
  Dependencies installed
  Service nero-core: ACTIVE

=== Deploying nero-channel-web (systemd) ===
  Synced: ...
  Creating virtualenv...
  Dependencies installed
  Service nero-channel-web: ACTIVE
...
```

## Example 2: Rollback After Bad Deploy

A code change in nero-core introduced a bug. Rolling back to the previous version.

### Detect the Problem

```bash
$ systemctl --user status nero-core
nero-core.service - NERO Core (Celery Workers)
     Active: failed (Result: exit-code) since ...
     Process: 12345 ExecStart=... (code=exited, status=1/FAILURE)

$ journalctl --user -u nero-core --since "5 min ago" | tail -10
Mar 21 10:15:30 nero-hetzner celery[12345]: ModuleNotFoundError: No module named 'nero_core.new_feature'
```

### Rollback

```bash
$ bash ~/workspace/deploy/rollback.sh nero-core
Current commit: abc1234 (feat: add new feature)
Rolling back to: HEAD~1
Now at: def5678 (fix: update error handling)

=== Deploying nero-core (systemd) ===
  Synced: ...
  Dependencies installed
  Service nero-core: ACTIVE

============================================================
Rollback complete: abc1234 -> def5678
To undo: bash rollback.sh nero-core abc1234
============================================================
```

### Verify Rollback

```bash
$ systemctl --user status nero-core
  Active: active (running)

$ curl http://127.0.0.1:8100/health
{"status": "ok", "checks": {"database": {"status": "ok"}, "redis": {"status": "ok"}}}

# Return to latest when fix is ready
$ cd ~/workspace/repos/nero-core
$ git checkout main
$ bash ~/workspace/deploy/deploy.sh nero-core
```

## Example 3: Deploy with Database Migration

Deploying nero-channel-web with a new database migration.

### Deploy Hook: post-sync.sh

```bash
# ~/workspace/repos/nero-channel-web/deploy-hooks/post-sync.sh
#!/bin/bash
SERVICE="$1"
RUNTIME_DIR="$2"

echo "  Running database migrations..."
cd /srv/nero/nero-infra/src
/srv/nero/nero-channel-web/.venv/bin/alembic upgrade head
echo "  Migrations complete"
```

### Deploy with Migration

```bash
$ bash ~/workspace/deploy/deploy.sh nero-channel-web
============================================================
Deploy: nero-channel-web
============================================================
Pre-deploy checks passed
=== Deploying nero-channel-web (systemd) ===
  Synced: /home/nero/workspace/repos/nero-channel-web -> /srv/nero/nero-channel-web/src
  Dependencies installed
  Running database migrations...
  INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, add user preferences table
  Migrations complete
  Service nero-channel-web: ACTIVE

============================================================
Deploy complete
============================================================
```

## Example 4: Pre-Deploy Validation

Running pre-deploy checks before deployment.

```bash
$ bash ~/workspace/deploy/pre-deploy-check.sh
=== Pre-Deploy Validation ===

--- Environment ---
[PASS] .env file exists
[PASS] Runtime dir exists
[PASS] Workspace dir exists
[PASS] DATABASE_URL is set
[PASS] REDIS_URL is set
[PASS] ANTHROPIC_API_KEY is set
[PASS] RABBITMQ_URL is set
[PASS] Disk space: 283000MB free
[PASS] systemd user session available
[PASS] Docker is running
[PASS] Python3: Python 3.12.8

--- Git Status ---
[PASS] nero-sdk: clean
[WARN] nero-core: uncommitted changes
[PASS] nero-channel-web: clean
[PASS] nero-channel-tg: clean
[PASS] nero-web: clean
[PASS] nero-infra: clean

--- Backing Services ---
[PASS] Redis: responding

=== Results: 0 errors, 1 warnings ===
Ready to deploy.
```

## Example 5: Status Check After Deploy

```bash
$ bash ~/workspace/deploy/status.sh
=== NERO Platform Status ===

--- systemd Services ---
  nero-core                 ACTIVE
  nero-channel-web          ACTIVE
  nero-channel-tg           ACTIVE
  nero-web                  ACTIVE
  nero-watcher              ACTIVE

--- Docker Services ---
  nero-postgres    Up 3 days (healthy)
  nero-redis       Up 3 days (healthy)
  nero-rabbitmq    Up 3 days (healthy)
  nero-flower      Up 3 days

--- Health Checks ---
  nero-channel-web          ok (port 8100)

--- Resources ---
  Memory: 8.2Gi/30Gi
  Swap:   0B/4.0Gi
  Disk:   12G/310G (4% used)
  Load:   0.45 0.38 0.32
```

## Example 6: SDK Change Triggers Multi-Service Deploy

When nero-sdk changes, all dependent services need redeployment.

```bash
# nero-sdk was updated with a new model
$ cd ~/workspace/repos/nero-sdk
$ git log --oneline -1
abc1234 feat: add message priority field

# Deploy SDK first (library), then all dependents
$ bash ~/workspace/deploy/deploy.sh nero-sdk
=== Deploying nero-sdk (library) ===
  Synced: ...
  Library synced (no service to restart)

# Now deploy services that depend on nero-sdk
$ for svc in nero-core nero-channel-web nero-channel-tg; do
    bash ~/workspace/deploy/deploy.sh "$svc"
done

=== Deploying nero-core (systemd) ===
  Synced: ...
  Dependencies installed   # pip install -e . picks up new nero-sdk
  Service nero-core: ACTIVE

=== Deploying nero-channel-web (systemd) ===
  Synced: ...
  Dependencies installed
  Service nero-channel-web: ACTIVE

=== Deploying nero-channel-tg (systemd) ===
  Synced: ...
  Dependencies installed
  Service nero-channel-tg: ACTIVE
```
