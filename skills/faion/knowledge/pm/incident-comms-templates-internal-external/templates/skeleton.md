<!--
purpose: Four-template bundle: status-page update, customer email, exec brief, internal channel — plus the severity x audience matrix and the token list, each with severity-aware placeholders.
consumes: severity definitions from the incident runbook; status-page components; customer comms list; exec distribution list; incident channel
produces: a filled IncidentCommsBundle matching the JSON Schema in content/02-output-contract.xml
depends-on: templates/header.yaml for frontmatter contract; content/01-core-rules.xml for the rules each template encodes
token-budget-impact: ~600-1000 tokens to fill end-to-end; ~200 to validate
-->

---
version: 0.1.0           # bump on every refresh and after every drill that changes a template
owner: <owner_role>:<owner_full_name>   # never a team
last_reviewed: YYYY-MM-DD
---

# Incident comms bundle — <service>

## Severity x audience matrix (one row per severity in the runbook; the highest severity always includes the status page)

| Severity | Audiences (status_page / customer_email / exec_brief / internal_channel) | First post deadline (min) | Update interval (min) | Post-incident email deadline (h) |
|----------|------|------|------|------|
| P1 | status_page, customer_email, exec_brief, internal_channel | 15 | 30 | 72 |
| P2 | status_page, exec_brief, internal_channel | 30 | 60 | 120 |
| P3 | internal_channel | 60 | 120 | 240 |

## Token list (closed; every double-brace token in a template must be here; a filled instance carries none)

incident_id, state, timestamp, impact, next_update_at, customer_impact, eta, decisions_needed, what_is_being_done, severity, commander, comms_lead, blast_radius, hypothesis, actions, incident_link, next_checkpoint_at, start_at, end_at, fix_applied, postmortem_due

Tokens are written as the name between double braces in the live bundle; this skeleton shows them in angle brackets.

## Template: status page (states in order: Investigating, Identified, Monitoring, Resolved; last_drilled: YYYY-MM-DD)

<state> (<timestamp>): <impact>. We will post the next update by <next_update_at>.

Resolved form: Resolved (<timestamp>): between <start_at> and <end_at> <impact>. <fix_applied>. A post-incident report will be published by <postmortem_due>.

## Template: customer email (no cause, no blame, no internal names, no customer data before Resolved; last_drilled: YYYY-MM-DD)

Subject: <incident_id> service disruption
We are aware of an issue affecting <impact>. Our team is working on it; next update by <next_update_at>. We will share a full report by <postmortem_due>.

## Template: exec brief (exactly five fields, one screen, under 150 words, no technical narrative; last_drilled: YYYY-MM-DD)

Impact: <customer_impact> (customers affected, revenue at risk, SLA credits exposed)
ETA: <eta> or "unknown, next update at <next_update_at>"
Decisions needed from you: <decisions_needed>
In progress: <what_is_being_done>
Next update: <next_update_at>

## Template: internal channel (hypotheses and system names live here only; last_drilled: YYYY-MM-DD)

Sev <severity> | IC <commander> | Comms <comms_lead> | Blast radius: <blast_radius> | Hypothesis: <hypothesis> | In flight (owner per action): <actions> | Channel: <incident_link> | Next checkpoint <next_checkpoint_at>

## Per incident (filled instances; the validator checks each)

- incident_id, severity, declared_at (with timezone), audiences_sent (= the matrix row)
- updates: channel, state (status page), posted_at, minutes_after_declaration, impact, text, component_status_matches_text, next_update_at, review flags (unconfirmed_cause / blame / internal_names / customer_pii all false), approved_by (commander or comms lead)
- internal_post, exec_brief, resolved (start_at, end_at, affected_scope, fix_applied, postmortem_due, post_incident_email_sent_at)
