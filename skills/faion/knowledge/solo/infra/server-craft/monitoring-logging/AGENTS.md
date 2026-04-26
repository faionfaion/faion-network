# Monitoring & Logging

## Summary

Lightweight monitoring and logging for solo developer VPS platforms using journald, health-check scripts, and Telegram alerts — no Prometheus/Grafana required. Provides journalctl query patterns, log rotation config, FLOW-style autonomous hourly/daily reports, and a tmux-based status dashboard.

## Why

A solo developer server needs 95% of enterprise monitoring value at 1% of the complexity. Journald + a few shell scripts + Telegram alerts cover service-down detection, disk/memory thresholds, OOM kills, and daily status summaries without running a full observability stack.

## When To Use

- Setting up observability from scratch on a solo-developer VPS
- A service went down silently and you need alerting before it happens again
- Writing a health-check script for a cron job or FLOW guardian
- Building an autonomous monitoring loop that sends Telegram alerts on anomalies
- Investigating a production incident retroactively via journalctl

## When NOT To Use

- Multi-server environments where Prometheus/Grafana/Loki is justified (use pro/infra/devops-engineer)
- Kubernetes clusters (use Datadog, Grafana Loki, or similar)
- Compliance-heavy environments requiring tamper-proof audit-trail log storage
- High-frequency trading or sub-second SLOs where journald latency is unacceptable

## Content

| File | What's inside |
|------|---------------|
| `content/01-journald.xml` | journalctl filter patterns, journald.conf size/retention settings, Docker log rotation |
| `content/02-health-check.xml` | Health-check script structure, resource thresholds, exit code conventions |
| `content/03-alerting.xml` | Telegram alert function, FLOW schedule (hourly/daily/startup), alert-on-failure pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-check.sh` | Comprehensive health-check script for Docker + systemd + resources |
| `templates/notify-telegram.sh` | Minimal Telegram send function, stdin or arg mode |
| `templates/flow-hourly.sh` | FLOW-style silent-on-success hourly monitor |
| `templates/flow-daily.sh` | FLOW daily report with uptime, resources, errors, backup status |
| `templates/journald.conf` | journald.conf with size caps, persistence, rate limiting |
| `templates/logrotate-app.conf` | logrotate config for application log files |
