# fail2ban Templates

Copy-paste ready fail2ban configurations for Ubuntu 24.04.

## Template 1: jail.local (Global Defaults)

File: `/etc/fail2ban/jail.local`

```ini
# /etc/fail2ban/jail.local
# Global defaults for all jails

[DEFAULT]
# --- Backend ---
# systemd = read from journald (preferred for Ubuntu 24.04)
# auto = auto-detect (fallback)
backend = systemd

# --- Ban Action ---
# nftables for Ubuntu 24.04 (replaces iptables)
banaction = nftables
banaction_allports = nftables[type=allports]

# --- Default Thresholds ---
# Ban for 1 hour after 5 failures in 10 minutes
bantime = 3600
findtime = 600
maxretry = 5

# --- Whitelist ---
# Never ban these IPs
# Include: localhost, Docker networks, your static IP
ignoreip = 127.0.0.1/8
           ::1
           172.16.0.0/12
           10.0.0.0/8

# --- Ban Time Increment ---
# Double ban time for repeat offenders
bantime.increment = true
bantime.rndtime = 600
bantime.maxtime = 604800
bantime.factor = 2
bantime.formula = ban.Time * math.exp(float(ban.Count+1)*banFactor)/math.exp(1*banFactor)

# --- Logging ---
# Log banned IPs for analysis
loglevel = INFO
logtarget = /var/log/fail2ban.log
```

## Template 2: SSH Jail

File: `/etc/fail2ban/jail.d/sshd.conf`

```ini
# /etc/fail2ban/jail.d/sshd.conf
# SSH brute-force protection

[sshd]
enabled  = true
port     = 2222
filter   = sshd[mode=aggressive]
backend  = systemd

# Strict: 3 failures in 10 minutes = 1 hour ban
maxretry = 3
findtime = 600
bantime  = 3600
```

## Template 3: nginx Jails

File: `/etc/fail2ban/jail.d/nginx.conf`

```ini
# /etc/fail2ban/jail.d/nginx.conf
# nginx protection jails

# --- HTTP Auth Failures ---
# Catches 401 errors from nginx basic auth
[nginx-http-auth]
enabled  = true
port     = http,https
filter   = nginx-http-auth
logpath  = /var/log/nginx/error.log
maxretry = 3
findtime = 600
bantime  = 3600

# --- Bot Scanner Detection ---
# Catches 404 errors from scanner bots probing for vulnerabilities
# (wp-login.php, .env, phpmyadmin, etc.)
[nginx-botsearch]
enabled  = true
port     = http,https
filter   = nginx-botsearch
logpath  = /var/log/nginx/access.log
maxretry = 10
findtime = 600
bantime  = 7200

# --- Rate Limit Violations ---
# Catches nginx limit_req zone violations
[nginx-limit-req]
enabled  = true
port     = http,https
filter   = nginx-limit-req
logpath  = /var/log/nginx/error.log
maxretry = 5
findtime = 600
bantime  = 3600

# --- Bad Requests ---
# Catches malformed HTTP requests (400 errors)
[nginx-bad-request]
enabled  = true
port     = http,https
filter   = nginx-bad-request
logpath  = /var/log/nginx/access.log
maxretry = 15
findtime = 600
bantime  = 1800
```

## Template 4: Custom nginx Bad Request Filter

File: `/etc/fail2ban/filter.d/nginx-bad-request.conf`

```ini
# /etc/fail2ban/filter.d/nginx-bad-request.conf
# Match 400 Bad Request responses in nginx access log

[Definition]
failregex = ^<HOST> -.*"(GET|POST|HEAD|PUT|DELETE|PATCH|OPTIONS) .* HTTP/\d\.\d" 400
ignoreregex =
```

## Template 5: Custom Web App Auth Filter

File: `/etc/fail2ban/filter.d/webapp-auth.conf`

```ini
# /etc/fail2ban/filter.d/webapp-auth.conf
# Match authentication failures in web application
# Works with nginx access log in combined format

[Definition]
# Match 401 Unauthorized on login endpoints
failregex = ^<HOST> -.*"POST /api/auth/login.*" 401
            ^<HOST> -.*"POST /api/auth/token.*" 401
            ^<HOST> -.*"POST /login.*" 401

# Don't match legitimate 401s (API key refresh, etc.)
ignoreregex = ^<HOST> -.*"GET /api/auth/refresh.*" 401
```

## Template 6: Recidive Jail (Ban Escalation)

File: `/etc/fail2ban/jail.d/recidive.conf`

