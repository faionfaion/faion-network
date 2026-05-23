<!-- purpose: EVM report template: PV, EV, AC, SPI, CPI, EAC, TCPI per period -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# EVM Report: [Project Name] — [Period End]

## Key Measurements

| Metric | Value |
|--------|-------|
| BAC (Budget at Completion) | $[X] |
| PV (Planned Value) | $[X] |
| EV (Earned Value) | $[X] |
| AC (Actual Cost) | $[X] |

## Performance Indices

| Index | Value | Threshold | Status |
|-------|-------|-----------|--------|
| SPI (Schedule Performance Index) | [X.XX] | >= 0.95 GREEN / < 0.85 RED | [G/Y/R] |
| CPI (Cost Performance Index) | [X.XX] | >= 0.95 GREEN / < 0.85 RED | [G/Y/R] |
| TCPI (To-Complete Perf. Index) | [X.XX] | > 1.10 = escalation trigger | [G/Y/R] |

## Variances

| Metric | Value | Meaning |
|--------|-------|---------|
| SV (Schedule Variance) | $[X] | Positive = ahead; negative = behind |
| CV (Cost Variance) | $[X] | Positive = under budget; negative = over |

## Forecasts

| Scenario | EAC | ETC | VAC |
|----------|-----|-----|-----|
| CPI-only (trend continues) | $[X] | $[X] | $[X] |
| CPI x SPI (both persist) | $[X] | $[X] | $[X] |
| Bottom-up ETC | $[X] | $[X] | $[X] |

**Team-endorsed scenario:** [CPI-only / CPI x SPI / Bottom-up] — [one-line rationale]

## Overall RAG: [GREEN / YELLOW / RED]

**Drivers:** [Top 1-3 WBS areas causing variance]

**Linked risks:** [RISK-NN: description]

**Actions required:** [Owner — action — due date]

**Sponsor override note (if softening RED):** [Explicit rationale required]
