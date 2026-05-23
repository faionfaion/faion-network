# LLM Drift Daily Triage

## Summary

**One-sentence:** Produces a daily 15-minute drift triage — yesterday's eval delta, refusal-rate delta, cost delta, top-3 failing prompts, decision-record (continue / mitigate / escalate).

**One-paragraph:** Model providers ship silent updates; prompt edits land daily; tool descriptions creep. Any of these can move a production behaviour by 5-20 percentage points between yesterday and today. Without a daily 15-minute ritual the signal disappears in the noise and the team finds out from a customer email. This methodology pins a daily report (3 metric deltas + 3 failing-prompt traces + 1 decision) into the on-call rotation; under 15 minutes per day if the report template is filled by the runner.

**Ефективно для:** customer-facing AI products, regulated pipelines (finance, health), agents with paid downstream effects, model upgrades pre-rollout.

## Applies If (ALL must hold)

- A production LLM call path has run for ≥7 days (enough history for a delta).
- A daily eval pulse exists (cron, GitHub Action, etc.) producing per-day scores.
- An on-call (or single owner) reviews the report.
- A decision channel exists (Slack, ticket, alert) where the day's decision is recorded.

## Skip If (ANY kills it)

- No production traffic — drift is hypothetical.
- No eval set — there is no signal to triage; bootstrap the eval first.
- Single-shot pipeline, never updated — drift surface is empty.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Daily eval-run summary | JSON | eval runner artifact |
| Refusal-rate log | JSONL | application telemetry |
| Cost-per-call log | JSONL | billing webhook / cost dashboard |
| On-call rotation | calendar | PagerDuty / OpsGenie |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[jailbreak-eval-suite-bootstrap]]` | Suite produces the eval-delta input. |
| `[[ai-cost-attribution-schema]]` | Cost log uses the attribution schema. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: 15-min cap, 3-delta + 3-trace report, named owner, escalation path, weekly trend, no-skip | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for triage-report.json | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: skipped-day, eyeball-only, no-escalation, single-metric-tunnel, retro-edit | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: pull metrics → compute deltas → load failing traces → decide → log → schedule follow-up | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "is the absolute eval delta > 2pp OR refusal-rate delta > 3pp OR cost delta > 10%?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pull metrics & compute deltas | haiku | Deterministic numerical. |
| Summarise top-3 failing traces | sonnet | Bounded summarisation. |
| Recommend decision | opus | Multi-axis reasoning. |
| File ticket / page on-call | haiku | Mechanical channel write. |

## Templates

| File | Purpose |
|---|---|
| `templates/triage-report.schema.json` | JSON Schema for the daily report. |
| `templates/triage-report.md` | Markdown skeleton (3 deltas + 3 traces + decision). |
| `templates/runner.py` | Reference runner that produces triage-report.json from telemetry sources. |
| `templates/_smoke-test.json` | Minimum-viable triage report. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llm-drift-daily-triage.py` | Validates triage-report.json schema + asserts owner + decision present. | Pre-commit on report PR; CI before posting to Slack. |

## Related

- parent skill: `geek/ai/`
- `[[ai-cost-attribution-schema]]`
- `[[jailbreak-eval-suite-bootstrap]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides the day's action: small deltas → continue (log only); medium deltas → mitigate (revert last change, page owner); large deltas → escalate (incident + page on-call). Thresholds are configurable per call site.
