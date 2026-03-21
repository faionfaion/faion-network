# Firewall Management Examples

Real-world firewall configurations based on production Hetzner VPS running NERO AI platform.

## Example 1: NERO Production Server (Current Setup)

**Server:** Ubuntu 24.04, Hetzner CX53
**Services:** nginx (80/443), SSH (2222), Docker (PostgreSQL, Redis, RabbitMQ)
**External access:** Cloudflare-proxied domains

### Current UFW Rules

```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)

To                         Action      From
--                         ------      ----
2222/tcp                   ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
3333                       ALLOW IN    172.16.0.0/12
2222/tcp (v6)              ALLOW IN    Anywhere (v6)
80/tcp (v6)                ALLOW IN    Anywhere (v6)
443/tcp (v6)               ALLOW IN    Anywhere (v6)
```

### Docker Port Bindings

```yaml
# ~/workspace/repos/nero-infra/docker-compose.yml
services:
  postgres:
    ports:
      - "127.0.0.1:5432:5432"    # Bound to localhost only
  redis:
    ports:
      - "127.0.0.1:6379:6379"    # Bound to localhost only
  rabbitmq:
    ports:
      - "127.0.0.1:5672:5672"    # AMQP, localhost only
      - "127.0.0.1:15672:15672"  # Management, localhost only
  flower:
    ports:
      - "127.0.0.1:5555:5555"    # Flower UI, localhost only
```

### Port Map

| Port | Service | Binding | UFW Rule | External Access |
|------|---------|---------|----------|----------------|
| 2222 | SSH | 0.0.0.0 | ALLOW | Yes (direct IP) |
| 80 | nginx | 0.0.0.0 | ALLOW | Yes (Cloudflare) |
| 443 | nginx | 0.0.0.0 | ALLOW | Yes (Cloudflare) |
| 5432 | PostgreSQL | 127.0.0.1 | None needed | No |
| 5555 | Flower | 127.0.0.1 | None needed | No |
| 5672 | RabbitMQ | 127.0.0.1 | None needed | No |
| 6379 | Redis | 127.0.0.1 | None needed | No |
| 8100 | nero-channel-web | 127.0.0.1 | None needed | Via nginx /api |
| 8101 | nero-web | 127.0.0.1 | None needed | Via nginx / |
| 15672 | RabbitMQ Mgmt | 127.0.0.1 | None needed | No |

Key insight: Because Docker services bind to 127.0.0.1, no UFW rules are needed for them. They are only accessible from the host itself, and nginx proxies external traffic to them.

## Example 2: Multi-Domain Setup

**Scenario:** Single VPS hosting multiple projects (NERO, MeetingTax, EulaGuard)

```
# All three domains go through Cloudflare to the same server
nero.faion.net    -> Cloudflare -> 168.119.x.x:443 -> nginx -> 127.0.0.1:8100/8101
meetingtax.io     -> Cloudflare -> 168.119.x.x:443 -> nginx -> 127.0.0.1:8000/3000
eulaguard.com     -> Cloudflare -> 168.119.x.x:443 -> nginx -> 127.0.0.1:8001
```

### UFW Rules for Multi-Domain

```bash
# Same simple rules — nginx handles routing per domain
sudo ufw limit 2222/tcp comment "SSH"
sudo ufw allow 80/tcp comment "HTTP (all domains)"
sudo ufw allow 443/tcp comment "HTTPS (all domains)"

# No per-domain UFW rules needed — nginx server_name handles routing
# Internal ports (8000, 8001, 8100, 8101, 3000) bind to 127.0.0.1
```

### nginx Handles the Routing

```
nero.faion.net     -> /api/* -> 127.0.0.1:8100
                      /ws    -> 127.0.0.1:8100
                      /      -> 127.0.0.1:8101

meetingtax.io      -> /      -> /var/www/meetingtax (static)
app.meetingtax.io  -> /api/* -> 127.0.0.1:8000
                      /      -> 127.0.0.1:3000

eulaguard.com      -> /api/* -> 127.0.0.1:8001
                      /      -> /var/www/eulaguard (static)
```

## Example 3: Debugging Docker Port Exposure

**Problem:** RabbitMQ Management UI (port 15672) was accessible from the internet despite UFW.

