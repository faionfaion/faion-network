# Unattended Upgrades Templates

Copy-paste ready configurations for automatic security updates on Ubuntu 24.04.

## Template 1: 50unattended-upgrades (Production Server)

File: `/etc/apt/apt.conf.d/50unattended-upgrades`

```
// /etc/apt/apt.conf.d/50unattended-upgrades
// Production server — security updates only, auto-reboot at 4 AM

// --- Update Origins ---
// Only install security patches automatically
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
    // Uncomment to also install regular updates:
    // "${distro_id}:${distro_codename}-updates";
};

// --- Blacklist ---
// Packages that should NOT be auto-upgraded
// (require manual intervention or testing)
Unattended-Upgrade::Package-Blacklist {
    // Docker (version changes can break containers)
    "docker-ce";
    "docker-ce-cli";
    "containerd.io";
    "docker-buildx-plugin";
    "docker-compose-plugin";

    // Database (major upgrades need migration)
    // "postgresql-16";
    // "redis-server";

    // Web server (if custom-compiled)
    // "nginx";
};

// --- Reboot ---
// Auto-reboot at 4 AM when needed (kernel updates, libc, etc.)
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";

// --- Cleanup ---
// Remove old packages to save disk space
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";

// --- Upgrade Behavior ---
// Split into minimal steps for graceful interruption
Unattended-Upgrade::MinimalSteps "true";

// Fix interrupted dpkg runs
Unattended-Upgrade::AutoFixInterruptedDpkg "true";

// --- Logging ---
Unattended-Upgrade::SyslogEnable "true";
Unattended-Upgrade::SyslogFacility "daemon";
Unattended-Upgrade::Verbose "false";

// --- dpkg options ---
// Keep existing config files during upgrades
Dpkg::Options {
    "--force-confdef";
    "--force-confold";
};

// --- Bandwidth ---
// Limit download speed (bytes/sec, 0 = unlimited)
// Acquire::http::Dl-Limit "0";
```

## Template 2: 20auto-upgrades (Schedule)

File: `/etc/apt/apt.conf.d/20auto-upgrades`

```
// /etc/apt/apt.conf.d/20auto-upgrades
// How often to run automated package management

// Check for updates daily (1 = once per day)
APT::Periodic::Update-Package-Lists "1";

// Download upgradeable packages daily
APT::Periodic::Download-Upgradeable-Packages "1";

// Install security updates daily
APT::Periodic::Unattended-Upgrade "1";

// Clean package cache weekly
APT::Periodic::AutocleanInterval "7";
```

## Template 3: Timer Override (Fixed Schedule)

File: `/etc/systemd/system/apt-daily.timer.d/override.conf`

```ini
# Override apt-daily timer to run at 2 AM
# This controls when apt update runs (checks for new packages)
[Timer]
OnCalendar=
OnCalendar=*-*-* 02:00:00
RandomizedDelaySec=0
```

File: `/etc/systemd/system/apt-daily-upgrade.timer.d/override.conf`

```ini
# Override apt-daily-upgrade timer to run at 3 AM
# This controls when unattended-upgrade runs (installs packages)
# Set 1 hour after apt-daily to ensure package lists are fresh
[Timer]
OnCalendar=
OnCalendar=*-*-* 03:00:00
RandomizedDelaySec=0
```

Apply:
```bash
sudo systemctl daemon-reload
sudo systemctl restart apt-daily.timer
sudo systemctl restart apt-daily-upgrade.timer
systemctl list-timers apt-daily apt-daily-upgrade
```

## Template 4: Slack Notification Script

File: `/usr/local/bin/unattended-upgrade-notify.sh`

```bash
#!/bin/bash
# /usr/local/bin/unattended-upgrade-notify.sh
# Send Slack notification after unattended-upgrade runs
# Called via APT::Update::Post-Invoke or cron

set -euo pipefail

SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"
HOSTNAME=$(hostname)
LOG="/var/log/unattended-upgrades/unattended-upgrades.log"

# Exit if no webhook configured
[ -z "$SLACK_WEBHOOK" ] && exit 0

# Get today's upgrade activity
TODAY=$(date +%Y-%m-%d)
UPGRADES=$(grep "$TODAY" "$LOG" 2>/dev/null | grep -c "Packages that will be upgraded:" || echo "0")
INSTALLED=$(grep "$TODAY" "$LOG" 2>/dev/null | grep "Packages that will be upgraded:" | tail -1 || echo "none")
REBOOT_NEEDED="No"
[ -f /var/run/reboot-required ] && REBOOT_NEEDED="Yes"

# Only notify if something happened
[ "$UPGRADES" -eq 0 ] && exit 0

# Send notification
curl -s -X POST -H 'Content-type: application/json' \
    --data "{
        \"text\": \"*[$HOSTNAME]* Unattended upgrade completed\n- Packages: $INSTALLED\n- Reboot needed: $REBOOT_NEEDED\"
    }" \
    "$SLACK_WEBHOOK"
```

