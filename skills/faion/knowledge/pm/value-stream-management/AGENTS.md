# Value Stream Management

## Summary

**One-sentence:** Maps the end-to-end value stream (customer request → customer value), measures Flow Metrics (Lead/Cycle/Throughput/WIP/%C&A) + DORA (DF/CLT/CFR/MTTR), identifies the constraint via Theory of Constraints, runs targeted experiments, and emits a `ValueStreamReport` with ranked interventions.

**One-paragraph:** AI productivity gains and DevOps automation frequently fail to improve customer-visible delivery time because the bottleneck lives outside the software team (product spec, design review, compliance gate, support queue). Flow Metrics expose end-to-end flow; DORA measures only DevOps efficiency. Used together they locate where value actually stalls. This methodology codifies a 5-step procedure (instrument → map → measure DORA → identify constraint → experiment), with three sub-agents (flow-instrumenter, dora-collector, bottleneck-analyzer) and a hard minimum sample size (≥ 50 items per work type) before declaring a constraint. Output is a typed `ValueStreamReport` carrying constraint stage, distribution by Kersten's four work types (feature/defect/risk/debt), DORA four-tuple, and 1–3 ranked experiments with expected throughput lift / cost.

**Ефективно для:**

- DevOps automation shipped but customer lead time has not improved.
- Cross-functional bottleneck suspected across product → design → eng → release → support.
- Org adopting SAFe / FAST Agile / Project-to-Product and shifting from output to flow metrics.
- DORA elite labels reaching diminishing returns — need upstream Flow Metrics for honest signal.

## Applies If (ALL must hold)

- Telemetry exists for at least 3 of: Jira/Linear, GitHub/GitLab, deploy log, PagerDuty, Zendesk.
- Stable system: each work type has ≥ 50 historical items (Little's Law assumptions hold).
- Stakeholders own at least 2 stages of the stream (single-team without upstream/downstream ≠ value-stream).
- 90+ days of timestamp data available.

## Skip If (ANY kills it)

- Single-team pre-PMF startup — premature optimisation.
- No telemetry baseline (no commit timestamps, no deploy log) — instrument first.
- Pure cost-cutting / layoff context — VSM is not a layoff lever.
- Teams without shared ownership across the stream — VSM names the bottleneck but cannot move it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool ID-link map | YAML | platform team |
| Git + deploy log access | API tokens | platform team |
| Work-type taxonomy | YAML (feature/defect/risk/debt) | Kersten Flow Framework |
| 90+ days timestamp data | per source | git/jira/deploy/incident |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[work-breakdown-structure]] | Provides the deliverable taxonomy each flow item maps to. |
| [[team-development]] | Throughput shape is an input to Tuckman staging. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: customer-anchored boundary, work-type split, pair DORA metrics, ≥50-item sample before constraint, no elite-label without trend, AI-PR human/bot split | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `ValueStreamReport` + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: hallucinated ID links, timezone bugs, elite-DORA-no-trend, webhook drops, AI-PR flood | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: instrument → map → DORA → constraint → experiment | ~800 |
| `content/05-examples.xml` | medium | One worked report: 90-day window, design-review constraint surfaced, 3 ranked experiments | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: telemetry coverage + sample size + work-type split → suppress/measure/declare-constraint | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `flow-instrumenter` | sonnet | ID-link reasoning + timestamp normalisation. |
| `dora-collector` | haiku | Mechanical reduction of git + incident logs. |
| `bottleneck-analyzer` | sonnet | Theory-of-Constraints application + experiment ranking. |
| `experiment-tracker` | sonnet | Before/after distribution comparison with judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flow-item.yaml` | Schema for a single traced work item across VSM stages |
| `templates/dora-quick.sh` | Bash script: compute last-30-day DORA from git + deploy log |
| `templates/_smoke-test.json` | Minimum-viable filled `ValueStreamReport` for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-value-stream-management.py` | Validate a `ValueStreamReport` against the JSON Schema | Pre-commit on every report change |

## Related

