# Governance — <Project>

_Last reviewed: <date> — re-validate every 30 days._

## Decision Authority

| Decision Type | Authority (named person) | Escalation (named person) | Artifact |
|---------------|--------------------------|---------------------------|----------|
| New requirement | BA Lead | PM | Jira REQ |
| Scope change | Steering Committee Chair | Sponsor | Jira CR |
| Priority change | Product Owner | PM | Backlog |
| Baseline update | BA Lead + PO | PM | Confluence page |

## Change Control

1. Submit CR (Jira "CR" issue type) — link to affected REQ IDs.
2. Impact assessment: T-shirt sizing (S/M/L/XL) against scope, schedule, cost. Mandatory for all CRs.
3. Review by authority from matrix above.
4. Decision: Approve / Reject (with written reason) / Defer (owner + date). No open-ended CRs.
5. Update baseline; link CR → REQ in Jira.

## Communication

| Audience | Information | Format | Frequency | Channel | Feedback mechanism |
|----------|-------------|--------|-----------|---------|-------------------|
| Sponsor | Status, risks | Summary | Weekly | Email | Standing review slot |
| Dev team | Detailed reqs | Full doc | Per sprint | Jira | Refinement questions log |
| Ops | Release plan | Checklist | Pre-release | Slack | Acknowledgment + blockers thread |

## Owners

- Artifact owner: <named person>
- Decision-log owner: <named person>
- Re-validation cadence: 30 days
- Stakeholder contact data: 1Password vault (NOT in this file)
