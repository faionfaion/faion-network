# fail2ban Setup

Comprehensive fail2ban configuration methodology for Ubuntu/Debian servers. Covers architecture, jail configuration, custom filters, nftables backend, and multi-service protection for web applications.

## Scope

- fail2ban architecture (jails, filters, actions)
- nftables backend configuration (Ubuntu 24.04 default)
- SSH jail hardening
- nginx jails (botsearch, limit-req, auth failures)
- Custom filter creation for application-specific patterns
- Ban time escalation (recidive jail)
- Whitelisting and ignoring IPs
- Monitoring and log analysis

## Why This Matters

Even with SSH key-only auth and a firewall, servers face:

- Automated SSH brute-force attempts (thousands per day)
- Web scanner bots probing for vulnerabilities
- Authentication brute-force against web applications
- Resource exhaustion from persistent attackers

fail2ban monitors log files and temporarily bans IPs that show malicious behavior, adding a dynamic defense layer.

## Architecture

```
Log files (auth.log, nginx error.log, etc.)
  -> fail2ban-server (daemon)
    -> Filters (regex patterns match log lines)
      -> Jails (combine filter + log + action + thresholds)
        -> Actions (ban/unban via nftables/iptables/sendmail)
```

### Configuration Hierarchy

```
/etc/fail2ban/
  fail2ban.conf            # Daemon settings (log level, socket, PID)
  jail.conf                # Default jail settings (DO NOT EDIT)
  jail.local               # Local overrides for jail.conf
  jail.d/                  # Drop-in jail configs (recommended)
    defaults-debian.conf   # Debian/Ubuntu defaults
  filter.d/                # Filter definitions (regex patterns)
    sshd.conf              # SSH filter
    nginx-botsearch.conf   # nginx bot scanner filter
    ...
  action.d/                # Action definitions (ban/unban commands)
    nftables.conf          # nftables ban action
    sendmail.conf          # Email notification action
    ...
```

**Best practice:** Never edit `jail.conf` or `fail2ban.conf`. Use `jail.local` or drop-in files in `jail.d/`.

### Backend

Ubuntu 24.04 uses systemd journal as the log backend and nftables for banning:

```ini
[DEFAULT]
backend = systemd         # Read logs from systemd journal
banaction = nftables       # Use nftables to ban IPs
banaction_allports = nftables[type=allports]
```

## Key Concepts

### 1. Jails

A jail combines:
- **Filter:** What log patterns to match
- **Log path:** Where to find the logs
- **Max retry:** How many matches before banning
- **Find time:** Time window for counting matches
- **Ban time:** How long to ban

```ini
[sshd]
enabled  = true
port     = 2222
filter   = sshd
backend  = systemd
maxretry = 3
findtime = 600
bantime  = 3600
```

### 2. Filters

Filters are regex patterns that match log lines. Each match counts as a "failure":

```ini
# /etc/fail2ban/filter.d/sshd.conf (simplified)
[Definition]
failregex = ^.*sshd.*: Failed password for .* from <HOST>
            ^.*sshd.*: Invalid user .* from <HOST>
            ^.*sshd.*: Connection closed by authenticating user .* <HOST>
```

`<HOST>` is a special placeholder that captures the IP address.

### 3. Actions

Actions define what happens when an IP is banned/unbanned:

| Action | What It Does |
|--------|-------------|
| `nftables` | Add/remove nftables rules |
| `nftables[type=allports]` | Block all ports, not just the jail's port |
| `sendmail` | Send email notification |
| `slack` | Send Slack notification (custom action) |

### 4. Ban Time Escalation (Recidive)

The recidive jail monitors fail2ban's own log to catch repeat offenders:

```ini
[recidive]
enabled  = true
filter   = recidive
logpath  = /var/log/fail2ban.log
bantime  = 604800    # 1 week
findtime = 86400     # Look back 24 hours
maxretry = 3         # After 3 bans in 24h, ban for 1 week
banaction = nftables[type=allports]
```

### 5. Whitelisting

IPs that should never be banned:

```ini
[DEFAULT]
ignoreip = 127.0.0.1/8 ::1 10.0.0.0/8 172.16.0.0/12
```

Always whitelist:
- Localhost (127.0.0.1)
- Docker networks (172.16.0.0/12)
- Your static IP (if you have one)
- VPN subnet
- Monitoring service IPs

### 6. nginx Jails

Common nginx jails:

| Jail | Matches | Log Source |
|------|---------|------------|
| `nginx-http-auth` | 401 auth failures | error.log |
| `nginx-botsearch` | 404s from scanners | access.log |
| `nginx-limit-req` | Rate limit violations | error.log |
| `nginx-bad-request` | Malformed requests | access.log |

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Not whitelisting your own IP | Lock yourself out | Add to ignoreip |
| Wrong port in jail config | Banning doesn't work | Match jail port to actual service port |
| Missing log path | Jail doesn't start | Verify log file exists |
| systemd backend with non-systemd service | No matches found | Use auto backend or specify logpath |
| Docker containers use different log paths | Jails don't match | Use docker logs or volume-mounted logs |
| Banning Cloudflare IPs | Blocking legitimate users | Whitelist Cloudflare IPs or use X-Forwarded-For |

## Verification Commands

```bash
# Check fail2ban status
sudo fail2ban-client status

# Check specific jail status
sudo fail2ban-client status sshd

# Check banned IPs
sudo fail2ban-client get sshd banip

# Manually ban an IP
sudo fail2ban-client set sshd banip 1.2.3.4

# Manually unban an IP
sudo fail2ban-client set sshd unbanip 1.2.3.4

# Test a filter against a log file
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf

# Check nftables rules created by fail2ban
sudo nft list ruleset | grep -A5 "f2b"

# Check fail2ban log
sudo tail -50 /var/log/fail2ban.log

# Reload fail2ban after config changes
sudo fail2ban-client reload
```

## Integration Points

| Component | Integration |
|-----------|------------|
| SSH | sshd jail with custom port |
| nginx | botsearch, limit-req, http-auth jails |
| UFW | Both use nftables; fail2ban rules coexist with UFW rules |
| Docker | Containers log differently; may need custom log paths |
| Cloudflare | Must whitelist Cloudflare IPs to avoid banning proxy |
| RabbitMQ | Custom jail for management UI auth failures |
| Systemd | Use systemd backend for services logging to journal |

## References

- [fail2ban documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [fail2ban manual](https://manpages.debian.org/testing/fail2ban/jail.conf.5.en.html)
- [fail2ban filters](https://github.com/fail2ban/fail2ban/tree/master/config/filter.d)
