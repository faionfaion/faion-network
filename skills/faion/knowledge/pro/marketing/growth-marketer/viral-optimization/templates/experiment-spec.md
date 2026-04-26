# K-Factor Experiment: [Name]

## Hypothesis
IF we [change to invite flow / landing page / incentive],
THEN K-factor will increase by [X%]
BECAUSE [mechanism: more share moments / higher conversion / shorter cycle].

## Target Metric
- Primary: K-factor (measured over 28-day rolling window)
- Secondary: i (invites/user), c (conversion rate), cycle_time_p50

## Variants
| Variant | Description |
|---------|-------------|
| Control | [Current state] |
| Treatment | [Proposed change — one change only] |

## Sample Size
- Weekly users entering loop: ______
- Baseline K: ______  (i=____, c=____)
- MDE relative: ____% on c or i (specify which leg)
- n_per_variant: ______  Duration: ______ days

## Anti-Fraud Checks
- [ ] Invitee D7 retention vs organic tracked separately
- [ ] Self-referral IP/device check configured
- [ ] Reward gate: activation required before reward issued

## Decision
Winner declared only when: n >= sample_size AND days >= 14
