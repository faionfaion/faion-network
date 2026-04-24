# SSH Hardening Examples

Real-world SSH hardening configurations based on production Hetzner VPS running NERO AI platform.

## Example 1: NERO Production Server (Hetzner CX53)

**Server:** Ubuntu 24.04, Hetzner CX53, 16 CPUs, 30GB RAM
**SSH Port:** 2222
**User:** nero (non-root, sudo access)
**Access:** Behind Cloudflare (DNS only, not proxied for SSH)

### Server Config: `/etc/ssh/sshd_config.d/99-hardening.conf`

```bash
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
KbdInteractiveAuthentication no
X11Forwarding no
MaxAuthTries 3
MaxSessions 10
LoginGraceTime 30
AllowUsers nero
HostKey /etc/ssh/ssh_host_ed25519_key
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
LogLevel VERBOSE
```

**Why MaxSessions 10:** Claude Code and other AI agents open multiple SSH sessions simultaneously. Default 10 handles this well. If running many parallel agents, increase to 20.

### Client Config (Developer Workstation)

```bash
# ~/.ssh/config

Host *
    HashKnownHosts yes
    IdentitiesOnly yes
    AddKeysToAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

Host nero
    HostName 168.119.xxx.xxx
    User nero
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    # Higher MaxSessions for AI agent work
    # (client-side has no effect, but documents intent)

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

### Setup Commands (Executed Once)

```bash
# 1. Create sockets directory for connection multiplexing
mkdir -p ~/.ssh/sockets

# 2. Generate key (on workstation)
ssh-keygen -t ed25519 -C "ruslan@workstation"

# 3. Copy key to server (while still on port 22)
ssh-copy-id -i ~/.ssh/id_ed25519.pub nero@168.119.xxx.xxx

# 4. Test key auth works (NEW terminal, keep old one open!)
ssh nero@168.119.xxx.xxx

# 5. Apply hardening config on server
sudo tee /etc/ssh/sshd_config.d/99-hardening.conf << 'SSHEOF'
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
KbdInteractiveAuthentication no
X11Forwarding no
MaxAuthTries 3
AllowUsers nero
SSHEOF

# 6. Add new port to firewall BEFORE restarting SSH
sudo ufw allow 2222/tcp comment "SSH"

# 7. Update systemd socket
sudo systemctl edit ssh.socket
# Add: [Socket]\nListenStream=\nListenStream=2222

# 8. Restart SSH
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
sudo systemctl restart ssh

# 9. Test on new port (NEW terminal!)
ssh -p 2222 nero@168.119.xxx.xxx

# 10. Remove old port from firewall
sudo ufw delete allow 22/tcp
```

## Example 2: Multi-Server Setup with ProxyJump

**Scenario:** Production server behind a jump host, plus a staging server.

```bash
# ~/.ssh/config

# Jump host (publicly accessible)
Host jump
    HostName jump.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_jump

# Production (only accessible via jump host)
Host prod
    HostName 10.0.1.10
    User nero
    Port 22
    IdentityFile ~/.ssh/id_ed25519_prod
    ProxyJump jump

# Staging (only accessible via jump host)
Host staging
    HostName 10.0.1.20
    User nero
    Port 22
    IdentityFile ~/.ssh/id_ed25519_staging
    ProxyJump jump

# Database server (accessible via prod)
Host prod-db
    HostName 10.0.2.5
    User postgres
    Port 22
    IdentityFile ~/.ssh/id_ed25519_db
    ProxyJump prod
```

Usage:
```bash
# Single command connects through jump host transparently
ssh prod
ssh staging
ssh prod-db  # Two hops: local -> jump -> prod -> prod-db

# SCP through jump host
scp local-file.txt prod:/tmp/

# Port forwarding through jump host (access prod DB from local)
ssh -L 5432:10.0.2.5:5432 prod
```

## Example 3: CI/CD Deploy Key with Restricted Commands

**Scenario:** GitHub Actions needs SSH access for deployment, but should only run the deploy script.

### On Server: `~/.ssh/authorized_keys`

```bash
# CI/CD deploy key — restricted to deploy command only
command="/home/nero/workspace/deploy/deploy.sh all",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIxxxxxxxxxx github-actions-deploy

# Developer workstation — full access
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIyyyyyyyyyy ruslan@workstation
```

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        env:
          SSH_PRIVATE_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
        run: |
          mkdir -p ~/.ssh
          echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -p 2222 168.119.xxx.xxx >> ~/.ssh/known_hosts
          ssh -p 2222 nero@168.119.xxx.xxx
          # The command= restriction in authorized_keys ensures
          # only deploy.sh runs, regardless of what we send
```

## Example 4: Cloudflare + SSH (Bypassing Proxy)

