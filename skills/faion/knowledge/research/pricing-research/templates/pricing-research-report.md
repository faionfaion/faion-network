<!--
purpose: Pricing research report — value analysis, competitor scan, Van Westendorp, recommended tiers
consumes: value model + competitor pricing pages + survey and interview results
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400-1200 tokens when loaded as context
variables:
  - name: product_name
    type: string
    required: true
    description: The product being priced, as customers name it. One product per report - two in one document means the cheaper one quietly subsidises the other and nobody notices for a year.
  - name: value_calculation
    type: text
    required: true
    description: The arithmetic behind the value claim - hours saved times their hourly rate, or the named tool this replaces and its price. Show the working; a value number without it is a wish.
  - name: van_westendorp_n
    type: integer
    required: true
    description: How many people answered the four price questions. Below 30 the thresholds are anecdotes drawn as a chart - state the real number so the reader can discount them properly.
  - name: interview_n
    type: integer
    required: true
    description: How many pricing interviews back the quotes below. Two enthusiastic quotes from a sample of two is the most common way a pricing report talks a team into the wrong number.
  - name: pricing_model
    type: enum
    required: true
    options: [subscription, one-time, usage-based, hybrid]
    description: The model recommended. Choose on how the buyer's value scales, not on billing convenience - usage-based on a metric the buyer cannot forecast is churn designed in from day one.
  - name: annual_discount
    type: string
    required: true
    description: Annual discount as a percentage, and say what it costs you in months free. It is the lever people set by feel; write the number so the margin impact is visible in the same document.
-->
## Pricing Research: {{product_name}}

### Value Analysis

**Value calculation:**

{{value_calculation}}

- Target capture (10-20% of delivered value): [$X – $Y/month]

### Competitor Analysis

| Competitor | Entry | Mid | Pro | Annual discount | Notes |
|------------|-------|-----|-----|-----------------|-------|
| [Name] | [$X/mo] | [$X/mo] | [$X/mo] | [X%] | [Model notes] |

**Market range:**
- Low end: [$X/month]
- Mid market: [$X/month]
- Premium: [$X/month]

### Customer Research

**Van Westendorp results (N={{van_westendorp_n}}; 30 is the minimum for significance):**
- Too expensive: [$X]
- Expensive but worth it: [$X]
- Good deal: [$X]
- Too cheap: [$X]
- **Optimal price point:** [$X]

**Interview insights (N={{interview_n}}):**
1. "[Quote about pricing expectations]"
2. "[Quote about perceived value]"

### Recommended Pricing

**Model:** {{pricing_model}}

**Tier structure:**

| Tier | Price | Target segment | Key differentiator |
|------|-------|----------------|-------------------|
| Starter | [$X/mo] | [Who] | [1 key feature] |
| Pro | [$X/mo] | [Who] | [1 key feature] |
| Enterprise | Custom | [Who] | [Dedicated support + SLA] |

**Annual discount:** {{annual_discount}}

### Validation Plan
- [ ] A/B test the pricing page (at least 1,000 visitors per variant)
- [ ] Track conversion rate by tier for the first 30 days
- [ ] Interview 5 churned customers about pricing

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Priced too low | Start high; discount available; review in 90 days |
| Priced too high | 14-day trial; money-back guarantee |
| Wrong model | Monitor usage patterns; plan quarterly review |
