# Steerco Meeting Playbook

## Summary

**One-sentence:** Structured Steerco playbook (T-7 pre-read pack → T-0 90-min facilitation arc → T+2 decision memo). Pre-read 3 days early; numbered binary asks; cancel if no decisions; ≥50% time on asks.

**One-paragraph:** End-to-end Steering Committee playbook across three phases: T-7 prep pack (pre-read materials, decisions log, asks list — sent 3 business days minimum before the meeting); T-0 facilitation arc (90-min standard agenda: status snapshot ≤30% / asks ≥50% / escalations / next-phase preview); T+2 decision memo (sent within 48h with each ask + decision + rationale + owner + deadline). Calibrated for outsource-PM monthly and product-PM quarterly cadences. Asks must be binary ('approve / reject / defer X by date Y'), not vague guidance.

**Ефективно для:**

- Project ≥1 quarter with named Steerco ≥3 senior stakeholders (sponsor, client lead, vendor lead)
- Regular cadence (monthly OR quarterly) with PM as convener
- Decisions exceeding PM's authority — scope, budget, risk
- Forum where escalations need executive air time in one room

## Applies If (ALL must hold)

- Project has a named Steering Committee with ≥3 senior stakeholders (sponsor, client lead, vendor lead)
- Cadence is regular (monthly OR quarterly) and the PM is the convener
- Project duration ≥1 quarter (Steerco overhead is not worth it on 4-week engagements)
- Decisions worth Steerco-level air time exist (scope, budget, risk above PM's authority)

## Skip If (ANY kills it)

- Forum is decorative — sponsor delegates, no quorum, decisions made elsewhere
- Project is in active rescue → daily war room + ad-hoc exec calls instead
- No decisions outstanding for this cycle — cancel the meeting (rule r3)
- A weekly status report already covers the audience — Steerco would duplicate

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Steerco invite + agenda template | calendar artefact | workspace standing |
| Decisions log | Markdown | running list of past Steerco decisions |
| Asks list | Markdown | open decisions needing Steerco approval |
| Pre-read materials | Markdown + slides | PM + workstream leads |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-integration]] | Integrated status feeds the snapshot slide |
| [[risk-management]] | Escalations source from the risk register |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: preread-3-days-early, ask-list-binary, cancel-if-no-decisions, decision-memo-48h, asks-not-status-time-split | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-preread` | sonnet | Status snapshot + asks list from integrated plan |
| `draft-decision-memo` | sonnet | Per-ask decision + rationale + owner + deadline |
| `audit-asks-form` | haiku | Binary-form check on each ask |

## Templates

| File | Purpose |
|------|---------|
| `templates/agenda-template.md` | Standing Steerco agenda: status snapshot / asks / escalations / next-phase preview |
| `templates/preread-pack.md` | Pre-read pack skeleton: status snapshot + decisions log + asks list |
| `templates/decision-memo.md` | T+2 decision memo: ask / decision / rationale / owner / deadline |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-steerco-meeting-playbook.py` | Validate pre-read timestamp + ask-list shape + memo lag | Pre-meeting; pre-merge |

## Related

- parent skill: `pro/pm/project-manager/`
- [[project-integration]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
