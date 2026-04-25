# Agent Integration — systemd User Services

## When to use
- Deploying a Python/Node application that must start at boot and restart on crash without root access
- Managing multiple per-user services (Celery, FastAPI, Telegram bot) with independent restart policies
- Adding resource limits (MemoryMax, CPUQuota) to a service that has been OOM-killed
- Replacing a `nohup ./app &` or `screen` pattern with proper lifecycle management
- Adding timer-based scheduled tasks as an alternative to cron (better logging, dependency support)

## When NOT to use
- Services that require binding ports below 1024 (< 1024 requires root or `CAP_NET_BIND_SERVICE`); use a reverse proxy (nginx) instead
- Containerized workloads managed by Docker Compose — `docker-compose.yml` restart policies replace unit files for containers
- One-shot scripts that run on demand, not continuously — use cron or explicit invocation
- Development environments where services are started/stopped manually during coding sessions

## Where it fails / limitations
- `systemctl --user` commands fail with "Failed to connect to bus" when run without a live user session (e.g., from `su`, `sudo -u`, or a cron job); must set `XDG_RUNTIME_DIR=/run/user/$(id -u)` and `DBUS_SESSION_BUS_ADDRESS`
- Linger must be enabled (`loginctl enable-linger`) for services to start at boot; without it, they only start on first login
- `EnvironmentFile=` does not support shell variable expansion inside the file (`${VAR}` is literal); values are taken verbatim
- `ExecStart=` requires an absolute path; relative paths cause the service to fail with a cryptic "No such file" error
- `systemctl --user reload` only works if the service defines `ExecReload=`; otherwise it silently does nothing and returns exit 0
- `StartLimitBurst` and `StartLimitIntervalSec` must be in the `[Unit]` section on modern systemd (≥ 229), not `[Service]`; placing them in `[Service]` silently has no effect on some versions

## Agentic workflow
When deploying a new service, an agent generates the unit file from a template (using service name, ExecStart path, EnvironmentFile path, and resource limits), writes it to `~/.config/systemd/user/<name>.service`, runs `systemctl --user daemon-reload && enable --now <name>`, and verifies with `is-active`. For resource limit changes, the agent edits the unit file, runs `daemon-reload && restart`, then confirms the new limits are active with `systemctl --user show <name> --property=MemoryMax`. Human approval is required before setting `OOMScoreAdjust < -500` or increasing resource limits beyond server capacity.

### Recommended subagents
- `faion-knowledge` (infra/server-craft/deploy-scripts) — deploy script invokes `systemctl --user restart` after rsync
- `faion-knowledge` (infra/server-craft/swap-memory-management) — `MemoryMax` and `OOMScoreAdjust` directives
- `faion-knowledge` (infra/server-craft/monitoring-logging) — `journalctl --user` log access and retention config
- `faion-knowledge` (infra/server-craft/health-checks-autoheal) — post-start health check + autoheal integration

### Prompt pattern
```
Create a systemd user service for nero-core (Celery worker):
- ExecStart: /srv/nero/nero-core/.venv/bin/celery -A nero_core worker -l info
- WorkingDirectory: /srv/nero/nero-core/src
- EnvironmentFile: /home/nero/workspace/.env
- Restart: on-failure, RestartSec: 10
- MemoryMax: 8G, MemoryHigh: 6G, OOMScoreAdjust: 0
- After: network-online.target

Write to ~/.config/systemd/user/nero-core.service
Then: systemctl --user daemon-reload && systemctl --user enable --now nero-core
Verify: systemctl --user status nero-core
```

