# purpose: Per-service health-check loop with retry + silent-OK + TG-on-fail.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

#!/usr/bin/env bash
set -euo pipefail

SVC=${1:?usage: health-check.sh <service> <url>}
URL=$2
MAX_RETRY=3

for i in $(seq 1 $MAX_RETRY); do
  if curl -fsS --max-time 5 "$URL" >/dev/null; then
    exit 0  # silent on success
  fi
  sleep 3
done

# escalate
msg="[$SVC] health-check FAILED at $URL after $MAX_RETRY retries; restarting"
curl -fsS -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
  -d chat_id="${TG_CHAT}" --data-urlencode text="$msg" || true
systemctl --user restart "$SVC" || true
exit 1
