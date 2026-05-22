---
slug: write-the-weekly-client-status-report-p4-leadership-update-p6
tier: solo
group: role-project-manager
persona: role-project-manager
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "A single 1-page report: RAG status, delivered/planned, top 3 risks, decisions needed, EVM headline (if pro tier). Generated once a week, scannable in 60 seconds by the reader."
content_id: 4d723b16c2cd223f
methodology_refs:
  - reporting-basics
  - communications-management
  - earned-value-management
  - stakeholder-engagement-advanced
  - raci-matrix
  - notion-pm
  - reporting-dashboards
---

# Write the weekly client status report / leadership update

## Context

A single 1-page report: RAG status, delivered/planned, top 3 risks, decisions needed, EVM headline (if pro tier). Generated once a week, scannable in 60 seconds by the reader.

Tier: **solo**. Complexity: **medium**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Report fits on one page.
- Every domain has a defensible RAG score.
- Decisions section has 1-3 explicit choices with owners.
- Report sent + archived same day.

## Steps

### 1. Pull the inputs

Gather all the source data before writing.

Tasks:
- Pull last week's delivered + planned items.
- Pull the risk register top 3.
- Pull EVM headline numbers if applicable.

Outputs:
- Source data pack.

Decision gate: Advance when the pack covers all required sections.

### 2. Score RAG

Score the project honestly.

Tasks:
- Apply the RAG policy thresholds.
- Set overall RAG plus per-domain (scope / schedule / cost / quality).
- Document why if RAG changed from last week.

Outputs:
- RAG scores.

Decision gate: Advance when every domain has a defensible RAG score.

### 3. Draft the one-pager

Hit the standard report structure.

Tasks:
- Use the audience-appropriate template (client-friendly vs leadership-direct).
- Lead with RAG + decisions needed (not 'work done').
- Keep to one page.

Outputs:
- Draft 1-pager.

Decision gate: Advance when the draft fits one page.

### 4. Decisions section

Make 'decisions needed' explicit.

Tasks:
- List 1-3 decisions the reader must make.
- Frame each as 'decide between X and Y by date Z'.
- Tag the decision owner.

Outputs:
- Decisions section.

Decision gate: Advance when each decision has a binary or trinary choice and an owner.

### 5. Send + log

Ship the report and store it for audit.

Tasks:
- Send via the canonical channel (email / Slack / portal).
- File the report in the client + internal archive.
- Tag any decisions into the decision log.

Outputs:
- Sent report + archive entry.

Decision gate: Required: report sent same day, archived same day.

## Decision points

- Client style vs leadership style — client-friendly downplays internal jargon; leadership-direct names blockers bluntly.
- RAG conservative vs honest — honest beats conservative; reporting 'amber' early earns trust over 'green-until-it-explodes'.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/reporting-basics`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/earned-value-management`
- `pro/pm/pm-traditional/stakeholder-engagement-advanced`
- `pro/pm/project-manager/raci-matrix`
- `solo/pm/pm-agile/notion-pm`
- `solo/pm/project-manager/reporting-dashboards`
