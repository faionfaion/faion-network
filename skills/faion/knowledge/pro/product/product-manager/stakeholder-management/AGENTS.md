# Stakeholder Management

## Summary

Stakeholder management is identifying everyone affected by your product, mapping them by power and interest, and running a systematic engagement cadence. The PM acts as broker — translating between engineering, design, sales, support, and executives — not as a communication bottleneck. The register must encode who makes decisions, not just who gets updates.

## Why

Products fail due to stakeholder misalignment, not technology. Silent stakeholders who block late, executives who are "surprised," and conflicting requirements all share one root cause: no systematic map of who matters, what they fear, and how decisions get made. A register with `decision_rights` and `comms_direction` columns converts political ambiguity into a routable contract.

## When To Use

- PM inherits a product line and needs to know who to talk to before the first 1:1.
- An executive flags being "surprised" — fix is an explicit upward-comms cadence, not more updates.
- A feature crosses 3+ functional silos — the register encodes the brokerage rules.
- Two stakeholders disagree publicly — use power × interest × attitude to choose the right forum.
- Pre-launch GTM coordination: marketing, sales, support, legal must each sign a Ready gate.

## When NOT To Use

- The "stakeholder" is actually a customer — use customer-discovery / Jobs-to-be-Done instead.
- Engineering-only refactor with no business stakeholders — RFC + tech-lead approval suffices.
- The conflict is a strategy disagreement — no comms cadence can paper over a missing strategy; run a strategy session first.
- Solo founder — you are all roles; skip.
- Org dysfunction (dual-hatted execs, unclear decision rights) — the register exposes it but cannot fix it.

## Content

| File | What's inside |
|------|---------------|
| `content/01-stakeholder-framework.xml` | Stakeholder types, Power/Interest grid, engagement levels, 4-step process |
| `content/02-stakeholder-antipatterns.xml` | Common mistakes: silent stakeholders, same message to all, no escalation path |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-register.md` | Register template with name, power, interest, attitude, cadence, decision_rights, comms_direction |
| `templates/communication-plan.md` | Communication matrix and escalation path template |
| `templates/pm-attention-diff.py` | Script flagging mismatch between PM time-spent and stakeholder power × interest |
