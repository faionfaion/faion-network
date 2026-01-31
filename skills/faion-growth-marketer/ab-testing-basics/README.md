---
id: ab-testing-basics
name: "A/B Testing Basics"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# A/B Testing Basics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | ab-testing-basics |
| **Name** | A/B Testing Basics |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | ab-testing-setup, multivariate-testing, statistical-significance |

---

## Problem

You want to improve your product but do not know what changes will work. You make decisions based on opinions ("I think users will like this") instead of data. Some changes hurt metrics, but you do not know until it is too late.

A/B testing lets you compare two versions of something and measure which performs better. It removes guesswork from decision-making.

---

## Framework

### What is A/B Testing?

A/B testing (also called split testing) is an experiment where you:
1. Show version A to half of users (control)
2. Show version B to half of users (treatment)
3. Measure which version performs better
4. Roll out the winner to everyone

```
         ALL USERS
             │
      ┌──────┴──────┐
      │             │
   50% A         50% B
  (control)   (treatment)
      │             │
  Measure       Measure
  metric        metric
      │             │
      └──────┬──────┘
             │
     Compare results
             │
    Statistical test
             │
    Winner → 100%
```

### A/B Test Lifecycle

```
1. HYPOTHESIS
   What do you believe? Why?
        ↓
2. DESIGN
   What will you change? What will you measure?
        ↓
3. SIZE CALCULATION
   How many users? How long?
        ↓
4. RUN EXPERIMENT
   Split traffic, collect data
        ↓
5. ANALYZE
   Is the difference statistically significant?
        ↓
6. DECIDE
   Ship winner, iterate, or kill
```

### Step 1: Hypothesis

A good hypothesis has three parts:

```
IF we [change X]
THEN [metric Y] will improve
BECAUSE [reason/evidence]
```

**Examples:**

| Bad Hypothesis | Good Hypothesis |
|----------------|-----------------|
| "The new design is better" | "If we simplify the signup form from 6 fields to 3, conversion will increase by 10% because friction decreases" |
| "Users will click more" | "If we change the CTA button from gray to green, CTR will increase by 5% because green stands out more" |

### Step 2: Design

**What to test (one change at a time):**
- Headlines and copy
- Button text, color, position
- Images and visuals
- Layout and flow
- Pricing and offers
- Email subject lines
- Feature presentation

**What to measure (primary metric):**
Choose ONE primary metric that directly measures success.

| Test Area | Primary Metric |
|-----------|---------------|
| Landing page | Signup conversion rate |
| Checkout flow | Purchase completion rate |
| Email | Open rate or click rate |
| Onboarding | Activation rate |
| Pricing page | Plan selection rate |

### Step 5: Analyze Results

**Statistical significance test:**

Calculate if the difference is real or just random chance.

```
Conversion A (control):    10.0% (1,500 / 15,000)
Conversion B (treatment):  11.2% (1,680 / 15,000)
Difference:                +1.2 percentage points (+12% relative)

p-value: 0.012 (< 0.05)
Confidence: 98.8%

RESULT: Statistically significant. B wins.
```

**Interpretation:**

| p-value | Confidence | Decision |
|---------|------------|----------|
| < 0.01 | > 99% | Strong evidence, ship B |
| 0.01 - 0.05 | 95-99% | Good evidence, ship B |
| 0.05 - 0.10 | 90-95% | Weak evidence, consider retest |
| > 0.10 | < 90% | Not significant, do not ship |

### Step 6: Decide

**Outcomes:**

| Situation | Action |
|-----------|--------|
| B wins significantly | Ship B to 100% |
| A wins significantly | Keep A, learn from failure |
| No significant difference | Keep A (simpler), test something else |
| B wins but hurts other metrics | Investigate tradeoffs |

---

## Examples

### Example 1: Signup Page Button

**Hypothesis:** If we change the CTA button from "Sign Up" to "Start Free Trial", conversions will increase by 8% because it emphasizes the free offer.

**Setup:**
- Baseline: 4.5% conversion
- MDE: 8% relative (0.36% absolute)
- Sample needed: ~50,000 per variant
- Duration: 3 weeks

**Results:**

| Variant | Visitors | Signups | Rate |
|---------|----------|---------|------|
| A: "Sign Up" | 52,340 | 2,355 | 4.50% |
| B: "Start Free Trial" | 51,890 | 2,543 | 4.90% |

- Difference: +0.40 pp (+8.9% relative)
- p-value: 0.003
- Confidence: 99.7%

**Decision:** Ship B. The new copy increased signups by ~9%.

### Example 2: Pricing Page Layout

**Hypothesis:** If we highlight the "Pro" plan with a "Most Popular" badge, Pro selections will increase by 15% because social proof influences choice.

**Results:**

| Variant | Visitors | Pro Selected | Rate |
|---------|----------|--------------|------|
| A: No badge | 8,450 | 1,267 | 15.0% |
| B: With badge | 8,380 | 1,424 | 17.0% |

- Difference: +2.0 pp (+13.3% relative)
- p-value: 0.048
- Confidence: 95.2%

**Decision:** Ship B. Marginal significance, but positive direction with good relative lift.

### Example 3: Failed Test

**Hypothesis:** If we add testimonials above the fold, conversions will increase by 10% because social proof builds trust.

**Results:**

| Variant | Visitors | Conversions | Rate |
|---------|----------|-------------|------|
| A: No testimonials | 12,000 | 600 | 5.00% |
| B: With testimonials | 12,200 | 585 | 4.79% |

- Difference: -0.21 pp (-4.2% relative)
- p-value: 0.32
- Confidence: 68%

**Decision:** No significant difference. Keep A (simpler). Hypothesis was wrong - testimonials may have distracted from CTA.

**Learning:** Test testimonial placement below the fold instead.

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Peeking at results | Inflates false positives | Wait for full sample size |
| Testing too many things | Cannot isolate cause | One change per test |
| Sample too small | Unreliable results | Calculate sample size upfront |
| Wrong metric | Optimizing for wrong thing | Choose metric tied to business goal |
| Running forever | Wastes traffic | Set end date based on sample size |
| Ignoring guardrail metrics | Win primary, hurt overall | Always check secondary metrics |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Web testing | Optimizely, VWO, Google Optimize |
| Product testing | LaunchDarkly, Split.io, Statsig |
| Statistics | Custom calculator, Evan Miller |
| Analysis | Mixpanel, Amplitude, Python |

---

## Related Methodologies

- **ab-testing-setup:** A/B Testing Setup (sample size, implementation)
- **multivariate-testing:** Multivariate Testing (testing multiple variables)
- **statistical-significance:** Statistical Significance (deep dive on stats)
- **funnel-optimization:** Funnel Optimization (where to test)

---

*Methodology: ab-testing-basics | Growth | faion-growth-agent*
