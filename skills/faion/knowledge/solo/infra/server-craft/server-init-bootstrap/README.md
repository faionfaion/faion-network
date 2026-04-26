# Server Init Bootstrap

## Overview

Complete first-login setup procedure for Ubuntu 24.04 VPS servers. Covers user creation, SSH hardening, hostname and timezone configuration, locale setup, essential package installation, firewall configuration, initial system tuning, and automation via bootstrap scripts and cloud-init. Designed for solo developers provisioning Hetzner/DigitalOcean/Linode VPS for AI agent platforms.

**Target:** Fresh Ubuntu 24.04 LTS VPS (Hetzner CX53 or similar), from root SSH to production-ready.

## When to Use

| Scenario | Fit |
|----------|-----|
| First login to a new VPS | Essential |
| Rebuilding a server from scratch | Essential |
| Automating server provisioning | Recommended |
| Documenting server setup for reproducibility | Recommended |
| Setting up cloud-init for auto-provisioning | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Bootstrap** | Automated first-login setup: user, SSH, packages, hardening |
| **cloud-init** | Vendor-neutral server initialization on first boot |
| **SSH hardening** | Disable password auth, disable root login, key-only access |
| **UFW** | Uncomplicated Firewall, frontend for iptables |
| **unattended-upgrades** | Automatic security updates |
| **fail2ban** | Intrusion prevention (brute-force SSH protection) |
| **systemd-timesyncd** | NTP time synchronization |

## First Login Checklist

### Phase 1: Access and Users (First 5 Minutes)

1. SSH as root with provider-given credentials
2. Create non-root user with sudo privileges
3. Deploy SSH key for new user
4. Test SSH login as new user (in separate terminal)
5. Disable root SSH login and password authentication

### Phase 2: System Identity

6. Set hostname
7. Configure timezone
8. Set locale
9. Update /etc/hosts

### Phase 3: Packages and Tools

10. Update system packages
11. Install essential packages
12. Install development tools (git, build-essential)
13. Install runtime managers (mise)
14. Install shell tools (direnv, tmux, htop)

### Phase 4: Security Hardening

15. Configure UFW firewall
16. Install and configure fail2ban
17. Enable unattended-upgrades
18. Configure SSH hardening
19. Set up swap (see swap-memory-management)

### Phase 5: Services Foundation

20. Enable systemd user linger (for user services)
21. Create service directories
22. Install Docker (if needed)
23. Configure log rotation

## User Creation

### Create Non-Root User

```bash
# As root
adduser nero                    # Interactive: set password, full name
usermod -aG sudo nero           # Add to sudo group

# Or non-interactive
useradd -m -s /bin/bash -G sudo nero
echo "nero:$(openssl rand -base64 32)" | chpasswd
```

### SSH Key Deployment

```bash
# On the SERVER as root (for the new user)
mkdir -p /home/nero/.ssh
chmod 700 /home/nero/.ssh

# Paste your public key
cat >> /home/nero/.ssh/authorized_keys << 'EOF'
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@workstation
EOF

chmod 600 /home/nero/.ssh/authorized_keys
chown -R nero:nero /home/nero/.ssh
```

```bash
# Or from your LOCAL machine
ssh-copy-id -i ~/.ssh/id_ed25519.pub nero@server-ip
```

### Verify Access (DO THIS BEFORE DISABLING ROOT)

```bash
# From local machine - test new user login
ssh nero@server-ip
sudo whoami   # Should output: root
```

## SSH Hardening

### /etc/ssh/sshd_config Changes

```bash
# Key settings to change
Port 22                              # Consider changing (e.g., 2222)
PermitRootLogin no                   # Disable root SSH
PasswordAuthentication no            # Key-only auth
PubkeyAuthentication yes             # Enable key auth
AuthorizedKeysFile .ssh/authorized_keys
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
MaxAuthTries 3                       # Limit login attempts
ClientAliveInterval 300              # Disconnect idle after 5min
ClientAliveCountMax 2                # 2 keepalive failures = disconnect
AllowUsers nero                      # Only allow specific users
```

```bash
# Apply changes
sudo sshd -t           # Test config syntax FIRST
sudo systemctl reload sshd
```

### SSH Key Best Practices

