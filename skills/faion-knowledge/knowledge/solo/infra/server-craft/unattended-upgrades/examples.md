# Unattended Upgrades Examples

Real-world configurations and scenarios for Ubuntu 24.04 on Hetzner CX53.

## Example 1: NERO Production Server Setup

**Server:** Ubuntu 24.04 (Noble Numbat), Hetzner CX53
**Services:** NERO AI platform (systemd user services), Docker (PostgreSQL, Redis, RabbitMQ)

### Current State

```bash
$ cat /etc/apt/apt.conf.d/50unattended-upgrades | grep -E "^[^/]" | head -10
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

$ cat /etc/apt/apt.conf.d/20auto-upgrades
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

### Recommended Configuration

```bash
# 1. Configure 50unattended-upgrades
sudo tee /etc/apt/apt.conf.d/50unattended-upgrades << 'EOF'
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

Unattended-Upgrade::Package-Blacklist {
    "docker-ce";
    "docker-ce-cli";
    "containerd.io";
    "docker-buildx-plugin";
    "docker-compose-plugin";
};

Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";

Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::MinimalSteps "true";

Unattended-Upgrade::SyslogEnable "true";

Dpkg::Options {
    "--force-confdef";
    "--force-confold";
};
EOF

# 2. Configure schedule
sudo tee /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
EOF

# 3. Dry run to verify
sudo unattended-upgrade --dry-run --debug 2>&1 | tail -20
```

### Service Recovery After Reboot

NERO uses systemd user services that start automatically:

```bash
$ systemctl --user list-unit-files 'nero-*' | grep enabled
nero-channel-tg.service    enabled
nero-channel-web.service   enabled
nero-core.service          enabled
nero-web.service           enabled

# User services start via lingering:
$ loginctl show-user nero | grep Linger
Linger=yes
```

Docker services recover automatically because docker.service has Restart=always, and Docker containers have `restart: unless-stopped` in docker-compose.yml.

## Example 2: Dry Run Output Analysis

```bash
$ sudo unattended-upgrade --dry-run --debug

Starting unattended upgrades script
Allowed origins are: o=Ubuntu,a=noble, o=Ubuntu,a=noble-security, o=UbuntuESMApps,a=noble-apps-security, o=UbuntuESM,a=noble-infra-security

Packages that will be upgraded:
  libssl3t64 openssl python3-cryptography

Packages with upgradable origin but held back:
  docker-ce (blacklisted)
  docker-ce-cli (blacklisted)

Writing dpkg log to /var/log/unattended-upgrades/unattended-upgrades-dpkg.log

All upgrades installed

Checking if reboot is required...
Reboot is not required
```

This shows:
- 3 security packages will be upgraded (libssl3t64, openssl, python3-cryptography)
- Docker packages are held back (blacklisted)
- No reboot needed for these packages

## Example 3: Kernel Update with Auto-Reboot

### Timeline

```
03:00 - apt-daily-upgrade.timer fires
03:01 - unattended-upgrade starts
03:02 - Downloads linux-image-6.8.0-92-generic
03:05 - Installs kernel package
03:06 - Creates /var/run/reboot-required
03:06 - Logs: "Reboot is required, scheduling for 04:00"
04:00 - Server reboots automatically
04:01 - GRUB loads new kernel
04:02 - systemd starts services
04:03 - Docker containers start (restart: unless-stopped)
04:04 - User services start (lingering enabled)
04:05 - nginx starts, health checks pass
04:06 - Server fully operational on new kernel
```

### Verification After Reboot

```bash
# Check new kernel
$ uname -r
6.8.0-92-generic

# Check services
$ systemctl --user status 'nero-*' | grep -E "Active:|nero-"
nero-core.service - Active: active (running) since ...
nero-channel-web.service - Active: active (running) since ...
nero-channel-tg.service - Active: active (running) since ...
nero-web.service - Active: active (running) since ...

# Check Docker
$ docker ps --format "table {{.Names}}\t{{.Status}}" | head -10
NAMES           STATUS
nero-postgres   Up 2 minutes
nero-redis      Up 2 minutes
nero-rabbitmq   Up 2 minutes