**Problem:** Cloudflare proxies HTTP/HTTPS traffic but cannot proxy SSH. SSH must connect to the server's direct IP, not through Cloudflare.

**Setup:**

1. DNS A record for `nero.faion.net` points to Cloudflare proxy (orange cloud) for HTTP/HTTPS
2. SSH connects directly to the server IP, not the domain name
3. Optionally, create a non-proxied DNS record for SSH:
   - `ssh.faion.net` -> direct IP (grey cloud, DNS only)

```bash
# ~/.ssh/config

# Use direct IP or non-proxied subdomain for SSH
Host nero
    HostName 168.119.xxx.xxx    # Direct IP, not nero.faion.net
    User nero
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

# Alternative: use a DNS-only (non-proxied) subdomain
Host nero-dns
    HostName ssh.faion.net      # Grey cloud in Cloudflare
    User nero
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
```

## Example 5: SSH Audit Output (Before vs After)

### Before Hardening (Default Ubuntu 24.04)

```
$ ssh-audit localhost
# General
(gen) banner: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13
(gen) software: OpenSSH 9.6p1
(gen) compression: enabled (zlib@openssh.com)

# Key Exchange Algorithms
(kex) curve25519-sha256           -- [info] available since OpenSSH 7.4
(kex) diffie-hellman-group16-sha512 -- [info] available since OpenSSH 7.3
(kex) diffie-hellman-group14-sha256 -- [warn] using a 2048-bit modulus
(kex) ecdh-sha2-nistp256          -- [warn] using NIST curve
(kex) ecdh-sha2-nistp384          -- [warn] using NIST curve
(kex) ecdh-sha2-nistp521          -- [warn] using NIST curve

# Host Keys
(key) rsa-sha2-512 (3072)        -- [info] available since OpenSSH 7.2
(key) ecdsa-sha2-nistp256         -- [warn] using NIST curve
(key) ssh-ed25519                 -- [info] available since OpenSSH 6.5

# Ciphers
(enc) aes128-ctr                  -- [info] available since OpenSSH 3.7
(enc) aes192-ctr                  -- [info] available since OpenSSH 3.7
(enc) aes256-ctr                  -- [info] available since OpenSSH 3.7
(enc) chacha20-poly1305@openssh.com -- [info] available since OpenSSH 6.5
(enc) aes128-gcm@openssh.com     -- [info] available since OpenSSH 6.2
(enc) aes256-gcm@openssh.com     -- [info] available since OpenSSH 6.2

# MACs
(mac) hmac-sha1                   -- [warn] using broken SHA-1 hash
(mac) hmac-sha2-256               -- [warn] using encrypt-and-MAC instead of EtM
```

### After Hardening

```
$ ssh-audit -p 2222 localhost
# General
(gen) banner: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13
(gen) software: OpenSSH 9.6p1
(gen) compression: enabled (zlib@openssh.com)

# Key Exchange Algorithms
(kex) sntrup761x25519-sha512@openssh.com -- [info] post-quantum hybrid
(kex) curve25519-sha256           -- [info] available since OpenSSH 7.4
(kex) curve25519-sha256@libssh.org -- [info] available since OpenSSH 6.5

# Host Keys
(key) ssh-ed25519                 -- [info] available since OpenSSH 6.5

# Ciphers (AEAD only)
(enc) chacha20-poly1305@openssh.com -- [info] available since OpenSSH 6.5
(enc) aes256-gcm@openssh.com     -- [info] available since OpenSSH 6.2
(enc) aes128-gcm@openssh.com     -- [info] available since OpenSSH 6.2

# MACs (EtM only)
(mac) hmac-sha2-512-etm@openssh.com -- [info] available since OpenSSH 6.2
(mac) hmac-sha2-256-etm@openssh.com -- [info] available since OpenSSH 6.2

# No warnings! All algorithms are modern and secure.
```

## Example 6: Troubleshooting Connection Issues

### Problem: "Connection refused" after port change

```bash
# Check if SSH is listening on new port
sudo ss -tlnp | grep ssh

# If not listening, check socket activation
sudo systemctl status ssh.socket
sudo systemctl status ssh

# Check if systemd override was applied
sudo systemctl cat ssh.socket

# Common fix: socket override not applied
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```

### Problem: "Permission denied (publickey)"

```bash
# On server, check permissions
ls -la ~/.ssh/
# Should be: drwx------ (700)

ls -la ~/.ssh/authorized_keys
# Should be: -rw------- (600)

# Check if key is in authorized_keys
grep "your-key-comment" ~/.ssh/authorized_keys

# Check sshd logs
sudo journalctl -u ssh -f
# Then try to connect from another terminal

# Common fix: wrong permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### Problem: "Too many authentication failures"

```bash
# Local machine: force specific key
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes -p 2222 nero@server

# Or in ~/.ssh/config:
Host myserver
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```
