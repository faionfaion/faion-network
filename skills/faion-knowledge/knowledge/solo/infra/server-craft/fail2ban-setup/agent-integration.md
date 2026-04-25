# Agent Integration — fail2ban Setup

## When to use
- After SSH hardening — fail2ban is the dynamic defense layer that bans brute-force IPs automatically
- When adding a new publicly exposed service (nginx web app, mail server, RabbitMQ management) — add a jail for that service
- When reviewing auth logs and finding repeated scanner traffic — use `fail2ban-regex` to verify filter match before enabling a jail
- When deploying behind Cloudflare — configure `X-Forwarded-For` header extraction so the real IP is banned, not Cloudflare's proxy IP

## When NOT to use
- Servers behind a private VPN where SSH is not reachable from the public internet — the attack surface is already eliminated
- Kubernetes pods / Docker containers that log to Docker log driver, not to a file fail2ban can tail (requires custom setup)
- Cloudflare Workers or serverless — there is no server-level log to monitor
- As a substitute for SSH key-only auth — it is a complement, not a replacement

## Where it fails / limitations
- Banning Cloudflare's own IP ranges blocks legitimate users whose traffic transits Cloudflare — must whitelist all Cloudflare IPs in `ignoreip`
- Docker containers log via Docker log driver by default; fail2ban cannot read those logs without volume-mounting or configuring a file log driver
- The nftables backend requires nftables to be the active firewall; mixing with iptables rules causes conflicts on Ubuntu 24.04
- The `systemd` log backend reads the journal, not a log file; the `logpath` directive is ignored when `backend = systemd`
- `recidive` jail requires `/var/log/fail2ban.log` to exist; if fail2ban logging is set to journal-only, recidive never fires
- Ban time escalation via recidive only works if `bantime` in the sshd jail is shorter than `findtime` in recidive (default thresholds need tuning)

## Agentic workflow
An agent configuring fail2ban generates drop-in jail files in `/etc/fail2ban/jail.d/`, tests each filter against real log samples with `fail2ban-regex`, reloads the daemon with `fail2ban-client reload`, and verifies that each new jail is active with `fail2ban-client status <jail>`. For a new web application, the agent reads the nginx access/error log to identify the log pattern, generates a custom filter, tests it, and only then enables the jail.

### Recommended subagents
- `bash-agent` — generates jail drop-in, runs `fail2ban-regex` test, reloads daemon, verifies status
- `log-analysis-agent` — reads nginx/auth logs, identifies scanner patterns, proposes custom filter regex

### Prompt pattern
```
Generate a fail2ban jail configuration for nginx on Ubuntu 24.04 with:
- nftables backend
- SSH jail on port <port>, maxretry 3, bantime 1h
- nginx-botsearch jail, maxretry 10, bantime 24h
- recidive jail: 3 bans in 24h → 1 week ban on all ports
- ignoreip: 127.0.0.1/8, ::1, <my-ip>, <vpn-subnet>, <cloudflare-ranges>

Return drop-in file contents for /etc/fail2ban/jail.d/server.conf
and the commands to reload and verify.
```

```
Test this filter against the log file:
Filter: /etc/fail2ban/filter.d/nginx-botsearch.conf
Log: /var/log/nginx/access.log

Run: sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-botsearch.conf
Report: number of matches, sample matched lines, and whether the IP capture group works.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fail2ban-client` | Manage jails, ban/unban IPs, reload config | `apt install fail2ban` / [fail2ban.org](https://www.fail2ban.org/) |
| `fail2ban-regex` | Test a filter pattern against a real log file | included with fail2ban |
| `nft list ruleset` | Inspect active nftables rules including fail2ban bans | built-in |
| `journalctl -u fail2ban` | Read fail2ban daemon logs | built-in systemd |
| `whois` / `ipinfo.io` | Identify the owner of a banned IP for context | built-in / API |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare IP list | SaaS | Yes — `curl https://www.cloudflare.com/ips-v4` | Fetch current Cloudflare IPv4/IPv6 ranges for ignoreip |
| AbuseIPDB | SaaS | Yes — REST API | Report or look up banned IPs; custom action integration possible |
| Telegram Bot API | SaaS | Yes — `curl` POST | Custom fail2ban action to send Telegram notification on ban |

## Templates & scripts
See `templates.md` for the full `jail.d/server.conf` template.

Custom Telegram notification action (inline, 18 lines):
```bash
# /etc/fail2ban/action.d/telegram.conf
[Definition]
actionstart =
actionstop =
actioncheck =
actionban = curl -s -X POST \
    "https://api.telegram.org/bot<TOKEN>/sendMessage" \
    -d chat_id="<CHAT_ID>" \
    -d text="fail2ban: <name> banned <ip> (<failures> failures in <findtime>s)"
actionunban = curl -s -X POST \
    "https://api.telegram.org/bot<TOKEN>/sendMessage" \
    -d chat_id="<CHAT_ID>" \
    -d text="fail2ban: <name> unbanned <ip>"

[Init]
name = default
```

## Best practices
- Never edit `jail.conf` or `fail2ban.conf` directly — use drop-in files in `jail.d/` and `filter.d/` only; they survive package upgrades
- Always test filters with `fail2ban-regex` against real logs before enabling a jail — an unmatched filter silently does nothing
- Whitelist your own static IP, VPN subnet, and all Cloudflare IPs in `ignoreip` before enabling any jail — one wrong whois lookup can lock you out
- Enable `recidive` jail as the last layer: it catches IPs that get banned repeatedly across jails and applies a week-long all-ports ban
- For SSH: set `maxretry = 3` and `bantime = 3600` — aggressive enough to deter brute force, short enough that legitimate mistakes are recoverable
- Set `banaction_allports = nftables[type=allports]` in `[DEFAULT]` for recidive so the IP is completely blocked, not just on one port
- After any config change: `sudo fail2ban-client reload` (not restart) preserves existing ban state

## AI-agent gotchas
- **Human-in-loop checkpoint before adding your own IP to `ignoreip`:** Agents generating `ignoreip` lists must ask the operator to confirm their current public IP — an incorrect IP in `ignoreip` is a silent security gap
- **Cloudflare IP list changes over time.** Agents must fetch the live list (`curl https://www.cloudflare.com/ips-v4`) rather than hardcoding it; hardcoded lists become stale
- **`systemd` backend ignores `logpath`.** Agents generating jail configs for systemd-journal services (sshd on Ubuntu 24.04) must set `backend = systemd` and omit `logpath` — including `logpath` with `systemd` backend causes a warning and may prevent the jail from starting
- **fail2ban-regex exit codes are unintuitive.** A zero exit code does not mean matches were found; agents must parse stdout for the match count line
- **recidive needs its own log file.** If fail2ban logs exclusively to journal (`logtarget = SYSTEMD-JOURNAL`), recidive has nothing to read. Agents must ensure `logtarget = /var/log/fail2ban.log` is set when recidive is enabled

## References
- [fail2ban documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [fail2ban jail.conf manual](https://manpages.debian.org/testing/fail2ban/jail.conf.5.en.html)
- [fail2ban filter library](https://github.com/fail2ban/fail2ban/tree/master/config/filter.d)
- [Cloudflare IP ranges](https://www.cloudflare.com/ips/)
- [nftables documentation](https://wiki.nftables.org/)
