# fail2ban Setup Checklist

Step-by-step checklist for setting up fail2ban on Ubuntu 24.04 with multiple jails.

## Prerequisites

- [ ] Root or sudo access
- [ ] Know your SSH port: `sshd -T | grep port`
- [ ] Know which services to protect (SSH, nginx, etc.)
- [ ] Know your own IP (to whitelist): `curl -s ifconfig.me`

## Phase 1: Installation

- [ ] **Install fail2ban**
  ```bash
  sudo apt update
  sudo apt install -y fail2ban
  ```

- [ ] **Verify installation**
  ```bash
  fail2ban-server --version
  sudo systemctl status fail2ban
  ```

- [ ] **Check default backend**
  ```bash
  sudo fail2ban-client get sshd backend 2>/dev/null || echo "sshd jail not yet configured"
  ```

## Phase 2: Base Configuration

- [ ] **Create jail.local with defaults**
  ```bash
  sudo tee /etc/fail2ban/jail.local << 'EOF'
  [DEFAULT]
  # Backend: systemd journal
  backend = systemd

  # Ban action: nftables
  banaction = nftables
  banaction_allports = nftables[type=allports]

  # Default ban settings
  bantime = 3600
  findtime = 600
  maxretry = 5

  # Whitelist
  ignoreip = 127.0.0.1/8 ::1 172.16.0.0/12

  # Email (if configured)
  # destemail = admin@example.com
  # sender = fail2ban@example.com
  # mta = sendmail
  # action = %(action_mwl)s
  EOF
  ```

- [ ] **Verify config syntax**
  ```bash
  sudo fail2ban-client -t
  ```

## Phase 3: SSH Jail

- [ ] **Configure SSH jail**
  ```bash
  sudo tee /etc/fail2ban/jail.d/sshd.conf << 'EOF'
  [sshd]
  enabled = true
  port = 2222
  filter = sshd
  backend = systemd
  maxretry = 3
  findtime = 600
  bantime = 3600
  EOF
  ```

- [ ] **Restart fail2ban**
  ```bash
  sudo systemctl restart fail2ban
  ```

- [ ] **Verify SSH jail is active**
  ```bash
  sudo fail2ban-client status sshd
  ```

- [ ] **Test filter matches**
  ```bash
  sudo fail2ban-regex systemd-journal /etc/fail2ban/filter.d/sshd.conf
  ```

## Phase 4: nginx Jails

- [ ] **Verify nginx error log exists**
  ```bash
  ls -la /var/log/nginx/error.log
  ls -la /var/log/nginx/access.log
  ```

- [ ] **Configure nginx jails**
  ```bash
  sudo tee /etc/fail2ban/jail.d/nginx.conf << 'EOF'
  [nginx-http-auth]
  enabled = true
  port = http,https
  filter = nginx-http-auth
  logpath = /var/log/nginx/error.log
  maxretry = 3
  findtime = 600
  bantime = 3600

  [nginx-botsearch]
  enabled = true
  port = http,https
  filter = nginx-botsearch
  logpath = /var/log/nginx/access.log
  maxretry = 10
  findtime = 600
  bantime = 7200

  [nginx-limit-req]
  enabled = true
  port = http,https
  filter = nginx-limit-req
  logpath = /var/log/nginx/error.log
  maxretry = 5
  findtime = 600
  bantime = 3600
  EOF
  ```

- [ ] **Restart and verify**
  ```bash
  sudo systemctl restart fail2ban
  sudo fail2ban-client status
  ```

## Phase 5: Recidive Jail (Ban Escalation)

- [ ] **Configure recidive jail**
  ```bash
  sudo tee /etc/fail2ban/jail.d/recidive.conf << 'EOF'
  [recidive]
  enabled = true
  filter = recidive
  logpath = /var/log/fail2ban.log
  bantime = 604800
  findtime = 86400
  maxretry = 3
  banaction = nftables[type=allports]
  EOF
  ```

- [ ] **Restart and verify**
  ```bash
  sudo systemctl restart fail2ban
  sudo fail2ban-client status recidive
  ```

## Phase 6: Custom Filters (Optional)

- [ ] **Create custom filter for application auth failures**
  ```bash
  sudo tee /etc/fail2ban/filter.d/nero-web-auth.conf << 'EOF'
  [Definition]
  failregex = ^.*"POST /api/auth/login.*" 401.*<HOST>
              ^.*"POST /api/auth/register.*" 429.*<HOST>
  ignoreregex =
  EOF
  ```

- [ ] **Test custom filter**
  ```bash
  sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nero-web-auth.conf
  ```

## Phase 7: Verification

- [ ] **Check all jails**
  ```bash
  sudo fail2ban-client status
  ```

- [ ] **Check each jail individually**
  ```bash
  for jail in $(sudo fail2ban-client status | grep "Jail list" | sed 's/.*://;s/,//g'); do
      echo "=== $jail ==="
      sudo fail2ban-client status "$jail"
      echo ""
  done
  ```

- [ ] **Check nftables rules**
  ```bash
  sudo nft list ruleset | grep -c "f2b"
  ```

- [ ] **Check fail2ban log for errors**
  ```bash
  sudo grep -E "ERROR|WARNING" /var/log/fail2ban.log | tail -10
  ```

- [ ] **Verify your IP is not banned**
  ```bash
  MY_IP=$(curl -s ifconfig.me)
  for jail in $(sudo fail2ban-client status | grep "Jail list" | sed 's/.*://;s/,//g'); do
      BANNED=$(sudo fail2ban-client get "$jail" banip 2>/dev/null | grep -c "$MY_IP")
      [ "$BANNED" -gt 0 ] && echo "WARNING: $MY_IP is banned in $jail!"
  done
  echo "Check complete"
  ```

## Phase 8: Monitoring Setup

- [ ] **Create status script**
  ```bash
  sudo tee /usr/local/bin/f2b-status << 'SCRIPT'
  #!/bin/bash
  echo "=== fail2ban Status ==="
  echo "Jails: $(sudo fail2ban-client status | grep 'Jail list' | sed 's/.*://')"
  echo ""
  for jail in $(sudo fail2ban-client status | grep "Jail list" | sed 's/.*://;s/,//g'); do
      BANNED=$(sudo fail2ban-client status "$jail" | grep "Currently banned" | awk '{print $NF}')
      TOTAL=$(sudo fail2ban-client status "$jail" | grep "Total banned" | awk '{print $NF}')
      printf "%-20s Currently: %-5s Total: %s\n" "$jail" "$BANNED" "$TOTAL"
  done
  SCRIPT
  sudo chmod +x /usr/local/bin/f2b-status
  ```

- [ ] **Test status script**
  ```bash
  f2b-status
  ```

## Post-Setup Monitoring

- [ ] **Check logs daily** for the first week
  ```bash
  sudo tail -50 /var/log/fail2ban.log
  ```

- [ ] **Monitor false positives** (legitimate users being banned)
  ```bash
  sudo grep "Ban" /var/log/fail2ban.log | tail -20
  ```

## Rollback

If fail2ban causes issues:

```bash
# Unban all IPs
sudo fail2ban-client unban --all

# Stop fail2ban
sudo systemctl stop fail2ban

# Remove custom configs
sudo rm /etc/fail2ban/jail.d/sshd.conf
sudo rm /etc/fail2ban/jail.d/nginx.conf
sudo rm /etc/fail2ban/jail.d/recidive.conf
sudo rm /etc/fail2ban/jail.local

# Restart with defaults
sudo systemctl start fail2ban
```
