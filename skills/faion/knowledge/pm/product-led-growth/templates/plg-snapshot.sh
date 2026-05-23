#!/usr/bin/env bash
# purpose: Weekly PLG snapshot script.
# consumes: input from methodology
# produces: artefact for downstream agent
# depends-on: content/02-output-contract.xml
# token-budget-impact: 0 (executes locally)
set -euo pipefail
#!/usr/bin/env bash
# plg-snapshot.sh — weekly PLG metric snapshot for the PM.
# Usage: plg-snapshot.sh [yyyy-mm-dd]
# Reads .aidocs/product_docs/plg-definitions.yml (frozen activation/PQL spec).
# Requires: POSTHOG_HOST, POSTHOG_KEY env vars.
# Output: .aidocs/product_docs/plg-weekly/<date>.md
set -euo pipefail
date_arg="${1:-$(date -I)}"
out=".aidocs/product_docs/plg-weekly/${date_arg}.md"
mkdir -p "$(dirname "$out")"
python3 - "$date_arg" "$out" <<'PY'
import os, sys, yaml, datetime, json, urllib.request
date_arg, out = sys.argv[1], sys.argv[2]
spec = yaml.safe_load(open(".aidocs/product_docs/plg-definitions.yml"))
host = os.environ["POSTHOG_HOST"]
key = os.environ["POSTHOG_KEY"]

def hogql(q):
    req = urllib.request.Request(
        f"{host}/api/projects/@current/query/",
        data=json.dumps({"query": {"kind": "HogQLQuery", "query": q}}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    return json.loads(urllib.request.urlopen(req).read())["results"]

end = datetime.date.fromisoformat(date_arg)
start = end - datetime.timedelta(days=7)
act_event = spec["activation"]["event"]
target_pct = spec["activation"]["target_pct"]

signups = hogql(
    f"select count() from events where event='signed_up' "
    f"and timestamp>='{start}' and timestamp<'{end}'"
)[0][0]
activated = hogql(
    f"select count(distinct distinct_id) from events "
    f"where event='{act_event}' and timestamp>='{start}' and timestamp<'{end}'"
)[0][0]
rate = (activated / signups * 100) if signups else 0

with open(out, "w") as f:
    f.write(f"# PLG snapshot {date_arg}\n\n")
    f.write("| Metric | Value | Target |\n|---|---|---|\n")
    f.write(f"| Signups | {signups} | — |\n")
    f.write(f"| Activated | {activated} | — |\n")
    f.write(f"| Activation rate | {rate:.1f}% | {target_pct}% |\n")
    f.write(f"| Frozen activation event | `{act_event}` | (do not edit without ADR) |\n")
    status = "OK" if rate >= target_pct else "BELOW TARGET"
    f.write(f"\nStatus: {status}\n")
print(out)
PY
git add "$out" && git diff --cached --stat
