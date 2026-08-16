# Cron Automation for VPS

## Summary

**One-sentence:** Linux cron patterns for VPS: script structure (lock + log + trap + env), flock-based overlap prevention, env handling for non-login shells, FLOW-style hourly silent / daily report cadence, robust error reporting via Telegram.

**One-paragraph:** Cron is the cheapest scheduler in existence but every solo operator burns a weekend on its quirks: scripts run under sh not bash, $PATH is minimal, $HOME may be unset, two crons can race the same job. This methodology codifies a script template (set -euo pipefail + flock + log rotation + trap on EXIT) and a frequency pattern (hourly silent health, daily report, weekly digest) plus alerting that fires once per failure, not per minute.

## Applies If (ALL must hold)

- VPS runs at least one scheduled task (backup, sync, report, cleanup).
- Operator can read /var/log/syslog and add cron entries to a service user.
- Telegram bot or equivalent webhook channel is configured for alerts.

## Skip If (ANY kills it)

- Managed scheduler available (e.g. Vercel Cron, Cloudflare Cron Triggers, Render Cron).
- Workflow needs second-level precision — use systemd timers with OnUnitActiveSec.
- Single ad-hoc one-shot — `at` is simpler than cron.

**Ефективно для:**

- VPS-фаундери що тримають 5-15 cron jobs (backup, sync, report).
- FLOW-style monitoring: hourly silent + daily digest у TG.
- Команди де cron-race-condition спричинив duplicate emails або money charges.
- Аудит cron-таблиці перед прод-релізом.

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
| `solo/infra/server-craft/monitoring-logging` | Cron logs feed the monitoring pipeline. |
| `solo/infra/server-craft/systemd-user-services` | Sibling — systemd timers for finer control. |

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
| `templates/skeleton.md.j2` | Cron audit report listing jobs + lock + alert routing. |
| `templates/skeleton.md` | Cron audit report listing jobs + lock + alert routing. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in cron audit. |
| `templates/_smoke-test.md` | Minimum viable filled-in cron audit. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/cron-job.sh` | Cron script template with flock + strict mode + log + Telegram-on-fail. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cron-automation.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[monitoring-logging]]
- [[systemd-user-services]]
- [[deploy-scripts]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/cron-job.sh`

```bash
#!/usr/bin/env bash
# Usage: install in cron with `flock -n /var/lock/<job>.lock /path/to/cron-job.sh`
set -euo pipefail

JOB_NAME=${0##*/}
LOG=/var/log/${JOB_NAME%.sh}.log

exec >>"$LOG" 2>&1
echo "[$(date -Is)] START $JOB_NAME"

on_exit() {
  local rc=$?
  if [ $rc -ne 0 ]; then
    msg="[$JOB_NAME] failed exit=$rc at $(date -Is); tail: $(tail -n 5 "$LOG")"
    curl -fsS -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
      -d chat_id="${TG_CHAT}" --data-urlencode text="$msg" || true
  fi
  echo "[$(date -Is)] END $JOB_NAME rc=$rc"
}
trap on_exit EXIT

# --- job body below ---
echo "do the work here"
```
