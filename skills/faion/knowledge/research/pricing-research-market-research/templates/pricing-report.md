<!-- purpose: Full pricing research report — value analysis, competitor analysis, Van Westendorp synthesis, recommended tiers, validation plan and risk assessment. -->
<!-- consumes: customer-value math + competitor price matrix + Van Westendorp survey results, per AGENTS.md Prerequisites -->
<!-- produces: pricing research report feeding content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml (value-anchored, vw-min-30, tier-feature-distribution, billing-model-named) -->
<!-- token-budget-impact: ~700-1300 tokens when loaded as context -->

# Pricing Research Report: <product>

## 1. Value Analysis

**Core value delivered:**
| Value type | Quantified impact | Calculation |
|------------|------------------|-------------|
| Time saved | [X] hours/week | X hrs x $rate x 4 wks = $X/mo |
| Money saved/earned | $X/month | <method> |
| **Total monthly value** | **$X/mo** | |

**Value-based price ceiling:**
- Category: <category>
- Capture rate applied: <capture_rate_applied>%
- Price ceiling: $X/mo

---

## 2. Competitor Analysis

| Competitor | Free? | Entry | Mid | Pro/Enterprise | Notes |
|------------|-------|-------|-----|----------------|-------|
| <name> | Y/N | $X/mo | $X/mo | $X/mo or "contact" | <model_notes> |

Competitor processing order: randomized (prevents anchoring)
Sales-led tiers: marked as "negotiated" — excluded from median calculations

**Market range:**
- Low end: $X/mo
- Median: $X/mo
- Premium: $X/mo

---

## 3. Customer Research (Van Westendorp)

N respondents: <n_respondents> — must be >= 30 for synthesis. If < 30, skip synthesis, record raw quotes only.

| Question | Median response |
|----------|----------------|
| Too expensive | $X |
| Expensive but worth it | $X |
| Good deal | $X |
| Too cheap | $X |
| **Optimal price point** | **$X** |

**Interview quotes:**
- "<quote_about_pricing>"
- "<quote_about_value>"

---

## 4. Recommended Pricing

**Billing model:** <billing_model>
**Rationale:** [Why this model fits the usage pattern]

| Tier | Price | Target user | Key differentiator | Upgrade trigger |
|------|-------|-------------|-------------------|-----------------|
| Starter | $X/mo | [Who] | [Feature] | <what_forces_upgrade> |
| Pro | $X/mo | [Who] | [Feature] | |
| Enterprise | Custom | [Who] | [Feature] | |

Annual pricing: $X/yr = monthly x 10 (= 2 months free)
Grandfather policy: [honor current price for 12 months on increase]

---

## 5. Validation Plan

- [ ] A/B test pricing page (track conversion by tier)
- [ ] Track upgrade rate from Starter to Pro (target: >15%)
- [ ] Interview churned customers on price sensitivity
- [ ] Review and adjust at 90-day mark

---

## 6. Risk Assessment

| Risk | Mitigation |
|------|------------|
| Priced too low | Start at upper band; discount with annual |
| Priced too high | 14-day trial + money-back guarantee |
| Wrong model | Monitor usage patterns; pivot at 90-day review |
| Wrong tier structure | Track which tier gets most upgrades |
