# Unattended Upgrades Checklist

Step-by-step checklist for configuring automatic security updates on Ubuntu 24.04.

## Prerequisites

- [ ] Root or sudo access
- [ ] Verify server has systemd services with Restart=always (for reboot recovery)

## Phase 1: Installation

- [ ] **Install packages**
  ```bash
  sudo apt update
  sudo apt install -y unattended-upgrades apt-listchanges
  ```

- [ ] **Verify installation**
  ```bash
  dpkg -l | grep unattended-upgrades
  ```

## Phase 2: Enable Auto-Updates

- [ ] **Configure auto-update schedule**
  ```bash
  sudo tee /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
  APT::Periodic::Update-Package-Lists "1";
  APT::Periodic::Unattended-Upgrade "1";
  APT::Periodic::Download-Upgradeable-Packages "1";
  APT::Periodic::AutocleanInterval "7";
  EOF
  ```
  Meaning:
  - Check for updates daily
  - Install security updates daily
  - Download upgradeable packages daily
  - Clean old packages weekly

## Phase 3: Configure Unattended Upgrades

- [ ] **Edit main configuration**
  ```bash
  sudo tee /etc/apt/apt.conf.d/50unattended-upgrades << 'UPGEOF'
  // Automatically upgrade packages from these origins
  Unattended-Upgrade::Allowed-Origins {
      "${distro_id}:${distro_codename}";
      "${distro_id}:${distro_codename}-security";
      "${distro_id}ESMApps:${distro_codename}-apps-security";
      "${distro_id}ESM:${distro_codename}-infra-security";
  };

  // Packages to never auto-upgrade
  Unattended-Upgrade::Package-Blacklist {
      "docker-ce";
      "docker-ce-cli";
      "containerd.io";
      "docker-buildx-plugin";
      "docker-compose-plugin";
  };

  // Auto-reboot at 4 AM if needed
  Unattended-Upgrade::Automatic-Reboot "true";
  Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
  Unattended-Upgrade::Automatic-Reboot-Time "04:00";

  // Cleanup old packages
  Unattended-Upgrade::Remove-Unused-Dependencies "true";
  Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
  Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";

  // Split upgrade to allow graceful shutdown
  Unattended-Upgrade::MinimalSteps "true";

  // Log syslog
  Unattended-Upgrade::SyslogEnable "true";
  Unattended-Upgrade::SyslogFacility "daemon";

  // Keep existing config files during upgrade
  Dpkg::Options {
      "--force-confdef";
      "--force-confold";
  };
  UPGEOF
  ```

- [ ] **Verify config syntax**
  ```bash
  sudo unattended-upgrade --dry-run --debug 2>&1 | head -20
  ```

## Phase 4: Verify Systemd Timers

- [ ] **Check timers are active**
  ```bash
  systemctl list-timers apt-daily apt-daily-upgrade
  ```

- [ ] **Verify timers are enabled**
  ```bash
  systemctl is-enabled apt-daily.timer
  systemctl is-enabled apt-daily-upgrade.timer
  ```

## Phase 5: Test

- [ ] **Run dry run**
  ```bash
  sudo unattended-upgrade --dry-run --debug 2>&1 | tail -30
  ```

- [ ] **Check for pending security updates**
  ```bash
  sudo apt list --upgradable 2>/dev/null | grep -i security
  ```

- [ ] **Check reboot requirement**
  ```bash
  [ -f /var/run/reboot-required ] && echo "REBOOT REQUIRED" || echo "No reboot needed"
  ```

## Phase 6: Verify Service Recovery After Reboot

- [ ] **Check all services have Restart=always**
  ```bash
  for svc in nero-core nero-channel-web nero-channel-tg nero-web; do
      RESTART=$(systemctl --user show "$svc" -p Restart 2>/dev/null | cut -d= -f2)
      echo "$svc: Restart=$RESTART"
  done
  ```

- [ ] **Test reboot recovery** (during maintenance window)
  ```bash
  # Reboot
  sudo reboot

  # After reboot, verify services are running
  systemctl --user status 'nero-*'
  curl -s http://127.0.0.1:8100/health
  ```

## Phase 7: Monitoring

- [ ] **Create reboot-check script**
  ```bash
  sudo tee /usr/local/bin/check-reboot << 'EOF'
  #!/bin/bash
  if [ -f /var/run/reboot-required ]; then
      echo "REBOOT REQUIRED"
      cat /var/run/reboot-required.pkgs 2>/dev/null
  else
      echo "No reboot needed"
  fi
  EOF
  sudo chmod +x /usr/local/bin/check-reboot
  ```

- [ ] **Check upgrade logs**
  ```bash
  sudo ls -la /var/log/unattended-upgrades/
  sudo tail -50 /var/log/unattended-upgrades/unattended-upgrades.log
  ```

## Post-Setup Verification

- [ ] **Wait 24 hours and verify** auto-update ran
  ```bash
  sudo cat /var/log/unattended-upgrades/unattended-upgrades.log | tail -20
  ```

- [ ] **Check apt history**
  ```bash
  sudo cat /var/log/apt/history.log | tail -30
  ```

## Rollback

If auto-upgrades cause issues:

```bash
# Disable auto-upgrades
sudo tee /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Unattended-Upgrade "0";
EOF

# Or remove the package entirely
sudo apt remove unattended-upgrades
```
