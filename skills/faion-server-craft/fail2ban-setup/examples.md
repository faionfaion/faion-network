# fail2ban Examples

Real-world fail2ban configurations for Hetzner CX53 running NERO AI platform.

## Example 1: NERO Production Setup

**Server:** Ubuntu 24.04, SSH on port 2222, nginx on 80/443
**Services protected:** SSH, nginx (3 jails)

### Current Configuration

```
/etc/fail2ban/jail.d/
  defaults-debian.conf    # [sshd] enabled=true, nftables backend
```

### Recommended Setup

```bash
# 1. Create jail.local
sudo tee /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
backend = systemd
banaction = nftables
banaction_allports = nftables[type=allports]
bantime = 3600
findtime = 600
maxretry = 5
ignoreip = 127.0.0.1/8 ::1 172.16.0.0/12
EOF

# 2. SSH jail (update existing)
sudo tee /etc/fail2ban/jail.d/defaults-debian.conf << 'EOF'
[DEFAULT]
banaction = nftables
banaction_allports = nftables[type=allports]
backend = systemd

[sshd]
enabled = true
port = 2222
maxretry = 3
findtime = 600
bantime = 3600
EOF

# 3. nginx jails
sudo tee /etc/fail2ban/jail.d/nginx.conf << 'EOF'
[nginx-botsearch]
enabled = true
port = http,https
filter = nginx-botsearch
logpath = /var/log/nginx/access.log
maxretry = 10
findtime = 600
bantime = 7200
backend = auto

[nginx-limit-req]
enabled = true
port = http,https
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 5
findtime = 600
bantime = 3600
backend = auto
EOF

# 4. Recidive
sudo tee /etc/fail2ban/jail.d/recidive.conf << 'EOF'
[recidive]
enabled = true
filter = recidive
logpath = /var/log/fail2ban.log
bantime = 604800
findtime = 86400
maxretry = 3
banaction = nftables[type=allports]
backend = auto
EOF

# 5. Restart
sudo systemctl restart fail2ban
sudo fail2ban-client status
```

### Expected Output

```
$ sudo fail2ban-client status
Status
|- Number of jail:      4
`- Jail list:   nginx-botsearch, nginx-limit-req, recidive, sshd

$ sudo fail2ban-client status sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed: 2
|  |- Total failed:     47
|  `- Journal matches:  _SYSTEMD_UNIT=ssh.service + _COMM=sshd
`- Actions
   |- Currently banned: 1
   |- Total banned:     12
   `- Banned IP list:   185.224.128.xxx
```

## Example 2: Analyzing Ban Activity

### Daily Ban Report

```bash
# Last 24 hours ban activity
$ sudo grep "Ban " /var/log/fail2ban.log | awk '{print $6, $NF}' | tail -20

sshd    185.224.128.71
sshd    45.148.10.93
sshd    194.169.175.36
sshd    92.118.39.54
nginx-botsearch  64.62.197.18
nginx-botsearch  71.6.199.42
sshd    162.142.125.10
nginx-botsearch  167.94.138.55
recidive  185.224.128.71    # Repeat offender, banned on all ports
```

### Top Attackers This Month

```bash
$ sudo grep "Ban " /var/log/fail2ban.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head -10

    47 185.224.128.71     # Persistent SSH scanner
    23 45.148.10.93       # SSH brute-force
    15 194.169.175.36     # Mixed SSH + web scanner
    12 92.118.39.54       # SSH scanner
     8 64.62.197.18       # Web scanner (Shodan)
     6 71.6.199.42        # Web scanner (Censys)
     5 162.142.125.10     # Web scanner (Censys)
     4 167.94.138.55      # Web scanner
     3 198.235.24.66      # SSH scanner
     2 45.79.181.217      # One-off attempt
```

### Jail Effectiveness

```bash
# How many unique IPs banned per jail
$ for jail in sshd nginx-botsearch nginx-limit-req recidive; do
    COUNT=$(sudo grep "Ban.*$jail" /var/log/fail2ban.log 2>/dev/null | awk '{print $NF}' | sort -u | wc -l)
    echo "$jail: $COUNT unique IPs banned"
done

sshd: 23 unique IPs banned
nginx-botsearch: 8 unique IPs banned
nginx-limit-req: 2 unique IPs banned
recidive: 3 unique IPs banned (repeat offenders)
```

## Example 3: Custom Filter for NERO API Auth

**Problem:** Brute-force attempts against NERO web API login endpoint.

### nginx Access Log Pattern

```
185.x.x.x - - [21/Mar/2026:14:23:15 +0000] "POST /api/auth/login HTTP/1.1" 401 27 "-" "python-requests/2.28.0"
185.x.x.x - - [21/Mar/2026:14:23:16 +0000] "POST /api/auth/login HTTP/1.1" 401 27 "-" "python-requests/2.28.0"
185.x.x.x - - [21/Mar/2026:14:23:17 +0000] "POST /api/auth/login HTTP/1.1" 401 27 "-" "python-requests/2.28.0"
```

