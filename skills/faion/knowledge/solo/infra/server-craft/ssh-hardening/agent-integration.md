# Agent Integration — SSH Hardening

## When to use
- Bootstrapping a new VPS — SSH hardening is required before any other service is exposed
- After adding a new user who needs SSH access — `AllowUsers` must be updated and key added
- Auditing an existing server's SSH configuration for compliance with Mozilla SSH guidelines
- Rotating SSH keys (compromised key, new machine, key expiry policy)
- Configuring SSH client `~/.ssh/config` for multi-server workflows with ProxyJump

## When NOT to use
- Servers that already have a vetted, tested sshd config — re-running risks lockout if the test sequence is skipped
- Environments using Tailscale/WireGuard for access where SSH is intentionally behind VPN (hardening is still good practice, but urgency is lower)
- Ephemeral containers or CI runners — SSH hardening overhead is not worth it for short-lived instances

## Where it fails / limitations
- **Lockout risk is high** — disabling password auth before verifying key auth works in a second terminal is the most common failure mode
- Changing the SSH port requires updating the firewall (UFW/nftables) AND fail2ban jail port in the same change set; missing either causes lockout or unmonitored port
- Drop-in config files in `sshd_config.d/` are alphabetically merged — a later file silently overrides earlier settings; conflicts are invisible without `sshd -T`
- `AllowUsers` is a whitelist: adding a new system user without updating `AllowUsers` locks that user out of SSH entirely
- Ubuntu 24.04 uses systemd socket activation for SSH — port changes via `sshd_config` alone do not take effect; requires editing `ssh.socket`

## Agentic workflow
An SSH hardening agent operates in a strict sequence: first verify key-based auth works in a parallel session (human must confirm), then generate the drop-in config file, run `sudo sshd -t` to validate syntax, apply with `systemctl restart ssh`, and verify the connection is still alive by attempting a new login before closing the original session. The agent must not close the current session until login is confirmed working. Port changes require a separate sub-task that first opens the new port in the firewall, then restarts the SSH socket.

### Recommended subagents
- `bash-agent` — generates `sshd_config.d/hardening.conf`, runs `sshd -t`, restarts service, verifies
- `audit-agent` — runs `ssh-audit localhost` and `sudo sshd -T` to report effective configuration

### Prompt pattern
```
Generate a drop-in SSH hardening config for Ubuntu 24.04 with these requirements:
- Port: <port>
- AllowUsers: <user>
- Key-only auth, no passwords, no root login
- Modern crypto: ed25519 KEX + AEAD ciphers only
- MaxAuthTries: 3, LoginGraceTime: 30

Return the file contents for /etc/ssh/sshd_config.d/99-hardening.conf
and the commands to apply it safely (test → restart → verify).
```

```
Audit the effective SSH configuration on this server. Run:
1. sudo sshd -T | grep -E "passwordauthentication|permitrootlogin|maxauthtries|allowusers|kexalgorithms|ciphers"
2. ssh-audit localhost (if installed)
Report any settings that deviate from Mozilla SSH guidelines and propose the exact drop-in config lines to fix them.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sshd -t` | Validate sshd config syntax | built-in OpenSSH |
| `sshd -T` | Show effective (merged) sshd configuration | built-in OpenSSH |
| `ssh -Q kex/cipher/mac` | List supported algorithm sets | built-in OpenSSH |
| `ssh-audit` | Comprehensive SSH server audit (KEX, host keys, ciphers) | `pip install ssh-audit` / [github.com/jtesta/ssh-audit](https://github.com/jtesta/ssh-audit) |
| `ssh-keygen -t ed25519` | Generate ed25519 keypair | built-in OpenSSH |
| `systemctl edit ssh.socket` | Change SSH port via socket activation (Ubuntu 24.04) | built-in systemd |
| `journalctl -u ssh` | Read SSH daemon logs | built-in systemd |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| 1Password CLI (`op`) | SaaS | Yes — `op read` | Retrieve SSH private keys and passphrases stored in vault |
| Tailscale | SaaS | Yes — `tailscale status` | VPN layer; SSH behind Tailscale reduces exposure dramatically |
| Shodan | SaaS | Yes — API | Verify what SSH fingerprints are publicly visible after hardening |
| fail2ban | OSS | Yes — `fail2ban-client` | Must update jail port to match SSH port change |

## Templates & scripts
See `templates.md` for the full drop-in config and `~/.ssh/config` template.

Safe port-change sequence (inline, 20 lines):
```bash
#!/bin/bash
# change-ssh-port.sh NEW_PORT
# Run this BEFORE modifying sshd_config; do NOT close current session until verified.
set -euo pipefail
NEW_PORT="${1:?Usage: $0 NEW_PORT}"

# 1. Open new port in firewall FIRST
sudo ufw allow "${NEW_PORT}/tcp" comment "SSH new port"

# 2. Create socket override for new port
sudo mkdir -p /etc/systemd/system/ssh.socket.d
cat <<EOF | sudo tee /etc/systemd/system/ssh.socket.d/port.conf
[Socket]
ListenStream=
ListenStream=${NEW_PORT}
EOF

# 3. Reload and restart socket
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket

echo "SSH is now on port ${NEW_PORT}. Test login in a NEW terminal before closing this session."
echo "After confirming: sudo ufw delete allow 22/tcp"
```

## Best practices
- Always test the new sshd config syntax with `sshd -t` before restarting the daemon — a broken config locks everyone out
- Keep a separate terminal session open with an active SSH connection while making changes; only close it after confirming the new config works
- Use `sshd_config.d/` drop-in files rather than editing `sshd_config` directly — survives package upgrades and is easier to audit
- Remove weak host keys (`ssh_host_rsa_key`, `ssh_host_ecdsa_key`) and keep only `ssh_host_ed25519_key` to eliminate fingerprint confusion
- Store `authorized_keys` entries with comments indicating key source (`user@machine date`) for future audit
- Use `ProxyJump` instead of agent forwarding for multi-hop SSH — no key material touches intermediate hosts
- After port change: update fail2ban jail port, monitoring alerts, and any `~/.ssh/config` entries on client machines

## AI-agent gotchas
- **Hard human-in-loop checkpoint before restart:** An agent must never restart sshd without operator confirmation that a working backup session is open. This is a lockout-risk operation — the operator must explicitly acknowledge
- **`sshd -t` does not catch all errors:** It validates syntax but not runtime issues (e.g., missing host key file). Always follow with `systemctl status ssh` after restart
- **AllowUsers whitelist is cumulative across drop-in files** — if multiple drop-in files set `AllowUsers`, the last one wins, potentially excluding users set in an earlier file. Agents must consolidate `AllowUsers` into a single drop-in
- **Ubuntu 24.04 port change via `sshd_config` alone does NOT work** — the socket activation overrides `Port` in `sshd_config`. Agents that only edit `sshd_config` will find the old port still active
- **`ssh-audit` identifies weak algorithms** — agents running it must filter for actionable items (WARN/FAIL) rather than treating all INFO lines as problems

## References
- [OpenSSH sshd_config manual](https://man.openbsd.org/sshd_config)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
- [ssh-audit tool](https://github.com/jtesta/ssh-audit)
- [Secure Secure Shell (Stribika)](https://stribika.github.io/2015/01/04/secure-secure-shell.html)
- [Ubuntu 24.04 SSH socket activation](https://ubuntu.com/server/docs/service-openssh)
