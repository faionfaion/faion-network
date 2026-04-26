# SSH Hardening

## Summary

OpenSSH server hardening for Ubuntu/Debian VPS: key-only authentication (ed25519), drop-in config via `sshd_config.d/`, modern crypto (curve25519 KEX + AEAD ciphers), port change via systemd socket override, and client `~/.ssh/config` with connection multiplexing. The critical safety rule is: always keep a second terminal session open and test the new connection BEFORE closing the original session.

## Why

Default OpenSSH configs are permissive for compatibility. SSH is the primary public attack surface on any VPS. Key-only auth eliminates brute-force password attacks entirely. ed25519 is faster and more secure than RSA. Drop-in `sshd_config.d/` files survive package upgrades. Ubuntu 24.04 uses systemd socket activation — changing `Port` in `sshd_config` alone does not work; the socket override is required.

## When To Use

- Bootstrapping a new VPS — SSH hardening is required before any other service is exposed
- After adding a new user who needs SSH access — `AllowUsers` must be updated
- Auditing an existing server's SSH config against Mozilla SSH guidelines
- Rotating SSH keys (compromised key, new machine)
- Configuring SSH client for multi-server workflows with ProxyJump

## When NOT To Use

- Servers already behind Tailscale/WireGuard where SSH is not reachable from the public internet (still good practice, but urgency is lower)
- Ephemeral containers or CI runners — hardening overhead not worth it for short-lived instances
- Servers with a vetted existing config — re-running risks lockout if the second-terminal test sequence is skipped

## Content

| File | What's inside |
|------|---------------|
| `content/01-server-hardening.xml` | sshd_config.d drop-in settings: key-only auth, MaxAuthTries, AllowUsers, host keys, crypto algorithms |
| `content/02-port-change.xml` | Safe port change procedure via systemd socket override; UFW order; lockout prevention sequence |
| `content/03-client-config.xml` | ~/.ssh/config structure: global defaults, per-host entries, ProxyJump, connection multiplexing |

## Templates

| File | Purpose |
|------|---------|
| `templates/99-hardening.conf` | Drop-in sshd config for `/etc/ssh/sshd_config.d/` |
| `templates/ssh-client-config` | ~/.ssh/config template with global hardening and host entries |
