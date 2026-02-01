---
id: funnel-basics-framework
name: "Funnel Optimization Framework"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Funnel Optimization Framework

## Metadata

| Field | Value |
|-------|-------|
| **ID** | funnel-basics-framework |
| **Name** | Funnel Optimization Framework |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | funnel-basics-examples, funnel-tactics-basics, funnel-tactics-advanced, aarrr-pirate-metrics, ab-testing-framework, activation-rate |

---

## Problem

Users visit your product but do not convert. They start signing up but do not finish. They sign up but do not activate. At each step, you lose people.

Funnel optimization identifies WHERE users drop off and WHY, then tests changes to improve conversion at each step.

---

## Framework

### What is a Funnel?

A funnel is a sequence of steps users take toward a goal. Each step has fewer users than the previous one.

```
VISITORS         ████████████████████ 10,000  (100%)
                        ↓ 30%
SIGNUPS          ██████ 3,000                 (30%)
                        ↓ 40%
ACTIVATED        ███ 1,200                    (12%)
                        ↓ 25%
CONVERTED        █ 300                        (3%)
```

### The Funnel Optimization Process

```
1. MAP THE FUNNEL
   Define all steps from entry to goal
        ↓
2. MEASURE EACH STEP
   Track conversion rates between steps
        ↓
3. FIND THE BIGGEST DROP
   Identify where most users leave
        ↓
4. DIAGNOSE THE CAUSE
   Understand why users drop off
        ↓
5. GENERATE HYPOTHESES
   Ideas to improve that step
        ↓
6. TEST AND ITERATE
   Run A/B tests, measure impact
        ↓
7. REPEAT
   Move to next biggest drop
```

### Common Funnel Types

#### Marketing Funnel
```
Impression → Click → Landing Page → Signup → Activation → Purchase
```

#### SaaS Funnel
```
Visit → Signup → Onboarding → Activation → Engagement → Conversion → Retention
```

#### E-commerce Funnel
```
Visit → View Product → Add to Cart → Checkout Start → Payment → Confirmation
```

#### Mobile App Funnel
```
App Store → Download → Open → Onboarding → Core Action → Retention → Monetization
```

---

## Step-by-Step Process

### Step 1: Map the Funnel

Define every step from first touch to goal.

**Example - SaaS signup funnel:**

| Step | Description | Event Name |
|------|-------------|------------|
| 1 | Land on homepage | `page_view_home` |
| 2 | Click "Get Started" | `cta_clicked` |
| 3 | View signup form | `signup_form_viewed` |
| 4 | Submit email | `email_submitted` |
| 5 | Verify email | `email_verified` |
| 6 | Complete profile | `profile_completed` |
| 7 | First action | `first_action_completed` |

### Step 2: Measure Each Step

Track users at each step and calculate conversion rates.

```
FUNNEL ANALYSIS: Signup Flow (Last 30 Days)
─────────────────────────────────────────────────
Step                   Users    Conv %    Drop %
─────────────────────────────────────────────────
1. Homepage           10,000    100%      -
2. Click CTA           3,500     35%      65%  ← High drop
3. Signup form         3,200     91%       9%
4. Submit email        2,400     75%      25%  ← Moderate drop
5. Verify email        1,920     80%      20%
6. Profile complete    1,536     80%      20%
7. First action        1,075     70%      30%  ← High drop
─────────────────────────────────────────────────
Overall conversion: 10.75% (1,075 / 10,000)
```

### Step 3: Find the Biggest Drop

Identify the step with the largest absolute or percentage drop.

**Analysis:**

| Step | Users Lost | % of Total Lost |
|------|------------|-----------------|
| 1→2 Homepage to CTA | 6,500 | 73% |
| 2→3 CTA to Form | 300 | 3% |
| 3→4 Form to Submit | 800 | 9% |
| 4→5 Submit to Verify | 480 | 5% |
| 5→6 Verify to Profile | 384 | 4% |
| 6→7 Profile to Action | 461 | 5% |

**Priority:** Step 1→2 (Homepage to CTA click) is the biggest leak.

### Step 4: Diagnose the Cause

**Methods to understand why users drop:**

| Method | When to Use | Example |
|--------|------------|---------|
| Session recordings | See user behavior | Hotjar, FullStory |
| Heatmaps | Find attention areas | Crazy Egg, Hotjar |
| User surveys | Ask directly | Exit surveys, polls |
| User interviews | Deep understanding | 5-10 user calls |
| Analytics | Segment by attribute | Mobile vs desktop |

**Common drop-off causes:**

| Step | Common Causes |
|------|---------------|
| Landing → CTA | Unclear value prop, poor design, slow load |
| CTA → Form | Too many fields, scary commitment |
| Form → Submit | Technical errors, confusing UX |
| Submit → Verify | Email goes to spam, delay |
| Onboarding → Activation | Too complex, no guidance, no value shown |

### Step 5: Generate Hypotheses

Create testable hypotheses for the biggest drop.

