# Firewall Management

Comprehensive firewall configuration methodology for Ubuntu/Debian VPS servers using UFW (Uncomplicated Firewall) and nftables. Covers common rules, rate limiting, Docker integration, and production-ready configurations for solo developers.

## Scope

- UFW installation, configuration, and rule management
- Default policies (deny incoming, allow outgoing)
- Service-specific rules (SSH, HTTP, HTTPS, internal services)
- Rate limiting to mitigate brute-force attacks
- Docker and UFW interaction (the iptables problem)
- Logging and monitoring blocked traffic
- nftables basics (UFW backend on Ubuntu 24.04)
- Network segmentation for Docker containers

## Why This Matters

A VPS on the public internet receives constant automated scanning and attack attempts. Without a firewall:

- Every listening port is accessible to the world
- Internal services (PostgreSQL, Redis, RabbitMQ) are exposed
- Brute-force attacks hit services directly
- Docker bypasses UFW rules by default (major security issue)

## Architecture

Ubuntu 24.04 firewall stack:

```
UFW (user interface)
  -> nftables (backend, replaces iptables)
    -> netfilter (kernel module)
```

UFW stores rules in:

```
/etc/ufw/ufw.conf           # UFW global settings (enabled/disabled, logging)
/etc/ufw/before.rules        # Rules applied before user rules
/etc/ufw/user.rules          # User-defined rules (managed by ufw command)
/etc/ufw/after.rules          # Rules applied after user rules
/etc/default/ufw              # Default policies
```

## Key Concepts

### 1. Default Policies

The foundation of any firewall is deny-by-default:

```bash
sudo ufw default deny incoming    # Block all inbound traffic
sudo ufw default allow outgoing   # Allow all outbound traffic
sudo ufw default deny routed      # Block forwarded traffic (important for Docker)
```

### 2. Common Rules

| Rule | Command | Purpose |
|------|---------|---------|
| SSH (custom port) | `sudo ufw allow 2222/tcp` | SSH access |
| HTTP | `sudo ufw allow 80/tcp` | Web traffic |
| HTTPS | `sudo ufw allow 443/tcp` | Encrypted web traffic |
| Internal only | `sudo ufw allow from 172.16.0.0/12 to any port 5432` | Docker network access to PostgreSQL |
| Rate limit SSH | `sudo ufw limit 2222/tcp` | Max 6 connections in 30 seconds |
| Specific IP | `sudo ufw allow from 1.2.3.4 to any port 2222` | IP whitelist for SSH |
| Delete rule | `sudo ufw delete allow 80/tcp` | Remove a rule |

### 3. UFW Rate Limiting

UFW's built-in rate limiting (`ufw limit`) uses iptables/nftables `recent` module:

- Allows 6 connections within 30 seconds from a single IP
- After 6 connections, blocks additional connections for 30 seconds
- Only applies to new TCP connections (SYN packets)

Limitations:
- Cannot customize the 6/30s threshold (hardcoded in UFW)
- For finer control, use fail2ban or custom nftables rules

### 4. Docker and UFW (The Problem)

**Critical issue:** Docker manipulates iptables/nftables directly, bypassing UFW rules entirely. This means:

- A container with `-p 5432:5432` is accessible from the internet
- UFW rules do NOT apply to Docker-published ports
- This is the most common firewall misconfiguration on Docker hosts

**Solutions:**

**Option A: Bind to localhost only (recommended for single-host)**
```yaml
# docker-compose.yml
services:
  postgres:
    ports:
      - "127.0.0.1:5432:5432"  # Only accessible from localhost
```

**Option B: Use Docker internal network (no published ports)**
```yaml
services:
  postgres:
    # No ports: section — only accessible from Docker network
    networks:
      - internal
```

**Option C: Disable Docker's iptables management**
```json
// /etc/docker/daemon.json
{
  "iptables": false
}
```
Warning: This breaks container-to-internet networking. Requires manual nftables rules for NAT.

**Option D: UFW-Docker (community solution)**
```bash
# Install ufw-docker
sudo wget -O /usr/local/bin/ufw-docker \
  https://github.com/chaifeng/ufw-docker/raw/master/ufw-docker
sudo chmod +x /usr/local/bin/ufw-docker
sudo ufw-docker install

# Allow specific container port
sudo ufw-docker allow container-name 5432/tcp
```

### 5. Logging

UFW logging levels:

| Level | What it logs |
|-------|-------------|
| `off` | No logging |
| `low` | Blocked packets matching default policy |
| `medium` | + invalid packets, new connections |
| `high` | + all packets (rate limited) |
| `full` | Everything (no rate limiting, very verbose) |

```bash
sudo ufw logging low     # Recommended for production
```

Logs go to `/var/log/ufw.log` (via rsyslog) and `journalctl`.

### 6. nftables Direct Rules

For advanced use cases beyond UFW's capabilities:

```bash
# List current nftables rules
sudo nft list ruleset

# Add a custom rule (rate limit ICMP)
sudo nft add rule inet filter input icmp type echo-request limit rate 1/second accept

# Save rules
sudo nft list ruleset > /etc/nftables.conf
```

### 7. IPv6

UFW handles IPv6 automatically when `IPV6=yes` in `/etc/default/ufw` (default on Ubuntu 24.04). Each `ufw allow` command creates both IPv4 and IPv6 rules.

To disable IPv6 rules if not needed:
```bash
# /etc/default/ufw
IPV6=no
```

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Docker bypasses UFW | Internal services exposed to internet | Bind to 127.0.0.1 or use internal networks |
| Enabling UFW without SSH rule | Immediate lockout | Always add SSH rule first |
| Forgetting IPv6 | Services accessible via IPv6 when only IPv4 rules exist | Keep IPV6=yes in UFW config |
| Rate limiting HTTP/HTTPS | Legitimate users blocked | Only rate limit SSH, use nginx for HTTP rate limiting |
| Deleting rules by number after changes | Wrong rule deleted | Use `ufw delete allow <rule>` instead of `ufw delete <number>` |
| Not allowing Docker subnet | Container services break | Allow 172.16.0.0/12 for internal Docker traffic |

## Verification Commands

```bash
# Show all rules with numbers
sudo ufw status numbered

# Show verbose status (policies + rules)
sudo ufw status verbose

# Check nftables rules (backend)
sudo nft list ruleset | head -50

# Test if a port is open from outside
# (from another machine)
nc -zv server-ip 5432

# Check listening ports
sudo ss -tlnp

# Check UFW logs
sudo tail -f /var/log/ufw.log

# Test Docker port exposure
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

## Integration Points

| Component | Integration |
|-----------|------------|
| SSH | Must allow SSH port before enabling UFW |
| Docker | Bind to 127.0.0.1 or use ufw-docker |
| nginx | Allow 80/tcp and 443/tcp |
| fail2ban | Uses nftables backend to add/remove ban rules |
| Cloudflare | Can restrict HTTP to Cloudflare IPs only |
| Hetzner | Cloud firewall provides additional layer |
| WireGuard | Allow VPN port (e.g., 51820/udp) |

## References

- [UFW Manual](https://help.ubuntu.com/community/UFW)
- [Docker and iptables](https://docs.docker.com/network/iptables/)
- [ufw-docker](https://github.com/chaifeng/ufw-docker)
- [nftables wiki](https://wiki.nftables.org/)
- [Cloudflare IP ranges](https://www.cloudflare.com/ips/)
