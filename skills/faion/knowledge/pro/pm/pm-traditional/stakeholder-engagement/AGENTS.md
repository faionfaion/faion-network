# Stakeholder Engagement

## Summary

Systematic identification, classification, and engagement of everyone who affects or is affected by the project. The core artifact is a YAML-based stakeholder register (power, interest, attitude with evidence, quadrant, cadence, owner) stored in git so that engagement history is a diff log. Attitude assertions without evidence default to "unknown" — optimistic defaults ("supportive") are a known agent failure mode and a trust risk.

## Why

Projects fail when influential stakeholders are missed, misclassified, or over-engaged to the point of fatigue. The Power/Interest grid routes the right level of attention to each quadrant. Static analysis is insufficient — power and interest shift with project phases, org changes, and external events. Without a refresh cadence and a behavioural triangulation step, the register becomes a historical artefact rather than a live management tool.

## When To Use

- Project kickoff for any cross-functional initiative with more than 5 named parties
- Programs with high political risk: M&A, reorgs, regulated rollouts (HIPAA, SOX, GDPR)
- Pre-RFP / vendor selection where the buying committee has hidden influencers (security, procurement, FinOps)
- Multi-stakeholder transformation programs where power and interest shift across phases
- Pair with `communications-management/` so cadence in the register is reflected in the comms plan

## When NOT To Use

- Solo founders or teams under 5 stakeholders — direct conversation beats matrix overhead
- One-off internal hotfixes with no business stakeholder change — RACI is sufficient
- Crisis/incident response — incident command structure replaces engagement plan during a P0
- When stakeholder identification is unsolved — run BA stakeholder-analysis first to populate the register

## Content

| File | What's inside |
|------|---------------|
| `content/01-register.xml` | Register schema, evidence requirement, attitude policy, hidden stakeholder checklist |
| `content/02-engagement.xml` | Quadrant-based engagement strategy, cadence rules, refresh triggers, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/engagement-due.py` | Lists stakeholders overdue for engagement based on register YAML and cadence |
