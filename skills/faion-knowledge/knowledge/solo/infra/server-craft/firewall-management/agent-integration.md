# Agent Integration — Firewall Management

## When to use
- Provisioning a new VPS — set up firewall before any services are installed
- Auditing an existing server for exposed ports (internal DB ports reachable from internet)
- Adding a new service that needs a firewall rule (WireGuard, custom SSH port)
- Diagnosing Docker port exposure bypassing UFW
- Implementing IP allowlisting for SSH access

## When NOT to use
- Managed platforms (Heroku, Railway, Render) — firewall is handled at the platform level
- Pure Cloudflare-proxied traffic where the origin IP is hidden — cloud firewall at Cloudflare is the right layer
- Kubernetes clusters — use NetworkPolicy and cloud provider security groups instead
- Firewall changes are the root cause of an outage — rolling back rules requires console access; agent should not proceed without confirming out-of-band access

## Where it fails / limitations
- Docker bypasses UFW entirely by injecting iptables/nftables rules directly — UFW `deny` rules have no effect on Docker-published ports bound to `0.0.0.0`
- UFW rate limiting (`ufw limit`) uses hardcoded thresholds (6 connections / 30s) — no customization without dropping to raw nftables
- `ufw enable` without first adding the SSH rule causes immediate lockout — there is no recovery without physical console or cloud provider rescue mode
- UFW rule numbers shift when rules are inserted/deleted — deleting by number after a separate rule change removes the wrong rule
- On Ubuntu 24.04, UFW uses nftables as backend but the UFW CLI still shows iptables-style output; some advanced nftables features are invisible through UFW

## Agentic workflow
An agent handles firewall work by reading the current state (`ufw status verbose`), comparing against the required rule set from the server's service inventory, and emitting the minimal set of `ufw` commands to reconcile the difference. Before enabling UFW on a fresh server, the agent must verify the SSH port rule exists. For Docker-related port audit, the agent checks `docker ps --format "table {{.Names}}\t{{.Ports}}"` and cross-references against docker-compose.yml to identify any `0.0.0.0`-bound ports. The agent must never disable UFW or apply `ufw reset` without explicit human confirmation.

### Recommended subagents
- `faion-sdd-executor-agent` — execute server hardening SDD tasks that include firewall rules as a subtask

### Prompt pattern
```
Audit the firewall on this server. Steps:
1. Run `sudo ufw status verbose` and list all rules.
2. Run `docker ps --format "table {{.Names}}\t{{.Ports}}"` and identify any ports bound to 0.0.0.0.
3. Run `sudo ss -tlnp` to list all listening ports.
Report: which ports are internet-accessible that should not be, and what commands fix each issue.
```

```
Add the following rules to UFW without disrupting existing services:
- Allow UDP 51820 (WireGuard)
- Allow from 10.0.0.0/24 to any port 5432 (PostgreSQL from VPN subnet only)
- Rate-limit port 22022/tcp (SSH)
Output the exact commands in safe order.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ufw` | UFW firewall management | `apt install ufw` / [Ubuntu docs](https://help.ubuntu.com/community/UFW) |
| `nft` | Direct nftables rule management | `apt install nftables` / [nftables wiki](https://wiki.nftables.org/) |
| `ss` | Socket statistics (listening ports) | Built-in (iproute2) |
| `nc` / `ncat` | Port reachability test from another host | `apt install netcat-openbsd` |
| `ufw-docker` | Community tool to integrate UFW with Docker | [GitHub](https://github.com/chaifeng/ufw-docker) |
| `iptables-legacy` | Legacy iptables (if nftables compatibility needed) | `apt install iptables` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hetzner Cloud Firewall | SaaS | Yes | REST API; provides an additional layer before traffic reaches the host; does not solve Docker bypass issue |
| Cloudflare | SaaS | Yes | Can restrict HTTP/HTTPS to Cloudflare IP ranges only (`set_real_ip_from`) |
| fail2ban | OSS | Yes | Uses nftables backend to dynamically ban IPs; complements UFW rate limiting |
| Netbird / Tailscale | SaaS/OSS | Partial | Zero-trust overlay network; replaces traditional VPN + firewall hole approach for internal access |

## Templates & scripts
See templates.md for complete firewall bootstrap scripts. Key safe-order init sequence:

```bash
#!/usr/bin/env bash
# firewall-init.sh — safe UFW bootstrap
# Run BEFORE enabling UFW on a fresh server.
set -euo pipefail

SSH_PORT=${SSH_PORT:-22022}
WG_PORT=${WG_PORT:-51820}

# Defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default deny routed

# Critical: SSH first — never enable before this
sudo ufw allow "${SSH_PORT}/tcp" comment "SSH"

# Web
sudo ufw allow 80/tcp  comment "HTTP"
sudo ufw allow 443/tcp comment "HTTPS"

# WireGuard (optional)
[ -n "$WG_PORT" ] && sudo ufw allow "${WG_PORT}/udp" comment "WireGuard"

# Enable
sudo ufw --force enable
sudo ufw status verbose
```

## Best practices
- Always add the SSH rule before `ufw enable` — lockout has no agent-accessible recovery
- Use `ufw allow from <ip> to any port <ssh_port>` to restrict SSH to known IPs for maximum security
- Bind all Docker service ports to `127.0.0.1` in docker-compose.yml — this is more reliable than ufw-docker
- Use cloud provider firewall (Hetzner, DigitalOcean) as an outer layer — it blocks traffic before it reaches the host's UFW
- For services that need inter-container communication, use Docker internal networks (no `ports:` section) instead of published ports
- Set `UFW_LOGGING=low` in production to avoid log flood from routine scans
- After any Docker service change, verify `docker ps` shows only localhost-bound ports
- Never delete UFW rules by number in a script — rule numbers shift; always delete by specifying the exact rule

## AI-agent gotchas
- Agent must not run `sudo ufw enable` without first verifying the SSH rule is present — lockout is unrecoverable without console access
- `ufw delete <number>` is dangerous in automated scripts because rule numbers change between runs; agent must use `ufw delete allow <port/proto>` form
- UFW does not protect against Docker port exposure — agent must always check docker-compose.yml port bindings separately
- `ufw reset` wipes all rules including SSH — agent must never run this without explicit human confirmation and out-of-band access confirmation
- When adding rules inside a loop or script, `ufw --force` suppresses interactive prompts but also suppresses the confirmation that rules were added — agent must follow up with `ufw status` to verify
- On hosts with both IPv4 and IPv6, `ufw allow 80/tcp` creates both — if IPv6 should not be exposed, set `IPV6=no` in `/etc/default/ufw` before enabling

## References
- https://help.ubuntu.com/community/UFW
- https://wiki.nftables.org/wiki-nftables/index.php/Main_Page
- https://docs.docker.com/network/iptables/
- https://github.com/chaifeng/ufw-docker
- https://www.cloudflare.com/ips/
- https://docs.hetzner.com/cloud/firewalls/overview/
