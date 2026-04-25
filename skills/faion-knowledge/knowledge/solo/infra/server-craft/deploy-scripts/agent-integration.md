# Agent Integration — Deploy Scripts

## When to use
- Deploying a Python/Node service from workspace to runtime on a VPS without CI/CD
- First-time setup of a deploy pipeline for a new service in the workspace/runtime pattern
- Agents need to test a code change in production-like runtime without a full CI pipeline
- Adding rollback capability (pre-deploy snapshot or git-checkout) to an existing deploy workflow
- Post-deploy validation that a service actually started and passes health check

## When NOT to use
- Containerized deployments where the unit is a Docker image — use `docker compose pull && up -d`
- Multi-host deployments — these scripts are single-server; use Ansible or Fabric for multi-host
- When the team requires approval workflows before deploy — these scripts run immediately; wrap with human-in-loop step
- Repos without a stable `main` branch (chaotic commit history) — rollback via `HEAD~1` is unreliable
- Static-only sites with no server-side logic — direct rsync to webroot is simpler than the full deploy script pattern

## Where it fails / limitations
- `systemctl --user restart` succeeds even if the service fails to start (it schedules the restart); must follow with `is-active` check
- `pip install -e .` on a freshly rsynced directory may fail if `pyproject.toml` has changed in incompatible ways — requires venv rebuild
- Pre-deploy disk space check hardcodes `/srv` — must be updated for projects using different runtime roots
- rsync `--delete` combined with missing `--exclude` patterns can wipe runtime-only files (uploads, generated assets)
- The rollback script uses `git checkout` which puts the repo in detached HEAD state; it must return to `main` or subsequent commits are orphaned
- Zero-downtime reload via `systemctl reload` only works if the service handles `SIGHUP` (uvicorn/gunicorn do; raw Python scripts do not)

## Agentic workflow
An agent making code changes invokes the deploy script as a post-edit step: it rsyncs the workspace to the runtime directory, installs dependencies only if `requirements.txt` changed, restarts the service, and polls the health endpoint for up to 30 seconds. If the health check fails, the agent automatically runs the rollback script to restore the previous git state and redeploy, then surfaces the failure log for human review. Migration hooks (Alembic, Django) run in the `post-sync` hook slot between rsync and restart — agents must not skip them.

### Recommended subagents
- `faion-knowledge` (infra/server-craft/git-server-workflow) — git checkout + redeploy as rollback mechanism
- `faion-knowledge` (infra/server-craft/systemd-user-services) — the `systemctl --user restart` step and health check logic
- `faion-knowledge` (infra/server-craft/health-checks-autoheal) — post-deploy validation patterns

### Prompt pattern
```
Deploy service nero-core:
1. Run: bash ~/workspace/deploy/deploy.sh nero-core
2. Wait up to 30 seconds for health: poll `systemctl --user is-active nero-core` every 3s
3. If active: report success with last 10 lines of `journalctl --user -u nero-core -n 10 --no-pager`
4. If not active after 30s: run rollback, report failure with full error log
Do not proceed to next task until health is confirmed.
```

```
Add a new service "nero-media" to the deploy script.
Service type: systemd. Source: ~/workspace/repos/nero-media. Runtime: /srv/nero/nero-media.
Include: venv creation, pip install -e ., service restart, health check.
Dependencies: nero-sdk must be deployed first.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rsync` | Incremental file sync from workspace to runtime | Pre-installed on Ubuntu |
| `systemctl --user` | Service lifecycle management | systemd built-in |
| `pip install -e .` | Editable install using pyproject.toml | `python3 -m pip` |
| `diff -q` | Compare files to detect requirement changes | `diffutils` pre-installed |
| `fallocate` | Fast pre-allocate disk space (used in pre-deploy checks) | `util-linux` pre-installed |
| `curl -sf` | Silent health endpoint check with fail-on-error | Pre-installed |
| `flock` | Serialize concurrent deploy runs | `util-linux` pre-installed |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| systemd (user mode) | OSS | Yes (CLI) | Service lifecycle; `systemctl --user restart/is-active` |
| journald | OSS | Yes (CLI) | Log access via `journalctl --user -u <name>`; no API needed |
| GitHub | SaaS | Yes (CLI/API) | Source of truth for rollback tags and commit history |
| Telegram Bot API | SaaS | Yes (HTTP) | Deploy notifications via `tg-send`; add to post-deploy hook |
| Alembic / Django migrations | OSS | Yes (CLI) | Run in `post-sync` hook; agent must handle non-zero exit |

## Templates & scripts
See `templates.md` for full `deploy.sh` and `rollback.sh`. Inline pre-deploy validation:

```bash
#!/bin/bash
# pre-deploy-check.sh — validate environment before deploying
set -euo pipefail
RUNTIME="${1:-/srv/nero}"
ENV_FILE="${2:-$HOME/workspace/.env}"
ERRORS=0

[ -f "$ENV_FILE" ] || { echo "ERROR: $ENV_FILE missing"; ((ERRORS++)); }
FREE_MB=$(df "$RUNTIME" --output=avail -BM | tail -1 | tr -d ' M')
[ "$FREE_MB" -ge 1024 ] || { echo "ERROR: < 1GB free disk ($FREE_MB MB)"; ((ERRORS++)); }
systemctl --user status >/dev/null 2>&1 || { echo "ERROR: systemd user session unavailable"; ((ERRORS++)); }
[ -d "$RUNTIME" ] || { echo "ERROR: runtime dir $RUNTIME missing"; ((ERRORS++)); }
[ "$ERRORS" -eq 0 ] && echo "Pre-deploy OK" || { echo "$ERRORS check(s) failed"; exit 1; }
```

## Best practices
- Always run `pre-deploy-check.sh` before any rsync — a deploy that fails mid-way is harder to recover than one that never started
- Compare `requirements.txt` checksums before running `pip install` to avoid unnecessary 30-60s installs on every deploy
- Use `systemctl --user reload` (SIGHUP) instead of `restart` for uvicorn/gunicorn — it drains connections before restarting workers
- Keep a `deploy-hooks/` directory per service for migration scripts, cache warmup, and notification hooks — do not embed them inline in deploy.sh
- Pre-deploy snapshot (`rsync -a src/ .snapshots/$(date +%s)/`) enables instant file-level rollback without git checkout overhead
- Never run `pip install` as root or into the system Python — always activate the service-specific venv first
- Log deploy start, end, commit hash, and service health result to a deploy log file for audit trail

## AI-agent gotchas
- Agents must check `systemctl --user is-active` after restart, not `is-enabled`; a service can be enabled but fail to start
- `pip install -e .` requires `pyproject.toml` in the source directory; agents must verify it exists before attempting, not assume
- rsync `--delete` is irreversible for runtime-only files; agents must never run it without confirming the exclude list covers upload directories and generated assets
- The deploy script uses `set -euo pipefail`; any command failure aborts the script; agents must not wrap the script call in `|| true`
- Agents running parallel deploys of multiple services must serialize using `flock` or deploy in dependency order; parallel deploys of interdependent services cause race conditions in shared `.venv` pip installs
- Rollback via `git checkout` puts repo in detached HEAD; agents must always follow rollback with `git checkout main` or the next deploy will commit to a detached state

## References
- https://linux.die.net/man/1/rsync
- https://www.freedesktop.org/software/systemd/man/systemctl.html
- https://pip.pypa.io/en/stable/topics/local-project-installs/
- https://alembic.sqlalchemy.org/en/latest/tutorial.html
- https://man7.org/linux/man-pages/man1/flock.1.html
