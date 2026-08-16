<!--

purpose: Pre-registration plan — hypothesis, split, metrics, guardrails, sample size, timeline, risks, frozen before launch
consumes: baseline conversion rate + metric inventory
produces: the `design` block of the experiment-run artefact
depends-on: content/01-core-rules.xml#preregistered-design
token-budget-impact: ~350 tokens when loaded as context
-->


# A/B Test Plan: <test_name>

**Owner:** <owner>
**Status:** Planning / Running / Complete

## Hypothesis
If we <change_description>, then <primary_metric> will improve by <expected_lift> because <reason>.

## Test Details

| Element | Value |
|---------|-------|
| Page/Feature | <surface> |
| Control (A) | <current_state> |
| Variant (B) | <change_description> |
| Traffic split | 50/50 |
| Target audience | <who> |

## Metrics

**Primary:** <primary_metric> — current baseline: <baseline_rate>

**Secondary:**
- <metric_name>

**Guardrails (must not worsen):**
- <metric_name>

## Sample Size
- Required: <required> per variant
- Based on: baseline <baseline_rate>, MDE <expected_lift>, power 80%, significance 95%

## Timeline
- Launch: <date>
- Minimum end: [Date — at least 2 full weeks]
- Review: <date>

## Risks
- [Risk 1 — e.g., holiday traffic anomaly]
- [Risk 2 — e.g., concurrent feature release]

## Decisions Already Made (not open for discussion)
- <decision_1>
