<!-- purpose: Multi-persona pre-mortem exercise converting imagined failure branches into scored risks and mitigations. -->
<!-- consumes: a project/launch scope, per AGENTS.md Prerequisites -->
<!-- produces: consolidated failure modes converted into risk-register rows with mitigation owners -->
<!-- depends-on: content/01-core-rules.xml (risk-phrased-as-cause-event-consequence) -->
<!-- token-budget-impact: ~400-800 tokens when loaded as context -->

## Pre-Mortem: <project_launch>

### Setup
Imagine it is [future date, 12 months from now] and this project has FAILED completely.
Run with 3 agent personas: (1) skeptical customer, (2) well-funded competitor, (3) regulator or platform owner.
Each persona writes independently; consolidate outputs — do not average them.

### Failure Branch 1 — Segment Did Not Materialize
<skeptical_customer_persona>
What caused demand to be absent or too small?

### Failure Branch 2 — Competitor Won
[Well-funded competitor persona]
What did the competitor do to capture the segment?

### Failure Branch 3 — Price Elasticity Broke the Model
[Skeptical customer or regulator persona]
What caused the pricing model to fail (WTP collapse, commoditization, platform rule change)?

---

### Consolidated Failure Modes

| Failure Mode | Personas | Sub-Category |
|--------------|----------|--------------|
| [Mode 1] | [persona names] | [demand/competition/pricing/trend/channel] |
| <mode_2> | [persona names] | <sub_category> |

### Risk Conversion

| Failure Mode | Risk Statement | Prob | Impact | Trigger Metric |
|--------------|----------------|------|--------|----------------|
| [Mode 1] | [As a risk row] | H/M/L | H/M/L | <observable_metric> |

### Mitigation Actions

| Risk ID | Mitigation | Owner | Budget Cap |
|---------|------------|-------|------------|
| <id> | <specific_action> | <name> | <x> |

### Go / No-Go Decision
After review:
- [ ] Proceed with mitigations listed above
- [ ] Delay until <specific_condition>
- [ ] Cancel segment entry
