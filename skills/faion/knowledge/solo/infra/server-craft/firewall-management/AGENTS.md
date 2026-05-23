---
slug: firewall-management
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Configure UFW with nftables backend on Ubuntu 24: deny incoming, allow outgoing, deny routed before any allow rule, SSH rate-limited on actual port, Docker services bound to 127.0.0.1 to prevent UFW bypass."
content_id: "e22fe5f3d04bf05d"
complexity: medium
produces: report
est_tokens: 6000
tags: [firewall, ufw, nftables, docker, security]
---
# Firewall Management with UFW

## Summary

**One-sentence:** Configure UFW with nftables backend on Ubuntu 24: deny incoming, allow outgoing, deny routed before any allow rule, SSH rate-limited on actual port, Docker services bound to 127.0.0.1 to prevent UFW bypass.

**One-paragraph:** UFW is the cheapest production firewall on Linux but has two traps: ordering (defaults apply after user rules; routed traffic must be explicitly denied) and Docker (publishing ports to 0.0.0.0 bypasses UFW by inserting iptables rules above UFW chain). This methodology produces a verified UFW configuration with deny-by-default, SSH rate-limit on the actual port, and a verified inventory of Docker port bindings showing 127.0.0.1: prefix.

## Applies If (ALL must hold)

- Public VPS on Ubuntu 24 with sshd + ≥1 service exposed via reverse proxy.
- Operator can edit /etc/ufw/* with sudo.
- Docker services exist (or will exist) on the host.

## Skip If (ANY kills it)

- Managed cloud (AWS SGs, GCP firewall rules) — use those.
- iptables managed by another tool (k8s, docker rootless).
- Stricter zero-trust setup (mTLS bastion, no public ports).

**Ефективно для:**

- Перший firewall на новому VPS після bootstrap.
- Audit після виявлення публічного 5432/6379 порту.
- Restrict-to-Cloudflare-IPs flow (allow tcp/443 from CF only).
- Розслідування 'чому Postgres доступний з інтернету'.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/docker-compose-patterns` | 127.0.0.1 binds are the UFW-bypass guard. |
| `solo/infra/server-craft/ssh-hardening` | SSH port + rate-limit settings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | UFW audit report with deny defaults + SSH limit + Docker bind inventory. |
| `templates/_smoke-test.md` | Minimum viable filled-in UFW audit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-firewall-management.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[docker-compose-patterns]]
- [[ssh-hardening]]
- [[fail2ban-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
