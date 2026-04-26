# Agent Integration — Server Init Bootstrap

## When to use
- Provisioning a new Hetzner/DigitalOcean/Linode VPS for the first time
- Rebuilding a server from scratch after data loss or major failure
- Automating fleet provisioning via cloud-init or Ansible
- Documenting server setup for reproducibility across team or future rebuilds
- Creating a bootstrap script that a CI/CD pipeline runs post-provisioning

## When NOT to use
- Server is already running and needs only incremental changes (use individual methodology files)
- Managed hosting where SSH root access is unavailable
- Container-only environments (Docker, Kubernetes) where OS-level setup is irrelevant
- Windows servers

## Where it fails / limitations
- Bootstrap script failures mid-run leave server in a partially configured state; idempotency must be explicitly designed in
- cloud-init runs as root and may conflict with manual post-bootstrap steps
- UFW enable on a remote session without first allowing SSH port = permanent lockout
- Changing SSH port without updating fail2ban `port =` and UFW rule breaks fail2ban protection
- unattended-upgrades can restart services unexpectedly; kernel upgrades require manual reboot

## Agentic workflow
An agent can drive the full bootstrap sequence by SSH-ing to the new server and executing each phase as a sub-step. The critical human-in-loop checkpoint is before disabling root login — the agent must confirm the new user can sudo before locking out root. Generating a bootstrap script and running it idempotently is safer than running steps individually, because it allows re-runs on failure.

### Recommended subagents
- `faion-sdd-executor-agent` — execute bootstrap as an SDD task with phase gates
- `nero-sdd-executor-agent` — same pattern for NERO platform provisioning

### Prompt pattern
```
You are provisioning a new Hetzner CX53 Ubuntu 24.04 server.
Root IP: <ip>, root password: <pass>.
Follow the server-init-bootstrap methodology, Phase 1→5.
STOP before disabling root SSH and ask for confirmation that new user login works.
Output each completed phase as "PHASE N DONE".
```

```
Generate an idempotent bootstrap.sh script for Ubuntu 24.04 that:
- Creates user 'faion', deploys SSH key, disables root/password SSH
- Sets hostname, timezone Europe/Lisbon, locale en_US.UTF-8
- Installs: ufw, fail2ban, unattended-upgrades, docker, tmux, htop, jq, git
- Configures UFW: deny-in, allow-out, allow 22022/tcp, 80/tcp, 443/tcp
- Enables systemd linger for user faion
- Is safe to re-run
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ssh-copy-id` | Deploy public key to remote host | Built-in OpenSSH |
| `hostnamectl` | Set hostname | Built-in systemd |
| `timedatectl` | Set timezone and NTP | Built-in systemd |
| `ufw` | Uncomplicated Firewall | `apt install ufw` |
| `fail2ban-client` | Query/manage fail2ban | `apt install fail2ban` |
| `loginctl` | Manage user sessions (linger) | Built-in systemd |
| `sshd -t` | Test SSH config syntax before reload | Built-in OpenSSH |
| `unattended-upgrades` | Automatic security updates | `apt install unattended-upgrades` |
| `mise` | Runtime version manager | `curl https://mise.run \| sh` |
| `cloud-init` | First-boot automation | Pre-installed on cloud images |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hetzner Cloud | SaaS | Yes (API + CLI `hcloud`) | Create server, attach key, get IP |
| DigitalOcean | SaaS | Yes (API + `doctl`) | Droplets, user-data for cloud-init |
| Linode/Akamai | SaaS | Yes (API + `linode-cli`) | Linodes, StackScripts for bootstrap |
| cloud-init | OSS | Yes | Vendor-neutral first-boot YAML config |
| Ansible | OSS | Yes | Idempotent playbooks for full bootstrap |
| Terraform | OSS | Yes | Provision + configure in one pipeline |

## Templates & scripts
See `templates.md` for full bootstrap.sh template.

Key inline pattern — post-bootstrap verification script:
```bash
#!/bin/bash
# run on the server to confirm bootstrap succeeded
set -euo pipefail
errors=0
check() { eval "$2" &>/dev/null && echo "OK   $1" || { echo "FAIL $1"; ((errors++)); }; }
check "non-root user"     "id faion"
check "sudo access"       "sudo -u faion sudo -n true"
check "SSH key deployed"  "test -f /home/faion/.ssh/authorized_keys"
check "root SSH disabled" "grep -q 'PermitRootLogin no' /etc/ssh/sshd_config"
check "UFW active"        "ufw status | grep -q 'Status: active'"
check "fail2ban running"  "systemctl is-active fail2ban"
check "docker running"    "systemctl is-active docker"
check "NTP synced"        "timedatectl | grep -q 'synchronized: yes'"
echo ""; echo "Bootstrap check: $errors errors"
exit $errors
```

## Best practices
- Always test SSH as new user in a separate terminal before disabling root login
- Run `sudo sshd -t` to validate sshd_config syntax before reloading
- Create `/etc/fail2ban/jail.local` (not editing `jail.conf`) so package upgrades don't overwrite your config
- Set `MaxAuthTries 3` and `AllowUsers <username>` in sshd_config — reduces attack surface significantly
- Enable `loginctl enable-linger` for the app user so systemd user services survive logout
- Keep bootstrap script in the dotfiles or infra repo for reproducibility
- Separate bootstrap phases: access+users → identity → packages → security → services. Gate each phase.
- Test the bootstrap script on a throwaway VPS before running on production

## AI-agent gotchas
- Agent must NOT disable root SSH without first verifying new user can log in and sudo — this creates permanent lockout
- `ufw enable` on an active SSH session without pre-allowing SSH port = immediate disconnection, must be handled before enabling
- cloud-init `runcmd` runs as root; if it fails silently, the server appears provisioned but is not configured
- SSH key deployment via heredoc can fail silently if the key format has trailing spaces or wrong line endings — always verify with `ssh -v`
- Changing SSH port mid-session: update the port in UFW and fail2ban config BEFORE changing sshd_config, then reload both
- `unattended-upgrades` may trigger a kernel upgrade and require reboot; agent should check `needrestart` output post-bootstrap
- Agent should write an idempotent script rather than run steps sequentially, so re-runs on partial failure are safe

## References
- [Ubuntu Server Guide — Initial Server Setup](https://ubuntu.com/server/docs)
- [cloud-init documentation](https://cloudinit.readthedocs.io/)
- [UFW documentation](https://help.ubuntu.com/community/UFW)
- [fail2ban documentation](https://www.fail2ban.org/wiki/index.php/MANUAL_0_8)
- [Hetzner Cloud API](https://docs.hetzner.cloud/)
- [mise — runtime version manager](https://mise.jdx.dev/)
