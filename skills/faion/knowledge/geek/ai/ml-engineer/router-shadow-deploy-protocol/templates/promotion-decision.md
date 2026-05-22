<!--
purpose: go/no-go decision artefact for the promotion meeting
consumes: shadow-report.yaml + acceptance-contract.yaml
produces: report (signed decision)
depends-on: router-shadow-deploy-protocol methodology
token-budget-impact: 0 at runtime
-->

# Promotion Decision: <candidate_id>

## Inputs
- `shadow-report.yaml` (window: <YYYY-MM-DD> → <YYYY-MM-DD>)
- `acceptance-contract.yaml` v<X.Y.Z>

## Gate evaluation

| Gate | Threshold | Observed | Verdict |
|------|-----------|----------|---------|
| Scoring delta | within band per acceptance contract | <median> [95%CI: <lo>, <hi>] | PASS/FAIL |
| Cost delta | ≤ baseline × 1.10 | <cost_delta_mean>x | PASS/FAIL |
| Schema parity | == 1.00 across all days | <schema_parity_min_daily> | PASS/FAIL |

## Decision: GO / NO-GO

## Reasoning
<2-3 sentences citing the gate evaluation>

## If GO — rollout plan
- T+0: 1%
- T+24h: 10%
- T+72h: 50%
- T+5d: 100%
- T+12d: decommission old router

## If NO-GO — corrective actions
- <root cause>
- <fix>
- <re-shadow window plan>

## Sign-offs
- ML engineer: <email> <YYYY-MM-DD>
- Product owner: <email> <YYYY-MM-DD>
- On-call lead: <email> <YYYY-MM-DD>
