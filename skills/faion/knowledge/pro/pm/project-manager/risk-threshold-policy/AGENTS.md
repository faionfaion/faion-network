---
slug: risk-threshold-policy
tier: pro
group: project-manager
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d33f8f6d8b611986"
summary: Pre-agreed policy that defines which risk severity gets escalated to whom, when, and via which channel — closing the gap between "log the risk" and "act on the risk".
tags: [risk-management, escalation, project-manager, governance, communication]
---

# Risk Threshold Policy

## Summary

**One-sentence:** Pre-agreed escalation policy mapping risk severity (probability × impact) to a named escalation target, channel, and SLA — so PMs do not invent the escalation path mid-incident.

**One-paragraph:** Risk-register methodology covers identification, scoring, and tracking, but stays silent on the question that matters when a risk turns red: who do I tell, by when, and in what channel? Without a pre-agreed threshold policy, PMs either (a) escalate everything (steering-committee fatigue, lost credibility), (b) escalate too late (last-minute surprises, board-level blame), or (c) escalate to the wrong person (stakeholder mis-routing). This methodology pins a Risk Threshold Policy: a single document per engagement (or per portfolio) that lists each severity band, the named escalation owner per band, the channel (1:1 ping, email summary, scheduled meeting, board memo), the response SLA (1h, 24h, 1 week), and the de-escalation criteria. Mechanism: pre-agree once at engagement kickoff with the sponsor + delivery lead + PMO; refresh at major milestones. Primary output: a `risk-threshold-policy.yaml` co-signed by sponsor + delivery lead.

## Applies If (ALL must hold)

- engagement ≥4 weeks OR portfolio with multiple concurrent projects
- distinct stakeholder tiers exist (e.g. client champion, client sponsor, agency partner, PMO)
- risk register is in use (`pro/pm/project-manager/risk-register-refresh-30min` or similar)
- sponsor is named and available for the policy co-sign

## Skip If (ANY kills it)

- single-stakeholder engagement (one client, one decision-maker) — escalation is trivial, log it informally
- engagement &lt;2 weeks — overhead exceeds value
- sponsor refuses to sign a threshold policy — the policy needs sponsor buy-in to function; raise the issue before delivery starts

## Prerequisites

- risk register exists with a defined severity scale (e.g. 1-5 × 1-5 = 1-25)
- stakeholder map with named roles (`pro/ba/business-analyst/stakeholder-analysis`)
- communication channels enumerated (email, Slack, scheduled steering, exec memo)
- PMO or governance approver who can co-sign

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/risk-register-refresh-30min` | Defines the severity scale this policy maps to |
| `pro/ba/business-analyst/stakeholder-analysis` | Provides the named roles the policy escalates to |
| `pro/pm/project-manager/escalation-conversation-template` | The runbook for how to deliver the escalation once routed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit severity bands, named target per band, SLA per band, de-escalation criteria, co-signed policy | ~1000 |
| `content/02-output-contract.xml` | essential | risk-threshold-policy.yaml schema, severity-mapping table, channel taxonomy | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: over-escalation, under-escalation, channel mismatch, stale policy, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `policy_draft_from_stakeholder_map` | sonnet | Combine stakeholder roles + severity scale into proposed routing |
| `severity_assessment_per_risk` | sonnet | Score new risk against the policy and produce the escalation recommendation |
| `escalation_message_draft` | sonnet | Draft the actual ping / email / memo from the risk + audience |
| `policy_lint` | haiku | Verify schema + co-signatures |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-threshold-policy.schema.yaml` | Schema for the policy document |
| `templates/escalation-message.md` | Pre-formatted message templates per channel (Slack, email, memo) |
| `templates/quarterly-refresh-checklist.md` | Cadence checklist for policy review |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/lint-policy.py` | Validate policy against schema + signature presence | Pre-commit hook on the policy file |
| `scripts/route-risk.py` | Given a risk + current policy, output the recommended escalation tuple (owner, channel, SLA) | Daily risk-register refresh |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `risk-register-refresh-30min`, `escalation-conversation-template`, `stakeholder-analysis`
- external: [PMBOK 7 — risk management](https://www.pmi.org/pmbok-guide-standards) · [APM Body of Knowledge — escalation](https://www.apm.org.uk/body-of-knowledge/)
