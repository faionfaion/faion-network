# fail2ban Setup

## Summary

Dynamic IP banning layer for Ubuntu 24.04 servers using nftables backend and systemd journal log source: SSH jail (maxretry 3), nginx jails (botsearch, limit-req, http-auth), custom application filters, recidive jail for week-long all-ports bans on repeat offenders, and Cloudflare IP whitelisting. Configuration exclusively via drop-in files in `jail.d/` and `filter.d/` — never edit `jail.conf` directly.

## Why

Even with SSH key-only auth and a firewall, servers face thousands of automated SSH brute-force attempts and web scanner bots daily. fail2ban monitors logs and temporarily bans IPs exhibiting malicious behavior, adding a dynamic defense layer at zero throughput cost. The recidive jail catches IPs that evade short bans by returning repeatedly, escalating to a one-week all-ports block.

## When To Use

- After SSH hardening — fail2ban is the dynamic complement to static firewall rules
- When adding any publicly exposed service (nginx, mail server) — add a jail for that service
- When nginx logs show repeated scanner traffic for the same IP — verify filter match, then enable jail
- Deploying behind Cloudflare — configure real-IP extraction so the actual attacker IP is banned

## When NOT To Use

- Servers behind a private VPN where SSH is not reachable from the public internet
- Kubernetes pods / Docker containers logging to Docker log driver (not a file fail2ban can tail)
- As a substitute for SSH key-only auth — it is a complement, not a replacement
- Cloudflare Workers or serverless — no server-level log to monitor

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture.xml` | fail2ban components: jails, filters, actions, nftables backend, systemd journal source |
| `content/02-jail-configs.xml` | SSH jail, nginx jails, recidive, ban time escalation, ignoreip whitelisting |
| `content/03-custom-filters.xml` | Writing custom failregex patterns, testing with fail2ban-regex, Cloudflare real-IP issue |

## Templates

| File | Purpose |
|------|---------|
| `templates/jail.local` | Global defaults: nftables backend, ban thresholds, ignoreip |
| `templates/jail-sshd.conf` | SSH jail drop-in for `jail.d/` |
| `templates/jail-nginx.conf` | nginx jails: http-auth, botsearch, limit-req, bad-request |
| `templates/jail-recidive.conf` | Recidive jail for repeat-offender escalation |
