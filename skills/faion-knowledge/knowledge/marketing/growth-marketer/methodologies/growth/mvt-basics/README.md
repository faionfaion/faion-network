---
id: mvt-basics
name: "Multivariate Testing Basics"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Multivariate Testing Basics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | mvt-basics |
| **Name** | Multivariate Testing Basics |
| **Category** | Growth |
| **Difficulty** | Advanced |
| **Agent** | faion-growth-agent |
| **Related** | mvt-implementation, ab-testing-framework, statistical-significance |

---

## Problem

A/B testing changes one thing at a time. But sometimes you want to test multiple elements simultaneously. Should you test headline A vs B, then button A vs B, then image A vs B? That takes months.

Multivariate testing (MVT) lets you test multiple variables at once and discover which combination works best. You also learn which elements have the biggest impact.

---

## Framework

### What is Multivariate Testing?

Multivariate testing tests multiple variables and their combinations simultaneously.

```
A/B TEST                    MULTIVARIATE TEST
─────────────               ─────────────────
Variable: Button            Variables: Button + Headline + Image

Variants:                   Variants:
A: Blue button              1: Blue + "Sign Up" + Photo A
B: Green button             2: Blue + "Sign Up" + Photo B
                            3: Blue + "Get Started" + Photo A
                            4: Blue + "Get Started" + Photo B
                            5: Green + "Sign Up" + Photo A
                            6: Green + "Sign Up" + Photo B
                            7: Green + "Get Started" + Photo A
                            8: Green + "Get Started" + Photo B

2 variants                  8 variants (2 × 2 × 2)
```

### When to Use MVT vs A/B

| Use A/B Testing When | Use Multivariate When |
|---------------------|----------------------|
| Testing one major change | Testing multiple small changes |
| Limited traffic | High traffic |
| Need quick answer | Can wait longer |
| Big redesign | Optimizing existing page |
| Early-stage product | Mature product |

### Calculating Number of Variants

```
Total variants = (options for var 1) × (options for var 2) × ... × (options for var N)
```

**Example:**

| Variable | Options | Count |
|----------|---------|-------|
| Headline | A, B | 2 |
| Button color | Blue, Green, Red | 3 |
| Image | Photo, Illustration | 2 |
| **Total** | | 2 × 3 × 2 = **12** |

**Warning:** Variants grow exponentially. 4 variables with 3 options each = 81 variants!

### Traffic Requirements

Each variant needs enough traffic to reach statistical significance.

```
Traffic per variant = A/B sample size requirement

Total traffic needed = Traffic per variant × Number of variants

Example:
- 12 variants
- Need 3,000 per variant for significance
- Total: 36,000 users minimum
```

### Types of MVT

#### 1. Full Factorial

Test ALL possible combinations.

**Pros:**
- Complete picture
- Find all interactions

**Cons:**
- Requires massive traffic
- Takes longer

#### 2. Fractional Factorial

Test a subset of combinations using statistical design.

**Pros:**
- Fewer variants needed
- Still captures main effects

**Cons:**
- May miss some interactions
- More complex analysis

**Example (Taguchi method):**
```
Full factorial: 3 variables × 2 options = 8 combinations
Fractional:     Only 4 carefully chosen combinations

Selected combinations still reveal main effects.
```

---

## Statistical Analysis

### Main Effects

Main effect = the average impact of one variable across all combinations of other variables.

```
Main Effect of Variable A = Avg(all with A=B) - Avg(all with A=A)
```

### Interaction Effects

Interaction = when the effect of one variable depends on another variable.

```
Example interaction:
- Green button + "Buy Now" = 12% conversion
- Green button + "Learn More" = 6% conversion
- Blue button + "Buy Now" = 7% conversion
- Blue button + "Learn More" = 9% conversion

Green + "Buy Now" has unexpected synergy.
```

**How to detect:**
If sum of main effects does not equal observed result, there is an interaction.

### Significance Testing

With multiple variants, use Bonferroni correction:

```
Adjusted significance level = 0.05 / number of comparisons

Example with 16 variants:
- 15 comparisons to control
- Adjusted p-value threshold: 0.05 / 15 = 0.0033
```

---

## Traffic Calculator

```
INPUTS:
──────────────────────────────────────────
Number of variables:                 ____
Options per variable:                ____, ____, ____

Total variants = ____ × ____ × ____ =     ____

Baseline conversion:                 ____%
Minimum detectable effect:           ____%
Sample per variant needed:           ____

CALCULATIONS:
──────────────────────────────────────────
Total sample = Variants × Sample per variant
             = ____ × ____ = ____

Daily traffic:                       ____

Duration = Total / Daily = ____ / ____ = ____ days
```

---

## MVT vs Sequential A/B Tests

| Factor | MVT | Sequential A/B |
|--------|-----|----------------|
| Time | Faster (parallel) | Slower (one at a time) |
| Traffic | Higher requirement | Lower per test |
| Interactions | Discovered | Missed |
| Complexity | Higher | Lower |
| Tools | More sophisticated | Simpler |

**Recommendation:**
- Low traffic: Sequential A/B tests
- High traffic: MVT
- Unknown interactions: MVT
- Clear hypothesis: A/B test

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Too many variables | Exponential variants, never enough traffic | Max 3-4 variables |
| Too many options | Same problem | Max 2-3 options per variable |
| Ignoring interactions | Miss important combinations | Always check interaction effects |
| Stopping early | False positives | Wait for full sample size |
| Testing unrelated elements | Cannot learn patterns | Test related elements together |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Web MVT | Optimizely, VWO, Adobe Target |
| Analysis | Python (scipy), R, SPSS |
| Design of Experiments | JMP, Minitab |

---

## Related Methodologies

- **mvt-implementation:** Multivariate Testing Implementation (templates, examples)
- **ab-testing-framework:** A/B Testing Framework (foundation)
- **statistical-significance:** Statistical Significance (how to analyze)
- **funnel-optimization:** Funnel Optimization (what to test)

---

*Methodology: mvt-basics | Growth | faion-growth-agent*
