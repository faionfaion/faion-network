---
slug: blog-post-brief-ai-draft-human-polish-per-post
tier: solo
group: role-growth-marketing
persona: solo-founder, growth-marketer
goal: acquire-grow
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "One publish-ready post. AI does the volume, human adds: original POV, real example, internal links, structured data, EEAT signals. Output ranks in 3-6 weeks and does NOT trigger 'AI slop' detection."
content_id: d84757be48078f4c
methodology_refs:
  - ai-content-strategy
  - google-ai-overviews-optimization
  - technical-seo-for-ai
  - growth-content-marketing
  - growth-copywriting-fundamentals
  - zero-click-search-adaptation
  - growth-social-media-strategy
  - growth-email-marketing
  - seo-techniques
---

# Blog post brief → AI draft → human polish (per-post)

A 7-stage playbook for the atomic angle. Tier: **solo**. Complexity: **medium**.

## Context

One publish-ready post. AI does the volume, human adds: original POV, real example, internal links, structured data, EEAT signals. Output ranks in 3-6 weeks and does NOT trigger 'AI slop' detection.

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
- `geek/marketing/content-marketer/ai-content-strategy`
- `solo/marketing/seo-manager/zero-click-search-adaptation`

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
- `geek/marketing/seo-manager/google-ai-overviews-optimization`
- `solo/marketing/smm-manager/growth-social-media-strategy`

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
- `geek/marketing/seo-manager/technical-seo-for-ai`

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
- `solo/marketing/content-marketer/growth-content-marketing`

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
- `solo/marketing/content-marketer/growth-copywriting-fundamentals`

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
- `solo/marketing/content-marketer/growth-email-marketing`

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
- `solo/marketing/seo-manager/seo-techniques`

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

- `knowledge/geek/marketing/content-marketer/ai-content-strategy`
- `knowledge/geek/marketing/seo-manager/google-ai-overviews-optimization`
- `knowledge/geek/marketing/seo-manager/technical-seo-for-ai`
- `knowledge/solo/marketing/content-marketer/growth-content-marketing`
- `knowledge/solo/marketing/content-marketer/growth-copywriting-fundamentals`

Gaps (methodologies not yet authored) are listed in `playbook.yaml` under `gaps[]`. Until each gap is filled, the playbook stays in `status: draft`.