```ini
# /etc/fail2ban/jail.d/recidive.conf
# Escalate bans for repeat offenders
# If an IP gets banned 3 times in 24 hours, ban for 1 week on ALL ports

[recidive]
enabled  = true
filter   = recidive
logpath  = /var/log/fail2ban.log
bantime  = 604800
findtime = 86400
maxretry = 3
banaction = nftables[type=allports]
```

## Template 7: RabbitMQ Management UI Jail

File: `/etc/fail2ban/jail.d/rabbitmq.conf`

```ini
# /etc/fail2ban/jail.d/rabbitmq.conf
# Protect RabbitMQ Management UI from brute-force
# Only needed if management UI is exposed (not recommended)

[rabbitmq-management]
enabled  = false
port     = 15672
filter   = rabbitmq-management
logpath  = /var/log/rabbitmq/rabbit@*.log
maxretry = 3
findtime = 600
bantime  = 3600
```

File: `/etc/fail2ban/filter.d/rabbitmq-management.conf`

```ini
# /etc/fail2ban/filter.d/rabbitmq-management.conf
[Definition]
failregex = ^.*HTTP access denied: user .* - Not management user.*<HOST>
ignoreregex =
```

## Template 8: fail2ban Status Report Script

```bash
#!/bin/bash
# /usr/local/bin/f2b-report
# Generate fail2ban status report

set -euo pipefail

echo "=========================================="
echo "  fail2ban Status Report"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# Overall status
echo "--- Service Status ---"
sudo systemctl is-active fail2ban && echo "Running" || echo "STOPPED"
echo ""

# Jail summary
echo "--- Jail Summary ---"
printf "%-25s %-15s %-15s %-10s\n" "Jail" "Currently" "Total" "Status"
printf "%-25s %-15s %-15s %-10s\n" "----" "---------" "-----" "------"

for jail in $(sudo fail2ban-client status 2>/dev/null | grep "Jail list" | sed 's/.*://;s/,//g'); do
    STATUS=$(sudo fail2ban-client status "$jail" 2>/dev/null)
    CURRENT=$(echo "$STATUS" | grep "Currently banned" | awk '{print $NF}')
    TOTAL=$(echo "$STATUS" | grep "Total banned" | awk '{print $NF}')
    FAILED=$(echo "$STATUS" | grep "Currently failed" | awk '{print $NF}')
    printf "%-25s %-15s %-15s %-10s\n" "$jail" "$CURRENT banned" "$TOTAL total" "$FAILED failed"
done

echo ""

# Currently banned IPs
echo "--- Currently Banned IPs ---"
for jail in $(sudo fail2ban-client status 2>/dev/null | grep "Jail list" | sed 's/.*://;s/,//g'); do
    BANNED=$(sudo fail2ban-client status "$jail" 2>/dev/null | grep "Banned IP list" | sed 's/.*://')
    if [ -n "$(echo "$BANNED" | tr -d ' ')" ]; then
        echo "  $jail: $BANNED"
    fi
done

echo ""

# Recent bans (last 24h)
echo "--- Recent Bans (24h) ---"
if [ -f /var/log/fail2ban.log ]; then
    YESTERDAY=$(date -d "24 hours ago" '+%Y-%m-%d %H:%M:%S')
    grep "Ban " /var/log/fail2ban.log | awk -v d="$YESTERDAY" '$0 > d' | tail -20
else
    echo "(no log file)"
fi

echo ""

# Top banned IPs (all time)
echo "--- Top Banned IPs (all time) ---"
if [ -f /var/log/fail2ban.log ]; then
    grep "Ban " /var/log/fail2ban.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head -10
else
    echo "(no log file)"
fi
```

## Template 9: Slack Notification Action

File: `/etc/fail2ban/action.d/slack-notify.conf`

```ini
# /etc/fail2ban/action.d/slack-notify.conf
# Send Slack notification on ban/unban

[Definition]
actionban = curl -s -X POST -H 'Content-type: application/json' \
    --data '{"text":"[fail2ban] <name> BANNED <ip> (%(bantime)s seconds)"}' \
    <slack_webhook_url>

actionunban = curl -s -X POST -H 'Content-type: application/json' \
    --data '{"text":"[fail2ban] <name> UNBANNED <ip>"}' \
    <slack_webhook_url>

[Init]
slack_webhook_url = https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

Usage in jail config:
```ini
[sshd]
enabled = true
action = nftables
         slack-notify[slack_webhook_url="https://hooks.slack.com/services/..."]
```
