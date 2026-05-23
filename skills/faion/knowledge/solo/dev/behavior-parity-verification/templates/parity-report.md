<!--
purpose: per-stage parity report skeleton the engineer fills before promoting a ramp stage.
consumes: nothing — this IS the report artefact.
produces: a parity-report.md ready to convert to JSON via the scorer.
depends-on: parity_diffs table, normalizer code.
token-budget-impact: ~200 tokens when copied into a stage write-up.
-->

# Parity report — &lt;scope&gt; — stage &lt;1|2|3|4&gt;

## Scope
- Endpoint or function path:
- Legacy implementation handle:
- New implementation handle:

## Observable fields
- field_a (exact)
- field_b (sorted, exact)
- field_c (tolerance: ±N units)

Ignored (non-observable): request_id, computed_at_ms, server_version

## Ramp stage
- Stage number: 1 | 2 | 3 | 4 (= 1% | 10% | 50% | 100%)
- Window start (UTC):
- Window end (UTC):
- Total compared:
- Diff rate (%):

## Clusters
| cluster_id | sample_count | disposition | root cause / justification |
|------------|--------------|-------------|-----------------------------|
|            |              | fixed / accepted-with-justification / open |  |

## Verdict
- [ ] promote — diff_rate &lt; 0.5%, no open clusters, error_rate at parity
- [ ] freeze — investigate before promoting
- [ ] revert — roll back to previous stage

## Sign-off
- Signed off by:
- Signed off at (ISO date):
