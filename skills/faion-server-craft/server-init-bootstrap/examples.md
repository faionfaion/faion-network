# Server Init Bootstrap Examples

## Example 1: Hetzner CX53 Bootstrap

Complete bootstrap of a Hetzner CX53 server (16 CPUs, 30GB RAM, Ubuntu 24.04) for the NERO AI platform.

### Hetzner Console: Create Server

1. Hetzner Cloud Console > Create Server
2. Location: Nuremberg (eu-central)
3. Image: Ubuntu 24.04
4. Type: CX53 (16 vCPU, 30 GB RAM, 320 GB SSD)
5. SSH Key: Add your public key
6. Name: nero-hetzner
7. Create & Buy

Server IP: 203.0.113.50 (example)

### First Login and Bootstrap

```bash
# From workstation
$ ssh root@203.0.113.50

# Run bootstrap script
root@nero-hetzner:~# bash bootstrap.sh nero "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@workstation" nero-hetzner Europe/Lisbon

============================================================
Server Bootstrap: Ubuntu 24.04
User: nero
Hostname: nero-hetzner
Timezone: Europe/Lisbon
============================================================

=== Phase 1: System Identity ===
Hostname: nero-hetzner
Timezone: Europe/Lisbon

=== Phase 2: Create User ===
User nero created
SSH key deployed

=== Phase 3: SSH Hardening ===
SSH hardened (root login disabled, key-only auth)

=== Phase 4: System Update ===
Reading package lists... Done
...
74 packages upgraded, 12 newly installed, 0 to remove.

=== Phase 5: Essential Packages ===
...
Packages installed

=== Phase 6: Firewall ===
Default incoming policy changed to 'deny'
Default outgoing policy changed to 'allow'
Rules updated
Firewall is active and enabled on system startup
UFW enabled

=== Phase 7: Fail2ban ===
Fail2ban configured

=== Phase 8: Automatic Updates ===
Unattended upgrades configured

=== Phase 9: Swap ===
Swap created: 4G

=== Phase 10: systemd User Services ===
User linger enabled

=== Phase 11: Journal ===
Journal limited to 500M

============================================================
Bootstrap Complete!
============================================================
Hostname:   nero-hetzner
Timezone:   Europe/Lisbon
Locale:     LANG=en_US.UTF-8
UFW:        Status: active
Fail2ban:   active
SSH:        PermitRootLogin no
Swap:       4G
Swappiness: 10
Linger:     Linger=yes
Memory:     30Gi total, 1.2Gi used
Disk:       310G total, 4.8G used, 290G free

Next steps:
  1. SSH as nero: ssh nero@203.0.113.50
  2. Install mise: curl https://mise.run | sh
  3. Deploy dotfiles (if any)
  4. Set up project directories
  5. Install Docker (if needed)
```

### Post-Bootstrap: Switch to Non-Root User

```bash
# Test new user access (from workstation)
$ ssh nero@203.0.113.50
nero@nero-hetzner:~$

# Verify sudo
$ sudo whoami
root

# Root login is now blocked
$ ssh root@203.0.113.50
Permission denied (publickey).
```

### Post-Bootstrap: Install Docker

```bash
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list
$ sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
$ sudo usermod -aG docker nero

# Re-login to pick up docker group
$ exit
$ ssh nero@203.0.113.50

$ docker run hello-world
Hello from Docker!
```

### Post-Bootstrap: Install mise + direnv

```bash
$ curl https://mise.run | sh
$ echo 'eval "$(mise activate bash)"' >> ~/.bashrc
$ sudo apt install -y direnv
$ echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
$ source ~/.bashrc

$ mise install python@3.12.8
$ mise use --global python@3.12.8

$ python --version
Python 3.12.8
```

## Example 2: Cloud-Init Automated Provisioning

Using cloud-init to fully automate server setup at Hetzner.

### Hetzner Cloud: Create with Cloud Config

1. Hetzner Console > Create Server
2. At the bottom: "Cloud config" checkbox
3. Paste the cloud-init.yml content

### What Cloud-Init Does Automatically

