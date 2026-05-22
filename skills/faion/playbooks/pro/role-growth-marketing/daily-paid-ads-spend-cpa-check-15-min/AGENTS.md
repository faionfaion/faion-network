---
slug: daily-paid-ads-spend-cpa-check-15-min
tier: pro
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Every active ad account inspected once a day. Catch runaway spend, dead creatives, broken pixels before they cost real money. Output: pause / scale / leave alone per campaign."
content_id: 98a4bb5a4ac3259a
methodology_refs:
  - ads-ab-testing-ads
  - ads-analytics-setup
  - ads-attribution-models
  - ads-budget-optimization
  - ads-conversion-tracking
  - ads-retargeting
---

# Daily paid-ads spend + CPA check (15 min)

A 5-stage playbook for the atomic angle. Tier: **pro**. Complexity: **light**.

## Context

Every active ad account inspected once a day. Catch runaway spend, dead creatives, broken pixels before they cost real money. Output: pause / scale / leave alone per campaign.

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
- `pro/marketing/ppc-manager/ads-ab-testing-ads`
- `pro/marketing/ppc-manager/ads-retargeting`

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
- `pro/marketing/ppc-manager/ads-analytics-setup`

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
- `pro/marketing/ppc-manager/ads-attribution-models`

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
- `pro/marketing/ppc-manager/ads-budget-optimization`

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
- `pro/marketing/ppc-manager/ads-conversion-tracking`

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

- `knowledge/pro/marketing/ppc-manager/ads-ab-testing-ads`
- `knowledge/pro/marketing/ppc-manager/ads-analytics-setup`
- `knowledge/pro/marketing/ppc-manager/ads-attribution-models`
- `knowledge/pro/marketing/ppc-manager/ads-budget-optimization`
- `knowledge/pro/marketing/ppc-manager/ads-conversion-tracking`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
