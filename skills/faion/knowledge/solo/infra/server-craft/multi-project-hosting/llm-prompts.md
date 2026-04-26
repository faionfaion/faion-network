# Multi-Project Hosting LLM Prompts

## Plan New Project on Existing Server

```
Help me plan adding a new project to my existing VPS.

Current server:
- Ubuntu 24.04, [CPU, RAM, DISK]
- Current projects: [LIST with ports and resource usage]
- Shared services: PostgreSQL on 5432, Redis on 6379
- Memory usage: [current used/total]

New project:
- Name: [PROJECT_NAME]
- Domain: [DOMAIN]
- Architecture: [e.g., "FastAPI backend + React frontend"]
- Expected resources: [RAM, disk estimates]
- Needs database: [yes/no, which type]
- Needs cache: [yes/no]
- Needs message queue: [yes/no]

Please provide:
1. Port allocation (pick next available range)
2. Directory structure (/srv/ and ~/projects/)
3. systemd service files for each component
4. nginx site configuration
5. Database setup (shared PostgreSQL: CREATE DATABASE/USER)
6. .env template for the new project
7. Memory limits (MemoryMax, MemoryHigh)
8. Updated resource budget (will everything fit?)
9. Step-by-step deployment guide
```

## Port Conflict Resolution

```
I'm getting a port conflict on my server. Help me resolve it.

Error: [PASTE ERROR, e.g., "Address already in use"]
Port: [PORT NUMBER]
Expected service: [SERVICE]

Commands to run for diagnosis:
- What's using the port: ss -tlnp | grep PORT
- All listening ports: ss -tlnp

Current port allocation:
[PASTE port-registry.txt or list of known ports]

Please:
1. Identify what's causing the conflict
2. Suggest resolution (reassign port, stop conflicting service, etc.)
3. Update port allocation plan
4. Check for other potential conflicts
```

## nginx Multi-Domain Setup

```
Configure nginx for hosting multiple domains on my VPS.

Domains to configure:
[LIST with routing rules, e.g.:
- nero.faion.net: /api/* -> 8100, /ws -> 8100 (WebSocket), / -> 8101 (SPA)
- meetingtax.io: /api/* -> 8200, / -> 8201 (Next.js SSR)
- eulaguard.com: /api/* -> 8300 (API only, no frontend)
]

SSL: Cloudflare Origin Certificates (Full Strict mode)

Requirements:
- HTTP to HTTPS redirect for all domains
- WebSocket support where needed
- Security headers (X-Frame-Options, etc.)
- Shared snippets for common config
- Proper logging per domain

Provide:
1. /etc/nginx/snippets/ files (proxy-params, security-headers)
2. Site config for each domain
3. Commands to enable sites and reload nginx
4. How to test each domain
5. SSL certificate installation steps
```

## Resource Capacity Planning

```
Help me plan resource capacity for my multi-project VPS.

Server specs: [CPU, RAM, DISK]

Projects and services:
[TABLE of all services with:
- Service name
- Type (FastAPI, Celery, Next.js, static, Docker)
- Expected memory usage (average and peak)
- CPU profile (constant, bursty)
- Disk usage
]

Questions:
1. Will everything fit in available RAM?
2. What MemoryMax/MemoryHigh for each service?
3. How much headroom should I keep?
4. At what point should I split to a second server?
5. Can I reduce resource usage anywhere?
6. What monitoring should I set up?

Output as:
- Memory allocation table
- CPU allocation notes
- Disk budget
- "Traffic light" assessment (green/yellow/red)
```

## Shared vs Isolated Services Decision

```
Help me decide: should I use shared or isolated backing services for my projects?

Current setup:
- [NUMBER] projects on one server
- Projects: [LIST with descriptions]

Backing services in question:
- PostgreSQL: shared instance or per-project containers?
- Redis: shared instance or per-project containers?
- RabbitMQ: shared or only for projects that need it?

Considerations:
- I'm a solo developer
- [RAM] total RAM
- Projects are [related/unrelated]
- Uptime requirements: [describe]
- Compliance: [any requirements?]

Please analyze:
1. Pros/cons of shared vs isolated for each service
2. Resource comparison (how much RAM for shared vs isolated)
3. Backup implications
4. Upgrade risk assessment
5. My recommendation based on my specific situation
6. Migration path if I need to switch later
```

## Add Cloudflare DNS and SSL

```
Set up Cloudflare DNS and SSL for a new domain on my server.

Domain: [DOMAIN]
Server IP: [IP]
Cloudflare account: [already set up / need to set up]

Current state:
- Domain registered at: [registrar]
- Nameservers: [current, e.g., "registrar default"]
- nginx: [already installed / needs setup]

Tasks:
1. Point nameservers to Cloudflare
2. Add DNS records (A, CNAME, etc.)
3. Configure SSL mode (Full Strict)
4. Generate and install Origin Certificate
5. Configure nginx for the domain
6. Verify everything works

Provide step-by-step with:
- Cloudflare dashboard steps (describe what to click)
- Server commands
- Verification: curl commands to test SSL
- Common issues and fixes (SSL redirect loops, etc.)
```
