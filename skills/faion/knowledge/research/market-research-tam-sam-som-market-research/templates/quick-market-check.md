<!-- purpose: 15-minute rough TAM/SAM/SOM gut-check with a go/no-go verdict. -->
<!-- consumes: idea description + a quick industry-size search, per AGENTS.md Prerequisites -->
<!-- produces: quick market-check verdict, escalates to market-sizing-report when big enough -->
<!-- depends-on: content/01-core-rules.xml (two-methods-with-recorded-divergence-ratio) -->
<!-- token-budget-impact: ~150-300 tokens when loaded as context -->

## Quick Market Check: <idea> (~15 minutes)

### TAM (rough, top-down)
Industry: <name>
Google search: "<industry> market size <current_year>"
Result: $[X] (Source: <url>, Year: <y>)

### SAM (segment filter)
My segment: [geographic + industry + size constraints]
Estimate: [X]% of TAM = $[X]

### SOM (Year 1 bottom-up)
Target customers (can you name 100?): [X]
Average revenue per customer: $[X]/year
Year 1 SOM: <x_customers> × $[X] = $[X]
Year 3 SOM: <x_customers> × $[X] = $[X]

### Verdict
- [ ] Big enough — SOM Year 3 exceeds $1M
- [ ] Too small — SOM Year 3 below $500K
- [ ] Need more research — top-down and bottom-up diverge more than 2x

### Next step
[If big enough: proceed to full market sizing report]
[If diverged: identify which constraint is driving the gap and investigate]
