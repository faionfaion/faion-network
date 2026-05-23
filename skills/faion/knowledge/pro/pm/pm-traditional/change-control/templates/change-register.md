<!-- purpose: Change register template with CR ID, requestor, decision, baseline impact -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Change Register: [Project Name]

**Last Updated:** [Date]

| CR ID | Date | Requester | Description | Priority | +Days | +Cost | Decision | Authority | Decision Date | Reason Code |
|-------|------|-----------|-------------|----------|-------|-------|----------|-----------|---------------|-------------|
| CR-001 | [Date] | [Name] | [Description] | High | +3 | $1.5k | Approved | PM | [Date] | — |
| CR-002 | [Date] | [Name] | [Description] | Low | +2 | $1k | Rejected | PM | [Date] | Out-of-scope |
| CR-003 | [Date] | [Name] | [Description] | High | +8 | $4k | Under Review | Sponsor | — | — |

**Reason codes for rejections:** Out-of-scope / Deferred-to-phase-2 / Duplicate / Too-costly / Business-value-insufficient

## Cumulative Impact of Approved CRs

| Metric | Original Baseline | Approved CR Impact | Current Baseline |
|--------|-------------------|--------------------|-----------------|
| Schedule | [X days] | +[X days] | [X days] |
| Cost | $[X] | +$[X] | $[X] |

Run `scripts/cr_drift.sh` to recompute from the register table.
