# Communications Management

## Summary

Plan, execute, and monitor stakeholder communications so that the right people receive the right information at the right time. The core artifact is a per-stakeholder communication matrix (needs, format, frequency, owner). Every status report must show the worst metric as the headline, not the average — default-to-green status is the leading communication antipattern.

## Why

Stakeholder surprise is the most common symptom of failed communication management. Status reports that optimise for comfort over accuracy erode trust as soon as reality diverges from the narrative. A communication plan with defined cadences and channel rules prevents both information overload (too many meetings) and information gaps (missing owners, undocumented decisions).

## When To Use

- Bootstrapping a project's communication plan from a stakeholder register
- Designing meeting cadences to minimise load while keeping decisions flowing
- Generating standardised status report and meeting-notes templates across portfolios
- Auditing comms hygiene: too many meetings, missing owners, undocumented decisions
- Routing communications by channel per stakeholder type and message purpose

## When NOT To Use

- Single-stakeholder projects — informal communication is sufficient, the matrix is overkill
- Crisis/incident response — use an incident-management runbook (status page, war room, hourly updates)
- High-trust collocated small teams using ambient awareness — formalising channels can suppress collaboration
- Sales, marketing, or support comms — those are external channels with their own playbooks (CRM, email marketing, ticketing)

## Content

| File | What's inside |
|------|---------------|
| `content/01-plan.xml` | Communication matrix rules, channel selection, meeting cadence design |
| `content/02-status-reporting.xml` | Status report rules, RAG headline policy, action-item extraction, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/comms-plan.md` | Communication plan skeleton: stakeholder matrix, meeting schedule, escalation path |
| `templates/action-extractor.py` | Regex-based action-item extractor from markdown meeting notes |
