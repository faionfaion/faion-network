<!--

purpose: Pricing strategy doc skeleton — value analysis, competitor scan, model choice, validation plan
consumes: cost model + competitor pricing pages + Van Westendorp survey results
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400-1200 tokens when loaded as context
-->


# Pricing Strategy: <product_name>

## Value Analysis

**Customer value delivered:**

<quantified_value>

**Value metric (what scales with value delivered):** <value_metric>

**Our costs:**
- Fixed: [$X/month — hosting, tools, salaries]
- Variable: [$X/customer/month — support, API calls]
- Target gross margin: <target_margin>

## Market Research

**Competitor pricing:**

| Competitor | Price | Target Customer | vs. Us |
|------------|-------|-----------------|--------|
| [Name] | [$X/mo] | [Persona] | [Cheaper/Similar/More expensive] |

**Van Westendorp results (N=<survey_n>):**
- Too cheap threshold: <x_month>
- Acceptable range: <x_y_month>
- Too expensive threshold: <z_month>
- Target price: <x_month>

## Pricing Model

**Model:** <pricing_model>

**Tiers:**

| Tier | Price | Target Customer | Key Features | Limit (<value_metric>) |
|------|-------|-----------------|--------------|-------|
| [Name] | [$X/mo] | [Persona] | [Features] | <limit> |
| [Name] | [$X/mo] | [Persona] | [Features] | Unlimited |

## Validation Plan
- [ ] Survey at least 30 potential customers with the Van Westendorp questions
- [ ] Test with beta users at the target price for 30 days
- [ ] A/B test the landing page (current vs. new pricing)
- [ ] Review conversion rate after 30 days — adjust if below 1% or above 5%
