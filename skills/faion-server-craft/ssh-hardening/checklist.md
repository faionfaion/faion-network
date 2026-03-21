# SSH Hardening Checklist

Step-by-step checklist for hardening SSH on Ubuntu 24.04 VPS. Execute in order. Each step includes a verification command.

## Prerequisites

- [ ] Root or sudo access to the server
- [ ] At least one SSH key pair generated locally (`ssh-keygen -t ed25519`)
- [ ] Public key already in `~/.ssh/authorized_keys` on the server
- [ ] A second terminal/session open to the server (safety net)

## Phase 1: Key Setup

- [ ] **Generate ed25519 key** (on local machine)
  ```bash
  ssh-keygen -t ed25519 -C "user@workstation"
  ```
  Verify: `ls -la ~/.ssh/id_ed25519*`

- [ ] **Copy public key to server**
  ```bash
  ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server
  ```
  Verify: `ssh -i ~/.ssh/id_ed25519 user@server "echo OK"`

- [ ] **Test key-based login works** (in a NEW terminal)
  ```bash
  ssh user@server
  ```
  Verify: Connected without password prompt

## Phase 2: Server Configuration

- [ ] **Backup current sshd_config**
  ```bash
  sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)
  ```

- [ ] **Create hardening drop-in file**
  ```bash
  sudo tee /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
  Port 2222
  PermitRootLogin no
  PasswordAuthentication no
  PubkeyAuthentication yes
  ChallengeResponseAuthentication no
  KbdInteractiveAuthentication no
  X11Forwarding no
  AllowAgentForwarding no
  MaxAuthTries 3
  MaxSessions 5
  LoginGraceTime 30
  AllowUsers nero
  HostKey /etc/ssh/ssh_host_ed25519_key
  KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org
  Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
  MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
  EOF
  ```
  Verify: `sudo sshd -t` (no errors)

- [ ] **Update firewall BEFORE changing port**
  ```bash
  sudo ufw allow 2222/tcp comment "SSH"
  ```
  Verify: `sudo ufw status | grep 2222`

- [ ] **Update systemd socket for new port** (Ubuntu 24.04)
  ```bash
  sudo systemctl edit ssh.socket
  # Add:
  # [Socket]
  # ListenStream=
  # ListenStream=2222
  ```

- [ ] **Restart SSH**
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl restart ssh.socket
  sudo systemctl restart ssh
  ```
  Verify: `sudo ss -tlnp | grep 2222`

## Phase 3: Verification

- [ ] **Test connection on new port** (from local machine, NEW terminal)
  ```bash
  ssh -p 2222 user@server
  ```
  Verify: Connected successfully

- [ ] **Verify password auth is disabled**
  ```bash
  ssh -p 2222 -o PubkeyAuthentication=no user@server
  ```
  Verify: `Permission denied (publickey).`

- [ ] **Verify root login is disabled**
  ```bash
  ssh -p 2222 root@server
  ```
  Verify: `Permission denied (publickey).`

- [ ] **Check effective config**
  ```bash
  sudo sshd -T | grep -E 'port|permitrootlogin|passwordauthentication|pubkeyauthentication|maxauthtries|allowusers'
  ```

- [ ] **Run ssh-audit** (optional but recommended)
  ```bash
  pip install ssh-audit
  ssh-audit -p 2222 localhost
  ```
  Verify: No warnings for algorithms

## Phase 4: Cleanup

- [ ] **Remove old SSH port from firewall**
  ```bash
  sudo ufw delete allow 22/tcp
  # or: sudo ufw delete allow OpenSSH
  ```

- [ ] **Remove weak host keys**
  ```bash
  sudo rm -f /etc/ssh/ssh_host_rsa_key* /etc/ssh/ssh_host_ecdsa_key* /etc/ssh/ssh_host_dsa_key*
  ```

- [ ] **Update fail2ban SSH jail port**
  ```bash
  # In /etc/fail2ban/jail.d/defaults-debian.conf or custom:
  [sshd]
  port = 2222
  ```
  Restart: `sudo systemctl restart fail2ban`

- [ ] **Update local SSH config**
  ```bash
  # In ~/.ssh/config on local machine:
  Host myserver
      HostName 1.2.3.4
      User nero
      Port 2222
      IdentityFile ~/.ssh/id_ed25519
  ```

## Phase 5: Client-Side Hardening

- [ ] **Configure SSH client defaults** (on local machine)
  ```bash
  # In ~/.ssh/config:
  Host *
      HashKnownHosts yes
      IdentitiesOnly yes
      AddKeysToAgent yes
      ServerAliveInterval 60
      ServerAliveCountMax 3
  ```

- [ ] **Set correct permissions**
  ```bash
  chmod 700 ~/.ssh
  chmod 600 ~/.ssh/config
  chmod 600 ~/.ssh/id_ed25519
  chmod 644 ~/.ssh/id_ed25519.pub
  chmod 600 ~/.ssh/authorized_keys
  ```

## Post-Hardening Monitoring

- [ ] **Monitor auth log for anomalies**
  ```bash
  sudo journalctl -u ssh --since "24 hours ago" | grep -i "failed\|invalid\|accepted"
  ```

- [ ] **Set up log rotation** (usually default on Ubuntu)
  ```bash
  ls -la /etc/logrotate.d/rsyslog
  ```

## Rollback Plan

If locked out:

1. Access via VPS console (Hetzner Cloud Console)
2. Edit `/etc/ssh/sshd_config.d/99-hardening.conf` to restore defaults
3. `systemctl restart ssh`
4. Fix the issue and re-harden
