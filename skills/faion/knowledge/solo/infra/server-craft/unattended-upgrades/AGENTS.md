# Unattended Upgrades

## Summary

Automate security patch management on Ubuntu 24.04 with `unattended-upgrades`: enable daily security-origin updates, schedule auto-reboot at off-peak hours (4 AM), blacklist packages that require manual intervention (Docker, databases), and clean up old kernels automatically. Services must have `Restart=always` and Docker containers `restart: unless-stopped` to recover after automatic reboots.

## Why

Unpatched servers are the leading cause of security breaches, and manual patching is easily forgotten by a solo developer. The Ubuntu security pocket receives patches for known CVEs within hours — automatic installation closes the window between disclosure and exploitation without requiring manual SSH sessions.

## When To Use

- Any production Ubuntu VPS that should stay patched without manual intervention
- Servers running kernel-level services where CVEs appear frequently (OpenSSL, libc, systemd)
- Configuring auto-reboot after kernel updates to apply them
- Auditing whether existing auto-update config is correct

## When NOT To Use

- During initial server setup before verifying all services have `Restart=always` — auto-reboot will leave services down
- For database major version upgrades — blacklist the package and upgrade manually after testing
- When using a managed platform that handles patching (Heroku, Railway) — don't install unattended-upgrades there
- For Docker CE — version changes can break container runtimes; always blacklist and upgrade manually

## Content

| File | What's inside |
|------|---------------|
| `content/01-configuration.xml` | Update origins (security pockets), blacklist rules, auto-reboot settings, cleanup directives |
| `content/02-examples.xml` | NERO server dry-run output, kernel update timeline, handling held-back Docker packages |

## Templates

| File | Purpose |
|------|---------|
| `templates/50unattended-upgrades.conf` | Production config: security origins, Docker blacklist, auto-reboot at 04:00, cleanup |
| `templates/20auto-upgrades.conf` | Schedule: daily update check, download, install, weekly autoclean |
| `templates/apt-daily-timer-override.conf` | Fix apt-daily timer to exact time (2 AM) |
| `templates/apt-daily-upgrade-timer-override.conf` | Fix apt-daily-upgrade timer to exact time (3 AM) |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/check-reboot-required.sh` | Report reboot-required status, packages needing it, auto-reboot config |
| `scripts/upgrade-status.sh` | Dashboard: config state, pending updates, recent log, timer schedule, blacklist |
