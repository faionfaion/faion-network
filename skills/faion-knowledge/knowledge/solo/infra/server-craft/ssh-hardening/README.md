# SSH Hardening

Comprehensive SSH hardening methodology for Ubuntu/Debian VPS servers. Covers key-only authentication, cryptographic hardening, access control, and client configuration for solo developers managing production infrastructure.

## Scope

- OpenSSH server (`sshd`) configuration hardening
- Key generation and management (ed25519)
- Cryptographic algorithm selection (KEX, ciphers, MACs)
- Access control (AllowUsers, AllowGroups, MaxAuthTries)
- Port change and network-level SSH protection
- Client-side configuration (`~/.ssh/config`)
- SSH agent forwarding and ProxyJump
- Auditing and monitoring SSH access

## Why This Matters

SSH is the primary attack surface on any Linux VPS. Default OpenSSH configurations are permissive for compatibility. A solo developer running an AI agent platform needs:

- **Key-only auth** to eliminate brute-force password attacks entirely
- **ed25519 keys** for modern, fast, secure authentication
- **Port change** to reduce automated scanner noise (not security, but hygiene)
- **Crypto hardening** to prevent downgrade attacks
- **Access control** to limit who can connect and from where

## Architecture

Ubuntu 24.04 uses a drop-in configuration model:

```
/etc/ssh/sshd_config              # Main config (include directive)
/etc/ssh/sshd_config.d/*.conf     # Drop-in overrides (higher priority)
```

Drop-in files in `sshd_config.d/` override values in the main config. This is the recommended approach for custom settings because it survives package upgrades cleanly.

## Key Concepts

### 1. Key-Only Authentication

Disable all password-based authentication methods:

| Setting | Value | Purpose |
|---------|-------|---------|
| `PubkeyAuthentication` | `yes` | Enable SSH key login |
| `PasswordAuthentication` | `no` | Disable password login |
| `ChallengeResponseAuthentication` | `no` | Disable keyboard-interactive |
| `KbdInteractiveAuthentication` | `no` | Same as above (Ubuntu 24.04 name) |
| `UsePAM` | `yes` | Keep PAM for session/account management |

### 2. ed25519 Keys

ed25519 is the recommended key type:

- Shorter keys (256-bit vs RSA 4096-bit) with equivalent security
- Faster key generation and authentication
- Not susceptible to side-channel attacks on older RSA implementations
- Deterministic signatures (no random number dependency)

Generate: `ssh-keygen -t ed25519 -C "user@host"`

### 3. sshd_config Hardening

**Access control:**

| Setting | Recommended | Purpose |
|---------|-------------|---------|
| `PermitRootLogin` | `no` | Never allow direct root SSH |
| `MaxAuthTries` | `3` | Lock out after 3 failed attempts |
| `MaxSessions` | `5` | Limit multiplexed sessions |
| `LoginGraceTime` | `30` | 30 seconds to authenticate |
| `AllowUsers` | `nero` | Whitelist specific users |
| `AllowAgentForwarding` | `no` | Disable unless needed |
| `X11Forwarding` | `no` | Disable X11 (server has no GUI) |
| `PermitTunnel` | `no` | Disable SSH tunneling |

**Crypto hardening (restrict to modern algorithms):**

```
# Key Exchange
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org

# Ciphers (AEAD only)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# MACs (only needed for non-AEAD ciphers, but set for defense in depth)
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
```

### 4. Port Change

Changing the default port from 22 to a non-standard port (e.g., 2222) reduces automated scanner noise by ~99%. It is not a security measure by itself but significantly reduces log noise and fail2ban triggers.

On Ubuntu 24.04 with systemd socket activation:

```bash
# 1. Create socket override
sudo systemctl edit ssh.socket

# 2. Add:
[Socket]
ListenStream=
ListenStream=2222

# 3. Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```

### 5. SSH Agent Forwarding

Agent forwarding allows using local SSH keys on remote servers without copying private keys. Use with caution:

- Only enable for trusted hosts
- Use `ForwardAgent` per-host in `~/.ssh/config`, never globally
- Consider `ProxyJump` as a safer alternative for multi-hop SSH

### 6. ProxyJump (Jump Hosts)

ProxyJump (`-J`) replaces the older ProxyCommand pattern for multi-hop SSH:

```
ssh -J jumphost targethost
```

Or in `~/.ssh/config`:

```
Host target
    ProxyJump jumphost
```

This is more secure than agent forwarding because no key material is exposed on intermediate hosts.

### 7. Host Key Management

Remove weak host keys and keep only ed25519:

```bash
# Remove RSA and ECDSA host keys
sudo rm /etc/ssh/ssh_host_rsa_key* /etc/ssh/ssh_host_ecdsa_key*

# Keep only ed25519
# Add to sshd_config:
HostKey /etc/ssh/ssh_host_ed25519_key
```

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Changing port without updating firewall | Lockout | Always add new port to UFW before changing sshd |
| Disabling password auth without testing key auth | Lockout | Test key auth in a second terminal before disconnecting |
| Forgetting `AllowUsers` when adding new users | New user cannot SSH | Always update `AllowUsers` when adding users |
| Setting `UsePAM no` | Breaks session management | Keep `UsePAM yes` |
| Enabling agent forwarding globally | Key exposure on compromised hosts | Use per-host `ForwardAgent` only |
| Not restarting sshd after config changes | Changes not applied | `sudo systemctl restart ssh` |

## Verification Commands

```bash
# Test sshd config syntax
sudo sshd -t

# Show effective sshd configuration
sudo sshd -T

# Check which algorithms are supported
ssh -Q kex       # Key exchange
ssh -Q cipher    # Ciphers
ssh -Q mac       # MACs
ssh -Q key       # Key types

# Test connection with verbose output
ssh -vvv user@host

# Audit with ssh-audit (install via pip or apt)
ssh-audit localhost

# Check auth log for SSH events
sudo journalctl -u ssh --since "1 hour ago"
```

## Integration Points

| Component | Integration |
|-----------|------------|
| UFW | Must allow new SSH port before changing |
| fail2ban | SSH jail must match the configured port |
| Cloudflare | If using Cloudflare proxy, SSH must bypass it (direct IP) |
| systemd | Ubuntu 24.04 uses socket activation for SSH |
| authorized_keys | Key management, one key per line, comment with source |

## References

- [OpenSSH sshd_config manual](https://man.openbsd.org/sshd_config)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
- [ssh-audit tool](https://github.com/jtesta/ssh-audit)
- [Secure Secure Shell](https://stribika.github.io/2015/01/04/secure-secure-shell.html)
