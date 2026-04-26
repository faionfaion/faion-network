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
