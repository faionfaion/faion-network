<!-- purpose: Markdown 4-week XP adoption plan with metrics gates. -->
<!-- consumes: see content/02-output-contract.xml inputs for xp-extreme-programming -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# XP Adoption Plan

Duration: 4 weeks.

## Week 1 - Fast CI + TDD seed
- Optimise CI to <10 min (parallel + cache)
- TDD on all new code in feature area X
- Metric: ci_minutes < 10 by end of week

## Week 2 - Trunk-based + pairing
- Short-lived branches (<3d) + feature flags
- Pairing rotation daily (or AI-pair for solos)
- Metric: avg branch age < 2d

## Week 3 - Small releases + customer SLA
- Release cadence <=14 days (target 7)
- Designate customer with 24h SLA
- Metric: release_cadence_days_actual < 14

## Week 4 - Refactor while green + retrospective
- Refactor commit immediately after each green
- Retro: confirm adherence + lasso drift
- Metric: test_coverage delta positive
