<!-- purpose: Lightweight check (TAM + SOM only) for early ideation -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->
# Quick Market Check: <idea>

## TAM (Rough, ~5 min)
Industry: [X]
Google search: "<industry> market size <year>"
Result: $X (Source: <url>, accessed <date>)

## SAM (Segment, ~5 min)
My segment: [X — describe geography + industry + company size]
Estimate: X% of TAM = $X
Assumption: <why_x>

## SOM (Reality check, ~5 min)
Year 1 target: X customers x $X/year = $X ARR
Year 3 target: X customers x $X/year = $X ARR
Customer count source: <customer_count_source>

## Verdict
- [ ] Big enough (SOM year 3 > $1M ARR) → proceed to full sizing
- [ ] Too small (SOM year 3 < $500K) → explore adjacent market or higher price
- [ ] Need more research → specific unknown: [what is missing]

## Confidence
- TAM source age: <x_months> — <ok_stale>
- Bottom-up customer count: <sourced_estimated>
- Overall: High / Medium / Low
