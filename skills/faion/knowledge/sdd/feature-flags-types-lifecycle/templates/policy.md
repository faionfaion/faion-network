<!-- __faion_header_v1__ -->
<!-- purpose: Team flag policy: per-kind window + retirement criteria -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#four-flag-kinds -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Team flag policy: per-kind window + retirement criteria","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#four-flag-kinds","token_budget_impact":"~150 tokens when loaded"}} -->
# Feature Flag Policy

| Kind | Window | Cleanup Criteria |
|---|---|---|
| release | ≤30 days | 100% for 14 days, no rollback |
| experiment | 1-4 weeks | sample size reached, decision recorded |
| ops (kill-switch) | indefinite | none (operational tool) |
| permission | indefinite | only if user-cohort retired |
