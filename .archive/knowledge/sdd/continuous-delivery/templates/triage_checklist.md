<!-- __faion_header_v1__ -->
<!-- purpose: Triage checklist routing to cd-basics or cd-pipelines -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: decision-record -->
<!-- depends-on: content/01-core-rules.xml#principles-first -->
<!-- token-budget-impact: ~250 tokens when loaded as context -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Triage checklist routing to cd-basics or cd-pipelines","consumes":"see content/02-output-contract.xml","produces":"decision-record","depends_on":"content/01-core-rules.xml#principles-first","token_budget_impact":"~250 tokens when loaded as context"}} -->
# CD triage

- [ ] CI present? — yes → continue; no → cd-basics: install CI first
- [ ] Automated tests covering critical paths? — yes → continue; no → cd-basics: invest in tests
- [ ] Feature flag service in place? — yes → continue; no → cd-basics: install flags
- [ ] IaC for environments? — yes → continue; no → cd-basics: install IaC
- [ ] All four yes → cd-pipelines
