# Agent Integration — Monitoring & Logging

## When to use
- Setting up observability from scratch on a solo-developer VPS
- A service goes down and you need to establish alerting so it doesn't happen silently again
- Writing a health-check script that a cron job or FLOW guardian calls
- Building an autonomous monitoring loop that sends Telegram alerts on anomalies
- Investigating a production incident retrospectively via journalctl

## When NOT to use
- Multi-server environments where Prometheus/Grafana/Loki is justified (use pro/infra/devops-engineer)
- Kubernetes clusters (use Datadog, Grafana Loki, or similar)
- Compliance-heavy environments requiring audit trails with tamper-proof log storage
- High-frequency trading or sub-second SLOs where journald latency is unacceptable

## Where it fails / limitations
- journald `--user` logs are only available if the user session has lingered; agents running before linger is enabled see empty logs
- Telegram bot rate limit: 30 messages/second per bot, 20 messages/minute to same chat — alerting storms will be throttled
- Health check scripts hitting HTTP endpoints fail if network namespace is isolated (Docker bridge)
- `docker stats --no-stream` can hang if Docker daemon is unresponsive
- `journalctl -o json` output is line-delimited JSON, not an array — parsers expecting `[]` will fail
- FLOW-style autonomous monitoring generates noise if thresholds are misconfigured; alert fatigue is real even at solo scale

## Agentic workflow
An agent can be wired as a FLOW guardian: cron fires every hour, agent reads journalctl output for the last hour, checks disk/memory/load, calls health endpoints, and sends a Telegram summary only if issues are found. The key design decision is whether the agent runs inline (always fires) or conditionally (fires only on anomaly). For solo developers, anomaly-only is almost always the right choice to reduce noise.

### Recommended subagents
- `faion-sdd-executor-agent` — implement monitoring scripts as SDD tasks with test gates
- `nero-sdd-executor-agent` — NERO-specific FLOW guardian implementation

### Prompt pattern
```
You are a FLOW health monitor for the NERO platform.
Run the following checks and report results in JSON:
1. systemctl --user is-active for: nero-core, nero-channel-web, nero-channel-tg
2. docker inspect -f '{{.State.Running}}' for: nero-postgres, nero-redis
3. curl -sf http://127.0.0.1:8100/health
4. df / --output=pcent (alert if >85%)
5. free | awk '/Mem:/ {printf "%.0f", $3/$2*100}'
Output: {"status": "ok|warn|fail", "issues": [...], "timestamp": "<iso>"}
If status != "ok", call notify-telegram.sh with the issues list.
```

```
Parse the following journalctl JSON output from the last hour.
Extract: error count, critical errors with timestamps, any OOM kills.
Input: <journalctl -u nero-core -o json --since "1 hour ago" --no-pager>
Output: {"errors": N, "criticals": [...], "oom_kills": N}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `journalctl` | Query systemd journal | Built-in systemd |
| `systemctl` | Service status checks | Built-in systemd |
| `htop` / `btop` | Interactive process monitor | `apt install htop btop` |
| `watch` | Repeat command with refresh | Built-in (procps) |
| `curl` | HTTP health endpoint checks | `apt install curl` |
| `lsof` | Open file descriptors per process | `apt install lsof` |
| `iotop` | I/O per process | `apt install iotop` |
| `sysstat` (`sar`) | Historical CPU/IO stats | `apt install sysstat` |
| `netstat` / `ss` | Network connections | `apt install net-tools` / built-in |
| `logrotate` | Rotate application log files | `apt install logrotate` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Telegram Bot API | SaaS | Yes | `sendMessage` via curl; no SDK needed for alerts |
| UptimeRobot | SaaS | Yes (API) | External HTTP uptime monitoring; free tier sufficient |
| BetterStack (Uptime) | SaaS | Yes (API) | HTTP monitors + on-call; generous free tier |
| Grafana Cloud | SaaS | Yes (Loki/Prometheus) | Free tier 14-day retention; useful for growth |
| Prometheus | OSS | Yes (HTTP scrape) | Overkill for single server but scriptable |
| Netdata | OSS | Yes (API) | Per-process monitoring with web UI; low overhead |
| GoAlert | OSS | Partial | On-call scheduling; heavy for solo use |

## Templates & scripts
See `templates.md` for full health-check.sh and flow-hourly.sh templates.

Minimal Telegram alert function (≤20 lines, safe to inline in any script):
```bash
tg_alert() {
  local msg="$1"
  local token="${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN not set}"
  local chat="${TELEGRAM_CHAT_ID:?TELEGRAM_CHAT_ID not set}"
  curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    -d chat_id="$chat" \
    -d text="$msg" \
    -d parse_mode="Markdown" > /dev/null
}
# Usage: tg_alert "ALERT: *nero-core* is DOWN on $(hostname)"
```

## Best practices
- Use `journalctl --no-pager -o json` for machine-readable output in agent pipelines; parse with `jq`
- Set `Storage=persistent` in journald.conf so logs survive reboot — default is often volatile
- Cap journal size with `SystemMaxUse=2G` to prevent disk exhaustion
- Separate "check" from "alert": run checks every minute, alert only if 3 consecutive failures (reduces false positives)
- For Docker containers, configure `log-driver: json-file` with `max-size` and `max-file` in `/etc/docker/daemon.json`
- Health check HTTP endpoints should return 200 + JSON body; `/health` vs `/ready` distinction matters for restart logic
- Include hostname in Telegram alerts; on multi-server setups you need to know which server fired
- Keep health-check.sh exit code meaningful: `exit $ERRORS` so cron can detect failure and alert on cron failure itself

## AI-agent gotchas
- `journalctl --user` requires the calling process to be in the same user session or use `--machine` flag for cross-user queries
- `docker stats` blocks indefinitely without `--no-stream`; always add `--no-stream` in agent pipelines
- Telegram `parse_mode=Markdown` breaks if message contains unescaped `_`, `*`, `[`, `` ` `` — use `parse_mode=HTML` or escape carefully
- `curl` health checks must have `--max-time 5` or they block the agent if the service hangs without rejecting connections
- journald JSON timestamps are microseconds since epoch (field `__REALTIME_TIMESTAMP`), not ISO — parse accordingly
- Agent writing to cron-invoked scripts must not require interactive stdin or TTY; use `DEBIAN_FRONTEND=noninteractive` for any apt calls

## References
- [systemd journald man page](https://www.freedesktop.org/software/systemd/man/journald.conf.html)
- [Telegram Bot API — sendMessage](https://core.telegram.org/bots/api#sendmessage)
- [logrotate documentation](https://linux.die.net/man/8/logrotate)
- [Netdata — lightweight monitoring](https://www.netdata.cloud/)
- [BetterStack Uptime](https://betterstack.com/uptime)