### Custom Filter

```bash
sudo tee /etc/fail2ban/filter.d/nero-api-auth.conf << 'EOF'
[Definition]
failregex = ^<HOST> -.*"POST /api/auth/login.*" 401
            ^<HOST> -.*"POST /api/auth/token.*" 401
ignoreregex =
datepattern = %%d/%%b/%%Y:%%H:%%M:%%S
EOF
```

### Test the Filter

```bash
$ sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nero-api-auth.conf

Running tests
=============
Results
=======
Failregex: 15 total
|-  #) [# of hits] regular expression
|   1) [15] ^<HOST> -.*"POST /api/auth/login.*" 401
`-
Ignoreregex: 0 total
Date template hits:
|- [# of hits] date format
|  [245] Day/MONTH/Year:Hour:Minute:Second
`-
Lines: 245 lines, 15 ignored, 15 matched, 215 missed
```

### Create the Jail

```bash
sudo tee /etc/fail2ban/jail.d/nero-api.conf << 'EOF'
[nero-api-auth]
enabled = true
port = http,https
filter = nero-api-auth
logpath = /var/log/nginx/access.log
maxretry = 5
findtime = 300
bantime = 1800
backend = auto
EOF

sudo fail2ban-client reload
sudo fail2ban-client status nero-api-auth
```

## Example 4: Ban Time Escalation in Action

### Scenario: Persistent SSH Scanner

```
# First offense: 1 hour ban
2026-03-21 10:15:23 fail2ban.actions [sshd] Ban 185.224.128.71
2026-03-21 11:15:23 fail2ban.actions [sshd] Unban 185.224.128.71

# Second offense (back immediately): 2 hour ban (escalation)
2026-03-21 11:16:45 fail2ban.actions [sshd] Ban 185.224.128.71
2026-03-21 13:16:45 fail2ban.actions [sshd] Unban 185.224.128.71

# Third offense: recidive kicks in, 1 week ban on ALL ports
2026-03-21 13:18:02 fail2ban.actions [sshd] Ban 185.224.128.71
2026-03-21 13:18:03 fail2ban.actions [recidive] Ban 185.224.128.71
```

### nftables Rules After Recidive Ban

```bash
$ sudo nft list ruleset | grep "185.224.128.71"
    ip saddr 185.224.128.71 reject  # f2b-sshd chain
    ip saddr 185.224.128.71 reject  # f2b-recidive chain (all ports)
```

## Example 5: Troubleshooting Common Issues

### Issue: Jail Not Banning Despite Failures

```bash
# 1. Check if jail is enabled
$ sudo fail2ban-client status sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0    # <-- No failures detected!
...

# 2. Check if filter matches the log format
$ sudo fail2ban-regex systemd-journal /etc/fail2ban/filter.d/sshd.conf --print-all-matched
# If no matches: filter regex doesn't match log format

# 3. Check backend
$ sudo fail2ban-client get sshd backend
systemd

# 4. Try the log file directly
$ sudo journalctl -u ssh --since "1 hour ago" | grep -i "failed\|invalid"
# If matches here but fail2ban doesn't see them,
# check the journal filter: _SYSTEMD_UNIT=ssh.service
```

### Issue: Banning Cloudflare IPs (Wrong Client IP)

```bash
# Problem: nginx logs show Cloudflare IP, not real client IP
# 185.x.x.x is a Cloudflare edge server

# Solution: Configure nginx to use real IP from Cloudflare headers
# In /etc/nginx/nginx.conf http block:
set_real_ip_from 103.21.244.0/22;
set_real_ip_from 103.22.200.0/22;
# ... (all Cloudflare ranges)
real_ip_header CF-Connecting-IP;

# After nginx restart, access logs show real client IPs
# fail2ban will then ban the actual attacker, not Cloudflare
```

### Issue: fail2ban Using Too Much Memory

```bash
# Check memory usage
$ ps aux | grep fail2ban | grep -v grep
root  1234  0.5  0.3  234567  98765 ?  Ssl  10:00  0:45 /usr/bin/python3 /usr/bin/fail2ban-server

# If memory is high, reduce dbpurgeage in jail.local
[DEFAULT]
dbpurgeage = 86400     # Purge DB entries older than 1 day (default: 1 day)
```

## Example 6: Verifying nftables Integration

```bash
# List all nftables chains created by fail2ban
$ sudo nft list chains | grep f2b
  chain f2b-sshd {
  chain f2b-nginx-botsearch {
  chain f2b-nginx-limit-req {
  chain f2b-recidive {

# List rules in a specific chain
$ sudo nft list chain inet f2b-table f2b-sshd
table inet f2b-table {
    chain f2b-sshd {
        ip saddr 185.224.128.71 reject
        ip saddr 45.148.10.93 reject
    }
}

# Verify UFW and fail2ban coexist
$ sudo nft list ruleset | wc -l
# Both UFW rules and f2b rules should be present
```
