<!-- purpose: template for tech-debt-basics (TECH_DEBT_REGISTER.md) -->
<!-- consumes: tech-debt-basics methodology inputs (see AGENTS.md Prerequisites) -->
<!-- produces: filled-in artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: 01-core-rules.xml + tool-runtime in same dir -->
<!-- token-budget-impact: ~200-400 tokens when loaded as context -->

# Technical Debt Register

Cap: 20-30 items. Sort by severity (high → medium → low). Close only after human verification.

## Active Items

### TD-001: [Short title]
- **Type**: code | design | test | doc | infra | process
- **Severity**: high | medium | low
- **Quadrant**: deliberate-reckless | deliberate-prudent | inadvertent-reckless | inadvertent-prudent
- **Location**: `src/path/to/file.py:42`
- **Evidence**: [incident ID / linter rule / churn data / slow-query trace]
- **Interest**: ~X hours/week in [deployment friction / debugging / manual steps]
- **Payoff estimate**: ~Y tokens / complexity: high | medium | low
- **Business impact**: [concrete effect on velocity, incidents, security]
- **Opened**: YYYY-MM-DD

---

## Closed Items

### TD-000: [Title] ✅
- **Closed**: YYYY-MM-DD
- **PR**: #123
- **Verification**: [test metric or operational metric that confirmed fix]
