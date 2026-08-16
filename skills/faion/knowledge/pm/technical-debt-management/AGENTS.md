# Technical Debt Management

## Summary

**One-sentence:** Six-step technical-debt discipline (register -> score impact via interest × contagion / effort -> allocate capacity -> pay down -> prevent -> track) shared between PM and engineering with a quarterly capacity contract.

**One-paragraph:** Typed debt register (design/code/test/infra/docs/dependency); impact score = (interest_per_month × contagion_factor) / paydown_effort; written quarterly capacity contract (% sprint for debt); prevention policy paired with every paydown; public visibility to non-engineering stakeholders. Output: debt-register YAML + capacity contract memo.

**Ефективно для:**

- Roadmap velocity видимо падає при стабільному headcount.
- Quarterly planning, де 15-20% capacity резервується на paydown.
- Post-P0 outage, що ідентифікував debt як root cause.
- Перед major architectural change (auth rewrite, billing migration).

## Applies If (ALL must hold)

- Roadmap velocity visibly declining despite stable headcount.
- Quarterly planning where 15-20% capacity is reserved for paydown.
- Post-P0 outage or regression cluster where the post-mortem identifies debt as root cause.
- Before a major architectural change (auth rewrite, billing migration).
- Stakeholder pressure to ship features is visibly crowding debt work out of the sprint.
- Multi-repo solopreneur portfolio where debt silently compounds in lower-traffic repos.

## Skip If (ANY kills it)

- Greenfield product <3 months of code (premature optimization).
- Throwaway prototype.
- Team explicitly running tracer-bullet methodology with debt-acceptable-by-design.
- Crisis sprint stabilising production — debt work pauses until the incident closes.
- Capacity contract already in force <=90 days with no trigger event.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Codebase ownership map | table | engineering |
| Recent incident log | table | SRE / on-call |
| Sprint capacity baseline | doc | team lead |
| Roadmap of next quarter | doc | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[release-planning]] | Provides the release cadence the paydown capacity contract slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip-this-methodology: typed register, interest × contagion / effort score, interest-rate derivation, capacity contract, prevention policy paired, no zero-debt sprints, public visibility | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for debt-register + capacity-contract | 850 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: untyped register, effort-only score, soft capacity, fix-without-prevention, budget drift, big-bang refactor, invisible debt | 1100 |
| `content/04-procedure.xml` | essential | 6-step procedure: inventory -> classify -> score -> contract -> prevent -> track | 950 |
| `content/05-examples.xml` | medium | Worked debt register with capacity contract + prevention policy | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on code age + velocity trend | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `debt-classify` | haiku | Tag debt items by type. |
| `impact-score` | sonnet | Compute interest × contagion / effort with cited evidence. |
| `capacity-contract-author` | sonnet | Draft the quarterly capacity contract memo. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-register.md.j2` | Debt register skeleton with type + interest + contagion + effort. |
| `templates/debt-register.md` | Debt register skeleton with type + interest + contagion + effort. Generated from `templates/debt-register.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/debt-prioritization-matrix.md.j2` | Prioritization matrix template. |
| `templates/debt-prioritization-matrix.md` | Prioritization matrix template. Generated from `templates/debt-prioritization-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/debt-hotspots.sh` | Compute hotspots from churn + bug density. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-technical-debt-management.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[release-planning]]
- [[product-lifecycle]]
- [[product-operations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/debt-hotspots.sh`

```bash
set -euo pipefail
#!/usr/bin/env bash
# debt-hotspots.sh — find files most likely to be technical debt
# Usage: ./debt-hotspots.sh [since=6.months.ago] [top=20]
# Output: TSV table + JSONL file for scanner subagent consumption
set -euo pipefail

SINCE="${1:-6.months.ago}"
TOP="${2:-20}"
TMP="$(mktemp -d)"

# 1. churn: commits per file
git log --since="$SINCE" --name-only --pretty=format: \
  | grep -E '\.(py|ts|tsx|js|jsx|go|rs|java|rb)$' \
  | sort | uniq -c | sort -rn > "$TMP/churn.txt"

# 2. complexity proxy (lizard if available, else line count)
if command -v lizard >/dev/null; then
  lizard -l python -l javascript -l typescript -X -w 2>/dev/null \
    | awk -F, 'NR>1 {print $5"\t"$1}' | sort > "$TMP/cx.txt"
else
  awk '{ print FILENAME"\t"NR }' $(awk '{print $2}' "$TMP/churn.txt") 2>/dev/null \
    | awk '{a[$1]=$2} END{for (f in a) print a[f]"\t"f}' | sort > "$TMP/cx.txt"
fi

# 3. join and score: hotspot = churn * complexity
awk '{print $2"\t"$1}' "$TMP/churn.txt" | sort > "$TMP/churn_keyed.txt"
join -1 1 -2 2 "$TMP/churn_keyed.txt" "$TMP/cx.txt" 2>/dev/null \
  | awk '{print $1"\t"$2*$3"\t"$2"\t"$3}' \
  | sort -k2 -rn | head -n "$TOP" \
  | awk 'BEGIN{print "file\tscore\tchurn\tcomplexity"} {print}'

# 4. emit JSONL for scanner subagent
awk 'NR>1 {printf "{\"file\":\"%s\",\"score\":%s,\"churn\":%s,\"cx\":%s}\n",$1,$2,$3,$4}' \
  "$TMP/churn.txt" > "$TMP/hotspots.jsonl" 2>/dev/null || true
echo "--- hotspots.jsonl ---"
cat "$TMP/hotspots.jsonl"
```
