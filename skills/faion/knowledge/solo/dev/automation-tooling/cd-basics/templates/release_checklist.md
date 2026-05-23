<!-- __faion_header_v1__ -->
<!-- purpose: Per-commit release checklist: green CI + flag-default-off + DB migration phase -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: spec; depends-on: content/01-core-rules.xml#releasable-mainline -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Per-commit release checklist: green CI + flag-default-off + DB migration phase","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#releasable-mainline","token_budget_impact":"~150 tokens when loaded"}} -->
- [ ] CI green on mainline
- [ ] New behavior behind feature flag (default off)
- [ ] DB migration in expand phase only (no destructive)
- [ ] Rollback procedure tested in staging
- [ ] DORA event emitted (deployment_frequency, lead_time)
