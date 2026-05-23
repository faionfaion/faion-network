<!-- purpose: Rubric for impact + interest scores (1-5 anchored examples). -->
<!-- consumes: see content/02-output-contract.xml inputs for tech-debt-budget-for-solos -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-700 tokens when loaded as context -->

# Scoring Rubric

## Impact (cost-of-living-with-it)
- 1 = trivial annoyance (cosmetic)
- 2 = slows one task slightly
- 3 = recurring slowdown across multiple tasks per week
- 4 = blocks a roadmap item or a known incident path
- 5 = customer-visible bug or compliance risk

## Interest (rate-of-decay)
- 1 = stable; no compounding
- 2 = slow drift; quarterly noticeable
- 3 = monthly noticeable
- 4 = compounds across cycles; growing faster
- 5 = days-scale runaway (e.g. metrics rotting; data-quality decay)
