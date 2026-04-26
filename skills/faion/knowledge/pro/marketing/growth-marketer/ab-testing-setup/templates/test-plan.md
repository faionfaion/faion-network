# A/B Test Plan: [Name]

## Hypothesis
IF we [specific change]
THEN [metric] will improve by [X% relative]
BECAUSE [reasoning / evidence]

## Variants
| Variant | Description |
|---------|-------------|
| A (Control) | [Current state] |
| B (Treatment) | [Changed state] |

## Metrics
- **Primary:** [metric name — must tie to business outcome]
- **Secondary:** [additional metrics, informational only]
- **Guardrails:** [metrics that must not regress — watch only]

## Sample Size
- Baseline rate: ____%
- MDE relative: ____%  (absolute: ____pp)
- n_per_variant (statsmodels): ______
- Total sample: ______
- Daily traffic on surface: ______
- Estimated duration: ______ days

## Traffic Split
- [ ] 50/50
- [ ] Other: ____ (justify asymmetric split)

## Schedule
- SRM check configured: [ ]
- A/A test run (1-2 days): [ ]
- Start date: ____
- Pre-committed end date: ____

## Owner
[Name]
