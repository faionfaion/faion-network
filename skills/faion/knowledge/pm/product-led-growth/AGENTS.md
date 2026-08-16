# Product-Led Growth (PM Angle)

## Summary

**One-sentence:** Metric-driven PLG loop (visitor -> signup -> activated -> PQL -> SQL -> paying -> expansion) with PM-owned aha-moment instrumentation, activation rituals, and expansion-revenue accountability.

**One-paragraph:** Define aha moment as a single event (or short sequence) reachable in <=10 minutes from signup; write PQL criteria; track free->paid conversion by activation cohort (not signup cohort); PM owns expansion revenue; cap concurrent activation experiments at 2 per funnel step. Output: plg-funnel-spec YAML + activation dashboard.

**Ефективно для:**

- Self-serve SaaS / API / dev-tool, де buyer = user.
- Sales-led продукт, що програє на CAC payback >18 місяців.
- Bottom-up wedge у enterprise account через individual sign-up.
- Продукт із вимірюваним aha-moment <=10 хв від signup до first value.

## Applies If (ALL must hold)

- New SaaS / API / dev-tool product where the buyer is also the user.
- Existing sales-led product losing on CAC payback (>18 months) — convert top-of-funnel to self-serve.
- Bottom-up wedge into an enterprise account: individual signs up free, expansion to team is the business model.
- Product has a measurable aha moment reachable in <10 minutes from signup.
- Pricing-page experimentation: PM owns activation funnel and runs PQL -> SQL conversion tests.

## Skip If (ANY kills it)

- Enterprise-sales-only product where buyer != user.
- B2B with no self-serve surface.
- Product where aha moment is structurally > 10 min (long onboarding) — fix onboarding first.
- Commodity product where price/distribution dominates and PLG is not the wedge.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tracking plan | YAML | product-analytics |
| Signup -> aha funnel data | cohort table | BI |
| PQL criteria draft | YAML | PM |
| Sales hand-off SLA | doc | sales ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[product-analytics]] | Provides activation cohort + funnel instrumentation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: aha-instrumented, PQL written, activation-cohort tracking, expansion ownership, experiment throttle | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for plg-funnel-spec | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: aha-vague, PQL drift, signup-cohort conversion, expansion handed off | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: define aha -> instrument -> write PQL -> set cohort metrics -> run experiments | 900 |
| `content/05-examples.xml` | medium | Worked PLG loop for dev-tool with aha = first-successful-call | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on buyer=user + aha feasibility + CAC payback | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `aha-moment-extract` | sonnet | Define aha from spec + usage data. |
| `pql-criteria-author` | sonnet | Write the PQL criteria with hand-off triggers. |
| `activation-experiment-readout` | opus | Multi-cohort activation experiment synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plg-definitions.yml` | PLG terms + funnel stages + PQL criteria. |
| `templates/plg-snapshot.sh` | Weekly PLG snapshot script. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-led-growth.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[product-analytics]]
- [[experimentation-at-scale]]
- [[feedback-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/plg-definitions.yml`

```yaml
# PLG definitions — frozen activation/PQL spec.
# This file is the PM-to-growth contract.
# Edit only via PR with both PM owner and growth owner signing.
# Changes to this file invalidate historical cohort comparisons.

activation:
  event: "<object_action event name>"   # e.g., project_created
  threshold: 1                          # times the event must fire
  window_days: 7                        # within N days of signup
  target_pct: 40                        # target activation rate (%)
  frozen_since: "YYYY-MM-DD"
  owner_pm: "pm@team.com"
  note: "Must predict D30 retention; if activated users don't retain materially better, redefine."

pqls:
  - pql_name: "team-expansion"
    frozen_event_sequence:
      - event: "<activation_event>"
        min_count: 1
      - event: "<collaboration_event>"   # e.g., member_invited
        min_count: 2
    threshold_per_user: 2
    threshold_per_account: 5
    cooldown_period_days: 30
    sales_action: "book_call"           # book_call | email_drip | ignore
    owner_pm: "pm@team.com"
    owner_growth: "growth@team.com"
    sla_to_action_hours: 24

ttv_targets:
  consumer_saa_s_minutes: 5
  developer_api_minutes: 15             # first successful API call

expansion_revenue_target_pct: 30       # of total revenue
nrr_target_pct: 120

# Activation graveyard: past definitions and why they were retired.
retired_activations: []
# - event: "dashboard_viewed"
#   retired: "2025-Q4"
#   reason: "Did not predict D30 retention — activated users retained at same rate as non-activated"
```

### `templates/plg-snapshot.sh`

```bash
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
```
