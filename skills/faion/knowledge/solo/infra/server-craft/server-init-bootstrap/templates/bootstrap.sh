#!/usr/bin/env bash
# purpose: Template fixture for server-init-bootstrap: bootstrap.sh
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
# bootstrap.sh — Full interactive bootstrap: all 5 phases with verification steps
# Run as root or first-login user. Set variables at top before running.
set -euo pipefail

# === CONFIGURE THESE ===
NEW_USER="nero"
SSH_PORT="22022"
TIMEZONE="Europe/Lisbon"
HOSTNAME="server-name"
SSH_PUBLIC_KEY="ssh-ed25519 AAAAC3... your_key_here"
# ======================

echo "=== Phase 1: Access and Users ==="
useradd -m -s /bin/bash -G sudo "$NEW_USER" 2>/dev/null || echo "User $NEW_USER already exists"
mkdir -p "/home/$NEW_USER/.ssh"
chmod 700 "/home/$NEW_USER/.ssh"
echo "$SSH_PUBLIC_KEY" >> "/home/$NEW_USER/.ssh/authorized_keys"
chmod 600 "/home/$NEW_USER/.ssh/authorized_keys"
chown -R "$NEW_USER:$NEW_USER" "/home/$NEW_USER/.ssh"
echo "SSH key deployed. TEST LOGIN AS $NEW_USER IN A NEW TERMINAL BEFORE CONTINUING."
read -rp "Press ENTER after confirming SSH login works as $NEW_USER..."

echo ""
echo "=== Phase 2: System Identity ==="
hostnamectl set-hostname "$HOSTNAME"
grep -q "127.0.1.1" /etc/hosts || echo "127.0.1.1 $HOSTNAME" >> /etc/hosts
timedatectl set-timezone "$TIMEZONE"
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
timedatectl set-ntp true
echo "Hostname: $(hostname), Timezone: $(timedatectl | grep 'Time zone')"

echo ""
echo "=== Phase 3: Packages ==="
apt update && apt upgrade -y
apt install -y build-essential curl wget git htop tmux tree jq unzip zip \
  ca-certificates gnupg lsb-release rsync ncdu iotop sysstat \
  python3-dev python3-pip python3-venv libpq-dev libssl-dev \
  ufw fail2ban unattended-upgrades direnv

echo ""
echo "=== Phase 4: Security Hardening ==="
ufw default deny incoming
ufw default allow outgoing
ufw limit "${SSH_PORT}/tcp" comment 'SSH'
ufw allow 80/tcp  comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw logging low
ufw --force enable

cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local 2>/dev/null || true
cat > /etc/fail2ban/jail.local << 'FAIL2BAN'
[DEFAULT]
bantime  = 3600
findtime = 600
maxretry = 3

[sshd]
enabled  = true
port     = ssh
maxretry = 3
FAIL2BAN
systemctl enable fail2ban && systemctl restart fail2ban

dpkg-reconfigure -plow unattended-upgrades

# SSH hardening — review and apply manually
echo "TODO: edit /etc/ssh/sshd_config (Port, PermitRootLogin no, PasswordAuthentication no)"
echo "Then: sshd -t && systemctl reload sshd"

echo ""
echo "=== Phase 5: Services Foundation ==="
loginctl enable-linger "$NEW_USER"
sudo -u "$NEW_USER" mkdir -p "/home/$NEW_USER/.config/systemd/user"

echo ""
echo "=== Bootstrap Complete ==="
echo "Run verify-bootstrap.sh to confirm all settings."
