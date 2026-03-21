# Unattended Upgrades

Automated security patch management for Ubuntu/Debian servers. Covers package configuration, auto-reboot scheduling, cleanup, notifications, and package blacklisting for production stability.

## Scope

- unattended-upgrades package configuration
- Automatic security updates (Ubuntu security pocket)
- Auto-reboot scheduling for kernel updates
- Old kernel cleanup and disk space management
- Email/Slack notifications for applied updates
- Package blacklisting (hold specific packages)
- apt-listchanges integration
- Monitoring and troubleshooting

## Why This Matters

Unpatched servers are the leading cause of security breaches. Manual patching is:

- Easily forgotten (busy solo developer)
- Time-consuming (SSH, apt update, apt upgrade, reboot)
- Risky if delayed (known CVEs get exploited quickly)

Unattended-upgrades automates security patching while keeping production stable.

## Architecture

```
APT timer (systemd)
  -> apt-daily.timer (checks for updates twice daily)
    -> apt-daily.service (runs apt update)
  -> apt-daily-upgrade.timer (installs updates)
    -> apt-daily-upgrade.service (runs unattended-upgrade)
      -> /etc/apt/apt.conf.d/50unattended-upgrades (config)
      -> /etc/apt/apt.conf.d/20auto-upgrades (schedule)
```

### Configuration Files

| File | Purpose |
|------|---------|
| `/etc/apt/apt.conf.d/20auto-upgrades` | Enable/disable auto updates |
| `/etc/apt/apt.conf.d/50unattended-upgrades` | What to update, how to handle reboots |
| `/var/log/unattended-upgrades/` | Logs directory |
| `/var/run/reboot-required` | Flag file indicating reboot needed |

## Key Concepts

### 1. Update Origins

Ubuntu packages come from different origins (pockets):

| Origin | Contains | Auto-Update? |
|--------|----------|-------------|
| `${distro_id}:${distro_codename}` | Release packages | Optional |
| `${distro_id}:${distro_codename}-security` | Security patches | Yes (recommended) |
| `${distro_id}:${distro_codename}-updates` | Bug fixes, minor updates | Optional |
| `${distro_id}:${distro_codename}-proposed` | Pre-release testing | No |
| `${distro_id}:${distro_codename}-backports` | Newer versions | No |
| `${distro_id}ESMApps:${distro_codename}-apps-security` | ESM app security | Yes |
| `${distro_id}ESM:${distro_codename}-infra-security` | ESM infra security | Yes |

**Recommended:** Enable security pockets only. This ensures only security patches are applied automatically, not feature updates that could break things.

### 2. Auto-Reboot

Some updates (kernel, libc, systemd) require a reboot. Options:

| Setting | Value | Behavior |
|---------|-------|----------|
| `Automatic-Reboot` | `false` | Never auto-reboot (default) |
| `Automatic-Reboot` | `true` | Reboot immediately after updates if needed |
| `Automatic-Reboot-Time` | `"04:00"` | Reboot at 4 AM if needed |
| `Automatic-Reboot-WithUsers` | `true` | Reboot even if users are logged in |

For production servers: enable auto-reboot at a low-traffic time (e.g., 4 AM).

### 3. Package Blacklisting

Prevent specific packages from being upgraded automatically:

```
Unattended-Upgrade::Package-Blacklist {
    "docker-ce";
    "docker-ce-cli";
    "containerd.io";
    "nginx";
    "postgresql-16";
};
```

Use this for:
- Packages where upgrades require manual intervention
- Database servers (major version upgrades need migration)
- Docker (version changes can affect containers)
- nginx (config changes between versions)

### 4. Cleanup

Automatic cleanup of old packages:

```
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
```

This keeps disk space in check by removing old kernels and unused dependencies.

### 5. Email Notifications

Configure email notifications for applied updates:

```
Unattended-Upgrade::Mail "admin@example.com";
Unattended-Upgrade::MailReport "on-change";
```

Requires a working MTA (mail transfer agent). For simple setups, use `msmtp` or `ssmtp`. For Slack notifications, use a custom script.

### 6. Timing

The apt timers control when updates are checked and installed:

```bash
# Check timer schedules
systemctl list-timers apt-daily apt-daily-upgrade

# Default: randomized within a 12-hour window
# apt-daily: check for updates (6 AM - 6 PM random)
# apt-daily-upgrade: install updates (6 AM - 6 PM random)
```

To control timing precisely, override the systemd timers.

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Not enabling auto-reboot | Kernel patches never applied | Set Automatic-Reboot with time |
| Auto-rebooting during business hours | Downtime | Set Automatic-Reboot-Time to off-hours |
| Not blacklisting critical packages | Database/Docker breaks | Blacklist packages needing manual upgrade |
| Not testing reboot recovery | Services don't start after reboot | Ensure systemd services have Restart=always |
| Disk full from old kernels | Updates fail | Enable Remove-Unused-Kernel-Packages |
| No notifications | Unaware of applied updates | Configure email or Slack notifications |

## Verification Commands

```bash
# Check if unattended-upgrades is installed
dpkg -l unattended-upgrades

# Check if auto-updates are enabled
cat /etc/apt/apt.conf.d/20auto-upgrades

# Check unattended-upgrades configuration
cat /etc/apt/apt.conf.d/50unattended-upgrades

# Dry run (show what would be upgraded)
sudo unattended-upgrade --dry-run --debug

# Check upgrade log
sudo cat /var/log/unattended-upgrades/unattended-upgrades.log

# Check if reboot is required
[ -f /var/run/reboot-required ] && echo "REBOOT REQUIRED" || echo "No reboot needed"
cat /var/run/reboot-required.pkgs 2>/dev/null

# Check timer schedules
systemctl list-timers apt-daily apt-daily-upgrade

# Check last upgrade timestamp
ls -la /var/log/unattended-upgrades/
```

## Integration Points

| Component | Integration |
|-----------|------------|
| systemd | Services must auto-restart after reboot (Restart=always) |
| Docker | Blacklist docker-ce to prevent breaking containers |
| nginx | Blacklist if custom-compiled; safe if using Ubuntu packages |
| PostgreSQL | Blacklist major version, allow minor patches |
| Monitoring | Check /var/run/reboot-required for pending reboots |
| Backup | Run backups before auto-upgrades (via pre-hook) |

## References

- [Ubuntu AutomaticSecurityUpdates](https://help.ubuntu.com/community/AutomaticSecurityUpdates)
- [unattended-upgrades package](https://wiki.debian.org/UnattendedUpgrades)
- [Ubuntu security notices](https://ubuntu.com/security/notices)
