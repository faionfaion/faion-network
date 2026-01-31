# LLM Prompts: Funnel Optimization Tactics - Advanced

## Analysis Prompts

### Analyze Funnel Drop-Off Points

```
Analyze the following funnel data and identify the biggest drop-off points:

[PASTE FUNNEL METRICS]

Format your analysis:
1. Identify each step with conversion rate
2. Highlight the 3 biggest drop-offs
3. For each drop-off, suggest 2-3 probable causes
4. Rank by impact (highest drop-off first)
5. Recommend which to address first based on ease vs. impact

Data to provide:
- Users at each step
- Conversion rate per step
- Time to convert per step (if available)
```

### Industry Benchmarking Analysis

```
I'm optimizing a [SaaS/E-commerce/Mobile App] funnel.

Our current metrics:
- [Step 1]: [X]% conversion
- [Step 2]: [X]% conversion
- [Step 3]: [X]% conversion

How do we compare to industry benchmarks? What should we prioritize?

Please analyze:
1. Our metrics vs. industry benchmarks (good/average/poor)
2. Which steps are underperforming
3. Which steps have biggest improvement opportunity
4. Recommended optimization priority
```

### Personalization Opportunity Analysis

```
We have the following user segments:

[DESCRIBE SEGMENTS]
- Segment 1: [Traffic source/behavior/device]
- Segment 2: [Traffic source/behavior/device]
- Segment 3: [Traffic source/behavior/device]

For each segment, analyze:
1. Likely user intent and pain points
2. What messaging resonates most
3. What CTA would be most effective
4. Expected conversion lift (15-40% range)
5. Implementation priority (quick wins first)
```

### Exit Intent Opportunity Assessment

```
Our product: [DESCRIBE PRODUCT]
Target audience: [WHO]
Current homepage → signup conversion: [X]%

Where would exit intent help most?
- What triggers would be most effective? (mouse-leave, idle time, scroll depth)
- What offer would resonate? (discount, free trial, consultation)
- How urgent should the messaging be?
- What's the realistic recovery rate for our product?
- Draft the exit intent copy and CTA
```

## Hypothesis Generation Prompts

### Generate A/B Test Hypotheses

```
Context:
- Product: [PRODUCT NAME]
- Current funnel conversion: [X]%
- Biggest drop-off: [STEP A to STEP B] (-[X]%)
- Target audience: [AUDIENCE]

Generate 10 high-impact hypotheses to test, ranked by ICE score potential.

For each hypothesis, provide:
1. Hypothesis statement: "If we [change what], then [result], because [reason]"
2. Impact score (1-10): How much will this improve conversion?
3. Confidence score (1-10): How likely is this to work?
4. Ease score (1-10): How hard is this to implement?
5. ICE Score: Impact × Confidence × Ease
6. Why this is worth testing
```

### Personalization Segment Ideas

```
Product: [PRODUCT]
Current funnel metrics: [METRICS]

Generate 8 personalization segment ideas for our funnel.

For each segment, provide:
1. Segment name and size (estimated %)
2. Key differentiator (traffic source, device, intent, geography)
3. Unique pain point or motivation
4. Personalized messaging angle
5. Recommended CTA variation
6. Expected conversion lift
7. Implementation complexity (easy/medium/hard)
```

## Copy Generation Prompts

### Generate Exit Intent Copy

```
Product: [PRODUCT NAME]
Current conversion rate: [X]%
Target audience: [AUDIENCE]
Offer: [DISCOUNT/INCENTIVE]

Write compelling exit intent copy that recovers 8-12% of abandoning users.

Include:
- Headline: Grab attention in 2 seconds
- Subheadline: Create urgency or highlight value
- CTA: Action-oriented button copy
- Optional: Small social proof element

Style: [Formal/Casual/Friendly/Urgent]
Tone: [Friendly/FOMO/Value-focused]
Length: Headline (5-8 words), Subheadline (10-15 words), CTA (2-4 words)
```

### Generate Retargeting Email Subject Lines

```
Scenario: Email [1 of 3] in retargeting sequence, sent [TIMING]

Context:
- Product: [PRODUCT]
- User action: [What they did - visited pricing, viewed feature, started signup]
- Email goal: [Re-engage/Social proof/Final conversion]

Generate 5 email subject lines that:
1. Create curiosity or urgency
2. Reference their specific action
3. Avoid spam folder triggers
4. Personalize with first name [if possible]

For each subject line, provide:
- The subject line
- Expected open rate vs. baseline
- Why it works
```

### Generate Personalized Headlines

```
We're personalizing headlines by user segment.

Segment: [NAME]
Characteristics: [WHO THEY ARE]
Pain point: [WHAT THEY STRUGGLE WITH]
Current headline: [CURRENT COPY]

Generate 3 personalized headlines that:
1. Address their specific pain point
2. Show you understand their situation
3. Highlight relevant features/benefits
4. Create desire to learn more

For each headline:
- The headline
- Why it resonates with this segment
- Expected CTR lift
```

## Optimization Planning Prompts

### Create Test Priority Plan

```
We have [N] hypotheses to test but limited resources.

Hypotheses:
[LIST HYPOTHESES WITH ICE SCORES]

Create a testing roadmap that:
1. Prioritizes tests by ICE score (20-30, 15-20, 10-15, <10)
2. Identifies which tests to run immediately
3. Suggests which tests to batch together
4. Estimates total time/resources needed
5. Projects expected cumulative lift

Assume:
- 2 weeks per test (design, implement, run to significance)
- Can run 2 tests in parallel
- Have [TEAM SIZE] people available
```

### Create Retargeting Strategy

```
Situation:
- Product: [PRODUCT]
- Biggest drop-off: [STEP A → STEP B] at [X]%
- Monthly visitors: [NUMBER]
- Estimated abandoners: [NUMBER]
- Current email tool: [TOOL]

Design a retargeting strategy that recovers 10%+ of abandoners.

Include:
1. Email sequence (timing, goals, messaging angles)
2. Ad retargeting strategy (audience, creative, frequency)
3. Metrics to track and targets
4. Expected recovery rate per channel
5. Tech stack needed
6. Timeline to implement
7. Estimated ROI (cost per email vs. average LTV)
```

## Review & Optimization Prompts

### Evaluate Funnel Performance

```
Our current funnel:
- [Step 1]: [X] users, [X]% conversion to Step 2
- [Step 2]: [X] users, [X]% conversion to Step 3
- [Step 3]: [X] users, [X]% conversion to Step 4
- [Step 4]: [X] users (conversions)

Analyze:
1. Overall funnel conversion rate
2. Which step has biggest drop-off
3. Which step has biggest absolute lost value
4. Industry benchmark comparison
5. Top 3 optimization recommendations with projected impact
6. What we should NOT optimize (premature optimization)
```

### Post-Test Learning Capture

```
Test completed: [HYPOTHESIS]

Results:
- Control: [X] conversions, [Y]% conversion rate
- Variant: [X] conversions, [Y]% conversion rate
- Lift: [+X%]
- Statistical significance: [p-value]
- Test duration: [Days]

Help me capture learnings:
1. Why did this test win/lose?
2. What does this tell us about our audience?
3. What should we test next based on this result?
4. Are there other segments we should apply this to?
5. What was the financial impact?
6. What's the next hypothesis to test?
```
