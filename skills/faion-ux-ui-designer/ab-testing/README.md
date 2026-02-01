---
id: ab-testing
name: "A/B Testing"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# A/B Testing

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #ab-testing #quantitative
- **Agent:** faion-ux-researcher-agent

## Problem

Design decisions based on opinions create debates without resolution. Changes ship without measuring impact. Data is needed to validate design improvements.

## Key Concepts

| Term | Definition |
|------|------------|
| **Control (A)** | Current/original version |
| **Variant (B)** | New version being tested |
| **Conversion** | Desired user action |
| **Statistical significance** | Confidence result is real |
| **Sample size** | Number of users needed |

## When to Use

| Good For | Not Good For |
|----------|--------------|
| Clear metrics (conversion) | Exploring why |
| Enough traffic | Low traffic sites |
| Specific changes | Major redesigns |
| Iterative optimization | Early-stage discovery |

## Process

### Step 1: Form Hypothesis

```
Format:
If we [change], then [metric] will [improve/decrease]
because [reason].

Example:
If we make the CTA button larger and green, then
click-through rate will increase by 10% because
it will be more visible.
```

### Step 2: Define Metrics

**Primary metric:** The main thing you are measuring

**Secondary metrics:** Other impacts to watch

**Guardrail metrics:** Things that should not get worse

### Step 3: Calculate Sample Size

Factors:
- Baseline conversion rate
- Minimum detectable effect
- Statistical power (usually 80%)
- Significance level (usually 95%)

Use sample size calculator.

### Step 4: Implement Test

```
Requirements:
- Random user assignment
- Consistent experience per user
- Proper tracking
- No changes during test
```

### Step 5: Run Test

**Duration:**
- Long enough for sample size
- Full business cycles (week minimum)
- Avoid holidays/anomalies

### Step 6: Analyze Results

Check:
- Statistical significance reached?
- Practical significance?
- Segment differences?
- Guardrail metrics okay?

### Step 7: Make Decision

| Result | Action |
|--------|--------|
| Clear winner | Implement winner |
| No difference | Keep original (simpler) |
| Inconclusive | Extend test or re-test |
| Negative impact | Stop test, investigate |

---

## Templates

### A/B Test Plan Template

```markdown
# A/B Test Plan: [Test Name]

**Date:** [Date]
**Owner:** [Name]
**Status:** [Planning/Running/Complete]

## Hypothesis
If we [change], then [metric] will [improve] by [amount]
because [reason].

## Test Details

| Element | Value |
|---------|-------|
| Page/Feature | [Where] |
| Control | [Current state] |
| Variant | [Changed state] |
| Traffic split | 50/50 |
| Target audience | [Who] |

## Metrics

**Primary:**
- [Metric name]: [Current baseline]

**Secondary:**
- [Metric name]
- [Metric name]

**Guardrails:**
- [Metric that should not worsen]

## Sample Size
- **Required:** [N per variant]
- **Expected duration:** [X days]
- **Based on:** [Calculator assumptions]

## Screenshots/Designs

### Control (A)
[Image or description]

### Variant (B)
[Image or description]

## Timeline
- Design: [Date]
- Development: [Date]
- QA: [Date]
- Launch: [Date]
- Review: [Date]

## Risks
- [Risk 1]
- [Risk 2]
```

### A/B Test Results Template

```markdown
# A/B Test Results: [Test Name]

**Test Period:** [Start] to [End]
**Duration:** [X days]
**Status:** [Complete]

## Summary
**Winner:** [Control/Variant/No clear winner]
**Recommendation:** [Ship/Do not ship/Extend test]

## Results

| Metric | Control | Variant | Change | Significant? |
|--------|---------|---------|--------|--------------|
| [Primary] | [X%] | [Y%] | [+/-Z%] | Yes/No |
| [Secondary] | [X] | [Y] | [+/-Z] | Yes/No |
| [Guardrail] | [X] | [Y] | [+/-Z] | N/A |

## Statistical Details
- **Sample size:** [N] Control, [N] Variant
- **Confidence level:** [X%]
- **P-value:** [X]

## Segment Analysis

| Segment | Control | Variant | Notes |
|---------|---------|---------|-------|
| New users | [X%] | [Y%] | [Notes] |
| Returning | [X%] | [Y%] | [Notes] |
| Mobile | [X%] | [Y%] | [Notes] |

## Insights
- [Key learning 1]
- [Key learning 2]

## Next Steps
- [ ] [Action item]
- [ ] [Action item]

## Screenshots
### Control
[Image]

### Variant
[Image]
```

---

## Examples

### Example 1: CTA Button Test

**Hypothesis:** Changing CTA from "Submit" to "Get Started Free" will increase sign-ups by 15%.

**Results:**

| Metric | Control | Variant |
|--------|---------|---------|
| Click rate | 2.3% | 3.1% |
| Sign-ups | 1.2% | 1.5% |

**Lift:** +35% click rate, +25% sign-ups
**Decision:** Ship variant

### Example 2: No Clear Winner

**Test:** One-column vs. two-column checkout

**Results:**

| Metric | Control | Variant |
|--------|---------|---------|
| Completion | 68.2% | 69.1% |

**Lift:** +1.3% (not statistically significant)
**Decision:** Keep control (simpler, no real difference)

---

## Common Mistakes

1. **Stopping early** - Ending when results look good
2. **Too many variants** - Dilutes traffic
3. **Testing too many things** - Cannot isolate cause
4. **Ignoring segments** - Average hides differences
5. **Forgetting guardrails** - Win on one metric, lose on others

## Statistical Significance

**95% significance:** 5% chance the result is random noise

Larger sample needed when:
- Baseline conversion is low
- Desired lift is small
- Higher confidence required

## Multivariate Testing

Testing multiple changes at once requires exponentially more traffic:
- Button color (2 options) + Headline (3 options) + Image (2 options) = 12 combinations

## Checklist

- [ ] Clear hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Guardrail metrics identified
- [ ] Random assignment working
- [ ] Tracking verified
- [ ] Test running full duration
- [ ] Statistical significance checked
- [ ] Segments analyzed
- [ ] Decision documented
- [ ] Learnings shared

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| User experience testing feedback | sonnet | Analysis required: synthesizing usability testing results |

## Sources

- [Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing](https://experimentguide.com/) - Comprehensive guide by Microsoft researchers
- [Nielsen Norman Group: A/B Testing](https://www.nngroup.com/articles/ab-testing-usability-engineering/) - UX perspective on testing
- [Optimizely Stats Engine](https://www.optimizely.com/optimization-glossary/statistical-significance/) - Statistical significance explained
- [Google Optimize Help Center](https://support.google.com/optimize/) - Practical implementation guide
- [VWO A/B Testing Guide](https://vwo.com/ab-testing/) - Complete methodology and examples