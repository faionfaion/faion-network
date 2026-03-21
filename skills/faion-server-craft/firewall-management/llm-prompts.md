# Firewall Management LLM Prompts

Prompts for AI assistants to audit, configure, and troubleshoot firewall rules.

## Prompt 1: Firewall Security Audit

```
Audit the firewall configuration on this Ubuntu server. Perform these checks:

1. `sudo ufw status verbose` — current rules and policies
2. `sudo ss -tlnp` — all listening ports
3. `docker ps --format "table {{.Names}}\t{{.Ports}}"` — Docker port mappings
4. Check for 0.0.0.0 bindings that should be 127.0.0.1
5. `sudo nft list ruleset | head -100` — underlying nftables rules
6. Check /etc/default/ufw for IPv6 setting
7. `sudo journalctl -k --since "24 hours ago" | grep "UFW BLOCK" | wc -l` — blocked connections count

Report findings as a table:

| Port | Service | Binding | UFW Rule | Exposed | Should Be |
|------|---------|---------|----------|---------|-----------|
| ... | ... | ... | ... | ... | ... |

Flag any ports that are:
- Listening on 0.0.0.0 without a UFW rule (exposed by Docker)
- Internal services accessible from the internet
- Missing rate limiting on SSH

Provide specific commands to fix each issue.
```

## Prompt 2: UFW Setup from Scratch

```
Set up UFW firewall on this Ubuntu 24.04 server. The server runs:
- SSH on port {ssh_port}
- nginx on ports 80/443
- Docker containers for: {list services and ports}
- Application services on ports: {list ports}

Requirements:
1. Deny all incoming by default
2. Allow outgoing
3. Deny routed (Docker security)
4. Allow SSH with rate limiting
5. Allow HTTP/HTTPS
6. Ensure Docker services bind to 127.0.0.1

Execute the setup:
1. Set default policies
2. Add SSH rule FIRST
3. Enable UFW
4. Add remaining rules
5. Audit Docker port bindings
6. Fix any 0.0.0.0 bindings in docker-compose.yml
7. Verify all rules
8. Test SSH access still works

CRITICAL: Always add the SSH rule and verify it BEFORE enabling UFW.
```

## Prompt 3: Docker + UFW Fix

```
Docker is bypassing my UFW firewall. Internal services are exposed to the internet.

Diagnose and fix:

1. Check which Docker containers have exposed ports:
   `docker ps --format '{{.Names}}: {{.Ports}}'`

2. Check if any bind to 0.0.0.0:
   `sudo ss -tlnp | grep docker-proxy`

3. For each exposed container:
   - Show the current port mapping
   - Show the fix (127.0.0.1 binding)

4. Check docker-compose.yml files:
   `find / -name docker-compose.yml -exec grep -l "ports:" {} \; 2>/dev/null`

5. For each docker-compose.yml:
   - Show current port mappings
   - Show corrected port mappings (127.0.0.1:port:port)

6. Apply fixes:
   - Update docker-compose.yml
   - Restart containers
   - Verify ports are now localhost-only

7. Verify from outside that ports are no longer accessible
```

## Prompt 4: Rule Creation Helper

```
I need to add firewall rules for the following scenario:
{describe the scenario}

For each rule needed:
1. Show the exact UFW command
2. Explain why this rule is needed
3. Show how to verify the rule works
4. Note any security implications

Format:
| # | Rule | Command | Purpose | Verify |
|---|------|---------|---------|--------|

After creating rules, show the complete ruleset with `sudo ufw status numbered`.
```

## Prompt 5: Firewall Troubleshooting

```
I'm having a connectivity issue. {describe the problem}

Diagnostic checklist:
1. `sudo ufw status verbose` — is UFW enabled? What are the rules?
2. `sudo ss -tlnp | grep {port}` — is the service listening?
3. `sudo journalctl -k | grep "UFW BLOCK" | grep {port} | tail -5` — is UFW blocking it?
4. `sudo nft list ruleset | grep {port}` — any nftables rules?
5. Is the traffic going through Cloudflare? Check if direct IP or domain
6. Is Docker involved? Check docker-proxy bindings

Based on the output, identify whether the issue is:
- UFW blocking legitimate traffic (add rule)
- Service not listening (start/fix service)
- Docker binding issue (fix docker-compose)
- Cloudflare issue (check DNS proxying)
- nftables conflict (check for conflicting rules)

Provide the specific fix command.
```

## Prompt 6: Cloudflare IP Restriction

```
Restrict HTTP/HTTPS traffic to Cloudflare IPs only. This prevents direct IP access, ensuring all web traffic goes through Cloudflare's security features.

Steps:
1. Fetch current Cloudflare IP ranges from https://www.cloudflare.com/ips-v4 and ips-v6
2. Remove existing HTTP/HTTPS allow-all rules
3. Add per-IP-range rules for Cloudflare
4. Create an update script for monthly cron execution
5. Verify that direct IP access is blocked
6. Verify that Cloudflare-proxied access still works

IMPORTANT:
- Keep SSH rule unchanged (SSH goes direct, not through Cloudflare)
- Test that all domains still work after applying
- Create rollback commands in case of issues
- Document the cron job for monthly updates
```

## Prompt 7: Blocked Traffic Analysis

```
Analyze blocked firewall traffic to identify attack patterns and potential threats.

1. Get top blocked IPs (last 24h):
   `sudo journalctl -k --since "24 hours ago" | grep "UFW BLOCK" | grep -oP 'SRC=\K[^ ]+' | sort | uniq -c | sort -rn | head -20`

2. Get top targeted ports (last 24h):
   `sudo journalctl -k --since "24 hours ago" | grep "UFW BLOCK" | grep -oP 'DPT=\K[^ ]+' | sort | uniq -c | sort -rn | head -20`

3. Hourly block rate:
   `sudo journalctl -k --since "24 hours ago" | grep "UFW BLOCK" | awk '{print $1, $2, $3}' | cut -d: -f1 | sort | uniq -c`

4. Identify patterns:
   - Are there persistent attackers? (same IP, many attempts)
   - Are they targeting specific services? (SSH, MySQL, RDP)
   - Are they from known scanner networks? (Shodan, Censys)

5. Recommendations:
   - Should any IPs be permanently blocked?
   - Are fail2ban jails needed for any patterns?
   - Should Hetzner cloud firewall rules be added?
```

## Prompt 8: Port Audit

```
Perform a comprehensive port audit on this server.

1. List all listening ports:
   `sudo ss -tlnp` (TCP)
   `sudo ss -ulnp` (UDP)

2. For each listening port, determine:
   - What service is it?
   - Is it bound to 0.0.0.0 (all interfaces) or 127.0.0.1 (localhost)?
   - Is there a UFW rule for it?
   - Should it be accessible from the internet?

3. Report as:
   | Port | Proto | Service | Binding | UFW Rule | Should Be External | Action |
   |------|-------|---------|---------|----------|-------------------|--------|

4. Flag:
   - Ports open to internet that should be internal
   - Internal services without UFW rules (safe but document)
   - Docker services on 0.0.0.0 (highest risk)
   - Unknown services

5. Provide remediation commands for each flagged port.
```
