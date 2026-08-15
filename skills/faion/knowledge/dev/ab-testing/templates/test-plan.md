<!--
purpose: Pre-registration plan — hypothesis, split, metrics, guardrails, sample size, timeline, risks, frozen before launch
consumes: baseline conversion rate + metric inventory
produces: the `design` block of the experiment-run artefact
depends-on: content/01-core-rules.xml#preregistered-design
token-budget-impact: ~350 tokens when loaded as context
variables:
  - name: test_name
    type: string
    required: true
    description: Short name for the test, naming the change and the surface - "checkout-single-page". It will be quoted in the results post six weeks from now, when nobody remembers the ticket number.
  - name: owner
    type: string
    required: true
    description: The one person who decides to stop, extend or ship this. Not the squad - a test with a committee owner runs until somebody gets bored of it.
  - name: surface
    type: string
    required: true
    description: The page or feature the change lives on, as users would find it. If the change touches more than one surface, you are running more than one test.
  - name: change_description
    type: text
    required: true
    description: What variant B actually does differently, concrete enough to build from. "Improved copy" is not a change; "replaces the three-step checkout with one page" is.
  - name: primary_metric
    type: string
    required: true
    description: The single metric that decides this. One - if you name two, you will pick whichever moved and the pre-registration was theatre.
  - name: baseline_rate
    type: string
    required: true
    description: The primary metric's current value with the window it was measured over ("3.1 percent over the last 28 days"). Sample size depends on it, so a guess here quietly invalidates the whole plan.
  - name: expected_lift
    type: string
    required: true
    description: The minimum detectable effect you are powering for, as a relative or absolute change. Ask what improvement would be too small to bother shipping, and set it just above that.
-->
# A/B Test Plan: {{test_name}}

**Owner:** {{owner}}
**Status:** Planning / Running / Complete

## Hypothesis
If we {{change_description}}, then {{primary_metric}} will improve by {{expected_lift}} because [reason].

## Test Details

| Element | Value |
|---------|-------|
| Page/Feature | {{surface}} |
| Control (A) | [Current state] |
| Variant (B) | {{change_description}} |
| Traffic split | 50/50 |
| Target audience | [Who] |

## Metrics

**Primary:** {{primary_metric}} — current baseline: {{baseline_rate}}

**Secondary:**
- [Metric name]

**Guardrails (must not worsen):**
- [Metric name]

## Sample Size
- Required: [N] per variant
- Based on: baseline {{baseline_rate}}, MDE {{expected_lift}}, power 80%, significance 95%

## Timeline
- Launch: [Date]
- Minimum end: [Date — at least 2 full weeks]
- Review: [Date]

## Risks
- [Risk 1 — e.g., holiday traffic anomaly]
- [Risk 2 — e.g., concurrent feature release]

## Decisions Already Made (not open for discussion)
- [Decision 1]
