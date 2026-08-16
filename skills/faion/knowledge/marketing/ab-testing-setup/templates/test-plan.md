<!-- purpose: Pre-launch A/B test plan — hypothesis, variants, sample size, schedule, owner. -->
<!-- consumes: hypothesis + candidate metric + baseline rate + MDE (Prerequisites: Brief / inputs) -->
<!-- produces: working document (not the JSON `spec` artefact in content/02-output-contract.xml) -->
<!-- depends-on: content/01-core-rules.xml (rule named-owner) -->
<!-- token-budget-impact: ~250-400 tokens when loaded as context -->

# A/B Test Plan: [Name]

## Hypothesis
IF we <specific_change>
THEN <metric> will improve by <x_relative>
BECAUSE <reasoning_evidence>

## Variants
| Variant | Description |
|---------|-------------|
| A (Control) | <current_state> |
| B (Treatment) | <changed_state> |

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