Cron entry:
```bash
# Run after upgrade timer (4 AM)
30 4 * * * SLACK_WEBHOOK_URL="https://hooks.slack.com/..." /usr/local/bin/unattended-upgrade-notify.sh
```

## Template 5: Reboot Monitor Script

File: `/usr/local/bin/check-reboot-required.sh`

```bash
#!/bin/bash
# /usr/local/bin/check-reboot-required.sh
# Check if server needs reboot and report

set -euo pipefail

if [ -f /var/run/reboot-required ]; then
    echo "REBOOT REQUIRED on $(hostname)"
    echo ""
    echo "Packages requiring reboot:"
    cat /var/run/reboot-required.pkgs 2>/dev/null || echo "(unknown)"
    echo ""
    echo "Uptime: $(uptime -p)"
    echo ""
    echo "Auto-reboot scheduled: $(grep -q 'Automatic-Reboot "true"' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null && echo "Yes" || echo "No")"

    if grep -q 'Automatic-Reboot "true"' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null; then
        REBOOT_TIME=$(grep 'Automatic-Reboot-Time' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null | grep -oP '"[^"]*"' | tr -d '"')
        echo "Reboot time: ${REBOOT_TIME:-not set}"
    fi
    exit 1
else
    echo "No reboot needed on $(hostname)"
    echo "Last upgrade: $(stat -c %y /var/log/unattended-upgrades/unattended-upgrades.log 2>/dev/null | cut -d. -f1 || echo 'unknown')"
    exit 0
fi
```

## Template 6: Pre-Upgrade Hook

File: `/etc/apt/apt.conf.d/05pre-upgrade-hook`

```
// Run script before installing upgrades
// Use for: backups, notifications, health checks
Dpkg::Pre-Install-Pkgs {
    "/usr/local/bin/pre-upgrade-hook.sh";
};
```

File: `/usr/local/bin/pre-upgrade-hook.sh`

```bash
#!/bin/bash
# /usr/local/bin/pre-upgrade-hook.sh
# Runs before packages are installed

set -euo pipefail

LOG="/var/log/pre-upgrade-hook.log"

echo "$(date): Pre-upgrade hook started" >> "$LOG"

# Log which packages are about to be upgraded
echo "$(date): Packages to upgrade:" >> "$LOG"
while read -r line; do
    echo "  $line" >> "$LOG"
done

echo "$(date): Pre-upgrade hook completed" >> "$LOG"
```

## Template 7: Upgrade Status Dashboard

```bash
#!/bin/bash
# upgrade-status.sh — Show upgrade status dashboard

echo "=============================="
echo "  Upgrade Status Dashboard"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M')"
echo "=============================="
echo ""

echo "--- Auto-Upgrade Config ---"
echo -n "Enabled: "
grep -q "Unattended-Upgrade \"1\"" /etc/apt/apt.conf.d/20auto-upgrades 2>/dev/null && echo "Yes" || echo "No"
echo -n "Auto-Reboot: "
grep -oP 'Automatic-Reboot "\K[^"]+' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null || echo "not set"
echo -n "Reboot Time: "
grep -oP 'Automatic-Reboot-Time "\K[^"]+' /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null || echo "not set"
echo ""

echo "--- Reboot Status ---"
if [ -f /var/run/reboot-required ]; then
    echo "REBOOT REQUIRED"
    cat /var/run/reboot-required.pkgs 2>/dev/null
else
    echo "No reboot needed"
fi
echo ""

echo "--- Pending Updates ---"
apt list --upgradable 2>/dev/null | tail -n +2 | head -10
PENDING=$(apt list --upgradable 2>/dev/null | tail -n +2 | wc -l)
echo "Total: $PENDING packages"
echo ""

echo "--- Recent Upgrades ---"
sudo tail -20 /var/log/unattended-upgrades/unattended-upgrades.log 2>/dev/null || echo "(no log)"
echo ""

echo "--- Timer Schedule ---"
systemctl list-timers apt-daily apt-daily-upgrade --no-pager 2>/dev/null | head -5
echo ""

echo "--- Blacklisted Packages ---"
grep -A20 "Package-Blacklist" /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null | grep '^\s*"' | tr -d '";' | awk '{print "  " $1}'
```
