<!--
purpose: Per-stakeholder comms plan template.
consumes: input from methodology
produces: artefact for downstream agent
depends-on: content/02-output-contract.xml
token-budget-impact: ~200-500 tokens when loaded as context
variables:
  - name: project_name
    type: string
    required: true
    description: The project as stakeholders name it, not the internal code name. People forward these documents; a name only the delivery team recognises gets forwarded with a confused note attached.
  - name: pm_name
    type: string
    required: true
    description: The PM who owns this plan and the decisions claimed at the end of it. That last section is an authority claim, and it needs somebody prepared to make it out loud.
  - name: sponsor_role
    type: string
    required: true
    description: The executive sponsor's role as the org chart states it. The one-page brief below is written for this person specifically - written for "leadership" it becomes something nobody reads.
  - name: brief_cadence
    type: enum
    required: true
    options: [weekly, biweekly, monthly, quarterly]
    description: How often the executive brief goes out. Pick the longest interval you can defend - a brief arriving faster than decisions get made trains the reader to skip it, permanently.
  - name: escalation_l1
    type: string
    required: true
    description: Who receives an escalation still unresolved after 24 hours, by name and role. "The director" is not reachable at 18:00 on a Friday; a name with a phone number is.
  - name: decisions_i_own
    type: text
    required: true
    description: The decisions you make without escalating, listed explicitly. This is what stops upward-comms inflation - if you cannot name three, you do not have the authority this plan assumes you have.
-->

# Communication Plan: {{project_name}}

**Owner:** {{pm_name}}

## Communication Matrix

| Stakeholder | What | When | How | Owner |
|-------------|------|------|-----|-------|
| {{sponsor_role}} | Status, decisions, risks | {{brief_cadence}} written brief | 1-page brief (3 sections only) | {{pm_name}} |
| Dev team | Requirements, changes, decisions | Daily | Stand-up | {{pm_name}} |
| Sales team | Features, timeline, PQL definition | Bi-weekly | Email update | {{pm_name}} |
| Customers | Releases, feedback channels | Monthly | Newsletter | Marketing |

## Executive Brief Format (1 page max, 3 sections only)

**Section 1 — What changed (lead with the worst news)**
[What has changed since the last brief — surface bad news here, not in section 3]

**Section 2 — One decision I need from you**
[The single decision {{sponsor_role}} must make, with a clear deadline]

**Section 3 — One risk I am tracking**
[The top risk and the mitigation plan — link to the dashboard, do not repeat data inline]

## Key Messages by Audience

### For Executives
- Focus: Business impact, timelines, risks
- Avoid: Technical details, internal codenames without a gloss
- Format: 1-page brief, link to dashboard for data

### For Technical Team
- Focus: Requirements, decisions, blockers, constraints
- Avoid: Business politics
- Format: Detailed specs, decision log

### For Customers
- Focus: Benefits, how-to, support channels
- Avoid: Internal process
- Format: User-friendly guides, release notes

## Escalation Path

1. Issue raised to {{pm_name}}
2. If unresolved in 24h → {{escalation_l1}}
3. If unresolved in 48h → {{sponsor_role}}

## "I Will Decide" Column

Items {{pm_name}} decides without escalation (listed here to prevent upward-comms inflation):

{{decisions_i_own}}
