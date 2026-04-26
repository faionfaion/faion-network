# Agent Integration — Multi-Project Hosting

## When to use
- Adding a second (or Nth) project to an existing VPS — need port allocation and nginx config
- Provisioning a new domain on a shared server where Cloudflare DNS + origin cert must be configured
- Deciding whether to share PostgreSQL/Redis or isolate per project
- Auditing resource utilization to determine whether to split to a second server
- Generating a port registry as a machine-readable file agents can query

## When NOT to use
- Single-project servers where isolation is not a concern
- Kubernetes/Swarm clusters — use cluster-native ingress instead of nginx server blocks
- Serverless or PaaS deployments (Vercel, Railway) — hosting is abstracted away
- Projects with strict compliance requirements mandating physical isolation

## Where it fails / limitations
- Port registry is a plain text file — no enforcement; agents must read and update it manually
- Shared PostgreSQL/Redis creates a single failure domain; a misconfigured project can starve others
- Cloudflare IP whitelisting for fail2ban must be kept in sync when Cloudflare rotates IPs
- nginx config merging across many sites is brittle; a syntax error in one block brings down all sites
- Resource budget table assumes stable load; burst traffic from one project can evict another's memory pages

## Agentic workflow
An agent bootstrapping a new project on the server reads `/srv/port-registry.txt` to find the next free 100-port range, then generates the nginx server block and the DNS record payload for Cloudflare. A second agent validates the nginx config with `sudo nginx -t` and reloads if clean. A third agent (optional) writes the Cloudflare Origin Certificate install commands and runs them. The whole flow is deterministic and auditable from the port registry as a single source of truth.

### Recommended subagents
- `bash-agent` — reads port registry, finds free range, writes nginx block, runs `nginx -t` and reload
- `cloudflare-dns-agent` — creates A record via Cloudflare API and installs origin cert via SSH

### Prompt pattern
```
You are setting up <project-name> on the server. Read /srv/port-registry.txt and find the next free 100-port block. Generate:
1. nginx sites-available config for <domain> using the allocated port
2. SQL statements to create the project database and user
3. Port registry entry to append
Return each as a labelled code block.
```

```
Validate the multi-project nginx setup: run `sudo nginx -t`. If it fails, read the error, identify the broken site config, fix the syntax issue, and reload.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `nginx` | Reverse proxy and TLS termination | `apt install nginx` / [nginx.org](https://nginx.org/en/docs/) |
| `certbot` | Let's Encrypt cert management (alternative to Cloudflare origin) | `apt install certbot` / [certbot.eff.org](https://certbot.eff.org/) |
| `curl` (Cloudflare API) | Create/update DNS records, install origin certs | `curl` built-in / [Cloudflare API v4](https://developers.cloudflare.com/api/) |
| `ss` / `netstat` | Verify port bindings across projects | built-in |
| `systemctl` | Manage per-project systemd services | built-in |
| `free -h` / `vmstat` | Check live memory budget | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare DNS | SaaS | Yes — REST API | Create A records, origin certs; token scoped per zone |
| nginx | OSS | Yes — `nginx -t` + `systemctl reload nginx` | Config files are plain text; easy to generate |
| PostgreSQL | OSS | Yes — `psql` or SQL over subprocess | Create DB/user per project programmatically |
| Valkey/Redis | OSS | Yes — `redis-cli` | Allocate DB numbers or key-prefix namespaces |
| Hetzner Cloud | SaaS | Yes — REST API + `hcloud` CLI | Resize, snapshot, create volumes |

## Templates & scripts
See `templates.md` for nginx site block template and port registry format.

Minimal port-registry update script (inline):
```bash
#!/bin/bash
# append-port-entry.sh PROJECT PORT SERVICE NOTES
# Usage: ./append-port-entry.sh meetingtax 8200 "meetingtax-api" "FastAPI"
echo "$2    $3    $1    $4" >> /srv/port-registry.txt
echo "Added port $2 for $1"
```

## Best practices
- Always run `nginx -t` before `systemctl reload nginx` — a syntax error kills all sites, not just the new one
- Keep Cloudflare SSL mode at "Full (Strict)" with origin certificates; never use "Flexible" (exposes plaintext on origin)
- Allocate 100-port ranges per project from the start; gaps cost nothing and prevent future conflicts
- Use separate PostgreSQL databases (not schemas) per project; schema sharing creates migration conflicts
- Mount project `.env` files as mode `600`, owned by the service user — never world-readable
- Document each port in `/srv/port-registry.txt` at allocation time, not after; agents rely on this for idempotency
- Add `internal: true` to Docker networks that should not reach the host network

## AI-agent gotchas
- **Human-in-loop checkpoint:** Before allocating a new port range, confirm the range is truly free — agents must read the registry and also verify with `ss -tlnp | grep <port>` to catch unregistered services
- **Config generation without reload is safe; reload without test is not.** Always chain: generate → `nginx -t` → reload. Never skip the test step
- **Cloudflare API tokens must be zone-scoped** — if an agent uses a global token, it can accidentally modify unrelated zones; store per-zone tokens in secrets
- **Resource budget is static** — agents cannot automatically detect memory pressure from other projects at generation time; include a `free -m` snapshot in any provisioning report
- **Port registry drift:** agents that restart or crash mid-allocation may write a registry entry without completing nginx setup. A separate agent pass should reconcile registry entries against active nginx configs

## References
- [nginx documentation](https://nginx.org/en/docs/)
- [Cloudflare Origin CA certificates](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
- [Cloudflare API v4 DNS records](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-create-dns-record)
- [PostgreSQL: CREATE DATABASE](https://www.postgresql.org/docs/current/sql-createdatabase.html)
- [Hetzner Cloud API](https://docs.hetzner.cloud/)
