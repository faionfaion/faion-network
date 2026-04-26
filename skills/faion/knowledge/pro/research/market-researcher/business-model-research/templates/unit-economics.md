## Unit Economics: [Product]

### Revenue Metrics
- **ARPU (Monthly):** $[X]
- **ARPU (Annual):** $[X × 12]
- **Effective ARPU (Annual):** $[X × (1 - avg discount) × annual-billing-mix] [required — not list price]
- **Gross margin:** [X]%

### Acquisition Metrics
- **Marketing spend:** $[X]/month
- **Sales spend:** $[X]/month
- **New customers acquired:** [X]/month
- **CAC:** $[X] (= (Marketing + Sales) / New Customers)

### Retention Metrics
- **Monthly gross churn:** [X]% (logo churn — accounts lost)
- **Monthly net churn:** [X]% (revenue churn after expansion)
- **Average customer lifetime:** [1 / churn rate] = [X] months

### LTV Calculation
```
LTV = ARPU × Gross Margin × (1 / Monthly Churn Rate)
    = $[ARPU] × [GM%] × (1 / [churn%])
    = $[X]
```

### LTV/CAC Ratio
```
LTV/CAC = $[LTV] / $[CAC] = [X]:1
Target: 3:1 or higher. Below 3:1 = model at risk.
```

### CAC Payback Period
```
Payback = CAC / (ARPU × Gross Margin)
        = $[CAC] / ($[ARPU] × [GM%])
        = [X] months
Target: under 12 months. Above 18 = capital-intensive risk.
```

### Break-Even Analysis
- Fixed costs: $[X]/month
- Contribution margin per customer: $[ARPU × GM%]/month
- Break-even point: [Fixed costs / Contribution margin] = [X] customers

### Verdict
- [ ] Unit economics work — LTV/CAC above 3, payback under 12 months
- [ ] Need to improve [specific metric] — current value is [X], target is [Y]
- [ ] Model not viable at current CAC/churn — requires structural change
