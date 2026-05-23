<!-- purpose: AI Feedback Triage Protocol playbook-step skeleton -->
<!-- consumes: Prerequisites bundle (see AGENTS.md) -->
<!-- produces: artefact conforming to content/02-output-contract.xml (playbook-step) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->


# AI Feedback Triage Protocol — Playbook

_Last reviewed: 2026-05-23 — re-validate every 30 days._

## Owner

`<named person / email / handle>`

## Trigger

`<event / threshold / schedule>` — observable, not 'when needed'.

## Lanes

- hallucination
- refusal
- wrong-tool
- out-of-scope
- cost-spike

## Steps

| # | Name | Input | Owner | Exit criterion | Output location |
|---|------|-------|-------|----------------|------------------|
| 1 | classify | ticket.payload | ml-eng-oncall | lane assigned | `triage/{id}.json` |
| 2 | notify   | triage/{id}.json | ml-eng-oncall | owner ack | PagerDuty |
| 3 | decide   | PagerDuty ack | lane-owner | mitigation decision | `incident/{id}.md` |
| 4 | feedback | incident/{id}.md | ml-eng | golden candidate created | `golden/candidates/` |

## Decision branches

| Signal (observable) | Lane if true | Lane if false |
|---------------------|--------------|---------------|
| `ticket.labels CONTAINS hallucination OR feedback.score < 0.5` | `hallucination` | `out-of-scope` |

## Deviation log

URI: `<https://team.io/playbooks/triage/deviations.log>`. Every deviation requires one-line rationale.
