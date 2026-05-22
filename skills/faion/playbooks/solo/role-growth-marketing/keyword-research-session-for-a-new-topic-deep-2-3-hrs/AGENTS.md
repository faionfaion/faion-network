---
slug: keyword-research-session-for-a-new-topic-deep-2-3-hrs
tier: solo
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "From a fuzzy topic to a vetted cluster: pillar query + 8-15 supporting queries, intent- tagged, with difficulty + SERP feature notes. Output is a brief ready to hand to a writer (or yourself)."
content_id: 113b1a6bd3545f9c
methodology_refs:
  - google-ai-overviews-optimization
  - growth-content-marketing
  - growth-copywriting-fundamentals
  - growth-seo-fundamentals
  - seo-basics
  - topical-authority
  - zero-click-search-adaptation
---

# Keyword research session for a new topic (deep, 2-3 hrs)

A 9-stage playbook for the atomic angle. Tier: **solo**. Complexity: **deep**.

## Context

From a fuzzy topic to a vetted cluster: pillar query + 8-15 supporting queries, intent-tagged, with difficulty + SERP feature notes. Output is a brief ready to hand to a writer (or yourself).

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
- `geek/marketing/seo-manager/google-ai-overviews-optimization`

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
- `solo/marketing/content-marketer/growth-content-marketing`

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
- `solo/marketing/content-marketer/growth-copywriting-fundamentals`

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
- `solo/marketing/seo-manager/growth-seo-fundamentals`

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
- `solo/marketing/seo-manager/seo-basics`

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
- `solo/marketing/seo-manager/topical-authority`

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
- `solo/marketing/seo-manager/zero-click-search-adaptation`

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
- `geek/marketing/seo-manager/google-ai-overviews-optimization`

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
- `solo/marketing/content-marketer/growth-content-marketing`

Outputs:
- Tomorrow's pre-flight seeded

Decision gate: Required: next run can start in <5 min; if not, the handoff is broken.

## Decision points

- Per stage: written decision_gate must be satisfied before advancing — no implicit "close enough".
- End-of-playbook: a written verdict or continue/pivot/kill doc is the only acceptable exit.
- Mid-run pivot: if scope/charter drifts more than 25%, restart from the framing stage; never silently mutate.

## References

Existing knowledge methodologies cited by this playbook:

- `knowledge/geek/marketing/seo-manager/google-ai-overviews-optimization`
- `knowledge/solo/marketing/content-marketer/growth-content-marketing`
- `knowledge/solo/marketing/content-marketer/growth-copywriting-fundamentals`
- `knowledge/solo/marketing/seo-manager/growth-seo-fundamentals`
- `knowledge/solo/marketing/seo-manager/seo-basics`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
