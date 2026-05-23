# Alert Noise Budget

## Summary

**One-sentence:** Produces a weekly noise-budget report per service and a list of alerts requiring tuning this week (retire / threshold / hysteresis / suppression).

**One-paragraph:** Alerting works in theory (alerts exist) but in practice on-call is flooded with non-actionable noise until pages get ignored or filtered. This methodology defines a per-service noise budget (page-rate + non-actionable-rate), instruments each alert with an `actionable` flag at ack time, and runs a weekly review that triggers tuning actions (raise threshold, add hysteresis, add suppression window, delete alert) when a service exceeds budget. Output: a noise-budget dashboard + a list of alerts requiring tuning this week.

**Ефективно для:**

- per-service noise budget (page-rate + non-actionable-rate) із weekly enforcement loop.
- коли alerts є, але on-call ігнорує через flood — треба budget-driven retirement.
- alerting platform має >=4 тижні event history + actionable-flag workflow.
- team готова retire alerts (default-action: delete), а не permanently silence.

## Applies If (ALL must hold)

- Service has at least one alerting platform configured (Sentry, Datadog, Grafana, PagerDuty, OpsGenie).
- On-call rotation exists OR a solo founder gets paged.
- Alerts have produced >= 10 events over the past 4 weeks (enough data to budget against).
- Team can mark alerts actionable / non-actionable at ack time.

## Skip If (ANY kills it)

- Pre-launch service with no users — no real alerting yet; establish alerts first.
- Monitoring is `logs only, no alerts` — budget is moot until alerts exist.
- On-call practice does not exist (no one carries the pager) — fix that first.
- Team unwilling to retire alerts — budget will be permanently exceeded and ignored.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Alerting platform with event history | >= 4 weeks | platform |
| Alert acknowledgement workflow | captures actionable y/n | platform |
| Per-service ownership map | YAML / wiki | platform |
| Weekly review meeting (30 min) | calendar block | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/incident-response-rotation` | defines on-call structure; budget is per-shift |
| `pro/infra/devops-engineer/sli-slo-definition` | alerts should fire on SLO burn |
| `pro/infra/devops-engineer/api-monitoring-alerting` | budget runs on top of existing methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-per-service-budget) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/05-examples.xml` | medium | One full worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `alert_event_ingestion` | haiku | Pull events from platform API, normalize schema |
| `actionable_classification_review` | sonnet | Sanity-check responder's actionable flag against incident notes |
| `tuning_action_proposal` | sonnet | For over-budget alerts, propose threshold / hysteresis / suppression |
| `chronic_breach_synthesis` | opus | Cross-service synthesis when budget breach is systemic |

## Templates

| File | Purpose |
|------|---------|
| `templates/noise-budget.json` | Per-service budget config |
| `templates/alert-ack-record.json` | Per-event acknowledgement record |
| `templates/tuning-action-record.md` | Tuning decision log skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-alert-noise-budget.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[alert-deduplication-playbook]]
- [[sli-slo-definition]]
- [[incident-response-rotation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Alert Noise Budget methodology when in doubt about scope or fit.
