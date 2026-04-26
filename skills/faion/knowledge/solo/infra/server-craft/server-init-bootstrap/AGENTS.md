# Server Init Bootstrap

## Summary

Complete first-login setup for a fresh Ubuntu 24.04 VPS: 5-phase sequence (access+users → system identity → packages+tools → security hardening → services foundation). Critical sequence constraint: always test SSH login as the new user BEFORE disabling root login — one wrong sshd_config line will lock you out. Requires `loginctl enable-linger` for systemd user services to survive logout.

## Why

An unscripted first login takes 2+ hours and leaves gaps — forgotten fail2ban, wrong locale, root SSH still enabled. A documented bootstrap sequence is reproducible, auditable, and serves as the server runbook. Cloud-init can automate it on provisioning, eliminating the first manual SSH session entirely.

## When To Use

- First login to any new VPS (Hetzner, DigitalOcean, Linode, Vultr)
- Rebuilding a server after a breach or OS reinstall
- Automating server provisioning with cloud-init user-data
- Auditing an existing server against the bootstrap checklist

## When NOT To Use

- Managed platforms (Heroku, Railway, Render) — OS is abstracted, bootstrap doesn't apply
- Kubernetes nodes — managed by the cluster control plane, not manual setup
- Before verifying SSH key access as the new user — never disable root login first
- Running the full bootstrap on a live production server — only during initial setup

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases.xml` | 5-phase sequence, phase ordering rationale, SSH lockout prevention rule |
| `content/02-configuration.xml` | sshd_config hardening options, UFW setup, fail2ban jail.local, locale+timezone, linger |
| `content/03-examples.xml` | NERO nero-prod full bootstrap log, Hetzner cloud-init user-data, post-bootstrap verification script |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap.sh` | Full interactive bootstrap script: all 5 phases with verification steps |
| `templates/cloud-init.yml` | cloud-init user-data: user, SSH key, packages, UFW, unattended-upgrades |
| `templates/sshd-hardened.conf` | Production sshd_config: no root, no password, MaxAuthTries 3, AllowUsers |
| `templates/fail2ban-jail.local` | jail.local: 1h ban, 3 retries, sshd jail enabled |
| `templates/verify-bootstrap.sh` | Post-bootstrap checklist: hostname, timezone, locale, UFW, fail2ban, SSH config, swap, linger |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/server-status.sh` | Dashboard: uptime, disk, memory, swap, running services, UFW rules, open ports |
