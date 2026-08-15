# SSH Hardening

## Summary

**One-sentence:** Generates a sshd_config drop-in + client config + AllowUsers list — key-only ed25519, modern crypto, second-terminal safety rule — for an Ubuntu/Debian VPS.

**One-paragraph:** Hardening sshd is a controlled risky-edit: drop-in `/etc/ssh/sshd_config.d/99-hardening.conf` with key-only auth, ed25519 host keys, modern KEX/ciphers, and AllowUsers restricted to the operator. The critical safety rule: keep a second terminal session open, reload sshd, test login in a third terminal, and only then close the original. Output: a SshPlan + the drop-in config.

**Ефективно для:**

- Fresh VPS with default sshd open to the internet.
- Adding a new user who needs SSH access — AllowUsers must update.
- Auditing existing sshd against Mozilla SSH guidelines.
- Rotating compromised host or user keys.

## Applies If (ALL must hold)

- Bootstrapping a new VPS — SSH hardening required before any other public service.
- Adding a user who needs SSH access — AllowUsers update.
- Auditing an existing server against Mozilla SSH config.
- Rotating SSH keys after a leak.

## Skip If (ANY kills it)

- Servers behind Tailscale/WireGuard with sshd not reachable from public internet (still good practice; lower urgency).
- Ephemeral containers / CI runners — hardening overhead not worth it.
- Servers with a vetted config — re-running risks lockout if the second-terminal safety sequence is skipped.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operator ed25519 keypair | ssh-keygen -t ed25519 | operator workstation |
| Current sshd_config snapshot | file | /etc/ssh/sshd_config |
| Allowed users list | list of unix users | operator inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| server-init-bootstrap | Hardening runs in phase 4 of bootstrap; this methodology defines the exact config. |
| firewall-management | UFW must allow the chosen SSH port before sshd reload. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-second-terminal-rule, r2-key-only-auth, r3-allowusers-explicit, r4-modern-crypto, r5-drop-in-config | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the SSH Hardening artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: edit-without-second-terminal, password-auth-left-on, root-permit-yes, weak-kex-algorithms | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-sshd-config` | sonnet | Per-host tweaks with safety constraints. |
| `audit-existing-sshd` | sonnet | Diff live config against rules + Mozilla baseline. |
| `render-client-config` | haiku | Template fill for ~/.ssh/config. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ssh-hardening.json` | SshPlan JSON skeleton. |
| `templates/ssh-hardening.md` | Human-readable audit trail + rollback steps. |
| `templates/99-hardening.conf` | Drop-in sshd_config.d/99-hardening.conf (key-only, modern crypto, AllowUsers). |
| `templates/ssh-client-config` | Reference ~/.ssh/config with multiplexing + host alias. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ssh-hardening.py` | Validate SshPlan JSON against the schema. | Before applying drop-in to /etc/ssh/sshd_config.d/. |

## Related

- [[server-init-bootstrap]]
- [[firewall-management]]
- [[fail2ban-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ssh-hardening.json`

```json
{
  "artefact_id": "ssh-<host>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "host": "<host>",
  "port": 2222,
  "allow_users": [
    "<unix-user>"
  ],
  "password_auth": false,
  "permit_root_login": false,
  "second_terminal_verified": false,
  "owner": "<@handle>"
}
```

### `templates/99-hardening.conf`

```conf
# /etc/ssh/sshd_config.d/99-hardening.conf
# SSH Hardening — Production VPS (Ubuntu 24.04)
# Applied on top of default Ubuntu 24.04 sshd_config via drop-in

# --- Network ---
# Port is set via systemd socket override on Ubuntu 24.04
# See /etc/systemd/system/ssh.socket.d/override.conf

# --- Authentication ---
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
MaxAuthTries 3
MaxSessions 10
LoginGraceTime 30

# --- Access Control ---
# Space-separated list of allowed users
AllowUsers nero

# --- Host Keys (ed25519 only) ---
HostKey /etc/ssh/ssh_host_ed25519_key

# --- Cryptographic Hardening ---
# Key Exchange: post-quantum hybrid + curve25519
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org

# Ciphers: AEAD only
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# MACs: encrypt-then-mac only (used as fallback for non-AEAD)
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

### `templates/ssh-client-config`

```text
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

    # Connection multiplexing (reuse connections — speeds up agent tools)
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

    # Crypto (match server hardening)
    KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# --- Host Definitions ---

# Production VPS
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

# Internal host via jump (ProxyJump is safer than ForwardAgent)
Host internal-db
    HostName 10.0.0.5
    User dbadmin
    Port 22
    ProxyJump nero-prod
    IdentityFile ~/.ssh/id_ed25519_internal

# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```
