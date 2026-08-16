<!--
purpose: Per-feature RICE decision record — scoring, calculation, rank, decision and required co-signs.
consumes: a scored candidate feature (reach/impact/confidence/effort) from the RICE round (see content/02-output-contract.xml rows)
produces: a RICE decision record
depends-on: content/02-output-contract.xml (rows: reach, impact, confidence, effort, source, rice_score)
token-budget-impact: ~300 tokens when filled
-->

# RICE Decision Record: <feature_name>

## Scoring

| Factor | Score | Rationale |
|--------|-------|-----------|
| Reach | [X] users/quarter | [Analytics query or proxy metric — never "all users"] |
| Impact | [3/2/1/0.5/0.25] | [Which metric moves; why this tier] |
| Confidence | [100%/80%/50%] | [Evidence level; unknowns that caused downgrades] |
| Effort | [X] person-months | [Design + dev + QA + 30% buffer; engineer co-signed] |

## Calculation
RICE = (<r> × <i> × <c>) / <e> = <score>

## Rank
#[X] out of <y> candidates this quarter

## Decision
- [ ] Prioritized for <quarter_sprint>
- [ ] Backlogged for later — reason: [...]
- [ ] Rejected — reason: [...]

## Additional Considerations
- **Dependencies:** [Any features that must ship first]
- **Strategic alignment:** [How this fits current quarter's focus]
- **Risks:** <risks>

## Co-signs Required
- [ ] Engineering co-signed Effort estimate: <name>
- [ ] PM co-signed Impact=3 (if applicable): <name>
