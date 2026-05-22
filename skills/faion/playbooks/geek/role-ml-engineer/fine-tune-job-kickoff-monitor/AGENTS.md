---
slug: fine-tune-job-kickoff-monitor
tier: geek
group: role-ml-engineer
persona: geek-ai-engineer
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Engineer kicks off a small SFT / LoRA / DPO job (OpenAI or local), monitors training, runs holdout eval, decides keep or trash.
content_id: 576298e0933dc496
methodology_refs:
  - fine-tuning-lora
  - fine-tuning-openai-data-prep
  - fine-tuning-openai-deployment
  - fine-tuning-openai-dpo
  - fine-tuning-openai-eval
  - lora-qlora
  - fine-tuning-openai-sft
  - finetuning
  - model-evaluation
  - finetuning-datasets
---

# Fine-tune job kickoff + monitor

A 9-stage playbook for the atomic angle. Tier: **geek**. Complexity: **deep**.

## Context

Engineer kicks off a small SFT / LoRA / DPO job (OpenAI or local), monitors training, runs holdout eval, decides keep or trash.

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
- `geek/ai/ml-engineer/fine-tuning-lora`
- `geek/ai/ml-ops/lora-qlora`

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
- `geek/ai/ml-engineer/fine-tuning-openai-data-prep`

Outputs:
- Anomaly scratchpad with timestamps

Decision gate: Advance once the scan is complete; if scan reveals an incident, branch to incident response.

### 3. Reproduce

Reproduce the worst anomaly locally before acting.

Tasks:
- Pull a minimal repro from production data
- Confirm the anomaly is real, not a dashboard artifact
- Capture the repro for the eval set or test suite

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-openai-deployment`

Outputs:
- Repro snippet or fixture saved

Decision gate: Advance once the anomaly is confirmed real; if dashboard artifact, fix the dashboard.

### 4. Triage

Score and bucket anomalies into act-now / investigate / ignore.

Tasks:
- Score each anomaly by severity and reversibility
- Bucket into act-now / investigate / ignore
- Pick at most 1-3 act-now items for this cycle

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-openai-dpo`

Outputs:
- Triage table with verdicts

Decision gate: Advance with no more than 1-3 act-now items; if more, raise the bar.

### 5. Verify

Verify each act-now item landed and didn't regress neighbours.

Tasks:
- Run targeted check on the act-now item
- Run the regression sniff-test on adjacent surfaces
- Roll back any item that regressed something else

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-openai-eval`

Outputs:
- Verification table per item

Decision gate: Advance only on clean verification; rollback otherwise.

### 6. Act

Execute the chosen act-now items end-to-end.

Tasks:
- Execute each act-now item with an explicit owner and rollback plan
- Capture before/after evidence
- Hand off anything that exceeds the time-box

Methodologies:
- `geek/ai/ml-engineer/fine-tuning-openai-sft`

Outputs:
- Action log with before/after evidence

Decision gate: Advance once every act-now item is either done or explicitly handed off; never silent-drop.

### 7. Close

Post the one-line verdict, queue follow-ups, and end the loop.

Tasks:
- Post a one-line verdict to the team channel/dashboard
- Queue follow-ups in the appropriate backlog
- Update the cadence ledger so future runs see the trend

Methodologies:
- `geek/ai/ml-engineer/finetuning`

Outputs:
- One-line verdict posted
- Follow-ups queued

Decision gate: Required output: a written verdict; no "see how it goes".

### 8. Document

Promote learnings into runbook, eval set, or rule.

Tasks:
- Update runbook for the failure mode
- Add the failing example to the eval set
- Open a rule/lint PR if the pattern is systemic

Methodologies:
- `geek/ai/ml-engineer/model-evaluation`

Outputs:
- Runbook delta
- Eval set delta

Decision gate: Advance once learnings live outside this scratchpad.

### 9. Cadence handoff

Hand state to the next cycle so it starts faster.

Tasks:
- Pin open items to tomorrow's pre-flight
- Update on-call notes if any
- Close this run's loop with a timestamp

Methodologies:
- `geek/ai/ml-ops/finetuning-datasets`

Outputs:
- Tomorrow's pre-flight seeded

Decision gate: Required: next run can start in <5 min; if not, the handoff is broken.

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/geek/ai/ml-engineer/fine-tuning-lora`
- `knowledge/geek/ai/ml-engineer/fine-tuning-openai-data-prep`
- `knowledge/geek/ai/ml-engineer/fine-tuning-openai-deployment`
- `knowledge/geek/ai/ml-engineer/fine-tuning-openai-dpo`
- `knowledge/geek/ai/ml-engineer/fine-tuning-openai-eval`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
