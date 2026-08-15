<!-- __faion_header_v1__ -->
<!-- purpose: Human-readable results report — per-metric table, guardrails, statistical detail, pre-specified segments, learnings -->
<!-- consumes: the experiment-run artefact emitted at close -->
<!-- produces: report -->
<!-- depends-on: content/04-procedure.xml -->
<!-- token-budget-impact: ~350 tokens when loaded as context -->
# A/B Test Results: [Test Name]

**Test Period:** [Start] to [End]
**Duration:** [X days]

## Summary
**Winner:** Control / Variant / No clear winner
**Recommendation:** Ship / Do not ship / Extend test
**Guardrails:** none regressed / [name] regressed — blocks ship regardless of the primary metric
**Signed off by:** [named human — PM or analyst]

## Results

| Metric | Control | Variant | Change | Significant? |
|--------|---------|---------|--------|--------------|
| [Primary] | [X%] | [Y%] | [+/-Z%] | Yes/No |
| [Secondary] | [X] | [Y] | [+/-Z] | Yes/No |
| [Guardrail] | [X] | [Y] | [+/-Z] | N/A |

## Statistical Details
- Sample size: [N] Control, [N] Variant
- Confidence level: [X%]
- P-value: [X]
- Practical significance: [business impact in concrete terms]

## Segment Analysis

Only segments named in the pre-registration are results. Anything else below is exploratory
and carries a multiple-comparison caveat.

| Segment | Control | Variant | Notes |
|---------|---------|---------|-------|
| New users | [X%] | [Y%] | |
| Returning | [X%] | [Y%] | |
| Mobile | [X%] | [Y%] | |

## Key Learnings
- [Learning 1]

## Next Steps
- [ ] [Action item]
