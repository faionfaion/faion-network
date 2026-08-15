# Server Init Bootstrap

## Summary

**One-sentence:** Generates a 5-phase first-login plan for a fresh Ubuntu 24.04 VPS — access, identity, packages, hardening, services foundation — gated by SSH-key-verified non-root login.

**One-paragraph:** Fresh VPS bootstrap is a sequenced operation: create a non-root user, install your SSH key, verify login as that user, ONLY THEN disable root login and password auth. This methodology pins the 5-phase order, names the verification gate between each phase, and refuses to advance until SSH login as the new user is confirmed. Output: a BootstrapPlan + verify-bootstrap.sh report.

**Ефективно для:**

- Hetzner / DigitalOcean / Linode cx-class boxes minutes after creation.
- Operators who have locked themselves out at least once and want a checklist.
- Cloud-init user-data authoring for repeatable provisioning.
- Audit against an existing server for missing bootstrap steps.

## Applies If (ALL must hold)

- First login to any new VPS (Hetzner, DO, Linode, Vultr).
- Rebuilding a server after a breach or OS reinstall.
- Authoring cloud-init user-data for repeatable provisioning.
- Auditing an existing server against the bootstrap checklist.

## Skip If (ANY kills it)

- Managed platforms (Heroku, Railway, Render) — OS is abstracted.
- Kubernetes nodes — managed by the cluster control plane.
- Live production server already in use — only at initial setup.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VPS IP + root credential | string + ssh key OR password | provider dashboard |
| Operator SSH public key | ed25519 pubkey | operator workstation |
| Target hostname | string | operator naming convention |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| ssh-hardening | Phase 4 hardens sshd; this methodology delegates the exact config. |
| firewall-management | Phase 4 installs UFW; delegates rule set. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-verify-user-login-first, r2-loginctl-linger, r3-fail2ban-before-internet, r4-named-hostname, r5-cloud-init-idempotent | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Server Init Bootstrap artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: disabled-root-without-verify, no-linger-systemd-dies, fail2ban-after-exposure, hostname-default-localhost | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-cloud-init` | sonnet | YAML composition with sequence constraints. |
| `audit-existing-server` | sonnet | Diff live config against the 5-phase checklist. |
| `compose-bootstrap-script` | haiku | Mechanical render from BootstrapPlan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/server-init-bootstrap.json` | BootstrapPlan JSON skeleton (phases + verifications). |
| `templates/server-init-bootstrap.md` | Human-readable audit trail. |
| `templates/bootstrap.sh` | Idempotent bootstrap script — phases 1-5 in order. |
| `templates/cloud-init.yml` | user-data for cloud-init provisioning. |
| `templates/verify-bootstrap.sh` | Post-bootstrap audit script — every gate evaluated. |
| `templates/sshd-hardened.conf` | Drop-in sshd_config.d/ file. |
| `templates/fail2ban-jail.local` | Reference fail2ban jail config. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-server-init-bootstrap.py` | Validate BootstrapPlan JSON against the schema. | Before applying to a live host. |
| `scripts/server-status.sh` | Live host status against the 5-phase rule-set. | Post-bootstrap + weekly cron. |

## Related

- [[ssh-hardening]]
- [[firewall-management]]
- [[fail2ban-setup]]
- [[systemd-user-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/server-init-bootstrap.json`

```json
{
  "artefact_id": "bootstrap-<host>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "hostname": "<host>",
  "operator": "<unix-user>",
  "phases": [
    "access-users",
    "system-identity",
    "packages-tools",
    "security-hardening",
    "services-foundation"
  ],
  "verifications": [
    "ssh-as-operator",
    "loginctl-linger-enabled",
    "ufw-active",
    "fail2ban-active"
  ],
  "owner": "<@handle>"
}
```

### `templates/bootstrap.sh`

```bash
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
```

### `templates/cloud-init.yml`