**Template:**
```
IF we [change X]
THEN [metric] will improve by [Y%]
BECAUSE [reason based on diagnosis]
```

**Example hypotheses for Homepage → CTA drop:**

1. "If we make the CTA button larger and green, CTR will increase by 15% because it's more visible"
2. "If we add social proof above the fold, CTR will increase by 20% because trust increases"
3. "If we simplify the headline to focus on one benefit, CTR will increase by 10% because clarity improves"

### Step 6: Test and Iterate

Prioritize hypotheses and run A/B tests.

**Prioritization framework (ICE):**

| Hypothesis | Impact | Confidence | Ease | ICE Score |
|------------|--------|------------|------|-----------|
| Larger CTA | 7 | 8 | 9 | 24 | ← Test first |
| Social proof | 8 | 6 | 7 | 21 |
| Simpler headline | 6 | 5 | 8 | 19 |

---

## Templates

### Funnel Analysis Template

```markdown
# Funnel Analysis: [Name]

## Funnel Definition

| Step | Description | Event |
|------|-------------|-------|
| 1 | | |
| 2 | | |
| 3 | | |

## Current Performance (Last 30 Days)

| Step | Users | Conversion | Drop-off |
|------|-------|------------|----------|
| 1 | | 100% | - |
| 2 | | | |
| 3 | | | |

Overall conversion: ____%

## Biggest Leaks

| Priority | Step | Users Lost | % of Total |
|----------|------|------------|------------|
| 1 | | | |
| 2 | | | |

## Diagnosis

### Step [X] Analysis

**What we observed:**
- [Session recording insights]
- [Heatmap insights]
- [Survey feedback]

**Root cause hypothesis:**
[Why users are dropping off]

## Optimization Hypotheses

| # | If we... | Then... | Because... | ICE |
|---|----------|---------|------------|-----|
| 1 | | | | |
| 2 | | | | |

## Test Plan

| Priority | Hypothesis | Metric | Duration |
|----------|------------|--------|----------|
| 1 | | | |
| 2 | | | |
```

### Funnel Review Checklist

```markdown
## Weekly Funnel Review

### Overall Health
- [ ] Overall conversion: ____% (Target: ___%)
- [ ] Trend: [Improving / Stable / Declining]

### Step-by-Step Check
- [ ] Step 1→2: ____% (Target: ___%)
- [ ] Step 2→3: ____% (Target: ___%)
- [ ] Step 3→4: ____% (Target: ___%)

### Segment Analysis
- [ ] Mobile vs Desktop: [Any difference?]
- [ ] New vs Returning: [Any difference?]
- [ ] Traffic source: [Any difference?]

### Active Tests
- [ ] Test 1: [Name] - Day X of Y
- [ ] Test 2: [Name] - Day X of Y

### This Week's Focus
[Which step and what action?]
```

---

## Tools

| Purpose | Tools |
|---------|-------|
| Funnel analytics | Mixpanel, Amplitude, Posthog |
| Session recording | Hotjar, FullStory, LogRocket |
| Heatmaps | Crazy Egg, Hotjar |
| A/B testing | Optimizely, VWO |
| Surveys | Hotjar, Typeform |

---

## Related Methodologies

- **funnel-basics-examples:** Funnel Examples and Benchmarks
- **funnel-tactics-basics:** Quick wins, checklists, stage-specific optimization
- **funnel-tactics-advanced:** Industry-specific, personalization, measurement
- **aarrr-pirate-metrics:** AARRR Pirate Metrics (funnel framework)
- **ab-testing-framework:** A/B Testing Framework (how to test)
- **activation-rate:** Activation Rate Optimization (activation funnel)

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Map funnel metrics and baseline metrics | haiku | Direct query of existing data |
| A/B test hypothesis generation and prioritization | sonnet | Reasoning about impact/confidence/ease |
| Landing page copywriting and design feedback | sonnet | Creative iteration, user psychology |
| Funnel optimization campaign setup | opus | Complex multi-funnel strategy, org-wide impact |
| Free trial flow analysis and recommendations | sonnet | Understanding conversion psychology |
| PLG product strategy and feature design | opus | Architecture decisions, product-market fit |
| Onboarding flow user testing interpretation | sonnet | Qualitative analysis and recommendations |

---

## Sources

- [Funnel Optimization Guide (Mixpanel)](https://mixpanel.com/topics/funnel-analysis/)
- [Conversion Funnel Best Practices (Amplitude)](https://amplitude.com/blog/conversion-funnel-analysis)
- [Funnel Analysis Framework (Reforge)](https://www.reforge.com/blog/retention-engagement-growth-framework)
- [A/B Testing and Funnel Optimization (Optimizely)](https://www.optimizely.com/optimization-glossary/funnel-analysis/)
- [User Funnel Analytics (Heap)](https://heap.io/topics/what-is-funnel-analysis)

---

*Methodology: funnel-basics-framework | Growth | faion-growth-agent*