**Discovery:**
```bash
# Check what Docker is doing
$ sudo ss -tlnp | grep 15672
LISTEN  0  4096  0.0.0.0:15672  0.0.0.0:*  users:(("docker-proxy",pid=1234,fd=4))

# Docker-proxy is listening on 0.0.0.0 — exposed to internet!
# UFW cannot block this because Docker adds iptables rules directly.
```

**Root cause:** `docker-compose.yml` had:
```yaml
ports:
  - "15672:15672"    # Binds to 0.0.0.0 by default
```

**Fix:**
```yaml
ports:
  - "127.0.0.1:15672:15672"    # Binds to localhost only
```

**Verification after fix:**
```bash
$ sudo ss -tlnp | grep 15672
LISTEN  0  4096  127.0.0.1:15672  0.0.0.0:*  users:(("docker-proxy",pid=5678,fd=4))

# Now only accessible from localhost
# Access via SSH tunnel: ssh -L 15672:127.0.0.1:15672 nero@server
```

## Example 4: SSH Tunnel for Internal Services

Since internal services bind to 127.0.0.1, access them via SSH tunnels:

```bash
# Access RabbitMQ Management UI
ssh -p 2222 -L 15672:127.0.0.1:15672 nero@168.119.x.x
# Then open http://localhost:15672 in browser

# Access Flower (Celery monitor)
ssh -p 2222 -L 5555:127.0.0.1:5555 nero@168.119.x.x
# Then open http://localhost:5555 in browser

# Access PostgreSQL
ssh -p 2222 -L 5432:127.0.0.1:5432 nero@168.119.x.x
# Then: psql -h localhost -U nero_user nero_db

# Multiple tunnels in one command
ssh -p 2222 \
  -L 15672:127.0.0.1:15672 \
  -L 5555:127.0.0.1:5555 \
  -L 5432:127.0.0.1:5432 \
  nero@168.119.x.x
```

## Example 5: Blocked Traffic Analysis

```bash
# Top 10 blocked source IPs in last 24 hours
$ sudo journalctl -k --since "24 hours ago" | grep "UFW BLOCK" | \
    grep -oP 'SRC=\K[^ ]+' | sort | uniq -c | sort -rn | head -10

    847 185.224.128.xxx    # Known scanner
    312 45.148.10.xxx      # SSH brute-force
    156 194.169.175.xxx    # Port scanner
     89 92.118.39.xxx      # Web scanner
     45 64.62.197.xxx      # Shodan
     23 71.6.199.xxx       # Censys
     12 162.142.125.xxx    # Censys
      8 198.235.24.xxx     # Unknown
      5 167.94.138.xxx     # Censys
      3 45.79.181.xxx      # Unknown

# Most targeted blocked ports
$ sudo journalctl -k --since "24 hours ago" | grep "UFW BLOCK" | \
    grep -oP 'DPT=\K[^ ]+' | sort | uniq -c | sort -rn | head -10

    523 23      # Telnet
    312 22      # SSH (old port, now blocked)
    189 3389    # RDP
    145 445     # SMB
     89 8080    # HTTP alt
     67 3306    # MySQL
     45 1433    # MSSQL
     34 8443    # HTTPS alt
     23 5900    # VNC
     12 27017   # MongoDB
```

## Example 6: Emergency Lockout Recovery

**Scenario:** Accidentally locked out of SSH by misconfiguring UFW.

### Recovery via Hetzner Cloud Console

1. Go to https://console.hetzner.cloud
2. Select your server
3. Click "Console" (opens VNC session)
4. Log in with your username and password (or root if set)
5. Disable UFW:
   ```bash
   sudo ufw disable
   ```
6. Fix the rules:
   ```bash
   sudo ufw allow 2222/tcp
   sudo ufw enable
   ```
7. Verify:
   ```bash
   sudo ufw status
   ```
8. Test SSH from your machine

### Recovery via Hetzner Rescue Mode

If the console login also fails:

1. Hetzner Cloud Console -> "Rescue" tab
2. Enable rescue mode (note the root password)
3. Reboot the server
4. SSH into rescue: `ssh root@server-ip`
5. Mount filesystem:
   ```bash
   mount /dev/sda1 /mnt
   ```
6. Disable UFW:
   ```bash
   chroot /mnt
   ufw disable
   exit
   ```
7. Reboot: `reboot`
8. SSH normally and fix rules
