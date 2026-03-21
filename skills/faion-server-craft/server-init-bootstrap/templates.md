# Server Init Bootstrap Templates

## bootstrap.sh

Complete automated bootstrap script for a new Ubuntu 24.04 VPS.

```bash
#!/bin/bash
# bootstrap.sh - Full server bootstrap for Ubuntu 24.04 VPS
# Run as root on first login: bash bootstrap.sh <username> <ssh-pubkey>
# Example: bash bootstrap.sh nero "ssh-ed25519 AAAAC3... user@workstation"
set -euo pipefail

USERNAME="${1:?Usage: bash bootstrap.sh <username> <ssh-pubkey-string>}"
SSH_PUBKEY="${2:?Provide SSH public key as second argument}"
HOSTNAME="${3:-$(hostname)}"
TIMEZONE="${4:-Europe/Lisbon}"

echo "============================================================"
echo "Server Bootstrap: Ubuntu 24.04"
echo "User: $USERNAME"
echo "Hostname: $HOSTNAME"
echo "Timezone: $TIMEZONE"
echo "============================================================"

# ============================================================
# Phase 1: System Identity
# ============================================================
echo ""
echo "=== Phase 1: System Identity ==="

hostnamectl set-hostname "$HOSTNAME"
echo "127.0.1.1 $HOSTNAME" >> /etc/hosts

timedatectl set-timezone "$TIMEZONE"
timedatectl set-ntp true

locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

echo "Hostname: $(hostname)"
echo "Timezone: $(timedatectl | grep 'Time zone' | awk '{print $3}')"

# ============================================================
# Phase 2: Create User
# ============================================================
echo ""
echo "=== Phase 2: Create User ==="

if id "$USERNAME" &>/dev/null; then
    echo "User $USERNAME already exists"
else
    useradd -m -s /bin/bash -G sudo "$USERNAME"
    # Set a random password (user will use SSH key)
    echo "$USERNAME:$(openssl rand -base64 32)" | chpasswd
    echo "User $USERNAME created"
fi

# Deploy SSH key
SSH_DIR="/home/$USERNAME/.ssh"
mkdir -p "$SSH_DIR"
echo "$SSH_PUBKEY" >> "$SSH_DIR/authorized_keys"
chmod 700 "$SSH_DIR"
chmod 600 "$SSH_DIR/authorized_keys"
chown -R "$USERNAME:$USERNAME" "$SSH_DIR"
echo "SSH key deployed"

# ============================================================
# Phase 3: SSH Hardening
# ============================================================
echo ""
echo "=== Phase 3: SSH Hardening ==="

SSHD_CONFIG="/etc/ssh/sshd_config"
cp "$SSHD_CONFIG" "${SSHD_CONFIG}.backup"

# Apply hardening settings
sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin no/' "$SSHD_CONFIG"
sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication no/' "$SSHD_CONFIG"
sed -i 's/^#\?PubkeyAuthentication .*/PubkeyAuthentication yes/' "$SSHD_CONFIG"
sed -i 's/^#\?ChallengeResponseAuthentication .*/ChallengeResponseAuthentication no/' "$SSHD_CONFIG"
sed -i 's/^#\?X11Forwarding .*/X11Forwarding no/' "$SSHD_CONFIG"
sed -i 's/^#\?MaxAuthTries .*/MaxAuthTries 3/' "$SSHD_CONFIG"

# Add AllowUsers if not present
if ! grep -q "AllowUsers" "$SSHD_CONFIG"; then
    echo "AllowUsers $USERNAME" >> "$SSHD_CONFIG"
fi

# Test before applying
sshd -t && systemctl reload sshd
echo "SSH hardened (root login disabled, key-only auth)"

# ============================================================
# Phase 4: System Update
# ============================================================
echo ""
echo "=== Phase 4: System Update ==="

apt update
DEBIAN_FRONTEND=noninteractive apt upgrade -y
apt autoremove -y

# ============================================================
# Phase 5: Essential Packages
# ============================================================
echo ""
echo "=== Phase 5: Essential Packages ==="

DEBIAN_FRONTEND=noninteractive apt install -y \
    build-essential \
    curl \
    wget \
    git \
    htop \
    tmux \
    tree \
    jq \
    unzip \
    zip \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    net-tools \
    dnsutils \
    rsync \
    ncdu \
    iotop \
    sysstat \
    lsof \
    strace \
    python3-dev \
    python3-pip \
    python3-venv \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    direnv \
    stow \
    fail2ban \
    ufw \
    unattended-upgrades

echo "Packages installed"

# ============================================================
# Phase 6: Firewall
# ============================================================
echo ""
echo "=== Phase 6: Firewall ==="

ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
echo "y" | ufw enable
echo "UFW enabled"
ufw status

# ============================================================
# Phase 7: Fail2ban
# ============================================================
echo ""
echo "=== Phase 7: Fail2ban ==="

cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

cat > /etc/fail2ban/jail.d/custom.conf << 'FAIL2BAN'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
FAIL2BAN

systemctl enable fail2ban
systemctl restart fail2ban
echo "Fail2ban configured"

# ============================================================
# Phase 8: Automatic Updates
# ============================================================
echo ""
echo "=== Phase 8: Automatic Updates ==="

dpkg-reconfigure -plow unattended-upgrades
echo "Unattended upgrades configured"

# ============================================================
# Phase 9: Swap
# ============================================================
echo ""
echo "=== Phase 9: Swap ==="

SWAP_SIZE="4G"
if ! swapon --show | grep -q /swapfile; then
    fallocate -l "$SWAP_SIZE" /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap created: $SWAP_SIZE"
else
    echo "Swap already exists"
fi

# Memory tuning
cat > /etc/sysctl.d/99-memory.conf << 'SYSCTL'
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.min_free_kbytes=65536
SYSCTL
sysctl --system >/dev/null

# ============================================================
# Phase 10: systemd User Services
# ============================================================
echo ""
echo "=== Phase 10: systemd User Services ==="

loginctl enable-linger "$USERNAME"
sudo -u "$USERNAME" mkdir -p "/home/$USERNAME/.config/systemd/user"
echo "User linger enabled"

# ============================================================
# Phase 11: Journal Size
# ============================================================
echo ""
echo "=== Phase 11: Journal ==="

sed -i 's/#SystemMaxUse=/SystemMaxUse=500M/' /etc/systemd/journald.conf
systemctl restart systemd-journald
echo "Journal limited to 500M"

# ============================================================
# Verification
# ============================================================
echo ""
echo "============================================================"
echo "Bootstrap Complete!"
echo "============================================================"
echo "Hostname:   $(hostname)"
echo "Timezone:   $(timedatectl | grep 'Time zone' | awk '{print $3}')"
echo "Locale:     $(locale | head -1)"
echo "UFW:        $(ufw status | head -1)"
echo "Fail2ban:   $(systemctl is-active fail2ban)"
echo "SSH:        PermitRootLogin=$(grep PermitRootLogin /etc/ssh/sshd_config | head -1 | awk '{print $2}')"
echo "Swap:       $(swapon --show --noheadings | awk '{print $3}')"
echo "Swappiness: $(sysctl vm.swappiness | awk '{print $3}')"
echo "Linger:     $(loginctl show-user $USERNAME 2>/dev/null | grep Linger)"
echo "Memory:     $(free -h | awk '/^Mem:/{print $2 " total, " $3 " used"}')"
echo "Disk:       $(df -h / | awk 'NR==2{print $2 " total, " $3 " used, " $4 " free"}')"
echo ""
echo "Next steps:"
echo "  1. SSH as $USERNAME: ssh $USERNAME@$(hostname -I | awk '{print $1}')"
echo "  2. Install mise: curl https://mise.run | sh"
echo "  3. Deploy dotfiles (if any)"
echo "  4. Set up project directories"
echo "  5. Install Docker (if needed)"
```

