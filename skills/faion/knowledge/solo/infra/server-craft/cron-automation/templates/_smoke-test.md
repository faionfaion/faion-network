<!-- purpose: Minimum viable filled-in cron audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Cron Automation — Audit Report

## Host

- hostname: faion-net
- user: nero

## Jobs

| schedule | command | flock | logs | alert |
|----------|---------|-------|------|-------|
| `0 3 * * *` | /home/nero/scripts/backup.sh | yes | /var/log/backup.log | on-fail TG |
| `*/5 * * * *` | /home/nero/scripts/health.sh | yes | /var/log/health.log | on-fail TG |

## Frequency layers

- hourly silent health: every 5 min health.sh
- daily digest: 07:00 digest.sh
- weekly digest: Mon 09:00 weekly.sh

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
