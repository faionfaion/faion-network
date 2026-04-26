# Lessons Learned

## Summary

Structured knowledge-capture process that runs continuously throughout a project, not only at close-out. Each lesson requires five fields: Situation (facts), Impact (quantified), Root Cause (5-whys), Lesson (generalizable, two sentences max), Recommendation (action verb + owner role + where applied). Lessons stored in a versioned, searchable repository; application rate tracked as an SLO.

## Why

The canonical failure mode is "captured but never used": lessons sit in a wiki graveyard and the same mistakes recur. Enforcing structured fields with quantified impact prevents vague write-ups ("communication was bad"). Tracking application rate — what percent of last quarter's lessons triggered a process change — closes the feedback loop. Without it, lessons-learned is theater.

## When To Use

- Capturing knowledge during a project at milestone closes, post-incidents, and after major decisions.
- Building searchable organizational memory across multiple projects.
- Onboarding new PMs or engineers with curated patterns and anti-patterns.
- Post-incident reviews (PIR / blameless postmortems) when the incident touched scope, cost, or schedule.
- Continuous-improvement loop: lesson → updated checklist → applied next sprint or project.

## When NOT To Use

- One-person, one-week projects — a 5-line note in the README is enough; structured overhead exceeds value.
- Already-mature orgs with strong RCA culture and a working knowledge base — contribute, don't re-invent.
- Live incidents — capture facts now, run lessons later; do not derail incident response with a retro.

## Content

| File | What's inside |
|------|---------------|
| `content/01-capture-process.xml` | Structured capture fields, continuous-capture triggers, 5-whys rules, session ground rules. |
| `content/02-storage-application.xml` | Storage requirements, searchability rules, application SLO, staleness expiry. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lesson-record.md` | Single lesson document with all five required fields. |
| `templates/session-agenda.md` | Facilitated lessons-learned session agenda (75 min). |
