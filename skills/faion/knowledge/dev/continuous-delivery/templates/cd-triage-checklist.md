<!-- __faion_header_v1__ -->
<!-- purpose: Four-prerequisite CD triage that routes to cd-basics or cd-pipelines and records the choice -->
<!-- consumes: repository state (CI config, test suite, flag service, IaC) -->
<!-- produces: decision-record -->
<!-- depends-on: content/01-core-rules.xml#r7-prereqs-before-pipeline -->
<!-- token-budget-impact: ~250 tokens when loaded as context -->
# CD triage

Run before writing any pipeline YAML. Any unchecked box routes to `cd-basics`.

- [ ] CI present and green on main
- [ ] Automated tests covering the critical paths (not just unit tests on leaves)
- [ ] Feature-flag mechanism in place, flags carrying owner + expiry
- [ ] IaC for every environment the pipeline deploys to

All four checked, and deploy frequency is daily or above → `cd-pipelines`.
All four checked, deploy frequency below weekly → still `cd-basics`; the value is in the cadence, not the YAML.

## Decision record

```
next_methodology: cd-basics | cd-pipelines | skip
reason: <one line naming the missing prerequisite, or why the pipeline is the next action>
```

`skip` is correct when the next child is already known, or CD is out of scope (batch workload,
regulated per-release approval).
