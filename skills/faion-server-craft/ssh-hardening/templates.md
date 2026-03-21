# SSH Hardening Templates

Copy-paste ready configuration templates for SSH server and client hardening.

## Template 1: sshd_config Drop-in (Server)

File: `/etc/ssh/sshd_config.d/99-hardening.conf`

```bash
# /etc/ssh/sshd_config.d/99-hardening.conf
# SSH Hardening — Production VPS
# Applied on top of default Ubuntu 24.04 sshd_config

# --- Network ---
Port 2222

# --- Authentication ---
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
MaxAuthTries 3
MaxSessions 5
LoginGraceTime 30

# --- Access Control ---
# Only allow specific users (space-separated)
AllowUsers nero

# --- Host Keys (ed25519 only) ---
HostKey /etc/ssh/ssh_host_ed25519_key

# --- Cryptographic Hardening ---
# Key Exchange (post-quantum hybrid + curve25519)
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org

# Ciphers (AEAD only, chacha20 preferred)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# MACs (encrypt-then-mac only; used as fallback for non-AEAD ciphers)
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# --- Features ---
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
PermitTunnel no
GatewayPorts no

# --- Logging ---
LogLevel VERBOSE
SyslogFacility AUTH

# --- Misc ---
UsePAM yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
```

## Template 2: SSH Client Config (Local Machine)

File: `~/.ssh/config`

```bash
# ~/.ssh/config — SSH Client Configuration

# --- Global Defaults ---
Host *
    # Security
    HashKnownHosts yes
    IdentitiesOnly yes

    # Key management
    AddKeysToAgent yes

    # Connection keepalive
    ServerAliveInterval 60
    ServerAliveCountMax 3

    # Crypto (match server hardening)
    KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

    # Connection multiplexing (reuse connections)
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# --- Host Definitions ---

# Production VPS (Hetzner)
Host nero-prod
    HostName 1.2.3.4
    User nero
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

# Staging / Dev server
Host nero-staging
    HostName 5.6.7.8
    User nero
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

# Jump host example
Host internal-db
    HostName 10.0.0.5
    User dbadmin
    Port 22
    ProxyJump nero-prod
    IdentityFile ~/.ssh/id_ed25519_internal

# GitHub (force ed25519)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# GitLab
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

## Template 3: authorized_keys (Server)

File: `~/.ssh/authorized_keys`

```bash
# ~/.ssh/authorized_keys
# Format: <type> <key> <comment>
# One key per line. Comment identifies the source machine.

# Workstation (main dev machine)
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx user@workstation

# Laptop (travel)
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy user@laptop

# CI/CD (GitHub Actions deploy key — restrict with command=)
command="/usr/local/bin/deploy.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz ci-deploy
```

## Template 4: Systemd Socket Override (Ubuntu 24.04)

File: `/etc/systemd/system/ssh.socket.d/override.conf`

```ini
# /etc/systemd/system/ssh.socket.d/override.conf
# Override default SSH port from 22 to 2222
[Socket]
ListenStream=
ListenStream=2222
```

Apply:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```

## Template 5: SSH Key Generation Script

```bash
#!/bin/bash
# generate-ssh-key.sh — Generate ed25519 key with proper permissions

set -euo pipefail

KEY_NAME="${1:-id_ed25519}"
COMMENT="${2:-$(whoami)@$(hostname)}"

KEY_PATH="$HOME/.ssh/$KEY_NAME"

if [ -f "$KEY_PATH" ]; then
    echo "Key already exists: $KEY_PATH"
    echo "Delete it first if you want to regenerate."
    exit 1
fi

# Create .ssh directory if needed
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

# Generate key
ssh-keygen -t ed25519 -C "$COMMENT" -f "$KEY_PATH"

# Set permissions
chmod 600 "$KEY_PATH"
chmod 644 "$KEY_PATH.pub"

echo ""
echo "Key generated:"
echo "  Private: $KEY_PATH"
echo "  Public:  $KEY_PATH.pub"
echo ""
echo "Public key contents:"
cat "$KEY_PATH.pub"
echo ""
echo "Copy to server with:"
echo "  ssh-copy-id -i $KEY_PATH.pub user@server"
```

## Template 6: SSH Audit Script

```bash
#!/bin/bash
# ssh-audit-check.sh — Quick SSH security audit

set -euo pipefail

PORT="${1:-2222}"
HOST="${2:-localhost}"

echo "=== SSH Hardening Audit ==="
echo "Target: $HOST:$PORT"
echo ""

echo "--- Effective Configuration ---"
sudo sshd -T 2>/dev/null | grep -E \
    'port |permitrootlogin |passwordauthentication |pubkeyauthentication |maxauthtries |allowusers |kexalgorithms |ciphers |macs |x11forwarding |allowagentforwarding |loglevel ' \
    | sort

echo ""
echo "--- Host Keys ---"
ls -la /etc/ssh/ssh_host_*_key 2>/dev/null | awk '{print $NF}'

echo ""
echo "--- Listening Ports ---"
sudo ss -tlnp | grep ssh

echo ""
echo "--- Recent Auth Events (last 1h) ---"
sudo journalctl -u ssh --since "1 hour ago" --no-pager 2>/dev/null | \
    grep -cE 'Accepted|Failed|Invalid' || echo "0 events"

echo ""
echo "--- Config Syntax Check ---"
if sudo sshd -t 2>&1; then
    echo "OK: No syntax errors"
else
    echo "ERROR: Config has syntax errors"
fi
```
