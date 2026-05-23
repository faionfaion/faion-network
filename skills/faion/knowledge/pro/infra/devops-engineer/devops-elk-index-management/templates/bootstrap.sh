# purpose: Bootstrap script: create policy + template + initial index + write alias
# consumes: inputs declared in AGENTS.md `## Prerequisites`
# produces: artefact conforming to content/02-output-contract.xml (config)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~350 tokens when loaded

#!/usr/bin/env bash
set -euo pipefail
ES_URL="${ES_URL:?missing}"
AUTH=(-u "${ES_USER:?}:${ES_PASS:?}")

curl -sfX PUT "$ES_URL/_ilm/policy/logs-policy" "${AUTH[@]}" -H "Content-Type: application/json" --data-binary @ilm-policy.json
curl -sfX PUT "$ES_URL/_index_template/logs-template" "${AUTH[@]}" -H "Content-Type: application/json" --data-binary @index-template.json
curl -sfX PUT "$ES_URL/logs-000001" "${AUTH[@]}" -H "Content-Type: application/json" -d '{"aliases": {"logs-write": {"is_write_index": true}}}'
echo OK
