# Stakeholder Register

## Summary

Identify every person or group who affects or is affected by the project, analyze their influence (power) and interest, classify into Power-Interest quadrants, and define an engagement strategy per quadrant. Store as YAML in source control; generate Markdown view from it. The rule: verify attitude through direct conversation, not inference — written communication is systematically polite and will produce false "Supportive" ratings.

## Why

Projects stall when high-power stakeholders feel bypassed, or when teams waste communication cycles on low-influence parties while ignoring blockers. The Power-Interest grid gives a systematic, evidence-based way to allocate engagement effort. Treat the register as live data — after each stage gate, archive the old version so you can track how perceptions changed.

## When To Use

- Project initiation: before charter sign-off, identify who funds, approves, uses, blocks
- Bid/proposal phase: capture buyer, economic buyer, technical buyer, end users
- Cross-functional rollout (pricing change, ToS update, new platform) with regulatory and legal stakeholders
- Agency engagements: register both client-side and agency-side stakeholders
- After a reorg or M&A where the old register is stale

## When NOT To Use

- Fully internal personal-tool project with only you and your manager
- Pure agile team building for itself with one PO and no external dependencies
- Pre-discovery exploration where stakeholders are not yet defined — do problem framing first

## Content

| File | What's inside |
|------|---------------|
| `content/01-stakeholder-framework.xml` | Five-step process, Power-Interest quadrant strategies, engagement cadence rules |
| `content/02-stakeholder-data.xml` | YAML schema, agent gotchas, privacy/PII handling rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholders.yaml` | YAML register schema with id, influence, impact, attitude, comms, last_touch |
| `templates/stakeholder-profile.md` | Individual stakeholder profile: interests, concerns, engagement history |
