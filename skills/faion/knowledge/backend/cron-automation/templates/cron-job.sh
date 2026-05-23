# purpose: Cron script template with flock + strict mode + log + Telegram-on-fail.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

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
