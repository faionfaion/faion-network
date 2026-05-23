# Risk Threshold Policy

## Summary

**One-sentence:** Pre-agreed escalation policy mapping risk severity bands to named target + channel + SLA; co-signed by sponsor + delivery lead + PMO; explicit de-escalation criteria per band.

**One-paragraph:** Pre-agreed escalation policy that maps risk severity (probability × impact) to a named escalation target, channel, and SLA — so PMs do not invent the escalation path mid-incident. Single document per engagement co-signed by sponsor + delivery lead + PMO at kickoff; refresh at every milestone or every 12 weeks. Bands MUST be discrete (3-5 explicit bands), targets MUST be named individuals (not group inboxes), SLAs MUST be explicit (red ≤2h, amber ≤24h, green = weekly digest), de-escalation criteria MUST be defined per band. Primary output: risk-threshold-policy.yaml co-signed.

**Ефективно для:**

- Engagement ≥4 weeks OR portfolio with multiple concurrent projects
- Distinct stakeholder tiers exist (client champion, sponsor, agency partner, PMO)
- Risk register is in use with a defined severity scale
- Sponsor is named and available for the policy co-sign

## Applies If (ALL must hold)

- Engagement ≥4 weeks OR portfolio with multiple concurrent projects
- Distinct stakeholder tiers exist (client champion, client sponsor, agency partner, PMO)
- Risk register is in use with defined severity scale
- Sponsor is named and available for the policy co-sign

## Skip If (ANY kills it)

- Single-stakeholder engagement — escalation is trivial
- Engagement <2 weeks — overhead exceeds value
- Sponsor refuses to sign — raise the issue before delivery starts

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Risk register | YAML / Markdown | with defined severity scale |
| Stakeholder map | YAML | with named roles |
| Communication channels | list | email, Slack, scheduled steering, exec memo |
| Co-signer authority | named persons | PMO or governance approver |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[risk-register]] | Defines the severity scale this policy maps to |
| [[stakeholder-register]] | Provides named roles the policy escalates to |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit-severity-bands, named-target-per-band, sla-per-band, de-escalation-criteria, co-signed-policy | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `policy_draft_from_stakeholder_map` | sonnet | Combine stakeholder roles + severity scale into proposed routing |
| `severity_assessment_per_risk` | sonnet | Score new risk against policy; produce escalation recommendation |
| `escalation_message_draft` | sonnet | Draft actual ping / email / memo from risk + audience |
| `policy_lint` | haiku | Schema + co-signatures check |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-threshold-policy.schema.yaml` | Schema for the policy document |
| `templates/escalation-message.md` | Pre-formatted message templates per channel (Slack, email, memo) |
| `templates/quarterly-refresh-checklist.md` | Cadence checklist for policy review |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/lint-policy.py` | Validate policy against schema + signature presence | Pre-commit on policy file |
| `scripts/route-risk.py` | Given a risk + current policy, output recommended escalation tuple | Daily risk-register refresh |
| `scripts/validate-risk-threshold-policy.py` | Schema lint + named-target + SLA + de-escalation rule check | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[risk-register]]
- [[stakeholder-register]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
