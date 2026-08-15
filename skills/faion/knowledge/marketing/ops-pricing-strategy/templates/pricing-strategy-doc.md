<!--
purpose: Pricing strategy doc skeleton — value analysis, competitor scan, model choice, validation plan
consumes: cost model + competitor pricing pages + Van Westendorp survey results
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400-1200 tokens when loaded as context
variables:
  - name: product_name
    type: string
    required: true
    description: The product being priced, as customers say it. One product per document - bundling two into one pricing doc is how the cheaper one ends up subsidising the expensive one invisibly.
  - name: pricing_model
    type: enum
    required: true
    options: [flat, tiered, usage-based, freemium, hybrid]
    description: The model you are committing to. Pick on how the customer's value scales, not on what is easiest to bill - usage-based on a metric the buyer cannot predict is how churn gets designed in.
  - name: value_metric
    type: text
    required: true
    description: The one thing that grows as the customer gets more value - seats, projects, messages, GB. If you cannot name it, no tier boundary below will make sense to the buyer.
  - name: quantified_value
    type: text
    required: true
    description: What a customer gains per month, in their currency, with the arithmetic shown - hours saved times their rate, or the tool this replaces. Guessing here makes every number downstream a guess.
  - name: target_margin
    type: string
    required: true
    description: Target gross margin as a percentage, after support and variable infrastructure. Say what you counted as variable cost - most pricing docs quietly leave support out and report a margin that never arrives.
  - name: survey_n
    type: integer
    required: true
    description: How many people answered the Van Westendorp questions. Under 30 the four thresholds are anecdotes with a chart; give the real number so the reader can weigh them accordingly.
-->
# Pricing Strategy: {{product_name}}

## Value Analysis

**Customer value delivered:**

{{quantified_value}}

**Value metric (what scales with value delivered):** {{value_metric}}

**Our costs:**
- Fixed: [$X/month — hosting, tools, salaries]
- Variable: [$X/customer/month — support, API calls]
- Target gross margin: {{target_margin}}

## Market Research

**Competitor pricing:**

| Competitor | Price | Target Customer | vs. Us |
|------------|-------|-----------------|--------|
| [Name] | [$X/mo] | [Persona] | [Cheaper/Similar/More expensive] |

**Van Westendorp results (N={{survey_n}}):**
- Too cheap threshold: [$X/month]
- Acceptable range: [$X–$Y/month]
- Too expensive threshold: [$Z/month]
- Target price: [$X/month]

## Pricing Model

**Model:** {{pricing_model}}

**Tiers:**

| Tier | Price | Target Customer | Key Features | Limit ({{value_metric}}) |
|------|-------|-----------------|--------------|-------|
| [Name] | [$X/mo] | [Persona] | [Features] | [Limit] |
| [Name] | [$X/mo] | [Persona] | [Features] | Unlimited |

## Validation Plan
- [ ] Survey at least 30 potential customers with the Van Westendorp questions
- [ ] Test with beta users at the target price for 30 days
- [ ] A/B test the landing page (current vs. new pricing)
- [ ] Review conversion rate after 30 days — adjust if below 1% or above 5%
