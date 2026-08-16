<!-- purpose: Prioritized risk register (high/medium/low) with response and contingency plans per risk. -->
<!-- consumes: risk rows from pre-mortem.md or upstream research artefacts, per AGENTS.md Prerequisites -->
<!-- produces: scored, owned risk register with dashboard-observable trigger metrics -->
<!-- depends-on: content/01-core-rules.xml (single-human-owner-per-risk, top-quartile-rows-carry-trigger-and-dated-mitigation) -->
<!-- token-budget-impact: ~500-1000 tokens when loaded as context -->

## Risk Register: <product_business>

**Last Updated:** <last_reviewed_date>
**Review Cadence:** Monthly (full register) / Weekly (top 3)

### High Priority Risks (Score 6-9)

| ID | Risk | Sub-Category | Prob | Impact | Score | Citation | Status |
|----|------|--------------|------|--------|-------|----------|--------|
| demand-001 | [Risk description] | demand | H | H | 9 | market-research.md#tam-validation | Mitigating |
| comp-001 | [Risk description] | competition | H | M | 6 | competitive-analysis.md#direct-competitors | Monitoring |

### Medium Priority Risks (Score 3-5)

| ID | Risk | Sub-Category | Prob | Impact | Score | Citation | Status |
|----|------|--------------|------|--------|-------|----------|--------|
| pricing-001 | [Risk description] | pricing-commoditization | M | M | 4 | pricing-research.md#competitor-pricing | Accepted |

### Low Priority Risks (Score 1-2)

| ID | Risk | Sub-Category | Prob | Impact | Score | Citation | Status |
|----|------|--------------|------|--------|-------|----------|--------|
| channel-001 | [Risk description] | channel | L | L | 1 | market-research.md#distribution | Accepted |

---

### Response Plans

#### <risk_id>: <risk_name>
**Strategy:** [Avoid / Mitigate / Transfer / Accept]
**Actions:**
1. <specific_action> — Owner: <name> — Trigger: <observable_metric>
2. <specific_action> — Owner: <name> — Trigger: <observable_metric>

**Contingency Plan:**
- **Trigger metric:** [Specific, dashboard-observable — e.g., "ARPU drops below $X for 2 months"]
- **Response:** [Concrete actions, not "monitor the situation"]
- **Resources needed:** [Budget cap, headcount, tooling]
- **Kill/pivot criterion:** [Specific condition that triggers segment exit or major pivot]

**Progress:** <current_status>