```yaml
#cloud-config
# cloud-init user-data for Hetzner/DigitalOcean/Linode VPS provisioning
# Replace: NEW_USER, SSH_PUBLIC_KEY, SSH_PORT, HOSTNAME, TIMEZONE

users:
  - name: nero
    groups: sudo
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAAC3... your_key_here

package_update: true
package_upgrade: true
packages:
  - ufw
  - fail2ban
  - unattended-upgrades
  - curl
  - git
  - tmux
  - htop
  - jq
  - rsync
  - direnv
  - python3-dev
  - python3-venv

runcmd:
  - hostnamectl set-hostname server-name
  - timedatectl set-timezone Europe/Lisbon
  - locale-gen en_US.UTF-8
  - update-locale LANG=en_US.UTF-8
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw limit 2222/tcp
  - ufw allow 80/tcp
  - ufw allow 443/tcp
  - ufw --force enable
  - loginctl enable-linger nero
  - dpkg-reconfigure -plow unattended-upgrades
  - systemctl enable fail2ban
  - systemctl start fail2ban
```

### `templates/verify-bootstrap.sh`

```bash
# verify-bootstrap.sh — Post-bootstrap verification checklist
# Run as the non-root user after completing all 5 phases.
set -euo pipefail

USER="${1:-$(whoami)}"
PASS=0
FAIL=0

check() {
    local label="$1" result="$2"
    if [ "$result" = "ok" ]; then
        echo "  [OK]  $label"
        PASS=$(( PASS + 1 ))
    else
        echo "  [FAIL] $label — $result"
        FAIL=$(( FAIL + 1 ))
    fi
}

echo "=============================="
echo "  Bootstrap Verification"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

check "hostname set" "$(hostname | grep -v localhost > /dev/null && echo ok || echo 'still localhost')"
check "timezone set" "$(timedatectl | grep -v 'UTC$' > /dev/null && echo ok || echo 'still UTC')"
check "NTP sync"     "$(timedatectl | grep -q 'synchronized: yes' && echo ok || echo 'not synchronized')"
check "UFW active"   "$(sudo ufw status | grep -q '^Status: active' && echo ok || echo 'inactive')"
check "SSH in UFW"   "$(sudo ufw status | grep -qE 'ALLOW.*2202[0-9]' && echo ok || echo 'no SSH rule')"
check "fail2ban running" "$(systemctl is-active fail2ban 2>/dev/null | grep -q active && echo ok || echo 'not running')"
check "no root SSH"  "$(grep -q 'PermitRootLogin no' /etc/ssh/sshd_config && echo ok || echo 'root login still enabled')"
check "no password auth" "$(grep -q 'PasswordAuthentication no' /etc/ssh/sshd_config && echo ok || echo 'password auth still enabled')"
check "unattended-upgrades" "$(dpkg -l unattended-upgrades 2>/dev/null | grep -q '^ii' && echo ok || echo 'not installed')"
check "linger enabled" "$(loginctl show-user $USER 2>/dev/null | grep -q 'Linger=yes' && echo ok || echo 'linger not enabled')"

echo ""
echo "--- Summary: $PASS passed, $FAIL failed ---"
[ "$FAIL" -eq 0 ] && echo "Bootstrap verified." || echo "Fix failed items before proceeding."
exit "$FAIL"
```

### `templates/sshd-hardened.conf`

```conf
# /etc/ssh/sshd_config — Production hardened SSH configuration
# Test before applying: sudo sshd -t
# Apply: sudo systemctl reload sshd
# CRITICAL: Test SSH in a new terminal before closing existing session

Port                     2222
AddressFamily            inet
ListenAddress            0.0.0.0

# Authentication
PermitRootLogin          no
PasswordAuthentication   no
PubkeyAuthentication     yes
AuthorizedKeysFile       .ssh/authorized_keys
ChallengeResponseAuthentication no
UsePAM                   yes

# Restrict access
AllowUsers               nero
MaxAuthTries             3
MaxSessions              10

# Timeouts
ClientAliveInterval      300
ClientAliveCountMax      2
LoginGraceTime           30

# Security
X11Forwarding            no
PrintMotd                no
AcceptEnv                LANG LC_*
Subsystem                sftp /usr/lib/openssh/sftp-server
```

### `templates/fail2ban-jail.local`

```text
# /etc/fail2ban/jail.local
# Copy from jail.conf: cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
# This file survives package upgrades.

[DEFAULT]
bantime  = 3600    # 1 hour ban
findtime = 600     # 10 minute window
maxretry = 3       # 3 failed attempts

[sshd]
enabled  = true
port     = 2222   # match your SSH port
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
```