## cloud-init.yml

Cloud-init configuration for automated VPS provisioning (Hetzner, DigitalOcean, etc.).

```yaml
#cloud-config
# cloud-init.yml - Automated Ubuntu 24.04 server provisioning
# Use in Hetzner Cloud: paste in "Cloud config" during server creation

hostname: nero-hetzner
timezone: Europe/Lisbon
locale: en_US.UTF-8

# Create user with SSH key
users:
  - name: nero
    groups: [sudo, docker]
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@workstation

# Disable password auth
ssh_pwauth: false

# Install packages
package_update: true
package_upgrade: true
packages:
  - build-essential
  - curl
  - wget
  - git
  - htop
  - tmux
  - tree
  - jq
  - unzip
  - rsync
  - ncdu
  - sysstat
  - lsof
  - python3-dev
  - python3-pip
  - python3-venv
  - libpq-dev
  - libffi-dev
  - libssl-dev
  - direnv
  - stow
  - fail2ban
  - ufw
  - unattended-upgrades
  - net-tools
  - dnsutils
  - ca-certificates
  - gnupg

# Configure swap
swap:
  filename: /swapfile
  size: 4294967296  # 4GB in bytes
  maxsize: 4294967296

# Run commands after boot
runcmd:
  # SSH hardening
  - sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config
  - sed -i 's/^#\?MaxAuthTries .*/MaxAuthTries 3/' /etc/ssh/sshd_config
  - sed -i 's/^#\?X11Forwarding .*/X11Forwarding no/' /etc/ssh/sshd_config
  - echo "AllowUsers nero" >> /etc/ssh/sshd_config
  - systemctl reload sshd

  # Firewall
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow 22/tcp
  - ufw allow 80/tcp
  - ufw allow 443/tcp
  - echo "y" | ufw enable

  # Fail2ban
  - cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
  - systemctl enable fail2ban
  - systemctl start fail2ban

  # Memory tuning
  - echo 'vm.swappiness=10' > /etc/sysctl.d/99-memory.conf
  - echo 'vm.vfs_cache_pressure=50' >> /etc/sysctl.d/99-memory.conf
  - echo 'vm.min_free_kbytes=65536' >> /etc/sysctl.d/99-memory.conf
  - sysctl --system

  # systemd user linger
  - loginctl enable-linger nero

  # Journal size limit
  - sed -i 's/#SystemMaxUse=/SystemMaxUse=500M/' /etc/systemd/journald.conf
  - systemctl restart systemd-journald

  # Create directories
  - mkdir -p /srv/nero
  - chown nero:nero /srv/nero
  - sudo -u nero mkdir -p /home/nero/.config/systemd/user
  - sudo -u nero mkdir -p /home/nero/workspace

# Final message
final_message: "Server bootstrap complete. Login: ssh nero@$HOSTNAME"
```

