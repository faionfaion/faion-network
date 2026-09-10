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
SSH_PORT="2222"
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
# The firewall opens BOTH ports. sshd is still on 22 at this point, so enabling
# ufw with only $SSH_PORT allowed cuts the next login: the session you are typing
# in survives on conntrack, which is why it looks fine until you reconnect.
ufw default deny incoming
ufw default allow outgoing
ufw limit 22/tcp comment 'SSH (old port, revoked at the end of this phase)'
ufw limit "${SSH_PORT}/tcp" comment 'SSH'
ufw allow 80/tcp  comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw logging low
ufw --force enable

# SSH hardening is APPLIED here, not printed as a TODO. A drop-in survives
# package upgrades; editing sshd_config in place does not.
mkdir -p /etc/ssh/sshd_config.d
cat > /etc/ssh/sshd_config.d/99-hardening.conf << SSHD
Port ${SSH_PORT}
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AllowUsers ${NEW_USER}
MaxAuthTries 3
LoginGraceTime 30
X11Forwarding no
SSHD
sshd -t

# Ubuntu 24.04 and later socket-activate sshd: reloading the service there
# leaves the listener on the socket unit's port and the new Port is ignored.
if systemctl is-enabled --quiet ssh.socket 2>/dev/null; then
  mkdir -p /etc/systemd/system/ssh.socket.d
  printf '[Socket]\nListenStream=\nListenStream=%s\n' "$SSH_PORT" \
    > /etc/systemd/system/ssh.socket.d/port.conf
  systemctl daemon-reload
  systemctl restart ssh.socket
else
  systemctl reload ssh 2>/dev/null || systemctl reload sshd
fi

cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local 2>/dev/null || true
# Unquoted delimiter: the jail must watch the port sshd actually listens on.
# `port = ssh` resolves to 22 through /etc/services and watches nothing.
cat > /etc/fail2ban/jail.local << FAIL2BAN
[DEFAULT]
bantime  = 3600
findtime = 600
maxretry = 3

[sshd]
enabled  = true
port     = ${SSH_PORT}
filter   = sshd
backend  = systemd
maxretry = 3
FAIL2BAN
systemctl enable fail2ban && systemctl restart fail2ban

dpkg-reconfigure -plow unattended-upgrades

echo "SSH now listens on ${SSH_PORT} and rejects passwords and root."
echo "OPEN A NEW TERMINAL and run: ssh -p ${SSH_PORT} ${NEW_USER}@$(hostname -I | awk '{print $1}')"
read -rp "Press ENTER only after that login succeeded — port 22 closes next..."
ufw delete limit 22/tcp || true

echo ""
echo "=== Phase 5: Services Foundation ==="
loginctl enable-linger "$NEW_USER"
sudo -u "$NEW_USER" mkdir -p "/home/$NEW_USER/.config/systemd/user"

echo ""
echo "=== Bootstrap Complete ==="
echo "Run verify-bootstrap.sh to confirm all settings."
