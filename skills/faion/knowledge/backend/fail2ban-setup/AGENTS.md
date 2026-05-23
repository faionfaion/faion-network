# Fail2ban Setup for Ubuntu 24

## Summary

**One-sentence:** Dynamic IP banning with fail2ban + nftables backend on Ubuntu 24: SSH brute-force jail, sshd port 22022 awareness, retention (bantime 1h escalating to 1w), Telegram alert action, whitelist for WireGuard.

**One-paragraph:** SSH brute-force scans hit a public VPS every few seconds; the default sshd config + UFW does not stop them, just rate-limits SYN. Fail2ban parses auth.log and bans repeat offenders at the nftables layer. This methodology produces a verified fail2ban configuration with a sshd jail tuned for the host's actual port, escalating bantime, whitelisting for the operator's WireGuard subnet, and a Telegram action that pings on ban.

## Applies If (ALL must hold)

- Public VPS with sshd reachable from the internet.
- Logs in journald or /var/log/auth.log; not on read-only ramfs.
- Operator wants ban automation, not just rate-limiting.

## Skip If (ANY kills it)

- SSH not exposed publicly (WireGuard-only access).
- Strict zero-trust setup with mTLS + bastion; SSH already off.
- Managed PaaS without persistent VM (Cloudflare Workers, Vercel).

**Ефективно для:**

- VPS-фаундери де `lastb` показує 500+ failed attempts/day.
- Команди з sshd на non-standard порту що все ще бачать спроби.
- Compliance вимагає automated incident response для auth-failures.
- WireGuard-користувачі що хочуть whitelist VPN-subnet від ban.

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
| `solo/infra/server-craft/firewall-management` | UFW + nftables backend interactions. |
| `solo/infra/server-craft/ssh-hardening` | sshd port + key-only auth foundations. |

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
| `templates/skeleton.md` | fail2ban audit report listing jail + port + backend + escalation + whitelist + alert. |
| `templates/_smoke-test.md` | Minimum viable filled-in fail2ban audit. |
| `templates/jail.local` | fail2ban jail.local with sshd on non-standard port + escalating ban. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fail2ban-setup.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[firewall-management]]
- [[ssh-hardening]]
- [[monitoring-logging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
