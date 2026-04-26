# Firewall Management

## Summary

Configure UFW (Uncomplicated Firewall) with nftables backend on Ubuntu 24.04 VPS: deny-by-default policies, service rules, SSH rate limiting, and Docker port binding to prevent UFW bypass. The critical rule: Docker publishes ports by binding to 0.0.0.0 which bypasses UFW — always bind Docker services to 127.0.0.1.

## Why

Every public VPS faces constant automated scanning. Without a firewall, every listening port is exposed. The most common misconfiguration is Docker silently bypassing UFW by injecting iptables/nftables rules directly — UFW cannot block what Docker publishes at 0.0.0.0.

## When To Use

- Setting up a new VPS for the first time
- Adding a new service that listens on a port
- Auditing whether Docker services are accidentally exposed
- Restricting web traffic to Cloudflare IPs only
- Diagnosing unexpected port exposure

## When NOT To Use

- Managed cloud environments with their own security groups (AWS SGs, GCP firewall rules) — use those instead of or in addition to UFW
- When iptables is managed by another tool (docker rootless mode, k8s) — verify no conflicts before enabling UFW
- Rate-limiting HTTP/HTTPS at the firewall level — use nginx limit_req for that; UFW rate limit is for SSH only

## Content

| File | What's inside |
|------|---------------|
| `content/01-ufw-rules.xml` | Default policies, common rules, rate limiting SSH, UFW logging levels |
| `content/02-docker-security.xml` | Why Docker bypasses UFW, four solutions, bind to 127.0.0.1 pattern, SSH tunnel for internal access |
| `content/03-examples.xml` | NERO production rules, multi-domain setup, debugging exposed Docker ports, blocked traffic analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/ufw-setup-webserver.sh` | Standard web server + Docker host initial UFW setup script |
| `templates/ufw-setup-cloudflare.sh` | Restrict HTTP/HTTPS to Cloudflare IPs only |
| `templates/docker-compose-secure.yml` | Docker Compose with all services bound to 127.0.0.1 |
| `templates/update-cloudflare-ufw.sh` | Monthly cron script to refresh Cloudflare IP ranges in UFW |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/ufw-report.sh` | Status report: rules, listening ports, Docker mappings, exposed 0.0.0.0 ports, recent blocks |
