---
id: ab-testing-setup
name: "A/B Testing Setup"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# A/B Testing Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | ab-testing-setup |
| **Name** | A/B Testing Setup |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | ab-testing-basics, multivariate-testing, statistical-significance |

---

## Problem

You need to calculate sample sizes, set up experiments correctly, and analyze results reliably. Poor setup leads to invalid tests and wrong decisions.

---

## Framework

### Step 3: Sample Size Calculation

You need enough users to detect a real difference. Too few users = unreliable results.

**Variables:**
- **Baseline conversion rate:** Current performance
- **Minimum detectable effect (MDE):** Smallest improvement worth detecting
- **Statistical significance level (alpha):** Usually 95% (alpha = 0.05)
- **Statistical power:** Usually 80%

**Formula (simplified):**

```
Sample size per variant ≈ 16 × (baseline rate × (1 - baseline rate)) / MDE²
```

**Example:**
- Baseline conversion: 10% (0.10)
- Want to detect 10% relative improvement (MDE = 0.01 absolute)
- Sample needed: 16 × (0.10 × 0.90) / (0.01)² = 14,400 per variant
- Total: 28,800 users

**Quick Reference Table:**

| Baseline | 5% MDE | 10% MDE | 20% MDE |
|----------|--------|---------|---------|
| 1% | 62,000 | 16,000 | 4,000 |
| 5% | 30,000 | 8,000 | 2,000 |
| 10% | 28,000 | 7,000 | 1,800 |
| 25% | 20,000 | 5,000 | 1,300 |
| 50% | 16,000 | 4,000 | 1,000 |

### Step 4: Run the Experiment

**Rules:**
1. **Random assignment:** Users randomly see A or B
2. **No peeking:** Do not check results early and make decisions
3. **Run to completion:** Wait until sample size is reached
4. **One test at a time:** Do not run overlapping tests on same area
5. **Control for time:** Run both variants simultaneously

**Duration calculation:**

```
Test duration = Sample size needed / Daily traffic

Example:
- Need 30,000 users total
- Have 2,000 daily visitors
- Duration: 30,000 / 2,000 = 15 days
```

---

## Templates

### A/B Test Planning Template

```markdown
# A/B Test: [Name]

## Hypothesis
IF we [specific change]
THEN [metric] will improve by [X%]
BECAUSE [reasoning]

## Variants
| Variant | Description |
|---------|-------------|
| A (Control) | [Current state] |
| B (Treatment) | [Changed state] |

## Metrics
- **Primary:** [Main metric]
- **Secondary:** [Additional metrics to monitor]
- **Guardrail:** [Metric that should not go down]

## Sample Size
- Baseline rate: ____%
- Minimum detectable effect: ____%
- Required sample: _____ per variant
- Estimated duration: _____ days

## Traffic Split
[ ] 50/50
[ ] Other: ____

## Start/End Dates
- Start: ____
- End: ____

## Owner
[Name]
```

### A/B Test Results Template

```markdown
# A/B Test Results: [Name]

## Summary
| Metric | Control (A) | Treatment (B) | Difference | p-value |
|--------|-------------|---------------|------------|---------|
| [Primary] | X% | Y% | +Z% | 0.0X |
| [Secondary] | | | | |

## Sample Sizes
- Control: _____ users
- Treatment: _____ users
- Duration: _____ days

## Statistical Significance
- Confidence level: ____%
- Winner: A / B / No winner

## Decision
[ ] Ship B to 100%
[ ] Keep A
[ ] Retest with larger sample
[ ] Iterate and test again

## Learnings
[What did we learn? How does this inform future tests?]

## Next Steps
[Follow-up tests or actions]
```

---

## Implementation Checklist

- [ ] Define clear hypothesis (if/then/because)
- [ ] Choose ONE primary metric
- [ ] Calculate required sample size
- [ ] Set up proper randomization
- [ ] Run test to completion (no early stopping)
- [ ] Check statistical significance
- [ ] Document results and learnings
- [ ] Ship winner or iterate

---

## Sample Size Calculator

```
INPUTS:
────────────────────────────
Baseline conversion rate:    ____% [a]
Minimum detectable effect:   ____% relative [b]
Significance level:          95% (standard)
Power:                       80% (standard)

CALCULATION:
────────────────────────────
Absolute MDE = a × (b/100) = ____% [c]

Sample per variant ≈ 16 × (a × (1-a)) / c²
                   = 16 × (____ × ____) / ____²
                   = ______ users

Total sample needed = ______ × 2 = ______ users

Duration = Total sample / Daily traffic
         = ______ / ______ = ______ days
```

---

## Related Methodologies

- **ab-testing-basics:** A/B Testing Basics (concepts, examples)
- **multivariate-testing:** Multivariate Testing (testing multiple variables)
- **statistical-significance:** Statistical Significance (deep dive on stats)
- **funnel-optimization:** Funnel Optimization (where to test)

---

*Methodology: ab-testing-setup | Growth | faion-growth-agent*

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
