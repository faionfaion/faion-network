# Stakeholder Management

## Summary

Stakeholder management identifies everyone affected by a product (end users, decision makers, influencers, builders, support, external), maps them on a Power/Interest grid with an explicit attitude column (Supporter/Neutral/Resistor), assigns a named owner and engagement cadence per stakeholder, and codifies approval gates so agents can block SDD transitions until named approvers sign off.

## Why

Products fail due to stakeholder misalignment, not technology — silent resistors in the "Manage Closely" quadrant kill projects without appearing in any risk log. A Power/Interest grid without the attitude dimension is a 2D map of a 3D problem. Forcing one named owner per relationship and a concrete cadence (not "ad-hoc") converts a ceremony document into an executable engagement plan.

## When To Use

- Cross-functional product launch with 5+ named stakeholders where misalignment has already cost time once.
- Re-org or PM handover: dump every stakeholder relationship into a register so the incoming PM can start without rediscovery.
- Roadmap quarter start: refresh the grid, decide which stakeholders move from Inform to Partner for upcoming bets.
- An SDD feature has a named approval gate (legal, security, head of sales) — codify it so the executor agent blocks until the approver signs off.
- Building a multi-agent comms pipeline where status-bot, release-notes-bot, and executive-summary-bot all pull audience from a shared register.

## When NOT To Use

- Solo founder pre-revenue with only customers and family — a 5-line note in the project README is sufficient.
- Internal dev-tools used by under 10 engineers in the same Slack channel — async stand-up + RFC comments cover it.
- Crisis/incident mode: run incident-management first, restore service, update the register post-mortem.
- When the problem is "we don't know who's doing what work" — use raci-matrix or WBS, not this.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Stakeholder types, Power/Interest grid, engagement levels (Partner/Involved/Informed/Monitor), 4-step process |
| `content/02-templates-and-examples.xml` | Stakeholder register columns, communication plan matrix, meeting template, SaaS feature launch example, solo product example |
| `content/03-rules-and-gotchas.xml` | Attitude-column rule, one-owner rule, named cadence rule, decision-log pairing, register-rot prevention, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Stakeholder register with name/role/interest/power/attitude/engagement/owner columns and detailed profiles |
| `templates/communication-plan.md` | Communication matrix, key messages by audience, escalation path |
| `templates/meeting-template.md` | Stakeholder update meeting agenda: progress, decisions needed, risks, action items |
| `templates/stakeholder-lint.py` | Lint stakeholder register for rot patterns: unknown attitudes, missing owners, high-power under-engagement |
