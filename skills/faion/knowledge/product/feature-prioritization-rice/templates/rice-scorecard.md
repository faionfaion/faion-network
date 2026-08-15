<!--
purpose: RICE scorecard skeleton — scores, per-feature rationale, strategic veto, post-ship actuals
consumes: analytics reach estimates + effort breakdown from engineering
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
variables:
  - name: product_name
    type: string
    required: true
    description: The product these features belong to. Scores from two products in one table are not comparable - reach means different populations and effort means different teams.
  - name: quarter
    type: string
    required: true
    description: The planning period this covers, e.g. "Q4 2026". RICE scores only compare inside one period; carrying last quarter's reach forward is how a stale estimate wins a slot it should not.
  - name: source
    type: text
    required: true
    description: Where the reach numbers come from - the analytics query, the report, the proxy metric and why it stands in. Reach is the input people invent most freely, so name the source once for the whole sheet.
  - name: confidence_policy
    type: text
    required: true
    description: What each confidence level means here - what evidence earns 100 percent rather than 50. Without a shared rule, confidence quietly becomes how much the author likes the feature.
  - name: effort_unit
    type: enum
    required: true
    options: [person-days, person-weeks, person-months]
    description: The unit for the effort column, one for the whole sheet. A table mixing days and months produces a ranking that is arithmetically meaningless and looks perfectly reasonable.
  - name: veto_rationale
    type: text
    required: true
    description: If you overrode the ranking, say why - the moat, the contract, the bet RICE cannot encode. Overriding is legitimate; overriding silently is what teaches everyone the scores are theatre.
-->
# RICE Prioritization: {{product_name}} — {{quarter}}

**Reach derived from:** {{source}}
**Confidence scale:** {{confidence_policy}}
**Effort unit:** {{effort_unit}}

## Scores

| Feature | Reach | Impact | Confidence | Effort ({{effort_unit}}) | RICE Score | Rank |
|---------|-------|--------|------------|--------|------------|------|
| [Feature A] | [users/qtr] | 3/2/1/0.5/0.25 | 100%/80%/50% | [effort] | [R×I×C/E] | 1 |
| [Feature B] | [users/qtr] | 3/2/1/0.5/0.25 | 100%/80%/50% | [effort] | [R×I×C/E] | 2 |
| [Feature C] | [users/qtr] | 3/2/1/0.5/0.25 | 100%/80%/50% | [effort] | [R×I×C/E] | 3 |

## Rationale

### [Feature A]
- **Reach:** [How derived from the source above]
- **Impact:** [Which user-facing metric moves, by how much]
- **Confidence:** [Evidence level against the scale above]
- **Effort:** [Breakdown: design, dev, QA, plus buffer]

### [Feature B]
- [Same structure]

## Strategic Veto (if applied)

{{veto_rationale}}

## Post-Ship Actuals (fill in after delivery)

| Feature | Actual Reach | Actual Effort | Variance Note |
|---------|-------------|---------------|---------------|
| [Feature A] | [actual] | [actual] | [what was wrong in the estimate] |
