# Lessons Learned

## Summary

Continuous capture, structured categorisation, and mandatory retrieval of project knowledge so that the same mistakes are not repeated. A lesson is only valid if it has a specific situation, measurable impact, root cause, and an actionable recommendation with a verb. "Communication was bad" is not a lesson — it is noise.

## Why

Most lessons-learned databases are write-only: entries are logged at project close and never read again. The failure mode is not lack of capture — it is lack of retrieval at future project kickoff and lack of a feedback loop into checklists and templates. Without a mandatory retrieval step at kickoff, the database is decorative.

## When To Use

- Capturing decision rationale and outcomes throughout a project, not only at close-out
- Running structured retrospectives (per milestone, per sprint, project-end)
- Building an org-level knowledge base queried by future PMs before starting similar projects
- Feeding `faion-improver` and `faion-sdd-execution` mistake/pattern memories with structured lessons
- Generating project close-out reports where the top 5 lessons are the executive summary

## When NOT To Use

- Trivial routine work where lessons are predictable — capturing them adds noise
- Active blame/political environments — fix the culture first or run anonymous-only retros
- Live-incident postmortems — use a blameless postmortem template, not project lessons
- Confidential/regulated programs where each lesson requires individual legal review before sharing

## Content

| File | What's inside |
|------|---------------|
| `content/01-capture.xml` | Capture triggers, lesson schema, specificity rules, antipatterns |
| `content/02-retrieval.xml` | Retro session structure, retrieval at kickoff, storage and tagging rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/lesson-validator.py` | Validates a lesson dict against the required schema and rejects vague recommendations |
