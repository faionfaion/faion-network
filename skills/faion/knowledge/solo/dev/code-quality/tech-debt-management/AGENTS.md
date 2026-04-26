# Technical Debt Management

## Summary

Prioritization and payoff strategy for technical debt using a scoring formula (Impact × Risk × Interest / Cost), four execution strategies (Boy Scout, feature-attached, dedicated sprint, Strangler Fig), and CI/pre-commit gates to prevent accumulation. The concrete rule: track debt as labels on existing feature tickets, never in a separate backlog — separate backlogs are where debt goes to die.

## Why

Unprioritized debt reduces velocity non-linearly: high-complexity, high-churn files cause disproportionate bugs and slow down every adjacent feature. Git-history hotspot analysis (files changed often AND most complex) identifies the 20% of debt that causes 80% of friction. Automated quality gates (complexity check, duplication, TODO-ticket enforcement) prevent accumulation at zero marginal cost.

## When To Use

- Sprint planning where engineering velocity has visibly decayed and the team disagrees on which debt to address
- Onboarding a new codebase where debt is undocumented and needs triage
- Setting up CI quality gates and pre-commit hooks on a fresh project
- Planning a Strangler Fig migration of a legacy module
- Deciding payoff strategy per debt item (Boy Scout vs dedicated sprint vs Strangler Fig)

## When NOT To Use

- Greenfield codebase younger than 6 months: focus on prevention (linters, tests, ADRs), not payoff
- Codebase you intend to replace in less than 3 months: paying debt on a doomed system is sunk cost
- During an outage or launch crunch: debt management requires calm and capacity
- Solo project with no other contributors: most frameworks optimize for team coordination overhead you don't have

## Content

| File | What's inside |
|------|---------------|
| `content/01-prioritization.xml` | Priority score formula; pay-now/pay-soon/pay-later tiers; sprint allocation heuristics |
| `content/02-strategies.xml` | Boy Scout, feature-attached, dedicated sprint, Strangler Fig with concrete code examples |
| `content/03-prevention.xml` | CI quality gates (complexity, coverage, TODO enforcement); pre-commit config |

## Templates

| File | Purpose |
|------|---------|
| `templates/quality-gates.yml` | GitHub Actions workflow: complexity, coverage, duplication, dep audit, TODO count |
| `templates/check-debt-comments.py` | Pre-commit hook: enforces TODO(TICKET-ID) format on all debt markers |
| `templates/debt-hotspots.sh` | Bash: cross-reference git churn with lizard complexity to find top-20 debt targets |
