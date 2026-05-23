<!--
purpose: Weekly sentiment-tracker report skeleton.
consumes: header.yaml frontmatter + stakeholder source list + classification rubric.
produces: A versioned, consent-anchored weekly sentiment report.
depends-on: ../scripts/validate-stakeholder-sentiment-tracker.py.
token-budget-impact: ~600 tokens when filled.
-->

---
version: "1.0.0"
owner: "pm:<person>"
last_reviewed: "2026-05-22"
consent_root: "rescue/consent/"
rubric_path: "rescue/rubric.yaml"
run_date: "2026-05-22"
---

# Sentiment run — <ISO date>

## Stakeholder: <Name> (<role>)
- Sources: <count> emails, <count> meeting transcripts (consent: <ISO date>)
- Markers hit: <comma-separated markers>
- Class: supportive | cautious | hostile | no-signal
- Trend (last 6 weeks): <list>

<!-- repeat per stakeholder -->

## ALARM (only if fired)
- Stakeholder: <Name>
- Reason: 2-week decline | weekly hostile
- Action plan (filed <ISO date>):
  - Hypothesis: <text>
  - Intervention: <call / meeting / written response>
  - Deadline: <ISO date>
