# SSH Hardening LLM Prompts

Prompts for AI assistants to audit, harden, and troubleshoot SSH configurations.

## Prompt 1: SSH Security Audit

```
Audit the SSH configuration on this Ubuntu server. Perform these checks:

1. Read /etc/ssh/sshd_config and all files in /etc/ssh/sshd_config.d/
2. Check the effective configuration with `sudo sshd -T`
3. Check which host keys exist: `ls -la /etc/ssh/ssh_host_*_key`
4. Check the listening port: `sudo ss -tlnp | grep ssh`
5. Check authorized_keys for all users: `find /home -name authorized_keys -exec echo {} \; -exec cat {} \;`
6. Check recent auth events: `sudo journalctl -u ssh --since "24 hours ago" | grep -cE 'Failed|Invalid|Accepted'`
7. Check if ssh-audit is available and run it

Report findings as a table:

| Check | Current | Recommended | Status |
|-------|---------|-------------|--------|
| Port | ... | Non-standard | OK/WARN |
| Root login | ... | no | OK/WARN |
| Password auth | ... | no | OK/WARN |
| Key types | ... | ed25519 only | OK/WARN |
| Algorithms | ... | Modern only | OK/WARN |
| MaxAuthTries | ... | 3 | OK/WARN |

Provide specific commands to fix any WARN items.
```

## Prompt 2: SSH Hardening Implementation

```
Harden SSH on this Ubuntu 24.04 server. The server runs on Hetzner and uses Cloudflare for DNS.

Current state:
- User: {username}
- Current SSH port: {port}
- Target SSH port: 2222
- Key type in use: {check authorized_keys}

Execute the following safely:

1. First, verify key-based auth works by reading authorized_keys
2. Create a backup of current sshd_config
3. Create /etc/ssh/sshd_config.d/99-hardening.conf with:
   - Port 2222
   - Key-only auth (no passwords)
   - PermitRootLogin no
   - ed25519 host key only
   - Modern crypto algorithms only
   - AllowUsers {username}
   - VERBOSE logging
4. Add port 2222 to UFW BEFORE restarting SSH
5. Configure systemd socket for port 2222
6. Validate config with sshd -t
7. Restart SSH
8. Verify listening on new port

CRITICAL: Do NOT remove the old port from the firewall until the user confirms they can connect on the new port. Provide the test command they should run.
```

## Prompt 3: SSH Troubleshooting

```
I cannot connect to my server via SSH. Help me diagnose the issue.

Error message: {paste the error}
Server: {IP or hostname}
Port: {port}
User: {username}
OS: Ubuntu 24.04

Diagnostic steps to run ON THE SERVER (via console/VNC):
1. `sudo systemctl status ssh` — is SSH running?
2. `sudo ss -tlnp | grep ssh` — what port is it listening on?
3. `sudo sshd -T | grep -E 'port|permit|password|allow'` — effective config
4. `sudo journalctl -u ssh -n 50` — recent SSH logs
5. `sudo ufw status` — is the port allowed?
6. `ls -la /home/{user}/.ssh/` — permissions check
7. `cat /home/{user}/.ssh/authorized_keys` — is the key present?

Diagnostic steps to run ON THE CLIENT:
1. `ssh -vvv -p {port} {user}@{host}` — verbose connection attempt
2. `ssh-add -l` — is the key loaded in agent?
3. `cat ~/.ssh/config` — any conflicting config?

Based on the output, identify the root cause and provide the fix.
```

## Prompt 4: Key Rotation

```
Rotate SSH keys for this server. The goal is to replace the current key with a new ed25519 key without losing access.

Steps:
1. Generate new ed25519 key on the LOCAL machine:
   `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new -C "user@host-YYYY-MM-DD"`

2. Add the NEW public key to server's authorized_keys (while still connected with OLD key):
   `ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@server`

3. Test connection with NEW key (in a separate terminal):
   `ssh -i ~/.ssh/id_ed25519_new user@server`

4. Only after confirming the new key works, remove the OLD key from authorized_keys on the server

5. Update ~/.ssh/config to use the new key file

6. Securely delete the old key:
   `shred -u ~/.ssh/id_ed25519_old`

IMPORTANT: Never remove the old key from authorized_keys until the new key is confirmed working.
```

## Prompt 5: SSH Config Generator

```
Generate an SSH client config (~/.ssh/config) for the following setup:

Servers:
{list servers with: hostname/IP, port, user, purpose}

Requirements:
- Global defaults with modern crypto, keepalive, multiplexing
- Per-host entries with specific keys
- Connection multiplexing (ControlMaster)
- ProxyJump for any servers behind jump hosts
- GitHub/GitLab entries if needed

Output a complete ~/.ssh/config file with comments explaining each section.
Also output the commands to:
1. Create the sockets directory
2. Set correct permissions
3. Test each connection
```

## Prompt 6: Authorized Keys Audit

```
Audit the SSH authorized_keys on this server:

1. Find all authorized_keys files:
   `sudo find / -name authorized_keys -type f 2>/dev/null`

2. For each file, check:
   - File permissions (should be 600)
   - Parent directory permissions (should be 700)
   - Key types (should be ed25519, flag any RSA < 4096 or DSA)
   - Key comments (identify the source of each key)
   - Any command= restrictions
   - Any from= restrictions
   - Total number of keys per user

3. Check for keys in non-standard locations:
   - AuthorizedKeysFile setting in sshd_config
   - Any AuthorizedKeysCommand

4. Report:
   - List of all authorized keys with their type, comment, and any restrictions
   - Recommendations for removing unused keys
   - Recommendations for adding restrictions to service keys
```

## Prompt 7: Hetzner-Specific SSH Setup

```
Configure SSH for a new Hetzner Cloud server. Hetzner-specific considerations:

1. Hetzner provisions with root access and password — need to:
   - Create non-root user with sudo
   - Copy SSH key to new user
   - Disable root login

2. Hetzner Cloud Console is available as fallback if locked out

3. Hetzner firewall (cloud-level) can supplement UFW:
   - Consider adding SSH port rule at Hetzner level too
   - Hetzner firewall is stateful, applied before traffic reaches server

4. Hetzner rescue mode:
   - Available if completely locked out
   - Can mount filesystems and fix SSH config
   - Document rescue mode access procedure

Execute the full setup:
a) Create user, add to sudo group
b) Copy SSH key
c) Test key auth
d) Apply hardening config
e) Update firewall (both UFW and optionally Hetzner)
f) Change port
g) Verify everything works
h) Document rollback procedure using Hetzner console
```

## Prompt 8: SSH Connection Multiplexing Setup

```
Set up SSH connection multiplexing for faster subsequent connections.

1. Create sockets directory:
   `mkdir -p ~/.ssh/sockets`

2. Add to ~/.ssh/config:
   ```
   Host *
       ControlMaster auto
       ControlPath ~/.ssh/sockets/%r@%h-%p
       ControlPersist 600
   ```

3. Test:
   - First connection: `time ssh server "echo connected"` (slow, establishes)
   - Second connection: `time ssh server "echo connected"` (fast, reuses)

4. Manage connections:
   - List: `ssh -O check server`
   - Close: `ssh -O exit server`
   - Forward port on existing: `ssh -O forward -L 8080:localhost:80 server`

5. Verify socket:
   `ls -la ~/.ssh/sockets/`

Note: ControlPersist 600 = keep connection alive 10 minutes after last session closes.
For AI agent workloads, consider increasing to 3600 (1 hour).
```