# Check health
$ curl -s http://127.0.0.1:8100/health | python3 -m json.tool
{
    "status": "healthy",
    "uptime": "120 seconds"
}

# Check old kernels were cleaned
$ dpkg --list | grep linux-image | grep -v $(uname -r)
# Should show very few old kernels (cleanup removed them)
```

## Example 4: Handling Held-Back Packages

### Scenario: Docker upgrade available but blacklisted

```bash
$ apt list --upgradable 2>/dev/null
docker-ce/noble 5:26.0.1-1~ubuntu.24.04~noble amd64 [upgradable from: 5:25.0.5-1~ubuntu.24.04~noble]
docker-ce-cli/noble 5:26.0.1-1~ubuntu.24.04~noble amd64 [upgradable from: 5:25.0.5-1~ubuntu.24.04~noble]

$ sudo unattended-upgrade --dry-run 2>&1 | grep -i blacklist
docker-ce is blacklisted, skipping
docker-ce-cli is blacklisted, skipping
```

### Manual Docker Upgrade (When Ready)

```bash
# 1. Read changelog
apt changelog docker-ce 2>/dev/null | head -30

# 2. Stop containers gracefully
cd ~/workspace/repos/nero-infra
docker compose down

# 3. Upgrade Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# 4. Verify Docker
docker --version
docker compose version

# 5. Restart containers
docker compose up -d
docker ps
```

## Example 5: Monitoring Upgrade History

### Check What Was Upgraded This Month

```bash
$ sudo cat /var/log/apt/history.log | grep -A2 "Start-Date: 2026-03"

Start-Date: 2026-03-15  03:12:45
Commandline: /usr/bin/unattended-upgrade
Upgrade: libssl3t64:amd64 (3.0.13-0ubuntu3.5, 3.0.13-0ubuntu3.6), openssl:amd64 (3.0.13-0ubuntu3.5, 3.0.13-0ubuntu3.6)
End-Date: 2026-03-15  03:12:52

Start-Date: 2026-03-18  03:08:23
Commandline: /usr/bin/unattended-upgrade
Upgrade: linux-image-6.8.0-92-generic:amd64 (6.8.0-92.92, 6.8.0-92.93)
End-Date: 2026-03-18  03:09:45
```

### Check Upgrade Frequency

```bash
$ grep "Start-Date" /var/log/apt/history.log | grep "unattended" -A1 | wc -l

# Or check unattended-upgrades specific log
$ grep "Packages that will be upgraded" /var/log/unattended-upgrades/unattended-upgrades.log | wc -l
12    # 12 upgrade sessions this period
```

## Example 6: Troubleshooting Failed Upgrades

### Problem: Upgrades Not Running

```bash
# Check if timer is active
$ systemctl list-timers apt-daily-upgrade
NEXT                         LEFT       LAST                         PASSED    UNIT
Mon 2026-03-22 06:14:00 UTC  12h left   Sun 2026-03-21 06:14:00 UTC 11h ago   apt-daily-upgrade.timer

# Check if unattended-upgrade ran
$ sudo grep "$(date +%Y-%m-%d)" /var/log/unattended-upgrades/unattended-upgrades.log
# (empty means it didn't run today)

# Manual run with debug
$ sudo unattended-upgrade --debug 2>&1 | tail -30
# Look for: "No packages found that can be upgraded unattended"
# This means all security packages are already up to date (good!)
```

### Problem: dpkg Lock Error

```bash
# Error: "Could not get lock /var/lib/dpkg/lock-frontend"
# Another apt process is running

# Find the process
$ sudo lsof /var/lib/dpkg/lock-frontend
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
apt     1234 root   4uW  REG  259,1        0 1234567 /var/lib/dpkg/lock-frontend

# Wait for it to finish, or kill if stuck
$ ps aux | grep apt | grep -v grep
```

### Problem: Config File Conflict

```bash
# Error in log: "Configuration file '/etc/something.conf'
# ==> Modified (by you or by a script) since installation."

# Fix: Add dpkg options to keep old configs
# Already in our template:
Dpkg::Options {
    "--force-confdef";
    "--force-confold";
};
# --force-confold = keep your modified config
# --force-confdef = use default for new files
```
