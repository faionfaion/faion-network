# Agent Integration — Unattended Upgrades

## When to use
- Provisioning a new production VPS — enable security patching before the server goes live
- Auditing an existing server that has not been patched in weeks
- Configuring post-patch behavior (auto-reboot window, notifications)
- Blacklisting a specific package to prevent auto-upgrade breaking a dependency
- Investigating why a server rebooted unexpectedly (check upgrade logs)

## When NOT to use
- Development or staging servers where surprise reboots are acceptable and full upgrades (not just security) are preferred — use a cron `apt upgrade` instead
- Servers running database major versions that require manual migration before upgrade (blacklist the DB packages, handle manually)
- When the team follows a formal change-management process that requires approval before any package change — disable unattended-upgrades entirely and use a scheduled maintenance window

## Where it fails / limitations
- Packages that require config file prompts during upgrade will hang unattended-upgrades — use `Dpkg-Options` to force non-interactive behavior (`--force-confold`)
- Auto-reboot happens at the configured time only if `/var/run/reboot-required` exists; kernel updates that install without the flag are missed
- Email notifications require a working MTA — most minimal VPS installs have none; fallback to log monitoring or Telegram webhook scripts
- `Automatic-Reboot-Time` applies a fixed UTC time — it does not account for traffic patterns or active connections
- If disk is full, `apt` downloads fail silently and no upgrade happens — disk monitoring must be independent of unattended-upgrades

## Agentic workflow
An agent configures unattended upgrades by reading the two config files, verifying the enabled origins match the security pockets, checking the blacklist against the server's critical packages (Docker, nginx, PostgreSQL major versions), and confirming the auto-reboot window is set to off-hours. The agent should run `sudo unattended-upgrade --dry-run --debug` to show what would be upgraded without applying changes. For existing servers, the agent checks the upgrade log at `/var/log/unattended-upgrades/unattended-upgrades.log` to verify the last successful run and any failures.

### Recommended subagents
- `faion-sdd-executor-agent` — execute server-init or hardening SDD tasks that include unattended-upgrades setup as a step

### Prompt pattern
```
Configure unattended-upgrades on this Ubuntu 24.04 server.
Requirements:
- Auto-install security patches only (not all updates)
- Auto-reboot at 04:00 UTC if kernel/libc patch requires it
- Blacklist: docker-ce, docker-ce-cli, containerd.io, postgresql-16, nginx
- Remove old kernels and unused deps automatically
- Send alerts to Telegram (script at /usr/local/bin/tg-alert.sh)
Output the complete 50unattended-upgrades config and 20auto-upgrades content.
```

```
Check the unattended-upgrades status on this server:
1. Is it installed and enabled?
2. When did it last run successfully?
3. Are there any pending upgrades now?
4. Is a reboot currently required?
Run the appropriate commands and summarize.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `unattended-upgrade` | Manual trigger / dry-run | `apt install unattended-upgrades` |
| `apt-get` | Package management | Built-in |
| `systemctl` | Manage `apt-daily` and `apt-daily-upgrade` timers | Built-in |
| `needrestart` | Check which services need restart after library updates | `apt install needrestart` |
| `apt-listchanges` | Show changelogs before applying updates | `apt install apt-listchanges` |
| `debconf-set-selections` | Pre-answer package prompts for non-interactive upgrade | `apt install debconf-utils` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Ubuntu Security Notices | SaaS | Yes | RSS feed and API at `ubuntu.com/security/notices`; agent can poll for CVEs affecting installed packages |
| Canonical Livepatch | SaaS (free for personal) | Partial | Kernel patches without reboot; requires Canonical account; `snap install canonical-livepatch` |
| msmtp | OSS | Yes | Minimal SMTP client for sending email notifications; drop-in sendmail replacement |
| Telegram Bot API | SaaS | Yes | Webhook for upgrade notifications; reliable alternative to email on minimal servers |

## Templates & scripts
See templates.md for complete config file templates. Key notification hook:

```bash
#!/usr/bin/env bash
# /etc/apt/apt.conf.d/99-unattended-notify
# Post-upgrade Telegram notification
# Place this script at /usr/local/bin/apt-notify.sh and chmod +x

LOG_FILE="/var/log/unattended-upgrades/unattended-upgrades.log"
TG_TOKEN="${TELEGRAM_ALERT_BOT_TOKEN}"
TG_CHAT="${TELEGRAM_ALERT_CHAT_ID}"
HOSTNAME=$(hostname -s)

# Only send if something was upgraded (log changed in last 10 minutes)
if find "$LOG_FILE" -mmin -10 | grep -q .; then
    SUMMARY=$(tail -20 "$LOG_FILE" | grep -E "(Packages upgraded|No packages)" | tail -1)
    REBOOT=""
    [ -f /var/run/reboot-required ] && REBOOT=" REBOOT REQUIRED"

    curl -s -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
        -d "chat_id=${TG_CHAT}" \
        -d "text=[${HOSTNAME}] apt upgrade: ${SUMMARY}${REBOOT}" \
        -d "parse_mode=HTML" >/dev/null
fi
```

Place in `/etc/apt/apt.conf.d/99-unattended-notify` as a DPkg::Post-Invoke hook to run after each upgrade run.

## Best practices
- Enable only the `-security` pocket for auto-upgrades; `-updates` contains non-security changes that can break applications
- Always blacklist `docker-ce`, database major versions, and any package that requires manual config migration between versions
- Set `Automatic-Reboot-Time` to a low-traffic window (e.g., `04:00`); do not leave auto-reboot disabled — kernel patches never apply without it
- Use `Dpkg::Options { "--force-confold"; }` to prevent upgrade hangs on config file conflicts (keeps existing config)
- Pair with `needrestart` to restart services that loaded old library versions without rebooting
- Monitor `/var/run/reboot-required` in your health check scripts — a pending reboot means a kernel patch is not yet active
- Test the full flow with `sudo unattended-upgrade --dry-run --debug` before relying on it in production

## AI-agent gotchas
- Agent must not apply `apt upgrade` (full upgrade) vs `apt install <specific>` — unattended-upgrades is security-only; a full upgrade is a separate operation and may break pinned versions
- The dry-run command `sudo unattended-upgrade --dry-run --debug` produces verbose output — agent should parse for the `Packages upgraded:` and `Packages kept back:` lines, not the full log
- Config in `/etc/apt/apt.conf.d/50unattended-upgrades` uses APT's Debian-style syntax (not JSON/YAML) — syntax errors are silent; agent must validate with `sudo apt-config dump UnattendedUpgrade`
- `systemctl restart apt-daily.service` does not trigger an immediate upgrade — it only fetches the package lists; the actual upgrade is `apt-daily-upgrade.service`
- Adding a package to the blacklist stops automatic upgrade but does not hold the package — `apt upgrade` run manually will still upgrade it; use `apt-mark hold <package>` for a hard hold

## References
- https://help.ubuntu.com/community/AutomaticSecurityUpdates
- https://wiki.debian.org/UnattendedUpgrades
- https://ubuntu.com/security/notices
- https://manpages.ubuntu.com/manpages/noble/man8/unattended-upgrade.8.html
- https://github.com/msmtp/msmtp (minimal SMTP for notifications)
