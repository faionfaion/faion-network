# fail2ban LLM Prompts

Prompts for AI assistants to configure, troubleshoot, and audit fail2ban.

## Prompt 1: fail2ban Audit

```
Audit the fail2ban configuration on this Ubuntu server.

Steps:
1. `sudo systemctl status fail2ban` — service status
2. `sudo fail2ban-client status` — active jails
3. For each jail: `sudo fail2ban-client status <jail>` — ban stats
4. `ls -la /etc/fail2ban/jail.d/` — config files
5. `cat /etc/fail2ban/jail.local` — global settings (if exists)
6. `cat /etc/fail2ban/jail.d/*.conf` — jail configs
7. `sudo grep "ERROR\|WARNING" /var/log/fail2ban.log | tail -10` — errors
8. `sudo nft list ruleset | grep -c f2b` — nftables rules count
9. Check if any important services are NOT protected by fail2ban

Report as:

| Jail | Enabled | Port | MaxRetry | BanTime | Currently Banned | Total Banned |
|------|---------|------|----------|---------|-----------------|-------------|

Also check:
- Is SSH jail protecting the correct port?
- Are nginx jails configured?
- Is recidive (ban escalation) enabled?
- Are important IPs whitelisted (localhost, Docker networks)?
- Are there any errors in fail2ban log?

Provide recommendations for missing protections.
```

## Prompt 2: fail2ban Setup from Scratch

```
Set up fail2ban on this Ubuntu 24.04 server from scratch.

Server details:
- SSH port: {port}
- Web server: nginx
- Services: {list services}
- My IP (whitelist): {ip}

Configure:
1. Global defaults (jail.local):
   - nftables backend
   - systemd backend for logs
   - Default ban: 1 hour, 5 retries in 10 min
   - Whitelist: localhost, Docker networks, my IP

2. SSH jail:
   - Port {port}
   - Aggressive mode
   - 3 retries, 1 hour ban

3. nginx jails:
   - botsearch (scanner detection)
   - limit-req (rate limiting)
   - http-auth (authentication failures, if basic auth is used)

4. Recidive jail:
   - 3 bans in 24h = 1 week ban on all ports

5. Apply and verify each jail

Show the status after setup and explain what each jail does.
```

## Prompt 3: Custom Filter Creation

```
I need a custom fail2ban filter for the following log pattern:

Log file: {path}
Log format: {show sample lines}
Match pattern: {describe what to match}

Steps:
1. Analyze the log format
2. Write a failregex that matches the pattern
3. Write any necessary ignoreregex
4. Set the correct datepattern
5. Test with: `sudo fail2ban-regex <logpath> <filter-file>`
6. Create the jail configuration
7. Verify the jail is working

Output:
- The filter file (/etc/fail2ban/filter.d/<name>.conf)
- The jail config (/etc/fail2ban/jail.d/<name>.conf)
- Test command and expected output
```

## Prompt 4: fail2ban Troubleshooting

```
fail2ban is not working as expected. {describe the problem}

Diagnostic steps:

1. Service status:
   `sudo systemctl status fail2ban`
   `sudo fail2ban-client ping`

2. Jail status:
   `sudo fail2ban-client status`
   `sudo fail2ban-client status {jail}`

3. Log errors:
   `sudo tail -50 /var/log/fail2ban.log`
   `sudo grep "ERROR\|WARNING" /var/log/fail2ban.log | tail -20`

4. Filter test:
   `sudo fail2ban-regex {logpath} /etc/fail2ban/filter.d/{filter}.conf`

5. Backend check:
   `sudo fail2ban-client get {jail} backend`

6. nftables rules:
   `sudo nft list ruleset | grep f2b`

7. Config syntax:
   `sudo fail2ban-client -t`

Common issues:
- Wrong log path (file doesn't exist or empty)
- Wrong backend (systemd vs file)
- Filter regex doesn't match log format
- Wrong port in jail config
- Service not restarted after config change
- Log rotation breaking fail2ban (needs copytruncate or logrotate script)

Based on the output, identify the root cause and provide the fix.
```

## Prompt 5: Unban IP

```
I need to unban an IP address from fail2ban. The IP is: {ip}

Steps:
1. Check which jails have this IP banned:
   ```bash
   for jail in $(sudo fail2ban-client status | grep "Jail list" | sed 's/.*://;s/,//g'); do
       if sudo fail2ban-client status "$jail" | grep -q "{ip}"; then
           echo "Banned in: $jail"
       fi
   done
   ```

2. Unban from specific jail:
   `sudo fail2ban-client set {jail} unbanip {ip}`

3. Or unban from all jails:
   `sudo fail2ban-client unban {ip}`

4. To prevent future bans, add to whitelist:
   Add to ignoreip in /etc/fail2ban/jail.local:
   `ignoreip = 127.0.0.1/8 ::1 172.16.0.0/12 {ip}`

5. Reload: `sudo fail2ban-client reload`

6. Verify: `sudo fail2ban-client status {jail}`
```

## Prompt 6: Ban Statistics and Analysis

```
Generate fail2ban statistics for this server.

1. Overall stats:
   - Total bans (all time)
   - Currently banned IPs
   - Active jails count

2. Per-jail stats:
   ```bash
   for jail in $(sudo fail2ban-client status | grep "Jail list" | sed 's/.*://;s/,//g'); do
       echo "=== $jail ==="
       sudo fail2ban-client status "$jail"
   done
   ```

3. Top banned IPs (from log):
   ```bash
   sudo grep "Ban " /var/log/fail2ban.log | awk '{print $NF}' | sort | uniq -c | sort -rn | head -20
   ```

4. Bans per day (last 7 days):
   ```bash
   for i in $(seq 0 6); do
       DATE=$(date -d "$i days ago" +%Y-%m-%d)
       COUNT=$(sudo grep "Ban " /var/log/fail2ban.log | grep "$DATE" | wc -l)
       echo "$DATE: $COUNT bans"
   done
   ```

5. Bans by jail:
   ```bash
   sudo grep "Ban " /var/log/fail2ban.log | awk -F'[][]' '{print $2}' | sort | uniq -c | sort -rn
   ```

6. Recidive analysis:
   - How many IPs were banned by recidive?
   - What jails triggered the original bans?

Report findings and recommendations:
- Are thresholds too strict (too many bans) or too loose (too few)?
- Should any persistent attackers be permanently blocked at firewall level?
- Are there geographic patterns (useful for Cloudflare country blocking)?
```

## Prompt 7: Migrate from iptables to nftables Backend

```
Migrate fail2ban from iptables to nftables backend on Ubuntu 24.04.

Steps:
1. Check current backend:
   `sudo fail2ban-client get sshd banaction`

2. If currently using iptables:
   - Stop fail2ban: `sudo systemctl stop fail2ban`
   - Update jail.local:
     ```ini
     [DEFAULT]
     banaction = nftables
     banaction_allports = nftables[type=allports]
     ```
   - Start fail2ban: `sudo systemctl start fail2ban`

3. Verify nftables rules are created:
   `sudo nft list ruleset | grep f2b`

4. Verify iptables rules are NOT created:
   `sudo iptables -L | grep f2b` (should show nothing)

5. Test banning:
   `sudo fail2ban-client set sshd banip 198.51.100.1`
   `sudo nft list ruleset | grep 198.51.100.1`
   `sudo fail2ban-client set sshd unbanip 198.51.100.1`

Note: nftables is the recommended backend on Ubuntu 24.04. iptables is legacy.
```

## Prompt 8: Log Rotation for fail2ban

```
Ensure fail2ban handles log rotation correctly.

Check:
1. Is fail2ban using logpath (file-based) or systemd (journal-based)?
   - systemd backend: no log rotation issues (journal handles it)
   - file backend: needs to handle rotation

2. For file-based jails, check logrotate config:
   `cat /etc/logrotate.d/nginx`

   The logrotate config should include:
   ```
   postrotate
       /usr/sbin/nginx -s reload
   endscript
   ```

3. fail2ban's own log rotation:
   `cat /etc/logrotate.d/fail2ban`

   Should include:
   ```
   /var/log/fail2ban.log {
       weekly
       rotate 4
       compress
       delaycompress
       missingok
       notifempty
       postrotate
           fail2ban-client flushlogs 1>/dev/null
       endscript
   }
   ```

4. If using auto/polling backend, no special handling needed.
   If using pyinotify backend, `copytruncate` in logrotate is required.

Verify the setup is correct and fix any issues.
```
