# Communications Management

## Summary

A structured who-what-when-how matrix (comms/plan.yaml) that maps every stakeholder to their information need, delivery channel, cadence, and owner. Status report colour (GREEN/YELLOW/RED) derives from quantitative schedule and budget thresholds, not PM judgment. Decisions are never stored in chat — they are logged in a versioned decision record. The plan self-monitors via a weekly audit script that opens issues for overdue communications.

## Why

Stakeholder surprises and "drowning in Slack" both stem from the same root: no explicit model of who needs what, when, and through which channel. A written comms matrix makes those decisions visible and auditable. Plans go stale in 4-8 weeks without refresh; the weekly audit script replaces manual discipline with automated detection. Status colour from metrics (not mood) prevents optimism bias from hiding real problems.

## When To Use

- New projects where stakeholder count is above 5 and you need a written matrix before kickoff.
- Distributed or async-first teams where missed updates are the dominant failure mode.
- Regulated programs (SOX, HIPAA, GDPR, MDR) requiring traceable, dated, signed-off communications.
- "Drowning in Slack/email" situations: consolidate channels and kill duplicate updates.
- Multi-vendor engagements with formal status cadences and escalation paths required by contract.

## When NOT To Use

- Solo founders or 2-3-person startups pre-PMF — matrix overhead exceeds value; a single Slack channel works.
- Crisis or incident response — runbooks and on-call rotations replace this; do not retrofit during P0.
- Short spikes under 2 weeks — agree on channel verbally, skip the artifact.
- When stakeholders refuse classification or the political situation is too fluid to commit to a cadence.

## Content

| File | What's inside |
|------|---------------|
| `content/01-comms-matrix.xml` | Matrix structure, cadence rules, status-colour thresholds, decision-log rule. |
| `content/02-channel-selection.xml` | Channel-to-need mapping, timezone rules, confidentiality constraints, anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/comms-plan.md` | Communication plan with stakeholder matrix, meeting schedule, channels, escalation path. |
| `templates/meeting-notes.md` | Structured meeting notes with decisions, action items, and next meeting. |
| `templates/status-report.md` | Weekly status report with GREEN/YELLOW/RED colour from quantitative thresholds. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/comms_audit.py` | Reads comms/plan.yaml; lists stakeholders overdue for an update this week. |