```
Boot #1:
  1. Creates user "nero" with sudo + docker groups
  2. Deploys SSH key
  3. Updates all packages
  4. Installs 30+ packages (build-essential, git, Python, etc.)
  5. Creates 4GB swap
  6. Hardens SSH (disables root, password auth)
  7. Configures UFW (allows 22, 80, 443)
  8. Sets up fail2ban
  9. Tunes vm.swappiness=10
  10. Enables systemd linger for user services
  11. Creates /srv/nero/ directory
  12. Sets timezone to Europe/Lisbon
```

### Verify Cloud-Init Status

```bash
$ ssh nero@203.0.113.50

# Check cloud-init completed
$ cloud-init status
status: done

# Check cloud-init log for errors
$ sudo cat /var/log/cloud-init-output.log | tail -20
...
Cloud-init v. 24.1 finished at ...
```

### Run Verification Script

```bash
$ bash verify-bootstrap.sh
=== Server Bootstrap Verification ===

[PASS] Hostname is set
[PASS] Timezone is set
[PASS] Locale is UTF-8
[PASS] UFW is active
[PASS] Fail2ban is running
[PASS] Root login disabled
[PASS] Password auth disabled
[PASS] Swap is active
[PASS] Swappiness is 10
[PASS] Linger enabled
[PASS] systemd user dir exists
[PASS] Git installed
[PASS] Python3 installed
[PASS] pip3 installed
[PASS] tmux installed
[PASS] htop installed
[PASS] jq installed
[PASS] rsync installed
[PASS] direnv installed
[PASS] stow installed

=== Results: 20 passed, 0 failed ===
All checks passed. Server is ready.
```

## Example 3: NERO Platform Directory Setup (Post-Bootstrap)

After bootstrap, set up the NERO platform directory structure.

```bash
# Create workspace
mkdir -p ~/workspace/{repos,deploy,scripts}

# Clone all repositories
cd ~/workspace/repos
for repo in nero-sdk nero-core nero-channel-web nero-channel-tg nero-web nero-infra; do
    git clone git@github.com:faionfaion/$repo.git
done

# Create runtime directories
sudo mkdir -p /srv/nero
sudo chown nero:nero /srv/nero

# Create per-service runtime dirs
for svc in nero-core nero-channel-web nero-channel-tg nero-web nero-infra; do
    mkdir -p /srv/nero/$svc/{src,.venv}
done

# Create .env from example
cp ~/workspace/repos/nero-infra/.env.example ~/workspace/.env
chmod 600 ~/workspace/.env
nano ~/workspace/.env  # Fill in real values

# Symlink .env to runtime
ln -sf ~/workspace/.env /srv/nero/.env

# Create systemd service files
mkdir -p ~/.config/systemd/user
# Copy service files from nero-infra or create them

# Initial deploy
bash ~/workspace/deploy/deploy.sh all --rebuild-venv

# Start infrastructure
cd /srv/nero/nero-infra/src
docker compose up -d

# Verify everything
systemctl --user status 'nero-*'
curl http://127.0.0.1:8100/health
```

### Final Server State

```bash
$ systemctl --user list-units --type=service --state=active
UNIT                      LOAD   ACTIVE SUB     DESCRIPTION
nero-core.service         loaded active running NERO Core (Celery Workers)
nero-channel-web.service  loaded active running NERO Channel Web (FastAPI)
nero-channel-tg.service   loaded active running NERO Channel Telegram
nero-web.service          loaded active running NERO Web (React SPA)

$ docker ps --format "table {{.Names}}\t{{.Status}}"
NAMES            STATUS
nero-postgres    Up 2 hours (healthy)
nero-redis       Up 2 hours (healthy)
nero-rabbitmq    Up 2 hours (healthy)
nero-flower      Up 2 hours

$ free -h
               total        used        free      shared  buff/cache   available
Mem:            30Gi       6.5Gi        20Gi       128Mi       3.5Gi        23Gi
Swap:          4.0Gi          0B       4.0Gi

$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       310G   12G  283G   5% /
```
