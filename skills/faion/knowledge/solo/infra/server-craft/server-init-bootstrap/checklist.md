# Bootstrap New Ubuntu 24.04 Server Checklist

## Phase 1: Access and Users

- [ ] SSH as root: `ssh root@SERVER_IP`
- [ ] Create non-root user: `adduser nero`
- [ ] Add to sudo group: `usermod -aG sudo nero`
- [ ] Create .ssh directory: `mkdir -p /home/nero/.ssh && chmod 700 /home/nero/.ssh`
- [ ] Deploy SSH public key to `authorized_keys`
- [ ] Set permissions: `chmod 600 /home/nero/.ssh/authorized_keys`
- [ ] Set ownership: `chown -R nero:nero /home/nero/.ssh`
- [ ] **TEST** (in separate terminal): `ssh nero@SERVER_IP` works
- [ ] **TEST**: `sudo whoami` returns `root`
- [ ] ONLY THEN: disable root login and password auth

## Phase 2: SSH Hardening

- [ ] Edit `/etc/ssh/sshd_config`:
  - [ ] `PermitRootLogin no`
  - [ ] `PasswordAuthentication no`
  - [ ] `PubkeyAuthentication yes`
  - [ ] `ChallengeResponseAuthentication no`
  - [ ] `X11Forwarding no`
  - [ ] `MaxAuthTries 3`
  - [ ] `ClientAliveInterval 300`
  - [ ] `AllowUsers nero`
- [ ] Test config: `sudo sshd -t` (no errors)
- [ ] Reload SSH: `sudo systemctl reload sshd`
- [ ] **TEST** (in separate terminal): SSH still works with key
- [ ] **TEST**: SSH with password is rejected

## Phase 3: System Identity

- [ ] Set hostname: `sudo hostnamectl set-hostname HOSTNAME`
- [ ] Update /etc/hosts: `127.0.1.1 HOSTNAME`
- [ ] Set timezone: `sudo timedatectl set-timezone Europe/Lisbon`
- [ ] Verify timezone: `timedatectl status`
- [ ] Set locale: `sudo locale-gen en_US.UTF-8`
- [ ] Update locale: `sudo update-locale LANG=en_US.UTF-8`
- [ ] Enable NTP: `sudo timedatectl set-ntp true`

## Phase 4: System Update

- [ ] Update package lists: `sudo apt update`
- [ ] Upgrade all packages: `sudo apt upgrade -y`
- [ ] Remove unused packages: `sudo apt autoremove -y`
- [ ] Reboot if kernel was updated: `sudo reboot`
- [ ] Reconnect after reboot

## Phase 5: Essential Packages

- [ ] Install build tools: `build-essential, curl, wget, git`
- [ ] Install monitoring: `htop, tmux, tree, ncdu, iotop, sysstat, lsof`
- [ ] Install network: `net-tools, dnsutils, rsync`
- [ ] Install utilities: `jq, unzip, zip, strace`
- [ ] Install security: `ca-certificates, gnupg, lsb-release`
- [ ] Install Python dev: `python3-dev, python3-pip, python3-venv`
- [ ] Install C libraries: `libpq-dev, libffi-dev, libssl-dev`

## Phase 6: Firewall

- [ ] Install UFW: `sudo apt install ufw`
- [ ] Set default deny incoming: `sudo ufw default deny incoming`
- [ ] Set default allow outgoing: `sudo ufw default allow outgoing`
- [ ] Allow SSH: `sudo ufw allow 22/tcp`
- [ ] Allow HTTP: `sudo ufw allow 80/tcp`
- [ ] Allow HTTPS: `sudo ufw allow 443/tcp`
- [ ] Enable UFW: `sudo ufw enable`
- [ ] Verify: `sudo ufw status verbose`
- [ ] **TEST**: SSH still works after enabling UFW

## Phase 7: Intrusion Prevention

- [ ] Install fail2ban: `sudo apt install fail2ban`
- [ ] Create local config: `sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local`
- [ ] Configure: bantime=3600, findtime=600, maxretry=3
- [ ] Enable sshd jail
- [ ] Start service: `sudo systemctl enable --now fail2ban`
- [ ] Verify: `sudo fail2ban-client status sshd`

## Phase 8: Automatic Updates

- [ ] Install: `sudo apt install unattended-upgrades`
- [ ] Configure: `sudo dpkg-reconfigure -plow unattended-upgrades`
- [ ] Verify: `cat /etc/apt/apt.conf.d/20auto-upgrades`

## Phase 9: Swap

- [ ] Create swap file (4GB): `sudo fallocate -l 4G /swapfile`
- [ ] Set permissions: `sudo chmod 600 /swapfile`
- [ ] Format: `sudo mkswap /swapfile`
- [ ] Enable: `sudo swapon /swapfile`
- [ ] Add to fstab: `/swapfile none swap sw 0 0`
- [ ] Set swappiness=10 in `/etc/sysctl.d/99-memory.conf`
- [ ] Apply: `sudo sysctl --system`
- [ ] Verify: `free -h` shows swap

## Phase 10: systemd User Services

- [ ] Enable linger: `sudo loginctl enable-linger nero`
- [ ] Verify: `loginctl show-user nero | grep Linger`
- [ ] Create systemd user dir: `mkdir -p ~/.config/systemd/user`
- [ ] Create runtime directory: `sudo mkdir -p /srv/nero && sudo chown nero:nero /srv/nero`

## Phase 11: Logging

- [ ] Set journal max size: `SystemMaxUse=500M` in `/etc/systemd/journald.conf`
- [ ] Restart journald: `sudo systemctl restart systemd-journald`
- [ ] Create logrotate config for application logs

## Phase 12: Runtime Managers (Optional)

- [ ] Install mise: `curl https://mise.run | sh`
- [ ] Install direnv: `sudo apt install direnv`
- [ ] Add shell hooks to .bashrc
- [ ] Install default Python via mise

## Phase 13: Docker (Optional)

- [ ] Install Docker: official APT repository
- [ ] Add user to docker group: `sudo usermod -aG docker nero`
- [ ] Enable Docker: `sudo systemctl enable docker`
- [ ] Verify: `docker run hello-world`
- [ ] Install docker-compose-plugin

## Phase 14: Verification

- [ ] Hostname correct: `hostname`
- [ ] Timezone correct: `timedatectl | grep "Time zone"`
- [ ] Locale correct: `locale | head -1`
- [ ] UFW active: `sudo ufw status`
- [ ] Fail2ban running: `sudo fail2ban-client status sshd`
- [ ] SSH hardened: `grep PermitRootLogin /etc/ssh/sshd_config`
- [ ] Swap active: `swapon --show`
- [ ] Linger enabled: `loginctl show-user nero | grep Linger`
- [ ] Free disk: `df -h /`
- [ ] Memory: `free -h`

## Post-Bootstrap

- [ ] Deploy dotfiles (if using dotfiles repo)
- [ ] Set up .env file with secrets
- [ ] Install project-specific dependencies
- [ ] Set up nginx (if multi-domain hosting)
- [ ] Deploy application services
- [ ] Set up health monitoring