- [[work-breakdown-structure]]
- [[team-development]]
- [[wbs-creation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (telemetry coverage, sample-size per work type, customer-boundary anchor) to a concrete action — instrument-first, measure-only, declare-constraint, or run-experiment — each leaf references a rule in `01-core-rules.xml` so claims are grounded in checkable invariants.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/flow-item.yaml`

```yaml
item_id: "PROJ-1234"
work_type: "feature"        # feature | defect | risk | debt
outcome: "shipped"          # shipped | cancelled | in-progress

stages:
  - name: "spec"
    enter_ts: "2025-04-01T09:00:00Z"
    exit_ts: "2025-04-03T17:00:00Z"
    blocked_h: 8              # hours where work was waiting (queue time)

  - name: "design"
    enter_ts: "2025-04-04T09:00:00Z"
    exit_ts: "2025-04-07T17:00:00Z"
    blocked_h: 0

  - name: "development"
    enter_ts: "2025-04-08T09:00:00Z"
    exit_ts: "2025-04-14T17:00:00Z"
    blocked_h: 4

  - name: "review"
    enter_ts: "2025-04-15T09:00:00Z"
    exit_ts: "2025-04-16T17:00:00Z"
    blocked_h: 0

  - name: "deploy"
    enter_ts: "2025-04-17T10:00:00Z"
    exit_ts: "2025-04-17T10:30:00Z"
    blocked_h: 0

# Computed fields (filled by the flow-instrumenter or analytics layer)
lead_time_h: 408             # exit_ts(last stage) - enter_ts(first stage) in hours
process_time_h: 60           # sum of (exit_ts - enter_ts - blocked_h) per stage
efficiency_pct: 14.7         # process_time_h / lead_time_h * 100

# Source IDs for cross-tool tracing (required for instrumentation)
source_ids:
  jira: "PROJ-1234"
  github_pr: 567
  deploy_sha: "abc123def456"
```

### `templates/dora-quick.sh`

```bash
#
# Usage: ./dora-quick.sh [days=30]
set -euo pipefail

DAYS="${1:-30}"
SINCE="${DAYS} days ago"

# Deployment Frequency
DEPLOYS=$(awk -v cutoff="$(date -u -d "$SINCE" +%s 2>/dev/null || date -u -v-"${DAYS}"d +%s)" '
  { cmd="date -u -d \""$0"\" +%s 2>/dev/null || date -u -j -f \"%Y-%m-%dT%H:%M:%SZ\" \""$0"\" +%s"
    cmd | getline t; close(cmd)
    if (t > cutoff) c++ }
  END { print c+0 }' deploy.log 2>/dev/null || echo "0")

echo "Deployment Frequency: $(echo "scale=2; $DEPLOYS / $DAYS" | bc) /day (last ${DAYS}d)"

# Change Lead Time (commit ts → deploy ts, mean over matched commits)
LEAD_SECS=$(git log --since="$SINCE" --pretty=format:"%H %at" 2>/dev/null | \
  while read -r sha ts; do
    dep_ts=$(grep -m1 "$sha" deploy.log 2>/dev/null | \
             xargs -I{} date -u -d "{}" +%s 2>/dev/null || true)
    [ -n "$dep_ts" ] && echo "$((dep_ts - ts))"
  done | awk '{s+=$1; n++} END{ if(n) printf "%.0f\n", s/n }')

if [ -n "$LEAD_SECS" ] && [ "$LEAD_SECS" -gt 0 ]; then
  LEAD_H=$(echo "scale=1; $LEAD_SECS / 3600" | bc)
  echo "Change Lead Time (h, mean): ${LEAD_H}h"
else
  echo "Change Lead Time: n/a (no matched commits in deploy.log)"
fi

echo ""
echo "Note: CFR and MTTR require PagerDuty / incident log integration."
echo "Note: tag bot commits and report human/bot split before publishing DF."
```

### `templates/_smoke-test.json`

```json
{
  "stream_id": "smoke",
  "window": {
    "start": "2026-02-22",
    "end": "2026-05-23",
    "days": 90
  },
  "customer_anchor": {
    "start_event": "support_ticket_opened",
    "end_event": "feature_visible_in_prod"
  },
  "flow_metrics_by_type": {
    "feature": {
      "lead_time_days": 28,
      "cycle_time_days": 4,
      "throughput_per_week": 6,
      "wip": 12,
      "complete_and_accurate_pct": 0.82,
      "sample_size": 62
    },
    "defect": {
      "lead_time_days": 9,
      "cycle_time_days": 2,
      "throughput_per_week": 14,
      "wip": 6,
      "complete_and_accurate_pct": 0.91,
      "sample_size": 110
    },
    "risk": {
      "lead_time_days": 18,
      "cycle_time_days": 3,
      "throughput_per_week": 2,
      "wip": 4,
      "complete_and_accurate_pct": 0.95,
      "sample_size": 55
    },
    "debt": {
      "lead_time_days": 22,
      "cycle_time_days": 5,
      "throughput_per_week": 3,
      "wip": 8,
      "complete_and_accurate_pct": 0.85,
      "sample_size": 58
    }
  },
  "dora": {
    "deployment_frequency": {
      "human_prs": 220,
      "bot_prs": 90
    },
    "change_lead_time_minutes": 95,
    "change_failure_rate": 0.07,
    "mttr_minutes": 38,
    "trend_window_quarters": 3,
    "tier_label": "high",
    "tier_label_delta_vs_prior": "+1 vs prior quarter"
  },
  "constraint": {
    "stage": "design-review",
    "evidence": "design-review WIP*cycle dominates; feature LT 28 vs cycle 4 implies queue upstream",
    "samples_per_type": {
      "feature": 62,
      "defect": 110,
      "risk": 55,
      "debt": 58
    }
  },
  "experiments": [
    {
      "name": "WIP cap on design-review = 3",
      "expected_lift": "feature LT -25%",
      "cost": "1 designer day/wk",
      "rank": 1
    }
  ]
}
```
