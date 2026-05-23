<!--
purpose: 1-5 anchors per factor, signed off by stakeholder before scoring starts.
consumes: nothing — this IS the calibration artefact.
produces: shared meaning for each factor that downstream scoring uses.
depends-on: stakeholder available for sign-off.
token-budget-impact: ~200 tokens when copied.
-->

# Debt scoring — anchor calibration

## User-Impact
- 1: only affects internal tools
- 2: visible to &lt;1% of users
- 3: visible to 1–10% of users
- 4: visible to 10–50% of users
- 5: visible to &gt;50% of users OR money-path

## Change-Frequency (last 90 days)
- 1: ≤2 commits
- 2: 3–10 commits
- 3: 11–25 commits
- 4: 26–60 commits
- 5: &gt;60 commits

## Fragility (incident / bug count in last 90 days)
- 1: 0 bugs
- 2: 1–2 bugs
- 3: 3–6 bugs
- 4: 7–15 bugs
- 5: &gt;15 bugs OR P0/P1 incident

## Blast-Radius (services touched)
- 1: one module
- 2: one service
- 3: two services or shared lib
- 4: 3–5 services
- 5: shared lib used by &gt;5 services OR core auth/billing

## Fix-Cost
- 1: 1–4 hours
- 2: 1 day
- 3: 2–5 days
- 4: 1–2 weeks
- 5: &gt; 2 weeks

## Sign-off

- Signed by: pm@acme.com
- Date: YYYY-MM-DD
- Threshold for next-sprint inclusion: 30 (score ≥ 30 enters the sprint)
