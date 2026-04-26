# Technical Debt Basics

## Summary

A framework for making technical debt visible, typed, and actionable. Debt items are classified in Martin Fowler's quadrant (deliberate/inadvertent × reckless/prudent) and tracked in a `TECH_DEBT_REGISTER.md` with type, severity, location, evidence, and interest cost. Agents scan for candidates; humans approve before items are registered. Cap the register at 20–30 items.

## Why

Invisible debt accumulates silently into deployment friction, production incidents, and velocity loss. Fowler's quadrant prevents the false binary of "all debt is bad" — prudent-deliberate debt is a legitimate trade-off when logged and paid. Tracking interest cost (hours/week lost) makes debt tangible to stakeholders and enables evidence-based prioritization.

## When To Use

- Sprint/quarterly planning: surface debt before picking payoff items.
- Post-incident review: register the debt that caused the incident with severity and evidence.
- New-codebase onboarding: inventory existing debt before estimating work.
- Feature trade-off: deliberately taking prudent debt and logging it in the same commit.

## When NOT To Use

- Greenfield prototypes likely to be thrown away — registering debt is overhead with no reader.
- Sub-100-line scripts where the debt framework is heavier than the code.
- Code under active full rewrite — log the rewrite, not item-level debt deleted next week.
- Teams with no payoff process — registering debt no one will pay is theatre.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Fowler quadrant, six debt types (code/design/test/doc/infra/process), interest-cost framing. |
| `content/02-tracking.xml` | Register format, measurement metrics (complexity, velocity, operational), agent workflow, prompt patterns, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/TECH_DEBT_REGISTER.md` | Register template with ID, type, severity, location, evidence, interest, estimated payoff. |
| `templates/scan-debt.sh` | Emit candidate debt items as JSONL (complexity via lizard, missing tests, outdated deps). |
