# Faion.net Server

Production server for faion.net infrastructure.

## Server Info

- Host: faion-net (46.225.58.119)
- OS: Ubuntu 24.04 LTS (x86_64)
- SSH: port 22022, key-only auth
- Provider: Hetzner Cloud, cx53, nbg1

## Services

```
nginx                  - Reverse proxy (snakeoil certs)
faion-net-api          - Python API (port 8000)
faion-net-api-dev      - Python API dev (port 8001)
wg-quick@wg0           - WireGuard VPN (port 443/udp)
fail2ban               - SSH protection (port 22022, nftables)
postfix + opendkim     - Mail server
valkey-server          - Redis-compatible (port 6379)
docker: n8n            - Automation (port 5678)
docker: scanmecard     - ScanMeCard app
```

## Key Paths

```
/home/faion/Projects/  - Application code
/opt/n8n/              - n8n Docker setup
/etc/wireguard/wg0.conf - VPN config
/etc/nginx/sites-enabled/ - Nginx vhosts
```

## Secrets (1Password)

All secrets are stored in 1Password CLI (`op`). Unlock first: `op-unlock`.

Vault: `faion.net` — Hetzner, Cloudflare, email, service credentials.

Usage:
```bash
op-unlock                                                    # Unlock 1Password
op item list --vault "faion.net"                              # List all items
op item get "Hetzner" --vault "faion.net"                     # Get item
op item get "Hetzner" --vault "faion.net" --fields password   # Single field
```

## Language

- Communication - Ukrainian
- Code - English

## Commits

Format: `type: description`
Types: fix, feat, chore, refactor, docs
No Co-Authored-By or AI mentions.
