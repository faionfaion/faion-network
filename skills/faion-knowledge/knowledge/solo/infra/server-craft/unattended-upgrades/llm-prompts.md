# Unattended Upgrades LLM Prompts

Prompts for AI assistants to configure, troubleshoot, and audit automatic updates.

## Prompt 1: Upgrade Audit

```
Audit the automatic update configuration on this Ubuntu server.

Steps:
1. Check OS version: `cat /etc/os-release`
2. Check unattended-upgrades is installed: `dpkg -l unattended-upgrades`
3. Check auto-upgrade config: `cat /etc/apt/apt.conf.d/20auto-upgrades`
4. Check unattended-upgrades config: `cat /etc/apt/apt.conf.d/50unattended-upgrades`
5. Check timer status: `systemctl list-timers apt-daily apt-daily-upgrade`
6. Check last upgrade: `tail -30 /var/log/unattended-upgrades/unattended-upgrades.log`
7. Check pending updates: `apt list --upgradable 2>/dev/null | wc -l`
8. Check reboot required: `cat /var/run/reboot-required 2>/dev/null`
9. Check blacklisted packages: grep Package-Blacklist config
10. Check if auto-reboot is configured

Report:

| Setting | Current | Recommended | Status |
|---------|---------|-------------|--------|
| Auto-updates enabled | ... | Yes | OK/FIX |
| Security origin | ... | Yes | OK/FIX |
| Auto-reboot | ... | Yes, 4 AM | OK/FIX |
| Cleanup | ... | Yes | OK/FIX |
| Docker blacklisted | ... | Yes | OK/FIX |
| Reboot pending | ... | No | OK/WARN |

Provide specific fixes for any FIX items.
```

## Prompt 2: Setup Unattended Upgrades

```
Configure automatic security updates on this Ubuntu 24.04 server.

Server runs:
- systemd user services (must auto-restart after reboot)
- Docker containers (restart: unless-stopped)
- Web traffic is low at night (4 AM is safe for reboot)

Requirements:
1. Install unattended-upgrades if not present
2. Enable daily security updates only
3. Auto-reboot at 4 AM when kernel updates require it
4. Blacklist Docker packages (upgrade manually)
5. Clean up old kernels automatically
6. Keep existing config files during upgrades (--force-confold)
7. Enable syslog logging
8. Verify with a dry run

After setup:
- Show the complete 50unattended-upgrades config
- Show the 20auto-upgrades config
- Run dry run and show output
- Verify timers are active
```

## Prompt 3: Troubleshoot Upgrades

```
Automatic upgrades are not working on this server. {describe the problem}

Diagnostic steps:
1. Is the service installed? `dpkg -l unattended-upgrades`
2. Is it enabled? `cat /etc/apt/apt.conf.d/20auto-upgrades`
3. Are timers running? `systemctl list-timers apt-daily*`
4. Is there a lock? `sudo lsof /var/lib/dpkg/lock-frontend`
5. What does the log say? `tail -50 /var/log/unattended-upgrades/unattended-upgrades.log`
6. Any errors? `grep -i error /var/log/unattended-upgrades/unattended-upgrades.log | tail -10`
7. Manual dry run: `sudo unattended-upgrade --dry-run --debug`
8. Check apt sources: `sudo apt update` (any errors?)
9. Check disk space: `df -h /` (needs space for downloads)

Based on output, identify the issue and fix it.
Common causes:
- Lock file held by another apt process
- Disk full
- APT source errors (expired keys, unreachable repos)
- Config syntax error
- Timers disabled
```

## Prompt 4: Configure Notifications

```
Set up notifications for unattended-upgrades on this server.

Option A: Email (if MTA is configured)
- Configure Unattended-Upgrade::Mail and MailReport

Option B: Slack webhook
- Create a post-upgrade script that sends to Slack
- Include: packages upgraded, reboot status, any errors

Option C: Simple log monitoring
- Create a script that checks upgrade log and reboot status
- Run via cron daily, output to a monitoring endpoint

Implement the best option for this server setup.
Verify the notification triggers correctly.
```

## Prompt 5: Reboot Management

```
Manage the reboot cycle for this production server.

Check:
1. Is a reboot currently required? `cat /var/run/reboot-required`
2. Which packages need it? `cat /var/run/reboot-required.pkgs`
3. Is auto-reboot configured? Check 50unattended-upgrades
4. What time is auto-reboot set to?
5. Will services recover after reboot?
   - Check systemd user services have Restart=always
   - Check Docker containers have restart: unless-stopped
   - Check lingering is enabled for the user

If reboot is needed but auto-reboot is not configured:
- Option 1: Enable auto-reboot at 4 AM
- Option 2: Schedule manual reboot during maintenance window
- Option 3: Just reboot now (if safe)

After reboot:
- Verify all services are running
- Check health endpoints
- Verify Docker containers
```

## Prompt 6: Package Blacklist Management

```
Review and update the package blacklist for unattended-upgrades.

Steps:
1. Show current blacklist
2. List all installed packages that might need blacklisting:
   - Docker packages: `dpkg -l | grep docker`
   - Database packages: `dpkg -l | grep -E "postgres|redis|mysql"`
   - Web server: `dpkg -l | grep nginx`
   - Custom-compiled software

3. For each candidate:
   - Does it auto-restart safely after upgrade?
   - Does it require config migration between versions?
   - Is it managed by a separate update process?

4. Recommended blacklist categories:
   - Always blacklist: Docker CE, custom-compiled packages
   - Consider blacklisting: databases (if major versions), nginx (if custom modules)
   - Never blacklist: kernel, openssl, libc, systemd (security critical)

Update the blacklist and verify with a dry run.
```
