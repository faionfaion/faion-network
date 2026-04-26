# Risk Management

## Summary

Risk management is a structured process for identifying, scoring, responding to, and monitoring project uncertainty — including both threats (negative risks) and opportunities (positive risks). Every risk requires a trigger condition, an owner, and an explicit response strategy; risks without triggers are wishes, not plans.

## Why

Without risk management, surprises become crises and budgets have no contingency basis. Probability x Impact scoring with EMV enables defensible contingency reserves. Tracking opportunity-side risks prevents teams from focusing solely on threats and missing upside. A weekly register review cycle converts risk management from a kickoff artifact into a real control mechanism.

## When To Use

- Multi-month delivery where surprises cost real money (more than $10k or two weeks).
- Regulated, safety-critical, or contractual work where an audit trail is required.
- Cross-team programs with technical, vendor, and resource interdependencies.
- Initiatives where a quantitative reserve (contingency) must be defended to finance.
- Programs that exhibited risk failures on prior runs.

## When NOT To Use

- Pure exploratory R&D or spike work — fail-fast learning beats register hygiene.
- Single-developer hobby project; an issue tracker `risk` label is enough.
- Sub-two-week features where ceremony cost exceeds expected loss.
- Pure-Scrum teams already running impediment and retro loops with adequate coverage.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Risk types, P×I matrix, EMV computation, threat and opportunity response strategies |
| `content/02-rules.xml` | Rules for triggers, calibration, opportunity tracking, closing discipline, and agentic workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Risk register table template with all required columns |
| `templates/risk-response-plan.md` | Individual risk response plan template |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/emv.py` | Score a Markdown risk register; exits non-zero on critical untriaged risks |
