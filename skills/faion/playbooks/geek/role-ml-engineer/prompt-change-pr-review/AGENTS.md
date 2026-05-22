---
slug: prompt-change-pr-review
tier: geek
group: role-ml-engineer
persona: geek-ai-engineer
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Reviewer opens a PR that edits a production prompt template; runs the eval delta, checks regressions, requests changes or approves with rollout plan.
content_id: c73ea705f183f015
methodology_refs:
  - field-descriptions-as-prompts
  - prompt-cache-prefix-order
  - schema-version-pinning
  - model-evaluation
  - prompt-engineering-evaluation
  - prompt-engineering-fundamentals
  - prompt-engineering-production
  - prompt-engineering-security
  - rag-eval-ab-testing
---

# Prompt change PR review

A 5-stage playbook for the atomic angle. Tier: **geek**. Complexity: **light**.

## Context

Reviewer opens a PR that edits a production prompt template; runs the eval delta, checks regressions, requests changes or approves with rollout plan.

## Outcome

One disciplined cycle of this cadence: a verdict posted, follow-ups queued, the ledger advanced. The output is not a finished project — it is one more reliable data point in a long-running operating rhythm.

## Steps

### 1. Pre-flight

Confirm inputs, dashboards, access, and yesterday's open items.

Tasks:
- Verify required dashboards/logs are reachable and current
- Re-open yesterday's deferred items list
- Set a hard time-box for this run

Methodologies:
- `geek/ai/ai-agents/field-descriptions-as-prompts`
- `geek/ai/ml-engineer/prompt-engineering-fundamentals`

Outputs:
- Pre-flight checklist signed off

Decision gate: Advance once every required surface is green; otherwise resolve the access/data gap first.

### 2. Scan

Read the surface in one pass; capture anomalies without acting.

Tasks:
- Walk through every required panel/chart/feed once
- Log anomalies and outliers in a single scratchpad
- Do not act on anything yet

Methodologies:
- `geek/ai/ai-agents/prompt-cache-prefix-order`
- `geek/ai/ml-engineer/prompt-engineering-production`

Outputs:
- Anomaly scratchpad with timestamps

Decision gate: Advance once the scan is complete; if scan reveals an incident, branch to incident response.

### 3. Triage

Score and bucket anomalies into act-now / investigate / ignore.

Tasks:
- Score each anomaly by severity and reversibility
- Bucket into act-now / investigate / ignore
- Pick at most 1-3 act-now items for this cycle

Methodologies:
- `geek/ai/ai-agents/schema-version-pinning`
- `geek/ai/ml-engineer/prompt-engineering-security`

Outputs:
- Triage table with verdicts

Decision gate: Advance with no more than 1-3 act-now items; if more, raise the bar.

### 4. Act

Execute the chosen act-now items end-to-end.

Tasks:
- Execute each act-now item with an explicit owner and rollback plan
- Capture before/after evidence
- Hand off anything that exceeds the time-box

Methodologies:
- `geek/ai/ml-engineer/model-evaluation`
- `geek/ai/rag-engineer/rag-eval-ab-testing`

Outputs:
- Action log with before/after evidence

Decision gate: Advance once every act-now item is either done or explicitly handed off; never silent-drop.

### 5. Close

Post the one-line verdict, queue follow-ups, and end the loop.

Tasks:
- Post a one-line verdict to the team channel/dashboard
- Queue follow-ups in the appropriate backlog
- Update the cadence ledger so future runs see the trend

Methodologies:
- `geek/ai/ml-engineer/prompt-engineering-evaluation`

Outputs:
- One-line verdict posted
- Follow-ups queued

Decision gate: Required output: a written verdict; no "see how it goes".

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/geek/ai/ai-agents/field-descriptions-as-prompts`
- `knowledge/geek/ai/ai-agents/prompt-cache-prefix-order`
- `knowledge/geek/ai/ai-agents/schema-version-pinning`
- `knowledge/geek/ai/ml-engineer/model-evaluation`
- `knowledge/geek/ai/ml-engineer/prompt-engineering-evaluation`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
