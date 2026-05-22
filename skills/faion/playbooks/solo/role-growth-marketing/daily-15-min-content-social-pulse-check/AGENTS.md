---
slug: daily-15-min-content-social-pulse-check
tier: solo
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Every morning the marketer knows: what posts went out, what bombed, what's queued, what needs a fire-fix. No tab-graveyard, one tracked dashboard view, one decision."
content_id: a42846a7e55887de
methodology_refs:
  - ops-dashboard-setup
  - plausible-analytics
  - growth-community-building
  - growth-social-media-strategy
---

# Daily 15-min content + social pulse check

A 5-stage playbook for the atomic angle. Tier: **solo**. Complexity: **light**.

## Context

Every morning the marketer knows: what posts went out, what bombed, what's queued, what needs a fire-fix. No tab-graveyard, one tracked dashboard view, one decision.

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
- `solo/marketing/growth-marketer/ops-dashboard-setup`

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
- `solo/marketing/growth-marketer/plausible-analytics`

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
- `solo/marketing/smm-manager/growth-community-building`

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
- `solo/marketing/smm-manager/growth-social-media-strategy`

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
- `solo/marketing/growth-marketer/ops-dashboard-setup`

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

- `knowledge/solo/marketing/growth-marketer/ops-dashboard-setup`
- `knowledge/solo/marketing/growth-marketer/plausible-analytics`
- `knowledge/solo/marketing/smm-manager/growth-community-building`
- `knowledge/solo/marketing/smm-manager/growth-social-media-strategy`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
