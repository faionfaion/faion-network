---
slug: vector-db-query-optimization-pass
tier: geek
group: role-ml-engineer
persona: geek-ai-engineer
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Vector store latency or recall is off: tune index, filters, hybrid retrieval; ship or document why current setup is optimal."
content_id: d42c563479cadd99
methodology_refs:
  - hybrid-search
  - vector-databases
  - vector-db-index-tuning
  - vector-db-monitoring
  - vector-db-security
  - hybrid-search-implementation
  - vector-db-setup-prod
  - db-comparison
---

# Vector DB query optimization pass

A 7-stage playbook for the atomic angle. Tier: **geek**. Complexity: **medium**.

## Context

Vector store latency or recall is off: tune index, filters, hybrid retrieval; ship or document why current setup is optimal.

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
- `geek/ai/ml-engineer/hybrid-search`
- `geek/ai/rag-engineer/hybrid-search-implementation`

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
- `geek/ai/ml-engineer/vector-databases`

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
- `geek/ai/ml-engineer/vector-db-index-tuning`

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
- `geek/ai/ml-engineer/vector-db-monitoring`

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
- `geek/ai/ml-engineer/vector-db-security`

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
- `geek/ai/ml-engineer/vector-db-setup-prod`

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
- `geek/ai/rag-engineer/db-comparison`

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

- `knowledge/geek/ai/ml-engineer/hybrid-search`
- `knowledge/geek/ai/ml-engineer/vector-databases`
- `knowledge/geek/ai/ml-engineer/vector-db-index-tuning`
- `knowledge/geek/ai/ml-engineer/vector-db-monitoring`
- `knowledge/geek/ai/ml-engineer/vector-db-security`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