## Post-Bootstrap Verification Script

```bash
#!/bin/bash
# verify-bootstrap.sh - Verify server bootstrap was successful
# Run as the non-root user
set -euo pipefail

PASS=0
FAIL=0

check() {
    local desc="$1"
    local cmd="$2"
    if eval "$cmd" >/dev/null 2>&1; then
        echo "[PASS] $desc"
        ((PASS++))
    else
        echo "[FAIL] $desc"
        ((FAIL++))
    fi
}

echo "=== Server Bootstrap Verification ==="
echo ""

check "Hostname is set" "[ -n '$(hostname)' ]"
check "Timezone is set" "timedatectl | grep -q 'Time zone'"
check "Locale is UTF-8" "locale | grep -q 'UTF-8'"
check "UFW is active" "sudo ufw status | grep -q 'active'"
check "Fail2ban is running" "systemctl is-active fail2ban"
check "Root login disabled" "grep -q 'PermitRootLogin no' /etc/ssh/sshd_config"
check "Password auth disabled" "grep -q 'PasswordAuthentication no' /etc/ssh/sshd_config"
check "Swap is active" "swapon --show | grep -q swapfile"
check "Swappiness is 10" "[ $(sysctl -n vm.swappiness) -eq 10 ]"
check "Linger enabled" "loginctl show-user $(whoami) | grep -q 'Linger=yes'"
check "systemd user dir exists" "[ -d ~/.config/systemd/user ]"
check "Git installed" "command -v git"
check "Python3 installed" "command -v python3"
check "pip3 installed" "command -v pip3"
check "tmux installed" "command -v tmux"
check "htop installed" "command -v htop"
check "jq installed" "command -v jq"
check "rsync installed" "command -v rsync"
check "direnv installed" "command -v direnv"
check "stow installed" "command -v stow"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
    echo "Some checks failed. Review and fix."
    exit 1
else
    echo "All checks passed. Server is ready."
fi
```
