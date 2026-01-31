# Checklist

## Planning Phase

- [ ] Define hypothesis and success metric
- [ ] Determine minimum sample size needed
- [ ] Calculate required duration based on baseline rate
- [ ] Decide on control (A) vs treatment (B) variant
- [ ] Plan traffic allocation (50/50, 90/10)
- [ ] Set significance threshold (typically 0.05)
- [ ] Document guardrail metrics to protect

## Assignment Phase

- [ ] Implement experiment assigner (hash-based, stable)
- [ ] Use consistent user ID (no reassignment)
- [ ] Configure variant traffic split
- [ ] Test assignment is deterministic
- [ ] Verify no selection bias in assignment
- [ ] Test bucketing across multiple days

## Tracking Implementation Phase

- [ ] Implement exposure tracking (when user sees variant)
- [ ] Deduplicate exposure events
- [ ] Implement conversion tracking
- [ ] Add custom metrics if needed
- [ ] Track experiment metadata (variant, timestamp)
- [ ] Send events to analytics system
- [ ] Verify events are being recorded

## Monitoring Phase

- [ ] Track enrollment numbers (exposures) per variant
- [ ] Monitor conversion rates trending up/down
- [ ] Check for data quality issues
- [ ] Monitor for technical issues affecting variant
- [ ] Set up alerts for anomalies
- [ ] Track guardrail metrics continuously

## Analysis Phase

- [ ] Calculate conversion rate per variant
- [ ] Calculate confidence intervals
- [ ] Run statistical significance test (z-test)
- [ ] Calculate relative lift (% improvement)
- [ ] Calculate power and sample size achieved
- [ ] Document statistical assumptions met

## Validation Phase

- [ ] Verify significance level (p-value < 0.05)
- [ ] Check statistical power (typically 80%+)
- [ ] Check for multiple testing issues
- [ ] Analyze segmented results (by cohort)
- [ ] Check for novelty effects
- [ ] Validate that guardrails not violated

## Decision Phase

- [ ] Review all metrics and guardrails
- [ ] Check for external factors affecting test
- [ ] Get stakeholder sign-off on results
- [ ] Document decision rationale
- [ ] Plan rollout if winner identified
- [ ] Schedule cleanup if no winner

## Deployment Phase

- [ ] Gradually roll out variant to 100% if winner
- [ ] Monitor metrics during rollout
- [ ] Keep monitoring post-rollout for regressions
- [ ] Document learnings from experiment
- [ ] Update success metrics baseline
- [ ] Archive experiment data and analysis