<!--

purpose: RICE scorecard skeleton — scores, per-feature rationale, strategic veto, post-ship actuals
consumes: analytics reach estimates + effort breakdown from engineering
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~300-800 tokens when loaded as context
-->


# RICE Prioritization: <product_name> — <quarter>

**Reach derived from:** <source>
**Confidence scale:** <confidence_policy>
**Effort unit:** <effort_unit>

## Scores

| Feature | Reach | Impact | Confidence | Effort (<effort_unit>) | RICE Score | Rank |
|---------|-------|--------|------------|--------|------------|------|
| [Feature A] | [users/qtr] | 3/2/1/0.5/0.25 | 100%/80%/50% | [effort] | [R×I×C/E] | 1 |
| <feature_b> | [users/qtr] | 3/2/1/0.5/0.25 | 100%/80%/50% | [effort] | [R×I×C/E] | 2 |
| <feature_c> | [users/qtr] | 3/2/1/0.5/0.25 | 100%/80%/50% | [effort] | [R×I×C/E] | 3 |

## Rationale

### [Feature A]
- **Reach:** [How derived from the source above]
- **Impact:** [Which user-facing metric moves, by how much]
- **Confidence:** [Evidence level against the scale above]
- **Effort:** [Breakdown: design, dev, QA, plus buffer]

### [Feature B]
- [Same structure]

## Strategic Veto (if applied)

<veto_rationale>

## Post-Ship Actuals (fill in after delivery)

| Feature | Actual Reach | Actual Effort | Variance Note |
|---------|-------------|---------------|---------------|
| [Feature A] | [actual] | [actual] | [what was wrong in the estimate] |
