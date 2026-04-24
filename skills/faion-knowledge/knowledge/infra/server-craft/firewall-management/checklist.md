# Firewall Management Checklist

Step-by-step checklist for setting up UFW on Ubuntu 24.04 from scratch. Designed for a VPS running web applications with Docker.

## Prerequisites

- [ ] Root or sudo access
- [ ] Know which SSH port is configured (check `sshd -T | grep port`)
- [ ] Know which services need public access
- [ ] Have VPS console access as fallback (Hetzner Cloud Console)

## Phase 1: Pre-Flight

- [ ] **Check current firewall status**
  ```bash
  sudo ufw status verbose
  ```
  If active, review existing rules before making changes.

- [ ] **Check listening ports**
  ```bash
  sudo ss -tlnp | sort -t: -k2 -n
  ```
  Document all listening ports and their services.

- [ ] **Check Docker port mappings**
  ```bash
  docker ps --format "table {{.Names}}\t{{.Ports}}" 2>/dev/null
  ```
  Identify any Docker containers with published ports.

## Phase 2: Initial Setup

- [ ] **Install UFW** (usually pre-installed on Ubuntu)
  ```bash
  sudo apt install -y ufw
  ```

- [ ] **Set default policies**
  ```bash
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw default deny routed
  ```
  Verify: `sudo ufw show raw | head -5`

- [ ] **Enable IPv6** (verify)
  ```bash
  grep IPV6 /etc/default/ufw
  # Should show: IPV6=yes
  ```

- [ ] **Add SSH rule FIRST** (critical, prevents lockout)
  ```bash
  sudo ufw allow 2222/tcp comment "SSH"
  ```
  Verify: `sudo ufw status | grep 2222`

- [ ] **Enable UFW**
  ```bash
  sudo ufw enable
  ```
  Verify: `sudo ufw status verbose`

## Phase 3: Service Rules

- [ ] **Allow HTTP/HTTPS** (for nginx)
  ```bash
  sudo ufw allow 80/tcp comment "HTTP"
  sudo ufw allow 443/tcp comment "HTTPS"
  ```

- [ ] **Allow internal Docker subnet** (if services communicate between containers and host)
  ```bash
  sudo ufw allow from 172.16.0.0/12 to any port 5432 comment "PostgreSQL from Docker"
  sudo ufw allow from 172.16.0.0/12 to any port 6379 comment "Redis from Docker"
  sudo ufw allow from 172.16.0.0/12 to any port 5672 comment "RabbitMQ from Docker"
  sudo ufw allow from 172.16.0.0/12 to any port 15672 comment "RabbitMQ Management from Docker"
  ```

- [ ] **Rate limit SSH** (optional, complementary to fail2ban)
  ```bash
  # Replace allow with limit for SSH
  sudo ufw delete allow 2222/tcp
  sudo ufw limit 2222/tcp comment "SSH rate-limited"
  ```

## Phase 4: Docker Security

- [ ] **Audit Docker port bindings**
  ```bash
  docker ps --format '{{.Names}}: {{.Ports}}' | grep '0.0.0.0'
  ```
  Any container binding to `0.0.0.0` is accessible from the internet, bypassing UFW.

- [ ] **Fix Docker port bindings** (bind to 127.0.0.1)
  ```yaml
  # In docker-compose.yml, change:
  # ports: ["5432:5432"]
  # To:
  # ports: ["127.0.0.1:5432:5432"]
  ```

- [ ] **Restart Docker containers**
  ```bash
  docker compose down && docker compose up -d
  ```

- [ ] **Verify Docker ports are local only**
  ```bash
  sudo ss -tlnp | grep -E '5432|6379|5672'
  # Should show 127.0.0.1:port, not 0.0.0.0:port
  ```

## Phase 5: Logging

- [ ] **Enable logging**
  ```bash
  sudo ufw logging low
  ```

- [ ] **Verify log file exists**
  ```bash
  ls -la /var/log/ufw.log
  ```

- [ ] **Test logging works** (from another machine, try connecting to a blocked port)
  ```bash
  # On another machine:
  nc -zv server-ip 9999

  # On server, check log:
  sudo tail -5 /var/log/ufw.log
  ```

## Phase 6: Verification

- [ ] **Review all rules**
  ```bash
  sudo ufw status numbered
  ```

- [ ] **Test SSH access** (from another terminal)
  ```bash
  ssh -p 2222 user@server
  ```

- [ ] **Test web access**
  ```bash
  curl -I http://server-ip
  curl -I https://server-domain
  ```

- [ ] **Test blocked ports** (from another machine)
  ```bash
  nc -zv server-ip 5432    # Should be refused/timeout
  nc -zv server-ip 6379    # Should be refused/timeout
  nc -zv server-ip 15672   # Should be refused/timeout
  ```

- [ ] **Verify Docker services still work internally**
  ```bash
  # On server:
  psql -h 127.0.0.1 -U postgres   # Should connect
  redis-cli -h 127.0.0.1 ping      # Should return PONG
  ```

## Phase 7: Advanced (Optional)

- [ ] **Restrict HTTP to Cloudflare IPs** (if using Cloudflare proxy)
  ```bash
  # Delete open HTTP/HTTPS rules
  sudo ufw delete allow 80/tcp
  sudo ufw delete allow 443/tcp

  # Allow only Cloudflare IPs
  for ip in $(curl -s https://www.cloudflare.com/ips-v4); do
      sudo ufw allow from $ip to any port 80,443 proto tcp comment "Cloudflare"
  done
  ```

- [ ] **Add Hetzner Cloud Firewall** (additional layer)
  - In Hetzner Cloud Console, create a firewall
  - Allow SSH port, HTTP, HTTPS
  - Attach to server

- [ ] **Add WireGuard port** (if using VPN)
  ```bash
  sudo ufw allow 51820/udp comment "WireGuard VPN"
  ```

## Post-Setup Monitoring

- [ ] **Schedule regular firewall review**
  ```bash
  # Add to crontab or periodic check:
  sudo ufw status numbered > /var/log/ufw-rules-$(date +%Y%m%d).log
  ```

- [ ] **Monitor blocked connections**
  ```bash
  sudo journalctl -k | grep "UFW BLOCK" | tail -20
  ```

## Rollback Plan

If locked out:

1. Access via Hetzner Cloud Console (VNC)
2. `sudo ufw disable`
3. Fix rules
4. `sudo ufw enable`

If UFW breaks Docker networking:

1. `sudo ufw disable`
2. `sudo systemctl restart docker`
3. Fix Docker port bindings
4. Re-enable UFW: `sudo ufw enable`
