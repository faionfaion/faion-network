---
slug: scope-change-vs-scope-creep-detection
tier: pro
group: project-manager
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c94aad50476dc06c"
summary: AI-assisted classifier that triages every new ticket as legitimate change (→ change-control process) vs scope creep (→ structured pushback) by comparing against the baseline spec, with Jira/Linear webhook integration.
tags: [scope-creep, change-control, project-manager, ai-classifier, jira, linear]
---

# Scope Change vs Scope Creep Detection

## Summary

**One-sentence:** AI-assisted classifier triggered by every Jira/Linear ticket creation that decides whether the new work is a legitimate scope change (route to change-control) or scope creep (route to structured pushback), using the signed scope baseline as ground truth.

**One-paragraph:** Scope-management methodology defines change-control theory; scope-creep playbooks are reactive runbooks for a project already in trouble. Neither covers the operational gap in the middle: triaging the steady drip of new tickets, half of which are legitimate changes and half of which are creep. This methodology pins an AI-assisted classifier hooked into Jira / Linear / Asana webhooks. Each new ticket is compared against the signed scope baseline (spec + AC + out-of-scope statements), a Push/Pull/Habit/Fear-style force diagnosis is applied, and the ticket is routed into one of four outcomes: (1) in-scope, accept; (2) legitimate change, send to change-control with impact draft; (3) creep, send back to requester with the "we agreed X" template; (4) ambiguous, escalate to the PM for judgement. Mechanism: webhook → classifier → labelled ticket → routing automation. Primary output: a per-ticket triage record + a weekly creep-vs-change dashboard.

## Applies If (ALL must hold)

- engagement has a signed scope baseline (spec + AC + out-of-scope explicit list)
- ticketing tool with webhook capability (Jira, Linear, Asana, ClickUp)
- AI tooling allowed for ticket text + spec context (vendor approval if needed)
- PM has authority to define routing rules and reject scope creep without escalation each time
- distressed-project rescue is desired OR sprint planning is regularly disrupted by mid-sprint additions

## Skip If (ANY kills it)

- spec / baseline is implicit or non-existent — define it first; the classifier has no ground truth
- vendor / data-residency restrictions prevent ticket text being sent to an LLM — use rules-only triage
- team explicitly accepts "everything that comes in is in-scope" (T&M billing model) — there is nothing to gate
- ticket volume &lt;5/week — overhead exceeds benefit; route manually

## Prerequisites

- signed scope baseline as a machine-readable document (markdown spec + acceptance criteria + out-of-scope list)
- webhook integration credentials for the ticket tool
- LLM access for classification (vendor-approved)
- routing destinations: change-control board, pushback responder, PM inbox

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/scope-creep-management-playbook` | The reactive playbook this gate prevents needing |
| `pro/ba/business-analyst/scope-creep-parking-lot-protocol` | Complementary BA-side mechanism during demos |
| `pro/pm/project-manager/change-control-process` | Where legitimate changes route to |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: signed baseline as ground truth, four-outcome routing, evidence citation, human override, audit trail | ~1000 |
| `content/02-output-contract.xml` | essential | Triage record schema, classifier output, dashboard fields | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: stale baseline, false-positive creep, requester-relationship damage, classifier hallucination, etc. | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_ticket_against_baseline` | sonnet | Bounded judgement with grounded context |
| `change_impact_draft` | sonnet | For "legitimate change" outcome, draft the impact estimate |
| `pushback_message_draft` | sonnet | For "creep" outcome, draft empathetic pushback |
| `ambiguity_escalation_brief` | opus | For ambiguous tickets, frame the decision for the PM |
| `dashboard_rollup` | n/a | Pure aggregation |

## Templates

| File | Purpose |
|------|---------|
| `templates/triage-record.schema.yaml` | Schema for per-ticket triage |
| `templates/pushback-message.md` | Empathetic creep-pushback message template |
| `templates/change-impact-draft.md` | Change-control input template |
| `templates/weekly-dashboard.md` | Creep-vs-change weekly summary |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/webhook-handler.py` | Receive ticket-created events, invoke classifier, write triage record, route | On ticket creation |
| `scripts/dashboard-rollup.py` | Aggregate weekly counts of creep/change/ambiguous/in-scope per source | Weekly cron |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `scope-creep-management-playbook`, `change-control-process`, `scope-creep-parking-lot-protocol`, `scope-drift-early-warning-metrics`
- external: [PMBOK 7 — change management](https://www.pmi.org/pmbok-guide-standards) · [Atlassian — Jira automation](https://www.atlassian.com/software/jira/automation) · [Linear API](https://developers.linear.app/)
