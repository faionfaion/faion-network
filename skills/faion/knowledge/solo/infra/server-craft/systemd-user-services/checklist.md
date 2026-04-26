# systemd User Services Checklist

## Prerequisites

- [ ] Verify systemd version: `systemctl --version`
- [ ] Enable linger for the user: `loginctl enable-linger`
- [ ] Verify linger: `loginctl show-user $USER | grep Linger`
- [ ] Create user service directory: `mkdir -p ~/.config/systemd/user`
- [ ] Verify XDG_RUNTIME_DIR is set: `echo $XDG_RUNTIME_DIR`

## Creating a New Service

### Unit File

- [ ] Create unit file in `~/.config/systemd/user/service-name.service`
- [ ] Set meaningful Description
- [ ] Set appropriate After/Wants dependencies
- [ ] Set Type (usually `simple` for long-running processes)
- [ ] Set WorkingDirectory to application directory
- [ ] Set ExecStart with absolute path to executable
- [ ] Set EnvironmentFile if using .env file
- [ ] Set Restart policy (usually `on-failure` or `always`)
- [ ] Set RestartSec (e.g., 5 seconds)
- [ ] Set WantedBy=default.target in [Install] section

### Resource Limits

- [ ] Set MemoryMax based on expected usage + headroom
- [ ] Set CPUQuota if CPU-intensive (optional)
- [ ] Set LimitNOFILE if app opens many files/connections
- [ ] Set TasksMax if app spawns many threads/processes

### Environment

- [ ] Create or reference .env file with secrets
- [ ] Set .env file permissions: `chmod 600`
- [ ] Verify .env file format (no quotes around values for systemd)
- [ ] Test environment loading: `systemd-run --user env`

### Activation

- [ ] Reload daemon: `systemctl --user daemon-reload`
- [ ] Start service: `systemctl --user start service-name`
- [ ] Check status: `systemctl --user status service-name`
- [ ] Check logs: `journalctl --user -u service-name -f`
- [ ] Enable on boot: `systemctl --user enable service-name`

## Verification

### Service Health

- [ ] Service shows "active (running)": `systemctl --user is-active service-name`
- [ ] Process is running: `pgrep -f "command-pattern"`
- [ ] Listening on expected port: `ss -tlnp | grep port`
- [ ] Logs show no errors: `journalctl --user -u service-name --since "5 min ago"`

### Restart Behavior

- [ ] Kill process and verify restart: `kill $(pgrep -f "pattern")`
- [ ] Verify RestartSec delay is applied
- [ ] Verify StartLimitBurst works (kill rapidly, should stop restarting)
- [ ] Reset after test: `systemctl --user reset-failed service-name`

### Boot Persistence

- [ ] Reboot server (or simulate): `systemctl --user daemon-reload`
- [ ] Verify service starts automatically after reboot
- [ ] Check startup ordering (After dependencies respected)

### Resource Limits

- [ ] Check actual memory usage: `systemctl --user status service-name` (Memory line)
- [ ] Verify MemoryMax enforcement: `systemctl --user show service-name -p MemoryMax`
- [ ] Check cgroup limits: `systemd-cgls --user`

## Multi-Service Management

### Dependency Chain

- [ ] Verify service start order matches After directives
- [ ] Test: stop a dependency, verify dependent services react correctly
- [ ] Ensure no circular dependencies

### Group Operations

- [ ] Test starting all services: `systemctl --user start nero-*`
- [ ] Test stopping all services: `systemctl --user stop nero-*`
- [ ] Test restarting a single service without affecting others
- [ ] Verify `systemctl --user status 'nero-*'` shows all services

## Timer Units (if applicable)

- [ ] Create paired `.timer` and `.service` files
- [ ] Set OnCalendar with correct schedule expression
- [ ] Set Persistent=true to catch up missed runs
- [ ] Set RandomizedDelaySec to avoid thundering herd
- [ ] Enable timer: `systemctl --user enable --now timer-name.timer`
- [ ] Verify next trigger: `systemctl --user list-timers`
- [ ] Test manually: `systemctl --user start service-name.service`

## Post-Setup

- [ ] Document service in project CLAUDE.md or runbook
- [ ] Add monitoring/health check for the service
- [ ] Set up log rotation (journald MaxRetentionSec)
- [ ] Create deploy script that handles service restart
- [ ] Test deploy workflow: update code, restart service, verify
