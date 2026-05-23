# Scope Change vs Scope Creep Detection

## Summary

**One-sentence:** AI classifier triggered on every Jira/Linear ticket: compares against signed baseline + AC + out-of-scope; routes into in_scope / legitimate_change / creep / ambiguous with cited evidence.

**One-paragraph:** AI-assisted classifier hooked into Jira / Linear / Asana webhooks. Each new ticket is compared against the signed scope baseline (spec + AC + out-of-scope statements), and routed into one of four outcomes: (1) in_scope → accept; (2) legitimate_change → change-control with impact draft; (3) creep → pushback template; (4) ambiguous → PM escalation brief. Every decision cites baseline lines; human can override with logged reason; >20% override rate triggers retraining. Audit log immutable for postmortem.

**Ефективно для:**

- Engagement with signed baseline and Jira/Linear webhook capability
- Distressed-project rescue where sprint planning is disrupted by mid-sprint additions
- Ticket volume ≥5/week justifying automation
- PM with authority to reject creep without escalating each time

## Applies If (ALL must hold)

- Engagement has a signed scope baseline (spec + AC + out-of-scope explicit list)
- Ticketing tool with webhook capability (Jira, Linear, Asana, ClickUp)
- AI tooling allowed for ticket text + spec context
- PM has authority to define routing rules and reject scope creep without escalation each time
- Sprint planning is regularly disrupted by mid-sprint additions

## Skip If (ANY kills it)

- Spec / baseline is implicit or non-existent — define it first
- Vendor / data-residency restrictions prevent ticket text being sent to an LLM — use rules-only triage
- Team explicitly accepts 'everything is in-scope' (T&M billing) — nothing to gate
- Ticket volume <5/week — overhead exceeds benefit

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signed baseline | Markdown | spec + AC + out-of-scope list |
| Webhook credentials | secret | ticket tool |
| LLM access | API key | vendor-approved |
| Routing destinations | config | change-control board, pushback responder, PM inbox |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[scope-management]] | baseline source + change-control process |
| [[project-integration]] | legitimate changes feed integrated plan |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: signed-baseline-as-ground-truth, four-outcome-routing, evidence-citation-required, human-override-with-log, immutable-audit-trail | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_ticket_against_baseline` | sonnet | Bounded judgement with grounded baseline citations |
| `change_impact_draft` | sonnet | For legitimate change, draft impact estimate |
| `pushback_message_draft` | sonnet | Empathetic creep-pushback |
| `ambiguity_escalation_brief` | opus | Cross-input judgement for PM |

## Templates

| File | Purpose |
|------|---------|
| `templates/triage-record.schema.yaml` | Schema for per-ticket triage record |
| `templates/pushback-message.md` | Empathetic creep-pushback message template |
| `templates/change-impact-draft.md` | Change-control input template |
| `templates/weekly-dashboard.md` | Creep-vs-change weekly summary template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/webhook-handler.py` | Receive ticket-created events, invoke classifier, write triage record, route | On ticket creation |
| `scripts/dashboard-rollup.py` | Aggregate weekly counts of creep/change/ambiguous/in-scope per source | Weekly cron |
| `scripts/validate-scope-change-vs-scope-creep-detection.py` | Lint triage records against schema + citation rule | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[scope-management]]
- [[project-integration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
