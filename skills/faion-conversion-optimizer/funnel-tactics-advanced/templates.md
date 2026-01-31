# Templates: Funnel Optimization Tactics - Advanced

## Personalization Strategy Template

```
## Segment: [Name]
- **Definition:** [Who are they?]
- **Traffic source/Behavior/Device/etc:** [Differentiator]
- **Personalization:** [What changes]
- **Expected lift:** [15-40%]

### Messaging
- **Headline:** [Personalized headline]
- **CTA:** [Personalized call-to-action]
- **Offer:** [Segment-specific offer if any]

### Implementation
- **Tool:** [Analytics platform, CDP, etc]
- **Rules:** [If X then show Y]
```

## Exit Intent Configuration Template

```javascript
// Exit Intent Implementation Template
exitIntentManager.configure({
  triggers: {
    mouseLeaveViewport: true,
    idleTime: null,
    scrollDepth: null
  },

  exclusions: {
    ifAlreadyConverted: true,
    ifAlreadyDismissed: true,
    ifCookie: 'exit-intent-shown'
  },

  offer: {
    title: "[Your compelling offer]",
    description: "[Value proposition]",
    cta: {
      text: "[Action button]",
      url: "/[destination]"
    },
    discount: "[10% off, $100 credit, free trial]",
    urgency: "[Limited time, today only]"
  },

  styling: {
    position: "center",
    animation: "fadeIn",
    backgroundColor: "#[color]"
  },

  tracking: {
    onShow: () => analytics.track('Exit Intent Shown'),
    onConvert: () => analytics.track('Exit Intent Converted'),
    onDismiss: () => analytics.track('Exit Intent Dismissed')
  }
});
```

## Retargeting Email Sequence Template

```
## Email Sequence: [Campaign Name]

### Email 1: Immediate (Sent within 24 hours)
**Subject:** [Personalized subject]
**Goal:** Re-engage, remind of value
**Copy:**
- Opening: [Acknowledge action taken]
- Body: [Specific value they'll miss]
- CTA: [Single clear action]
- Offer: [None or minimal]

**Metrics Target:** 15-20% open rate, 3-5% CTR

### Email 2: Day 1-3
**Subject:** [Create urgency]
**Goal:** Provide social proof
**Copy:**
- Opening: [New angle/proof]
- Body: [Customer success story or testimonial]
- CTA: [Same as Email 1 but stronger]
- Offer: [Small discount or incentive]

**Metrics Target:** 18-22% open rate, 5-8% CTR

### Email 3: Day 5-7
**Subject:** [Final call]
**Goal:** Convert with strong offer
**Copy:**
- Opening: [Last chance framing]
- Body: [Strongest incentive]
- CTA: [Urgent action required]
- Offer: [Significant discount or bonus]

**Metrics Target:** 15-18% open rate, 8-12% CTR

### Overall Sequence Metrics
- Target recovery rate: 10-15% of recipients
- Unsubscribe rate: <0.5%
- Complaint rate: <0.1%
```

## ICE Scoring Worksheet

```
## Hypothesis Prioritization - ICE Framework

| # | Hypothesis | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score | Priority |
|---|-----------|---------------|-------------------|-------------|-----------|----------|
| 1 | [Test description] | [Score] | [Score] | [Score] | [Result] | [Tier] |
| 2 | [Test description] | [Score] | [Score] | [Score] | [Result] | [Tier] |

**Scoring Guide:**
- **Impact:** How much will this improve conversion? (1=minimal, 10=transformational)
- **Confidence:** How confident are we this will work? (1=guess, 10=very confident)
- **Ease:** How easy is this to implement? (1=very hard, 10=trivial)

**Priority Tiers:**
- 20-30: Test immediately
- 15-20: Test this quarter
- 10-15: Test if resources available
- <10: Backlog
```

## Analytics Event Tracking Template

```javascript
// Funnel tracking events

// Step 1: Awareness
analytics.track('Homepage Viewed', {
  trafficSource: utm_source,
  device: 'mobile|desktop|tablet',
  timestamp: new Date()
});

// Step 2: Interest - CTA Interaction
analytics.track('CTA Clicked', {
  ctaText: '[Button text]',
  ctaLocation: 'hero|navbar|footer|sidebar',
  device: 'mobile|desktop',
  section: '[Page section]'
});

// Step 3: Consideration - Form Viewed
analytics.track('Signup Form Viewed', {
  formType: 'email|oauth|phone',
  device: 'mobile|desktop',
  entryPoint: '[Where they came from]'
});

// Step 4: Decision - Signup Complete
analytics.track('Signup Completed', {
  method: 'google|email|password|phone',
  planSelected: 'free|starter|pro',
  signupTime: '[Time taken]'
});

// Step 5: Activation - Onboarding Start
analytics.track('Onboarding Started', {
  planType: 'free|paid',
  flow: 'guided|self-serve',
  completionTime: '[Time taken]'
});

// Step 6: Usage - Core Action
analytics.track('First Action Completed', {
  actionType: '[Specific action]',
  timeToAction: '[Minutes from signup]',
  planType: 'free|paid'
});
```

## A/B Test Specification Template

```
## Test: [Hypothesis Name]

### Hypothesis
If we [change what], then [expected outcome] because [reasoning].

### Control vs. Variant
- **Control:** [Current version description]
- **Variant:** [New version description]
- **Only change:** [Single variable]

### Success Metrics
- **Primary:** [Main KPI to measure]
- **Secondary:** [Supporting metrics]
- **Target lift:** [Expected improvement %]

### Sample Size & Duration
- **Control sample:** [Number of users]
- **Variant sample:** [Number of users]
- **Minimum duration:** [Days to run]
- **Statistical significance:** p < 0.05

### Implementation
- **Tool:** [A/B testing platform]
- **Audience:** [Who gets the variant]
- **Tracking:** [Events to track]

### Decision Criteria
- **Win if:** [Variant outperforms by X%]
- **Loss if:** [Control outperforms by X%]
- **Inconclusive:** [What happens if unclear]

### Post-Test
- [ ] Document results
- [ ] Implement winner if +[X%]
- [ ] Archive learnings
- [ ] Plan next test
```
