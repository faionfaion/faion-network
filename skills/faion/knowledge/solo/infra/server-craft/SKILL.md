---
name: faion-server-craft
description: "Server configuration & tuning: SSH hardening, firewall, nginx, systemd, tmux, shell productivity, Docker, backups, agent dev tuning, deploy scripts. 27 methodologies."
tier: solo
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, TaskCreate, TaskUpdate, TaskList, AskUserQuestion, Skill
---

# Server Craft

Server configuration, hardening, tuning, and developer experience for Linux VPS/dedicated servers. Focused on solo developers running AI agent platforms, multi-project hosting, and production workloads on Ubuntu/Debian.

**Entry point:** `/faion-net` (routes here for server/infra/config tasks)

---

## How It Works

1. User describes server task (setup, harden, tune, configure, deploy)
2. Auto-investigate current server state (OS, services, configs)
3. Route to appropriate methodology
4. Execute with copy-paste ready configs and scripts

---

## Context Discovery

### Auto-Investigation

```
Glob: /etc/os-release                    # OS detection
Glob: /etc/ssh/sshd_config               # SSH config
Glob: /etc/nginx/sites-enabled/*         # nginx sites
Glob: /etc/systemd/system/*.service      # system services
Glob: ~/.config/systemd/user/*.service   # user services
Glob: /etc/fail2ban/jail.d/*             # fail2ban jails
Glob: /etc/sysctl.d/*                    # kernel tuning
Grep: "ListenPort" /etc/wireguard/*.conf # WireGuard
Bash: ufw status numbered                # firewall rules
Bash: tmux -V                            # tmux version
Bash: docker ps --format "table"         # running containers
Bash: systemctl --user list-units        # user services
Bash: crontab -l                         # cron jobs
```

### Discovery Questions

- **Q1: What do you want to do?** Setup new server / Harden existing / Tune performance / Configure service / Deploy app / Automate task
- **Q2: What OS/distro?** Ubuntu 24.04 / Debian 12 / Other
- **Q3: What services run?** Web (nginx) / DB (postgres/redis) / Queue (rabbitmq) / Docker / Custom apps
- **Q4: Security level?** Basic (dev) / Production / High-security

---

## Decision Tree

| User Intent | Methodology |
|-------------|-------------|
| "Harden SSH" / "secure SSH" | `ssh-hardening/` |
| "Setup firewall" / "UFW rules" | `firewall-management/` |
| "Tune kernel" / "sysctl" / "BBR" | `kernel-tuning/` |
| "Setup fail2ban" / "ban IPs" | `fail2ban-setup/` |
| "Auto updates" / "unattended upgrades" | `unattended-upgrades/` |
| "tmux config" / "tmux plugins" | `tmux-power-user/` |
| "Shell tools" / "fzf" / "starship" | `shell-productivity/` |
| "Aliases" / "shortcuts" | `bash-aliases/` |
| "nginx" / "reverse proxy" / "proxy_pass" | `nginx-reverse-proxy/` |
| "SSL" / "TLS" / "HTTPS" / "certbot" | `ssl-tls-management/` |
| "VPN" / "WireGuard" | `wireguard-vpn/` |
| "systemd service" / "unit file" | `systemd-user-services/` |
| "Docker Compose" / "container" | `docker-compose-patterns/` |
| "Backup" / "restore" / "disaster" | `backup-recovery/` |
| "Monitoring" / "logs" / "journald" | `monitoring-logging/` |
| "Agent tuning" / "Claude Code" / "inotify" | `agent-dev-tuning/` |
| "Git deploy" / "worktree" | `git-server-workflow/` |
| "Cron" / "scheduled task" / "automation" | `cron-automation/` |
| "Secrets" / ".env" / "1Password" | `secrets-management/` |
| "Swap" / "memory" / "OOM" | `swap-memory-management/` |
| "direnv" / "mise" / "asdf" / "versions" | `direnv-mise-versions/` |
| "New server" / "bootstrap" / "initial setup" | `server-init-bootstrap/` |
| "Multi-domain" / "multi-project" | `multi-project-hosting/` |
| "Deploy script" / "sync to runtime" | `deploy-scripts/` |
| "Health check" / "auto-heal" / "watchdog" | `health-checks-autoheal/` |
| "Dotfiles" / "config management" | `dotfiles-management/` |
| "Claude hooks" / "settings.json" | `claude-code-hooks/` |

### Multi-methodology flows

**"Setup production server from scratch":**
1. `server-init-bootstrap/` (user, SSH keys, basic tools)
2. `ssh-hardening/` (key-only, port change, ed25519)
3. `firewall-management/` (UFW rules)
4. `fail2ban-setup/` (jails)
5. `kernel-tuning/` (BBR, inotify, security)
6. `unattended-upgrades/` (auto security patches)
7. `swap-memory-management/` (swap file)
8. `nginx-reverse-proxy/` (domains)
9. `ssl-tls-management/` (HTTPS)
10. `systemd-user-services/` (app services)
11. `deploy-scripts/` (deployment flow)
12. `monitoring-logging/` (health + logs)
13. `backup-recovery/` (automated backups)

**"Optimize server for AI agent development":**
1. `agent-dev-tuning/` (inotify, swap, OOM, Claude hooks)
2. `tmux-power-user/` (session management)
3. `shell-productivity/` (modern CLI tools)
4. `bash-aliases/` (productivity shortcuts)
5. `claude-code-hooks/` (settings.json automation)

---

## Quick Reference

| Domain | Methodologies | Focus |
|--------|--------------|-------|
| Security | 5 | SSH, firewall, fail2ban, kernel hardening, unattended upgrades |
| Networking | 4 | nginx, SSL/TLS, WireGuard VPN, multi-project hosting |
| Services | 3 | systemd, Docker Compose, health checks |
| Automation | 4 | cron, deploy scripts, git workflow, Claude hooks |
| Developer UX | 4 | tmux, shell tools, aliases, dotfiles |
| Infrastructure | 4 | backup, monitoring, swap/memory, secrets |
| Setup | 3 | bootstrap, direnv/mise, agent tuning |
| **Total** | **27** | |

---

## Execution Pattern

For each methodology:
1. **Audit current state** (read existing configs)
2. **Show diff** (what changes, what stays)
3. **Apply incrementally** (one change at a time)
4. **Verify** (test the change works)
5. **Document** (note what was changed and why)

Always backup before modifying system configs:
```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)
```
