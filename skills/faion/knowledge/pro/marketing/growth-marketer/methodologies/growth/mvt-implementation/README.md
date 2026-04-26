---
id: mvt-implementation
name: "Multivariate Testing Implementation"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Multivariate Testing Implementation

## Metadata

| Field | Value |
|-------|-------|
| **ID** | mvt-implementation |
| **Name** | Multivariate Testing Implementation |
| **Category** | Growth |
| **Difficulty** | Advanced |
| **Agent** | faion-growth-agent |
| **Related** | mvt-basics, ab-testing-framework, funnel-optimization |

---

## Templates

### MVT Planning Template

```markdown
# Multivariate Test: [Name]

## Goal
[What are you trying to learn/improve?]

## Variables Being Tested

| Variable | Option A | Option B | Option C |
|----------|----------|----------|----------|
| [Var 1] | | | |
| [Var 2] | | | |
| [Var 3] | | | |

## Variant Matrix

| Variant | Var 1 | Var 2 | Var 3 |
|---------|-------|-------|-------|
| 1 | A | A | A |
| 2 | A | A | B |
| 3 | A | B | A |
| 4 | A | B | B |
| 5 | B | A | A |
| 6 | B | A | B |
| 7 | B | B | A |
| 8 | B | B | B |

## Sample Size
- Variants: ____
- Traffic per variant: ____
- Total traffic needed: ____
- Daily traffic: ____
- Estimated duration: ____ days

## Primary Metric
[Metric you are optimizing]

## Success Criteria
[How you will determine winner]
```

### MVT Results Template

```markdown
# MVT Results: [Name]

## Performance by Variant

| Variant | Var 1 | Var 2 | Var 3 | Conversions | Rate | vs Control |
|---------|-------|-------|-------|-------------|------|------------|
| 1 (ctrl) | A | A | A | X | X% | - |
| 2 | A | A | B | X | X% | +/-X% |
| ... | | | | | | |

## Element Impact Analysis

| Element | Level | Avg Conversion | Impact |
|---------|-------|----------------|--------|
| Var 1 | A | X% | baseline |
| Var 1 | B | X% | +X% |
| Var 2 | A | X% | baseline |
| Var 2 | B | X% | +X% |

## Interactions
[Any significant interactions between variables?]

## Winner
Variant [X]: [Var1 value] + [Var2 value] + [Var3 value]
Conversion: X% (+X% vs control)

## Recommendation
[Ship winner / Further testing needed / etc.]
```

---

## Examples

### Example 1: Landing Page MVT

**Goal:** Optimize landing page conversion

**Variables:**

| Variable | Option A | Option B |
|----------|----------|----------|
| Headline | "Save Time" | "Get More Done" |
| Hero Image | Person photo | Product screenshot |
| CTA Button | "Start Free" | "Try It Now" |
| Testimonial | 1 testimonial | 3 testimonials |

**Variants:** 2 × 2 × 2 × 2 = 16

**Results:**

| Rank | Headline | Image | CTA | Testimonials | Rate |
|------|----------|-------|-----|--------------|------|
| 1 | "Get More Done" | Screenshot | "Start Free" | 3 | 8.2% |
| 2 | "Get More Done" | Screenshot | "Try It Now" | 3 | 7.8% |
| 3 | "Get More Done" | Person | "Start Free" | 3 | 7.5% |
| ... | | | | | |
| 16 | "Save Time" | Person | "Try It Now" | 1 | 4.9% |

**Element Impact:**

| Element | Impact on Conversion |
|---------|---------------------|
| Headline | +1.2% ("Get More Done" wins) |
| Hero Image | +0.8% (Screenshot wins) |
| CTA Button | +0.3% ("Start Free" wins) |
| Testimonials | +0.5% (3 wins) |

**Insight:** Headline has biggest impact. Focus future tests there.

### Example 2: Email Subject Line MVT

**Variables:**

| Variable | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Emoji | None | One emoji | Multiple |
| Personalization | None | First name | Company name |
| Urgency | None | "Today only" | "Last chance" |

**Variants:** 3 × 3 × 3 = 27

**Top 5 Results:**

| Rank | Emoji | Personalization | Urgency | Open Rate |
|------|-------|-----------------|---------|-----------|
| 1 | One | First name | "Last chance" | 32% |
| 2 | One | First name | "Today only" | 29% |
| 3 | None | First name | "Last chance" | 28% |
| 4 | One | Company | "Last chance" | 26% |
| 5 | One | First name | None | 24% |

**Insight:** First name + urgency is the winning combination. One emoji helps but is not critical.

---

## Implementation Checklist

- [ ] Define 2-4 variables to test (no more)
- [ ] Limit options per variable (2-3)
- [ ] Calculate total variants
- [ ] Check traffic requirements
- [ ] Set up proper randomization
- [ ] Run until significance reached
- [ ] Analyze main effects
- [ ] Check for interactions
- [ ] Document learnings

---

## Related Methodologies

- **mvt-basics:** Multivariate Testing Basics (framework, statistics)
- **ab-testing-framework:** A/B Testing Framework (foundation)
- **statistical-significance:** Statistical Significance (analysis)
- **funnel-optimization:** Funnel Optimization (what to test)

---

*Methodology: mvt-implementation | Growth | faion-growth-agent*
