<!-- purpose: statistics-application — power analysis -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact aligned with content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Pre-test Power Analysis

## Inputs
- Baseline conversion rate: ____%
- MDE (relative): _____% → MDE (absolute): _____% = baseline × MDE_relative
- Significance level (alpha): 0.05
- Statistical power: 0.80

## Calculation
```
n = 16 × p × (1-p) / MDE_absolute^2

n = 16 × _____ × _____ / _____^2
n = _____ per variant
```

## Required Sample
- Per variant: _____
- Total (2 variants): _____
- Daily eligible traffic: _____
- Days needed: Total / Daily = _____ days

## Notes
- For asymmetric splits, use NormalIndPower().solve_power() in statsmodels
- For revenue/AOV, use bootstrapping instead of this formula
- MDE_absolute = baseline × MDE_relative — confirm which you mean
