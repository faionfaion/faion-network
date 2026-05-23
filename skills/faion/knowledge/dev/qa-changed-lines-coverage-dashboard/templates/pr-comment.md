<!--
purpose: PR-comment template with diff coverage as the headline metric.
consumes: see content/02-output-contract.xml inputs for qa-changed-lines-coverage-dashboard
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml + content/04-procedure.xml
token-budget-impact: ~150-400 tokens when loaded as context
-->

## Diff coverage: {{ diff_coverage_percent }}%  ({{ merge_gate_verdict }})

| File | Changed lines | Covered | % | Gate |
|------|---------------|---------|---|------|
{{# per_file }}
| {{ path }} | {{ diff_total_lines }} | {{ diff_covered_lines }} | {{ percent }} | {{ gate_pass }} |
{{/ per_file }}

trend (full repo, secondary): {{ full_repo_trend_line }}

Threshold: {{ default_threshold }}% per file (overrides per coverage-diff.yml).
