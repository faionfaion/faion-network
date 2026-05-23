<!-- purpose: A/B test brief: hypothesis, sample, duration, significance, named owner -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# A/B Test Brief: [Test Name]

## Hypothesis

We believe that [change]
will cause [effect]
because [rationale].

We will measure this by [metric]
and consider it successful if [target].

## Variants

- **Control:** [Current state description]
- **Variant:** [Change description]

## Metrics

- **Primary:** [What we are measuring]
- **Secondary:** [Supporting metrics to verify no regressions]

## Requirements

- Traffic needed: [X] visitors (use sample-size calculator)
- Minimum duration: [X] weeks (cover at least 2 full weekly cycles)
- Statistical significance: 95% (one-sided)
- Minimum detectable effect: [X]%

## Implementation

- [ ] Design approved
- [ ] Development complete
- [ ] QA passed — variant visible on target segments
- [ ] Test launched with correct traffic split
- [ ] Holdback cell configured (5% control post-ship)
- [ ] Results analyzed after minimum sample reached
- [ ] Learning library entry written
