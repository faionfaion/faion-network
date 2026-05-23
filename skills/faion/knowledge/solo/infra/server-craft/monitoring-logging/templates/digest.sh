# purpose: Daily digest builder: one line per service, sent to TG at 07:00.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

#!/usr/bin/env bash
set -euo pipefail

SERVICES="faion-net-api faion-net-api-dev valkey-server"
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