| Key Type | Recommendation |
|----------|---------------|
| ed25519 | Preferred (modern, fast, secure) |
| RSA 4096 | Acceptable (legacy compatibility) |
| DSA | Never use (deprecated) |
| ECDSA | Acceptable but ed25519 preferred |

## System Configuration

### Hostname

```bash
sudo hostnamectl set-hostname nero-hetzner
echo "127.0.1.1 nero-hetzner" | sudo tee -a /etc/hosts
```

### Timezone

```bash
sudo timedatectl set-timezone Europe/Lisbon
timedatectl status
```

### Locale

```bash
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
```

### Time Sync

```bash
sudo timedatectl set-ntp true
systemctl status systemd-timesyncd
```

## Essential Packages

### Core System Packages

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
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
  strace
```

### Python Development

```bash
sudo apt install -y \
  python3-dev \
  python3-pip \
  python3-venv \
  libpq-dev \
  libffi-dev \
  libssl-dev
```

### Runtime Managers (mise + direnv)

See [direnv-mise-versions](../direnv-mise-versions/) for detailed setup.

```bash
# mise
curl https://mise.run | sh
echo 'eval "$(mise activate bash)"' >> ~/.bashrc

# direnv
sudo apt install -y direnv
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
```

## Firewall (UFW)

```bash
# Install and configure
sudo apt install -y ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (do this BEFORE enabling!)
sudo ufw allow 22/tcp comment 'SSH'

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status verbose
```

### Additional Port Rules (After App Setup)

```bash
# Only if services need to be exposed directly (usually nginx proxies)
sudo ufw allow from 127.0.0.1 to any port 5432 comment 'PostgreSQL local'
sudo ufw allow from 127.0.0.1 to any port 6379 comment 'Redis local'
```

## Fail2ban

```bash
sudo apt install -y fail2ban

# Create local config (survives upgrades)
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

```ini
# /etc/fail2ban/jail.local - key settings
[DEFAULT]
bantime = 3600        # 1 hour ban
findtime = 600        # 10 minute window
maxretry = 3          # 3 failed attempts

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
```

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo fail2ban-client status sshd
```

## Automatic Security Updates

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Verify configuration
cat /etc/apt/apt.conf.d/20auto-upgrades
```

## systemd User Services

### Enable Linger (Required for User Services)

```bash
# Allow user services to run without active login session
sudo loginctl enable-linger nero

# Verify
loginctl show-user nero | grep Linger
```

### Create Service Directories

```bash
mkdir -p ~/.config/systemd/user
```

## Log Rotation

### systemd Journal Size Limit

```bash
# /etc/systemd/journald.conf
sudo sed -i 's/#SystemMaxUse=/SystemMaxUse=500M/' /etc/systemd/journald.conf
sudo systemctl restart systemd-journald
```

### Application Log Rotation

```bash
# /etc/logrotate.d/nero
/srv/nero/*/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nero nero
}
```

## Docker Installation (Optional)

```bash
# Official Docker install
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group (no sudo for docker commands)
sudo usermod -aG docker nero

# Enable and start
sudo systemctl enable docker
sudo systemctl start docker
```

## Post-Bootstrap Verification

```bash
# Verify all critical settings
echo "=== Hostname ===" && hostname
echo "=== Timezone ===" && timedatectl | grep "Time zone"
echo "=== Locale ===" && locale | head -1
echo "=== UFW ===" && sudo ufw status | head -5
echo "=== Fail2ban ===" && sudo fail2ban-client status sshd 2>/dev/null || echo "not running"
echo "=== SSH config ===" && grep -E "PermitRootLogin|PasswordAuthentication" /etc/ssh/sshd_config
echo "=== Swap ===" && swapon --show
echo "=== Memory ===" && free -h | head -2
echo "=== Disk ===" && df -h / | tail -1
echo "=== Linger ===" && loginctl show-user nero 2>/dev/null | grep Linger
```

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [secrets-management](../secrets-management/) | Set up .env after bootstrap |
| [swap-memory-management](../swap-memory-management/) | Configure swap during bootstrap |
| [direnv-mise-versions](../direnv-mise-versions/) | Install direnv + mise |
| [dotfiles-management](../dotfiles-management/) | Deploy dotfiles after bootstrap |
| [multi-project-hosting](../multi-project-hosting/) | Set up project structure |
