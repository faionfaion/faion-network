<!--
purpose: PR-comment report skeleton with three latency deltas + cost delta + eval pass-rate delta
consumes: deltas dict from validate-pr-time-cost-diff-tool.py output
produces: report (markdown posted as PR comment via GitHub API)
depends-on: content/01-core-rules.xml (report-three-deltas, eval-pass-rate-side-channel)
token-budget-impact: low — ~150 tokens when loaded as context
-->

## Cost + Time Diff (vs main)

| metric | base | head | delta |
|---|---|---|---|
| median latency | <base_md>ms | <head_md>ms | <delta_md>ms |
| p95 latency | <base_p95>ms | <head_p95>ms | <delta_p95>ms |
| $/req | <base_cents>¢ | <head_cents>¢ | <delta_cents>¢ (<delta_pct>%) |
| eval pass-rate | <base_pct>% | <head_pct>% | <delta_pp>pp |

Verdict: **<pass|fail|warn>** — <reason or "within budget">.
Eval set hash: `<eval_set_hash>` · Cost table: `<cost_table_version>`.
