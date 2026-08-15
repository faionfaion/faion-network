# Lightweight Monitoring + Logging

## Summary

**One-sentence:** Monitoring + logging for solo VPS without Prometheus/Grafana: journald with log rotation, health-check scripts, Telegram digest, single-line summaries per service per day, alert-only on failure.

**One-paragraph:** Prometheus + Grafana is overkill for 1-5 services; the operator-attention cost exceeds the value. This methodology produces a minimal stack: journald with rotation + per-service health-check + daily TG digest + alert-on-failure. The output is a verified config that emits one Telegram message per day with one line per service + one alert per incident.

## Applies If (ALL must hold)

- VPS with 1-10 services where Prometheus would be overkill.
- Operator wants a once-a-day digest, not a dashboard.
- Telegram bot configured for alerts.

## Skip If (ANY kills it)

- More than ~10 services or multiple hosts — graduate to Prometheus.
- Compliance requires structured metrics ingestion (Datadog, Splunk).
- Operator needs second-level granularity — journald digest is daily.

**Ефективно для:**

- Solo VPS-фаундери що не хочуть Grafana-stack.
- FLOW-style: hourly silent health + daily digest у TG.
- Indie hackers що читають один TG-feed замість трьох дашбордів.
- Compliance-light: 30-day log retention з journald rotation.

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
| `solo/infra/server-craft/cron-automation` | Digest runs from cron. |
| `solo/infra/server-craft/health-checks-autoheal` | Health-check feeds the alert path. |

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
| `templates/skeleton.md` | Monitoring audit listing journald + digest + alert routing. |
| `templates/_smoke-test.md` | Minimum viable filled-in monitoring audit. |
| `templates/digest.sh` | Daily digest builder: one line per service, sent to TG at 07:00. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monitoring-logging.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[cron-automation]]
- [[health-checks-autoheal]]
- [[secrets-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/digest.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

SERVICES="web-api.service web-worker.service valkey-server.service"
LINES=()

for svc in $SERVICES; do
  state=$(systemctl is-active "$svc" || true)
  restarts=$(systemctl show "$svc" -p NRestarts --value)
  errs=$(journalctl -u "$svc" --since '24 hours ago' -p err -q | wc -l)
  LINES+=("$svc: state=$state restarts=$restarts errors_24h=$errs")
done

msg="[digest $(date -u +%F)]"$'\n'$(printf '%s\n' "${LINES[@]}")
curl -fsS -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
  -d chat_id="${TG_CHAT}" --data-urlencode text="$msg"
```
