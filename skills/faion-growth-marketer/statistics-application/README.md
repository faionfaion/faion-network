---
id: statistics-application
name: "Statistical Significance: Application"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Statistical Significance: Application

## Metadata

| Field | Value |
|-------|-------|
| **ID** | statistics-application |
| **Name** | Statistical Significance: Application |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | statistics-basics, ab-testing-framework |

---

## Templates

### Significance Calculation Template

```markdown
# Statistical Significance Check

## Test: [Name]

## Raw Data
| Variant | Sample Size | Conversions | Rate |
|---------|-------------|-------------|------|
| A (Control) | | | |
| B (Treatment) | | | |

## Difference
- Absolute: B rate - A rate = _____%
- Relative: (B - A) / A × 100 = _____%

## Statistical Test
- Test type: Two-proportion z-test
- Z-score: _____
- P-value: _____
- 95% CI for difference: [_____, _____]

## Conclusion
[ ] p < 0.05 → Statistically significant
[ ] p >= 0.05 → NOT significant

## Recommendation
[Ship B / Keep A / Need more data]
```

### Pre-Test Power Analysis Template

```markdown
# Sample Size Calculation

## Inputs
- Baseline conversion rate: ____%
- Minimum detectable effect: _____% relative (_____% absolute)
- Significance level: 95%
- Power: 80%

## Calculation
n = 16 × p × (1-p) / MDE²
n = 16 × _____ × _____ / _____²
n = _____ per variant

## Total Sample Needed
- Per variant: _____
- Total (both variants): _____

## Duration Estimate
- Daily traffic: _____
- Days needed: Total / Daily = _____ days
```

---

## Examples

### Example 1: Significant Result

**Test:** New checkout button color

| Variant | Visitors | Purchases | Rate |
|---------|----------|-----------|------|
| A: Gray | 15,000 | 450 | 3.00% |
| B: Green | 15,000 | 525 | 3.50% |

**Calculation:**
- p_pooled = 975/30000 = 0.0325
- SE = 0.0129
- z = (0.035 - 0.030) / 0.0129 = 2.93
- p-value = 0.003

**Result:**
- p < 0.05 → Statistically significant
- 95% CI: [0.17%, 0.83%]
- Confident B is better

**Decision:** Ship green button

### Example 2: Not Significant (Need More Data)

**Test:** Headline change

| Variant | Visitors | Signups | Rate |
|---------|----------|---------|------|
| A: "Save Time" | 2,000 | 100 | 5.0% |
| B: "Work Smarter" | 2,000 | 110 | 5.5% |

**Calculation:**
- p_pooled = 0.0525
- SE = 0.0158
- z = 0.32
- p-value = 0.75

**Result:**
- p > 0.05 → NOT significant
- 95% CI: [-2.6%, +3.6%]
- CI includes 0 → cannot conclude difference

**Decision:** Need ~10,000 per variant to detect this difference

### Example 3: Underpowered Test

**Setup:**
- Expected baseline: 10%
- Expected lift: 5% relative (0.5% absolute)
- Actual sample: 500 per variant

**Power calculation:**
- Needed sample: 16 × 0.10 × 0.90 / 0.005² = 57,600 per variant
- Actual sample: 500
- Actual power: ~6%

**Problem:** Only 6% chance of detecting a real effect. Test was essentially useless.

---

## Significance Calculator

```
INPUTS:
─────────────────────────────────────────
Sample A (n1):           _____
Conversions A (x1):      _____
Conversion rate A (p1):  _____%

Sample B (n2):           _____
Conversions B (x2):      _____
Conversion rate B (p2):  _____%

CALCULATIONS:
─────────────────────────────────────────
Difference = p2 - p1 = _____%

Pooled rate = (x1 + x2) / (n1 + n2) = _____

SE = sqrt(pooled × (1-pooled) × (1/n1 + 1/n2))
   = sqrt(_____ × _____ × _____)
   = _____

Z-score = Difference / SE = _____

P-value (two-tailed) = _____

95% CI = Difference ± 1.96 × SE
       = [_____, _____]

RESULT:
─────────────────────────────────────────
[ ] Significant (p < 0.05)
[ ] Not significant (p >= 0.05)
```

---

## Tools

| Purpose | Tools |
|---------|-------|
| Calculators | Evan Miller, ABTestGuide |
| Analysis | Python (scipy.stats), R |
| Testing platforms | Optimizely, VWO, Statsig |
| Bayesian | Optimizely Stats Engine, VWO SmartStats |

---

## Related Methodologies

- **statistics-basics:** Statistical Significance: Basics (concepts, formulas, theory)
- **ab-testing-framework:** A/B Testing Framework (how to run tests)
- **multivariate-testing:** Multivariate Testing (testing multiple variables)
- **cohort-analysis:** Cohort Analysis (segmenting results)

---

*Methodology: statistics-application | Growth | faion-growth-agent*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Pull analytics data from Mixpanel, format report | haiku | Data extraction and formatting |
| Analyze A/B test results for statistical significance | sonnet | Statistical analysis and interpretation |
| Generate cohort retention curve analysis | sonnet | Data interpretation and visualization |
| Design growth loop for new product vertical | opus | Strategic design with multiple levers |
| Recommend optimization tactics for viral coefficient | sonnet | Metrics understanding and recommendations |
| Plan AARRR framework for pre-launch phase | opus | Comprehensive growth strategy |
| Implement custom analytics event tracking schema | sonnet | Technical setup and validation |