```
Check all user services for ones that have restarted more than 3 times in the last hour:
journalctl --user --since "1 hour ago" | grep -E "Started|Failed" | \
  awk '{print $NF}' | sort | uniq -c | sort -rn | head -10
For any service with > 3 restarts: show its last 20 log lines.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `systemctl --user` | Service lifecycle (start/stop/restart/enable/status) | systemd built-in |
| `journalctl --user -u` | Service log access | systemd built-in |
| `loginctl enable-linger` | Start user services at boot without login | systemd-logind |
| `systemctl --user daemon-reload` | Reload unit files after changes | systemd |
| `systemctl --user edit <name>` | Drop-in override editor (preserves original) | systemd |
| `systemctl --user show <name>` | Show all unit properties including applied limits | systemd |
| `systemd-analyze verify <file>` | Validate unit file syntax | systemd |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| systemd (user mode) | OSS | Yes (CLI) | Full lifecycle management; no root needed |
| journald | OSS | Yes (CLI) | Structured log storage; `journalctl --user` |
| Telegram Bot API | SaaS | Yes (curl) | Notification on service failure via `OnFailure=` hook + notify script |
| Netdata | OSS | Yes (REST API) | Real-time systemd service metrics |
| Monit | OSS | Yes (CLI) | Alternative to systemd autorestart for simpler setups |

## Templates & scripts
See `templates.md` for complete unit file templates for Celery, FastAPI (uvicorn), and Telegram bot. Inline unit validation:

```bash
#!/bin/bash
# validate-unit.sh — validate a systemd user unit file before installing
# Usage: bash validate-unit.sh nero-core.service
UNIT="${1:?unit filename required}"
UNIT_DIR="$HOME/.config/systemd/user"
UNIT_PATH="$UNIT_DIR/$UNIT"

[ -f "$UNIT_PATH" ] || { echo "ERROR: $UNIT_PATH not found"; exit 1; }

# Check required fields
grep -q "^ExecStart=" "$UNIT_PATH" || echo "WARN: ExecStart missing"
grep -q "^WantedBy=" "$UNIT_PATH" || echo "WARN: WantedBy missing (service won't be enabled)"
grep -q "^Restart=" "$UNIT_PATH" || echo "WARN: Restart policy not set"

# Check ExecStart uses absolute path
EXEC=$(grep "^ExecStart=" "$UNIT_PATH" | head -1 | cut -d= -f2- | awk '{print $1}')
[[ "$EXEC" == /* ]] || echo "ERROR: ExecStart path is not absolute: $EXEC"

# Validate with systemd-analyze if available
systemd-analyze --user verify "$UNIT_PATH" 2>&1 || true
echo "Validation complete: $UNIT_PATH"
```

## Best practices
- Always run `systemctl --user daemon-reload` after any unit file change — systemd caches the previous version in memory and changes have no effect until reload
- Use `systemctl --user edit <name>` for minor changes to system-provided or template units — it creates a drop-in override that survives package upgrades
- Set `Restart=on-failure` for all long-running services; `Restart=always` will loop on intentional `systemctl stop` until `StartLimitBurst` is exceeded
- Place `StartLimitBurst` and `StartLimitIntervalSec` in `[Unit]`, not `[Service]` — the `[Service]` location silently fails on systemd ≥ 229
- Write secrets via `EnvironmentFile=` pointing to a mode-600 file, not via `Environment=` in the unit file — `systemctl show` exposes `Environment=` values in plain text
- Use `Type=notify` only when the application explicitly calls `sd_notify(READY=1)` — using it with apps that do not send the notification causes the service to timeout on start

## AI-agent gotchas
- Agents running via `sudo -u <user>` or `su` must export `XDG_RUNTIME_DIR=/run/user/$(id -u <user>)` before calling `systemctl --user`; without it, the command fails with a bus error that looks like systemd is down
- `systemctl --user enable --now <name>` requires linger to be already enabled; agents must check and enable linger first on new servers
- `systemctl --user status` returns exit code 3 for inactive services, not 1; agents must not treat exit code 3 as a command failure
- Unit file parsing is strict: a trailing space after a value on a line (e.g., `MemoryMax=2G `) causes the directive to be silently ignored; agents must strip trailing whitespace from generated unit files
- `systemctl --user reload` returns exit 0 even when `ExecReload=` is not defined; agents must not use reload as a proxy for restart without verifying ExecReload is set

## References
- https://www.freedesktop.org/software/systemd/man/systemd.service.html
- https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html
- https://www.freedesktop.org/software/systemd/man/loginctl.html
- https://www.freedesktop.org/software/systemd/man/journalctl.html
- https://wiki.archlinux.org/title/Systemd/User
